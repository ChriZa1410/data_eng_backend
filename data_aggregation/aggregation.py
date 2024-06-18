# aggregation.py
#
# This python script receives raw sensor data from topic_raw_data which contains new information of one sensor in an unconditioned format.
# New sensor data will then be converted to a proper format for further processing steps.
# This contains splitting the input stream, rounding the timestamp to seconds, formatting sensor information to proper data types and adding a key.
# It sends the converted new data of the sensor to the topic_aggregated_data.

# importing necessary packages
import faust
import random
import datetime as dt

# defining Faust streaming app
app = faust.App('data_aggregation', broker='kafka://broker1:29092', store='memory://')

# defining classes for output data format
class AggregatedData(faust.Record):
    sensor_id : int
    data_type : str
    timestamp : str
    sensor_value: int

# defining Faust input and output topic serializer
input_topic = app.topic('topic_raw_data')
output_topic = app.topic('topic_aggregated_data', key_type=str, value_type=AggregatedData)

# defining function for rounding UTC timestamp to seconds
def round_seconds(date):
    obj=dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)

# Faust app: receives input topic data, converts sensor information and sends out to output topic
@app.agent(input_topic)
async def InputEvent(input_messages):
    async for key, message in input_messages.items():
        
        # splitting string input stream into single values
        split = message.split(",")

        # define output message
        output_message = AggregatedData(
            sensor_id = int(split[0]),
            data_type = split[1],
            timestamp = str(round_seconds(split[2])),
            sensor_value= int(split[3])
        )

        # adding key to producing topic 
        key=random.randint(1,100)

        # printing current output to stdOut
        print(f'Writing aggregated data: {key} - {output_message}')

        # producing data to output topic
        await output_topic.send(key=str(key), value=output_message)

# starting script
if __name__ == '__main__':
    app.main()