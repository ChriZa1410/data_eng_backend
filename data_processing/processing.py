import faust
import json

app = faust.App('data_processing', broker='kafka://broker:29092', store='memory://')

input_topic = app.topic('topic_aggregated_data', key_type=str, value_type=json)
output_topic = app.topic('topic_processed_data', key_type=str, value_type=json)

@app.agent(input_topic)
async def InputEvent(input_messages):
    async for key, message in input_messages:
            
        #split = message.split(",")
        # dictionary = {
        #     "sensor_id" : split[0],
        #     "data_type" : split[1],
        #     "timestamp" : pandas.to_datetime(split[2]).round('1s'),
        #     "sensor_value": split[3]
        # }
        output_message = message.upper()
        print(f'Writing processed data: {key} - {output_message}')
        await output_topic.send(key=str(key), value=output_message)

if __name__ == '__main__':
    app.main()