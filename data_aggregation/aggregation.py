import faust
import json
import random
import datetime as dt

app = faust.App('data_aggregation', broker='kafka://broker:29092', store='memory://')

input_topic = app.topic('topic_raw_data', key_type=None)
output_topic = app.topic('topic_aggregated_data', key_type=None, value_type=str)

def round_seconds(date):
    obj=dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)

@app.agent(input_topic)
async def InputEvent(input_messages):
    async for key, message in input_messages.items():
        
        split = message.split(",")
        split[2] = str(round_seconds(split[2]))
        dictionary = {
            "sensor_id" : split[0],
            "data_type" : split[1],
            "timestamp" : split[2],
            "sensor_value": split[3]
        }
        output_message = json.dumps(dictionary)
        key=random.randint(1,100)
        print(f'Writing aggregated data: {key} - {output_message}')
        await output_topic.send(key=str(key), value=output_message)

if __name__ == '__main__':
    app.main()