#!/bin/bash

# create_databases.sh 
#
# In this file the InfluxDB databases are created to store productive and metrics data.

set -e

# Wait until influxdb container has started
while ! curl -sL -I "http://influxdb:8086/ping" > /dev/null; do
  echo "Waiting for InfluxDB container to start..."
done

# Send POST request to create influxdb databases in influxdb container
echo 'Creating databases...'
curl -XPOST "http://influxdb:8086/query" --data-urlencode "q=CREATE DATABASE data_storage"
curl -XPOST "http://influxdb:8086/query" --data-urlencode "q=CREATE DATABASE kafka_metrics"

