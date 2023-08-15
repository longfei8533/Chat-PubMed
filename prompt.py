class Prompt:
    @property
    def pubmed_query_parse_prompt(self):
        prompt = """Use the following rules to reconstruct the query for an advanced search of PubMed. 
Rules: 
1. Needs to be reconstruct into English.
2. Combining search terms with Boolean operators (AND, OR, NOT).
3. Parentheses ( ) - used to create Boolean nesting. Square brackets [ ] - search field tag qualification. Double quotes " - used to force a phrase search. Colon : - designates a range operation.
4. Using search field tags. If a field is searchable, the search tag appears after the field name in square brackets. Tags include Affiliation [ad], All Fields [all], Article  identifier [aid], Author [au], Author Identifier [auid], Book [book],  Completion Date [dcom], Conflict of Interest Statement [cois], Corporate Author [cn], Create Date [crdt], EC/RN Number [rn], Editor [ed], Entry Date [edat], Filter [filter] [sb], First Author Name [1au], Full Author Name [fau], Full Investigator Name [fir], Grant Number [gr], Investigator [ir], ISBN [isbn], Issue [ip], Journal [ta], Language [la], Last Author Name [lastau], Location ID [lid], Modification Date [lr], NLM Unique ID [jid], Other Term [ot], Pagination [pg], Personal Name as Subject [ps], Pharmacological Action [pa], Place of Publication [pl], PMID [pmid], Publication Date [dp], Publication Type [pt], Publisher [pubn], Secondary Source ID [si], Subset [sb], Supplementary Concept [nm], Text Words [tw], Title [ti], Title/Abstract [tiab], Transliterated Title [tt], Volume [vi].
5. Searching by author. If you only know the author's last name, use the author search field tag [au], e.g., brody[au].
6. Searching by date. Date of Publication [dp] - Date searching includes both print and electronic dates of publication. Enter date ranges using a colon (:) between each date followed by a [dp]. e.g., 2019/01/01:2019/12/01[dp]. 
7. Filter by article type. Article publication types include Clinical Study, Clinical Trial, Comment, Letter, News, Preprint and Review. e.g., review type articles can be filtered using Review[filter].
Query: Articles on stomach cancer published between 2018 and 2019
Reconstruct : "stomach cancer" AND 2018:2019[dp]
Query: Author David 2019 published all reviews related to cancer.
Reconstruct : David[au] AND cancer AND 2019[dp] AND Review[filter]
Query: YY1 Gene therapy cancer clinical research related articles from 2018 to the present
Reconstruct : YY1 AND therapy AND cancer AND "Clinical Study"[filter] AND 2018:2023[dp]
Query: All articles published in Bioinformatics last year
Reconstruct :  Bioinformatics[ta] AND 2022[dp]
Query: Articles that include kidney failure in the title or abstract
Reconstruct: (kidney failure[tiab])
Query: 上年Nature期刊上发表的所有文章
Reconstruct: Nature[ta] AND 2022[dp]
Query: 上年作者Jobs发表的与胃癌相关的所有综述
Reconstruct: Jobs[au] AND (gastric cancer) AND Review[filter] AND 2022[dp]
Query: 与5-fu耐药相关的近五年的非综述文章
Reconstruct:  5-fu AND resistance NOT Review[filter] AND 2018:2023[dp]
Query: {}
Reconstruct: 
"""
        return prompt

    @property
    def system_prompt(self):
        prompt = "As an expert in the field of biomedicine, please answer the user's questions accurately."
        return prompt
