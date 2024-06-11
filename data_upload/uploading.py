import faust
import avro.schema
#from avro.io import DatumWriter, BinaryEncoder
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

# import faust
# import fastavro
#from faust_avro import SchemaRegistryClient, Record

#import requests
# import json
# from time import sleep
# # 3rd party library imported
# from confluent_kafka import SerializingProducer
#from confluent_kafka.schema_registry import SchemaRegistryClient
# from confluent_kafka.schema_registry.avro import AvroSerializer
# from confluent_kafka.schema_registry import Schema

# # imort from constants
# from constants import SCHEMA_STR

app = faust.App('data_upload', broker='kafka://broker:29092', store='memory://')

#schema_registry = SchemaRegistryClient(url="http://schema-registry:8081")
upload_schema_str = """
{"fields": [{"doc": "The ID of the smartwatch sensor.","name": "sensor_id","type": "int"},{"doc": "The type of data the sensor provides (e.g. heart rate).","name": "data_type","type": "string"},{"doc": "The timestamp when the sensor data was recorded.","name": "timestamp","type": "string"},{"doc": "The current value of the data which the sensor recorded.","name": "current_value","type": "int"},{"doc": "The mean value of the data type which the sensor with the specific ID recorded.","name": "mean_value","type": "float"},{"doc": "The count of values the sensor with this ID already recorded.","name": "mean_count","type": "int"},{"doc": "The highest value of the data type which the sensor with the specific ID recorded.","name": "highest_value","type": "int"},{"doc": "The lowest value of the data type which the sensor with the specific ID recorded.","name": "lowest_value","type": "int"}],"name": "value_topic_processed_data","type": "record"}
"""

upload_schema=avro.loads(upload_schema_str)

# class UploadData(faust.Record, serializer='avro', schema_registry=schema_registry, namespace='com.example'):
#     sensor_id : int
#     data_type : str
#     timestamp : str
#     current_value: int
#     mean_value: float
#     mean_count: int
#     highest_value: int
#     lowest_value: int

avro_producer_config = {
    'bootstrap.servers': 'broker:29092',
    'schema.registry.url': 'http://schema-registry:8081'
}
producer = AvroProducer(avro_producer_config, default_value_schema=upload_schema)



input_topic = app.topic('topic_processed_data', key_type = str) #, value_type=UploadData)
output_topic = app.topic('topic_upload_data', value_serializer='raw') #key_type = str, value_type=UploadData)

#this_sensor_data:UploadData

@app.agent(input_topic)
async def process(input_messages):
    async for key, message in input_messages.items():
        for index in message:
            
            print(index)
            print(index["sensor_id"])
            #await output_topic.send(key = key, value=index)
            producer.produce(topic='topic_upload_data', value=index)
            producer.flush

if __name__ == '__main__':
    app.main()


# #init_string = 'data: '
# #source_url = 'https://stream.wikimedia.org/v2/stream/recentchange'
# kafka_url = 'broker:29092'
# schema_registry_url = 'http://schema-registry:8081'
# kafka_topic = 'topic_upload_data'
# schema_registry_subject = f"{kafka_topic}-value"

# def delivery_report(errmsg, msg):
#     if errmsg is not None:
#         print("Delivery failed for Message: {} : {}".format(msg.key(), errmsg))
#         return
#     print('Message: {} successfully produced to Topic: {} Partition: [{}] at offset {}'.format(msg.key(), msg.topic(), msg.partition(), msg.offset()))

#xxx def avro_producer(source_url, kafka_url, schema_registry_url, schema_registry_subject):
# def avro_producer(kafka_url, schema_registry_url, schema_registry_subject):
#     # schema registry
#     sr, latest_version = get_schema_from_schema_registry(schema_registry_url, schema_registry_subject)
#     counter = 0


#     value_avro_serializer = AvroSerializer(schema_registry_client = sr,
#                                           schema_str = latest_version.schema.schema_str,
#                                           conf={
#                                               'auto.register.schemas': False
#                                             }
#                                           )

#     # Kafka Producer
#     producer = SerializingProducer({
#         'bootstrap.servers': kafka_url,
#         'security.protocol': 'plaintext',
#         'value.serializer': value_avro_serializer,
#         'delivery.timeout.ms': 120000, # set it to 2 mins
#         'enable.idempotence': 'true'
#     })

#     s = requests.Session()

#     while True:
#         #sleep(2)
#         try:
        

#             producer.produce(topic=kafka_topic, value=decoded_json, on_delivery=delivery_report)

#             # Trigger any available delivery report callbacks from previous produce() calls
#             events_processed = producer.poll(1)
#             print(f"events_processed: {events_processed}")

#             messages_in_queue = producer.flush(1)
#             print(f"messages_in_queue: {messages_in_queue}")
#         except Exception as e:
#             print(e)

    
                        
# def get_schema_from_schema_registry(schema_registry_url, schema_registry_subject):
#     sr = SchemaRegistryClient({'url': schema_registry_url})
#     latest_version = sr.get_latest_version(schema_registry_subject)

#     return sr, latest_version

# def register_schema(schema_registry_url, schema_registry_subject, schema_str):
#     sr = SchemaRegistryClient({'url': schema_registry_url})
#     schema = Schema(schema_str, schema_type="AVRO")
#     schema_id = sr.register_schema(subject_name=schema_registry_subject, schema=schema)

#     return schema_id

# def update_schema(schema_registry_url, schema_registry_subject, schema_str):
#     sr = SchemaRegistryClient({'url': schema_registry_url})
#     versions_deleted_list = sr.delete_subject(schema_registry_subject)
#     print(f"versions of schema deleted list: {versions_deleted_list}")

#     schema_id = register_schema(schema_registry_url, schema_registry_subject, schema_str)
#     return schema_id
                        
# #avro_producer(source_url, kafka_url, schema_registry_url, schema_registry_subject)
# avro_producer(kafka_url, schema_registry_url, schema_registry_subject)