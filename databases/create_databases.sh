#!/bin/bash

# create_databases.sh 
#
# In this file the InfluxDB databases are created to store productive and metrics data.

set -e

INFLUXDB_CONTAINER_PORT=8086

# Wait until influxdb container has started
while ! curl -sL -I "http://influxdb:$INFLUXDB_CONTAINER_PORT/ping" > /dev/null; do
  echo "Waiting for InfluxDB container to start..."
done

# Send POST request to create influxdb databases in influxdb container
echo 'Creating database...'
curl -XPOST "http://influxdb:$INFLUXDB_CONTAINER_PORT/query" --data-urlencode "q=CREATE DATABASE data_storage"

