#!/usr/bin/env python
from confluent_kafka import Consumer, KafkaError

c = Consumer({
    'group.id': 'docker-consumers',
    'bootstrap.servers': 'broker:29092',
    'auto.offset.reset' : 'earliest',
    'enable.auto.commit' : True,
    'security.protocol' : 'plaintext'
})

c.subscribe(['testtopic'])

while True:
    msg = c.poll(timeout=1.0)
    
    if msg is None:
        print("Msg ist None")
        continue
    if msg.error():
        print('Msg has error')
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            print(msg.error())
            break

    print('Received message: {}'.format(msg.value().decode('utf-8')))
