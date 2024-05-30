import faust
import csv
import io
import json

app = faust.App('data_aggregation', broker='kafka://broker:29092', store='memory://')

input_topic = app.topic('topic_raw_data', key_type=None, value_type=str)
output_topic = app.topic('topic_aggregated_data', key_type=None, value_type=str)

# class InputEvent(faust.Record):
#     value: str

# class OutputEvent(faust.Record):
#     value: str

@app.agent(input_topic)
async def InputEvent(input_messages):
    print("starting now...")
    async for key, message in input_messages.items():
        print(f'Got value {message}')
        print(f'Got key {key}')
        output_message = message.upper()
        print(f'Writing {output_message}')
        await output_topic.send(key=key, value=output_message)
        # csv_reader = csv.DictReader(io.StringIO(event))
        # for row in csv_reader:
        #     print('raw_data: ' + row)
        #     json_data = json.dumps(row)
        #     print('json_data: ' + json_data)
        #     await output_topic.send(value=json_data)

if __name__ == '__main__':
    app.main()

# import faust
# import csv
# import io
# import json

# # Faust app definieren
# app = faust.App('faust_app', broker='kafka://broker:29092', store='memory://')

# # Topics definieren
# input_topic = app.topic('topic_raw_data', value_type=str)
# output_topic = app.topic('topic_aggregated_data', value_type=str)

# # Agent definieren, der Nachrichten verarbeitet
# @app.agent(input_topic)
# async def process(stream):
#     async for event in stream:
#         csv_reader = csv.DictReader(io.StringIO(event))
#         for row in csv_reader:
#             print(row)
#             json_data = json.dumps(row)
#             print(json_data)
#             await output_topic.send(value=json_data)

# # Main-Methode
# if __name__ == '__main__':
#     app.main()