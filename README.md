# Chat-PubMed

![](https://github.com/longfei8533/Chat-PubMed/blob/main/image.png)
## Run

1. Runs directly in the python environment

   ```
   pip install -r requirements.txt
   streamlit run pubmed_app.py --server.port=8501
   ```

2. Deploy Streamlit using Docker

   https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker

   ```
   docker build -t chat_pubmed .
   docker run -p 8501:8501 chat_pubmed
   ```
