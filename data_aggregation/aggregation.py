import faust
import random
import datetime as dt

app = faust.App('data_aggregation', broker='kafka://broker:29092', store='memory://')

class AggregatedData(faust.Record):
    sensor_id : int
    data_type : str
    timestamp : str
    sensor_value: int

input_topic = app.topic('topic_raw_data')
output_topic = app.topic('topic_aggregated_data', key_type=str, value_type=AggregatedData)

def round_seconds(date):
    obj=dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)

@app.agent(input_topic)
async def InputEvent(input_messages):
    async for key, message in input_messages.items():
        
        split = message.split(",")

        output_message = AggregatedData(
            sensor_id = int(split[0]),
            data_type = split[1],
            timestamp = str(round_seconds(split[2])),
            sensor_value= int(split[3])
        )

        key=random.randint(1,100)
        print(f'Writing aggregated data: {key} - {output_message}')
        await output_topic.send(key=str(key), value=output_message)

if __name__ == '__main__':
    app.main()