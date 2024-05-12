FROM python:3.10.12-slim

RUN apt update
RUN apt install python3-pip -y
RUN pip install confluent_kafka
#RUN apt-get install time -y --no-install-recommends
#RUN apt-get install curl -y --no-install-recommends

WORKDIR /bin/data_consumer
COPY consumer.py ./
#COPY config.ini ./

#RUN pip install --upgrade pip
#RUN pip install confluent_kafka
#RUN curl -y -f -L --http1.1 https://cnfl.io/cli | sh -s -- -b /usr/local/bin
#RUN curl --version
#RUN curl -sL --http1.1 https://cnfl.io/cli | sh -s -- latest
#RUN export PATH=$(pwd)/bin:$PATH
# RUN confluent update
#RUN confluent login
#RUN confluent environment list

# COPY package.json yarn.lock ./
# RUN yarn install --production
# COPY . .


CMD ["python3", "./consumer.py"]