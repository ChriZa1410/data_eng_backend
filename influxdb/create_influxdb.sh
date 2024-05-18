#!/bin/bash

set -e

# Define database 
#DB_NAME=smartwatch_database

# Send POST request to create schema
#echo 'Waiting for server start...'
sleep 45
echo 'Creating influxdb-sink connector...'

docker-compose run kafkaconnect create influxdb-sink -d smartwatch_db db_upload
