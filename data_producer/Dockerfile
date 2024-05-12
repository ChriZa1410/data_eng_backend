FROM python:3.10.12-slim

WORKDIR /data_producer

RUN apt-get update
RUN apt install python3-pip -y
RUN pip install --upgrade pip 
RUN apt-get install curl -y --no-install-recommends

COPY . /data_producer/
RUN pip install -r /data_producer/requirements.txt

CMD ["python3", "./producer.py"]