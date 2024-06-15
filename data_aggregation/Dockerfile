# Docker file: data_aggregation
#
# Description: see docker-compose.yml

FROM python:3.9-slim

WORKDIR /bin/aggregation

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY aggregation.py ./

CMD ["faust", "-A", "aggregation", "worker", "-l", "info"]