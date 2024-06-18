# Docker file: data_upload
#
# Description: see docker-compose.yml

FROM python:3.9-slim

WORKDIR /bin/data_upload

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY uploading.py ./

CMD ["faust", "-A", "uploading", "worker", "-l", "info"]