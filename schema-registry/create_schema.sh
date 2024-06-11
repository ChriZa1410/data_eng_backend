#!/bin/bash

set -e

# Define schema JSON
#SCHEMA_UPLOAD='{"schema": "{\"type\":\"record\", \"name\":\"value_db_upload\", \"fields\":[{\"name\":\"bar\",\"type\":\"string\"}, {\"name\":\"baz\",\"type\":\"float\"}]}"}'
SCHEMA_AGGREGATED_DATA='{"schema": "{\"fields\": [{\"doc\": \"The ID of the smartwatch sensor.\",\"name\": \"sensor_id\",\"type\": \"int\"},{\"doc\": \"The type of data the sensor provides (e.g. heart rate).\",\"name\": \"data_type\",\"type\": \"string\"},{\"doc\": \"The timestamp when the sensor data was recorded.\",\"name\": \"timestamp\",\"type\": \"string\"},{\"doc\": \"The value of the data which the sensor recorded.\",\"name\": \"sensor_value\",\"type\": \"int\"}],\"name\": \"value_topic_aggregated_data\",\"type\": \"record\"}"}'
#SCHEMA_PROCESSED_DATA='{"schema": "{\"fields\": [{\"doc\": \"The ID of the smartwatch sensor.\",\"name\": \"sensor_id\",\"type\": \"int\"},{\"doc\": \"The type of data the sensor provides (e.g. heart rate).\",\"name\": \"data_type\",\"type\": \"string\"},{\"doc\": \"The timestamp when the sensor data was recorded (rounded to seconds).\",\"name\": \"timestamp\",\"type\": \"string\"},{\"doc\": \"The value of the data which the sensor recorded.\",\"name\": \"sensor_value\",\"type\": \"int\"},{\"doc\": \"The mean value of the data type which the sensor with the specific ID recorded.\",\"name\": \"mean_value\",\"type\": \"float\"},{\"doc\": \"The highest value of the data type which the sensor with the specific ID recorded.\",\"name\": \"highest_value\",\"type\": \"int\"},{\"doc\": \"The lowest value of the data type which the sensor with the specific ID recorded.\",\"name\": \"lowest_value\",\"type\": \"int\"}],\"name\": \"value_topic_processed_data\",\"type\": \"record\"}"}'
SCHEMA_UPLOAD_DATA='{"schema": "{\"fields\": [{\"doc\": \"The ID of the smartwatch sensor.\",\"name\": \"sensor_id\",\"type\": \"int\"},{\"doc\": \"The type of data the sensor provides (e.g. heart rate).\",\"name\": \"data_type\",\"type\": \"string\"},{\"doc\": \"The timestamp when the sensor data was recorded.\",\"name\": \"timestamp\",\"type\": \"string\"},{\"doc\": \"The current value of the data which the sensor recorded.\",\"name\": \"current_value\",\"type\": \"int\"},{\"doc\": \"The mean value of the data type which the sensor with the specific ID recorded.\",\"name\": \"mean_value\",\"type\": \"float\"},{\"doc\": \"The count of values the sensor with this ID already recorded.\",\"name\": \"mean_count\",\"type\": \"int\"},{\"doc\": \"The highest value of the data type which the sensor with the specific ID recorded.\",\"name\": \"highest_value\",\"type\": \"int\"},{\"doc\": \"The lowest value of the data type which the sensor with the specific ID recorded.\",\"name\": \"lowest_value\",\"type\": \"int\"}],\"name\": \"value_topic_processed_data\",\"type\": \"record\"}"}'

# Send POST request to create schema
echo 'Waiting for server start...'
sleep 60

echo 'Setting schemas...'
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
      --data "$SCHEMA_UPLOAD_DATA" \
      http://schema-registry:8081/subjects/topic_upload_data-value/versions

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
      --data "$SCHEMA_AGGREGATED_DATA" \
      http://schema-registry:8081/subjects/topic_aggregated_data-value/versions

# curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
#       --data "$SCHEMA_PROCESSED_DATA" \
#       http://schema-registry:8081/subjects/topic_processed_data-value/versions