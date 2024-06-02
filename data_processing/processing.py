import faust

app = faust.App('data_processing', broker='kafka://broker:29092', store='memory://')

class AggregatedData(faust.Record):
    sensor_id : int
    data_type : str
    timestamp : str
    sensor_value: int

class ProcessedData(faust.Record):
    sensor_id : int
    data_type : str
    timestamp : str
    sensor_value: int
    mean_value: float
    highest_value: int
    lowest_value: int


input_topic = app.topic('topic_aggregated_data', key_type = str, value_type=AggregatedData)
output_topic = app.topic('topic_processed_data', key_type = str, value_type=ProcessedData)

@app.agent(input_topic)
async def process(input_messages):
    async for key, message in input_messages.items():
        
        processed_message = ProcessedData(
            sensor_id = message.sensor_id,
            data_type = message.data_type,
            timestamp = message.timestamp,
            sensor_value= message.sensor_value,
            mean_value = 1,
            highest_value=2,
            lowest_value=0
        )
        
        print(f'Writing processed data: {key} - {processed_message}')
        await output_topic.send(key = key, value=processed_message)

if __name__ == '__main__':
    app.main()