FROM python:3.10.12-slim

WORKDIR /data_upload

RUN apt-get update
RUN apt install python3-pip -y
RUN pip install --upgrade pip 
RUN apt-get install curl -y --no-install-recommends

COPY . /data_upload/
RUN pip install -r /data_upload/requirements.txt

CMD ["python3", "./my_uploader.py"]