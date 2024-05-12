FROM python:3.10.12-slim

WORKDIR /influxdb

RUN apt-get update

COPY . /influxdb/

CMD ["./create_influxdb.sh"]