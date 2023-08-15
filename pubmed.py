import json
import time
import urllib.error
import urllib.request
from typing import List, Any


class PubMedAPIWrapper:
    """
    Wrapper around PubMed API (https://www.ncbi.nlm.nih.gov/books/NBK25501/).

    This wrapper will use the PubMed API to conduct searches and fetch
    document summaries. By default, it will return the document summaries
    of the top-k results of an input search.
    """

    base_url_esearch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    base_url_efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    doc_content_chars_max: int = 2000
    retmax = 500  # The number of articles fetched each time
    max_retry = 5
    sleep_time = 0.2

    def __init__(self, query: str, api_key: str = None, verbose: bool = False):
        """
        Parameters:
            api_key: Users can obtain an API key now from the Settings page of their NCBI account
                (to create an account, visit http://www.ncbi.nlm.nih.gov/account/).
                With an API, the request limit is 10 times per minute; without it,
                the limit is 3 times per minute.
        """
        self.query = query
        self.count = 0
        self.uid_list = []
        self.webenv = ""
        self.query_key = ""
        self.articles = []
        self.verboseprint = print if verbose else lambda *a, **k: None
        if api_key is not None:
            self.base_url_esearch = self.base_url_esearch + "api_key=" + api_key
            self.base_url_efetch = self.base_url_efetch + "api_key=" + api_key

    def run(self) -> str:
        """
        Run PubMed search and get the article meta information.
        """

        try:
            if self.articles == [] and self.webenv == "":
                self.fetch_article()

            if self.articles == []:
                return "No good PubMed Result was found"
            else:
                docs = [
                    f"Published: {result['pub_date']}\nTitle: {result['title']}\n"
                    f"Summary: {result['abstract']}"
                    for result in self.articles
                ]
                return "\n\n".join(docs)[: self.doc_content_chars_max]
        except Exception as ex:
            return f"PubMed exception: {ex}"

    def search_article(self, sort_by: str = "relevance") -> Any:
        """
        Search PubMed for documents matching the query.
        Return the counts of matched articles, the list of uids, the webenv, and the query_key.
        Parameters:
            sort_by: the sort order of the results. pub_date, Author, JournalName, or relevance (default).
        """
        url = (
            self.base_url_esearch
            + "&db=pubmed&term="
            + str({urllib.parse.quote(self.query)})
            + "&retmode=json&usehistory=y"
            + "&sort="
            + sort_by
        )
        # print("Processing url: ", url)
        result = urllib.request.urlopen(url)
        text = result.read().decode("utf-8")
        json_text = json.loads(text)

        self.count = int(json_text["esearchresult"]["count"])
        self.uid_list = json_text["esearchresult"]["idlist"]
        self.webenv = json_text["esearchresult"]["webenv"]
        self.query_key = json_text["esearchresult"]["querykey"]

        self.verboseprint("Total number of articles searched: ", self.count)
        return self.count, self.uid_list, self.webenv, self.query_key

    def fetch_article(self, top_k_results: int = 3) -> List[dict]:
        """
        Fetch the article according to the History server.
        Return a list of dictionaries containing the document metadata.
        Parameters:
            top_k_results: number of the top-scored document used for the PubMed tool.
        """

        if self.webenv == "":
            self.search_article()

        if self.count == 0:
            return []

        if self.count < top_k_results:
            top_k_results = self.count

        self.verboseprint(f"The top {top_k_results} results will be processed.")

        if top_k_results <= self.retmax:
            self.retmax = top_k_results

        articles = []
        for retstart in range(0, top_k_results, self.retmax):
            url = (
                self.base_url_efetch
                + "&db=pubmed&retmode=xml"
                + "&webenv="
                + self.webenv
                + "&query_key="
                + self.query_key
                + "&retmax="
                + str(self.retmax)
                + "&retstart="
                + str(retstart)
            )
            # print("Processing url: ", url)
            retry = 0
            while True:
                try:
                    result = urllib.request.urlopen(url)
                    break
                except urllib.error.HTTPError as e:
                    if e.code == 429 and retry < self.max_retry:
                        # Too Many Requests error
                        # wait for an exponentially increasing amount of time
                        self.verboseprint(
                            f"Too Many Requests, "
                            f"waiting for {self.sleep_time:.2f} seconds..."
                        )
                        time.sleep(self.sleep_time)
                        self.sleep_time *= 2
                        retry += 1
                    else:
                        raise e

            xml_text = result.read().decode("utf-8")
            xml_list = xml_text.split("</PubmedArticle>")[0:-1]

            for xml in xml_list:
                # Get uid
                uid = ""
                if '<PMID Version="1">' in xml and "</PMID>" in xml:
                    start_tag = '<PMID Version="1">'
                    end_tag = "</PMID>"
                    uid = xml[
                        xml.index(start_tag) + len(start_tag) : xml.index(end_tag)
                    ]
                # Get title
                title = ""
                if "<ArticleTitle>" in xml and "</ArticleTitle>" in xml:
                    start_tag = "<ArticleTitle>"
                    end_tag = "</ArticleTitle>"
                    title = xml[
                        xml.index(start_tag) + len(start_tag) : xml.index(end_tag)
                    ]

                # Get abstract
                abstract = ""
                if "<AbstractText>" in xml and "</AbstractText>" in xml:
                    start_tag = "<AbstractText>"
                    end_tag = "</AbstractText>"
                    abstract = xml[
                        xml.index(start_tag) + len(start_tag) : xml.index(end_tag)
                    ]

                # Get publication date
                pub_date = ""
                if "<PubDate>" in xml and "</PubDate>" in xml:
                    start_tag = "<PubDate>"
                    end_tag = "</PubDate>"
                    pub_date = xml[
                        xml.index(start_tag) + len(start_tag) : xml.index(end_tag)
                    ]

                # Return article as dictionary
                article = {
                    "uid": uid,
                    "title": title,
                    "abstract": abstract,
                    "pub_date": pub_date,
                }
                articles.append(article)

            per = (retstart + self.retmax) * 100 / top_k_results
            if per > 100:
                per = 100
            self.verboseprint(f"{per:.2f}% done")

        self.articles = articles[:top_k_results]
        return self.articles
