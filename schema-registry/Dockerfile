FROM python:3.10.12-slim

WORKDIR /schema-registry

RUN apt-get update
RUN apt-get install curl -y --no-install-recommends

COPY . /schema-registry/

CMD ["./create_schema.sh"]