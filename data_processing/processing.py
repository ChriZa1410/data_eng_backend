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
    current_value: int
    mean_value: float
    mean_count: int
    highest_value: int
    lowest_value: int

sensor_list=[]

input_topic = app.topic('topic_aggregated_data', key_type = str, value_type=AggregatedData)
output_topic = app.topic('topic_processed_data', key_type = str, value_type=ProcessedData)

@app.agent(input_topic)
async def process(input_messages):
    async for key, message in input_messages.items():
        contained=0
        index=None
        print("message: ")
        print(message)
        # check if there is already data in the memory of current sensor id
        for element in sensor_list:
            if element.sensor_id == message.sensor_id:
                contained=1
                index = sensor_list.index(element)
                break

        #sensor ID is not yet contained in sensor memory list
        if contained == 0:

            sensor_data = ProcessedData(
                sensor_id = message.sensor_id,
                data_type = message.data_type,
                timestamp = message.timestamp,
                current_value = message.sensor_value,
                mean_value = message.sensor_value,
                mean_count = 1,
                highest_value= message.sensor_value,
                lowest_value= message.sensor_value
            )
            sensor_list.append(sensor_data)
        
        #sensor ID is already contained in sensor memory list
        else:
            memory_mean = int(sensor_list[index].mean_value)
            memory_mean_count = int(sensor_list[index].mean_count)
            memory_highest =  sensor_list[index].highest_value
            memory_lowest =  sensor_list[index].lowest_value

            #update highest sensor value
            if memory_highest < message.sensor_value:
                output_highest = message.sensor_value
            else: output_highest = memory_highest
            
            #update lowest sensor value
            if memory_lowest > message.sensor_value:
                output_lowest = message.sensor_value
            else: output_lowest = memory_lowest

            #update mean sensor value
            output_mean = (memory_mean + int(message.sensor_value)) / (memory_mean_count + 1)
            output_mean_count = memory_mean_count+1

            sensor_data = ProcessedData(
                sensor_id = message.sensor_id,
                data_type = message.data_type,
                timestamp = message.timestamp,
                current_value = message.sensor_value,
                mean_value = output_mean,
                mean_count = output_mean_count,
                highest_value= output_highest,
                lowest_value= output_lowest
            )
            
            #update list element with new data
            sensor_list[index] = sensor_data

        print(f'Writing processed data: {key} - {sensor_list}')
        await output_topic.send(key = key, value=sensor_list)

if __name__ == '__main__':
    app.main()