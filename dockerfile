FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "pubmed_app.py", "--server.port=8501", "--server.address=0.0.0.0"]










