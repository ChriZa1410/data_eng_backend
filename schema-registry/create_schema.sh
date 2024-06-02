#!/bin/bash

set -e

# Define schema JSON
#SCHEMA='{"schema": "{\"type\":\"record\",\"name\":\"value_wikimedia\",\"namespace\":\"wikimedia\",\"fields\":[{\"name\":\"bot\",\"type\":[\"null\",\"boolean\"],\"default\":null},{\"name\":\"comment\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"id\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"length\",\"type\":[\"null\",{\"type\":\"record\",\"name\":\"Length\",\"fields\":[{\"name\":\"new\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"old\",\"type\":[\"null\",\"int\"],\"default\":null}]}],\"default\":null},{\"name\":\"meta\",\"type\":[\"null\",{\"type\":\"record\",\"name\":\"Meta\",\"fields\":[{\"name\":\"domain\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"dt\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"id\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"offset\",\"type\":[\"null\",\"long\"],\"default\":null},{\"name\":\"partition\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"request_id\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"stream\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"topic\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"uri\",\"type\":[\"null\",\"string\"],\"default\":null}]}],\"default\":null},{\"name\":\"minor\",\"type\":[\"null\",\"boolean\"],\"default\":null},{\"name\":\"namespace\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"parsedcomment\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"patrolled\",\"type\":[\"null\",\"boolean\"],\"default\":null},{\"name\":\"revision\",\"type\":[\"null\",{\"type\":\"record\",\"name\":\"Revision\",\"fields\":[{\"name\":\"new\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"old\",\"type\":[\"null\",\"int\"],\"default\":null}]}],\"default\":null},{\"name\":\"schema\",\"type\":[\"null\",\"string\"],\"doc\":\"Theoriginalfieldnamewas'$schema'butsomecharactersisnotacceptedinthefieldnameofAvrorecord\",\"default\":null},{\"name\":\"server_name\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"server_script_path\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"server_url\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"timestamp\",\"type\":[\"null\",\"int\"],\"default\":null},{\"name\":\"title\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"type\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"user\",\"type\":[\"null\",\"string\"],\"default\":null},{\"name\":\"wiki\",\"type\":[\"null\",\"string\"],\"default\":null}]}"}'
SCHEMA_UPLOAD='{"schema": "{\"type\":\"record\", \"name\":\"value_db_upload\", \"fields\":[{\"name\":\"bar\",\"type\":\"string\"}, {\"name\":\"baz\",\"type\":\"float\"}]}"}'
SCHEMA_CSV_SOURCE='{"schema": "{\"type\":\"record\", \"name\":\"CSVRecord\", \"fields\":[{\"name\": \"id\",\"type\": \"int\"}, {\"name\": \"data_type\", \"type\": \"string\"}, {\"name\": \"sample_timestamp\", \"type\": \"string\"},{\"name\": \"current_heartrate\", \"type\": \"float\"},{\"name\": \"source\", \"type\": \"int\"}]}"}'
SCHEMA_AGGREGATED_DATA='{"schema": "{\"fields\": [{\"doc\": \"The ID of the smartwatch sensor.\",\"name\": \"sensor_id\",\"type\": \"int\"},{\"doc\": \"The type of data the sensor provides (e.g. heart rate).\",\"name\": \"data_type\",\"type\": \"string\"},{\"doc\": \"The timestamp when the sensor data was recorded.\",\"name\": \"timestamp\",\"type\": \"string\"},{\"doc\": \"The value of the data which the sensor recorded.\",\"name\": \"sensor_value\",\"type\": \"int\"}],\"name\": \"value_topic_aggregated_data\",\"type\": \"record\"}"}'
# Send POST request to create schema
echo 'Waiting for server start...'
sleep 45

echo 'Setting schemas...'
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
      --data "$SCHEMA_UPLOAD" \
      http://schema-registry:8081/subjects/topic_upload_data-value/versions

# curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
#       --data "$SCHEMA_CSV_SOURCE" \
#       http://schema-registry:8081/subjects/topic_raw_data-value/versions

curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" \
      --data "$SCHEMA_AGGREGATED_DATA" \
      http://schema-registry:8081/subjects/topic_aggregated_data-value/versions
