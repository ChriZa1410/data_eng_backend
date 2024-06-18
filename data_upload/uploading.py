# uploading.py
#
# This python script receives processed data from topic_processed_data which contains current information of all sensors.
# It sends data of the single sensors separately to the topic_upload_data which represents the upload data to the database.


# importing necessary packages
import faust
import avro.schema
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# defining Faust streaming app
app = faust.App('data_upload', broker='kafka://broker1:29092', store='memory://')

# defining schema of output topic
upload_schema_str = """
{"fields": [{"doc": "The ID of the smartwatch sensor.","name": "sensor_id","type": "int"},{"doc": "The type of data the sensor provides (e.g. heart rate).","name": "data_type","type": "string"},{"doc": "The timestamp when the sensor data was recorded.","name": "timestamp","type": "string"},{"doc": "The current value of the data which the sensor recorded.","name": "current_value","type": "int"},{"doc": "The mean value of the data type which the sensor with the specific ID recorded.","name": "mean_value","type": "float"},{"doc": "The count of values the sensor with this ID already recorded.","name": "mean_count","type": "int"},{"doc": "The highest value of the data type which the sensor with the specific ID recorded.","name": "highest_value","type": "int"},{"doc": "The lowest value of the data type which the sensor with the specific ID recorded.","name": "lowest_value","type": "int"}],"name": "value_topic_processed_data","type": "record"}
"""
upload_schema=avro.loads(upload_schema_str)

# configuring avro producer for sending data to output topic for database import
avro_producer_config = {
    'bootstrap.servers': 'broker1:29092,broker2:29092,broker3:29092',
    'schema.registry.url': 'http://schema-registry:8081'
}
producer = AvroProducer(avro_producer_config, default_value_schema=upload_schema)

# defining Faust input and output topic serializer
input_topic = app.topic('topic_processed_data', key_type = str) 
output_topic = app.topic('topic_upload_data', value_serializer='raw')

# Faust app: receives input topic data, separates sensor information and sends out to output topic
@app.agent(input_topic)
async def process(input_messages):
    async for key, message in input_messages.items():
        for index in message:
            
            # printing current output to stdOut
            print(f'Uploading sensor data to database: {index}')

            # producing data to output topic
            producer.produce(topic='topic_upload_data', value=index)
            producer.flush

# starting script
if __name__ == '__main__':
    app.main()