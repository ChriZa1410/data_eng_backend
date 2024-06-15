# Docker file: init-databases
# Description: see docker-compose.yml

FROM python:3.10.12-slim

WORKDIR /databases

RUN apt-get update
RUN apt-get install curl -y --no-install-recommends

COPY . /databases/

CMD ["./create_databases.sh"]