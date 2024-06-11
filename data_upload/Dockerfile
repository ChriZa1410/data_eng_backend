FROM python:3.9-slim

WORKDIR /bin/data_upload

COPY requirements.txt requirements.txt
#RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY uploading.py ./

CMD ["faust", "-A", "uploading", "worker", "-l", "info"]