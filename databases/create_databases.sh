#!/bin/bash
set -e

# Send POST request to create influxdb databases
while ! curl -sL -I "http://influxdb:8086/ping" > /dev/null; do
  echo "Waiting for InfluxDB container to start..."
  sleep 1
done

echo 'Creating databases...'
curl -XPOST "http://influxdb:8086/query" --data-urlencode "q=CREATE DATABASE data_storage"
curl -XPOST "http://influxdb:8086/query" --data-urlencode "q=CREATE DATABASE kafka_metrics"

