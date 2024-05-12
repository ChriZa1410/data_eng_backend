#!/bin/bash

set -e

# Define database 
DB_NAME=smartwatch_database

# Send POST request to create schema
#echo 'Waiting for server start...'
#sleep 45
echo 'Creating database $DB_NAME...'

docker-compose exec influxdb influx -execute "CREATE DATABASE $DB_NAME"