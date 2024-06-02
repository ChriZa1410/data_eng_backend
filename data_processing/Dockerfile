FROM python:3.9-slim

WORKDIR /bin/processing

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY processing.py ./

CMD ["faust", "-A", "processing", "worker", "-l", "info"]