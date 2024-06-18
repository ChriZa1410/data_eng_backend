# processing.py
#
# This python script receives aggregated sensor data from topic_aggregated_data which contains new information of one sensor in a conditioned format.
# New sensor data will then be combined to historical data of the equivalent sensor and data type (e.g. heartbeat) and additional values are calculated.
# These contain the mean value of the data type (e.g. hearbeat), the highest value and the lowest value over time.
# It updates the historical data of the specific sensor, integrates it to the overall sensor list and sends updated information of all sensors to the topic_processed_data.

# importing necessary packages
import faust

# defining Faust streaming app
app = faust.App('data_processing', broker='kafka://broker1:29092', store='memory://')
sensor_list=[]

# defining classes for input and output data format
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

# defining Faust input and output topic serializer
input_topic = app.topic('topic_aggregated_data', key_type = str, value_type=AggregatedData)
output_topic = app.topic('topic_processed_data', key_type = str, value_type=ProcessedData)

# Faust app: receives input topic data, combines sensor information and sends out to output topic
@app.agent(input_topic)
async def process(input_messages):
    async for key, message in input_messages.items():
        
        contained=0 # indicates if sensor_list[] already contains information of specific sensor according to its ID.
        index=None

        # check if there is already data in the memory sensor_list of current sensor id
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
            # add sensor values to memory sensor list
            sensor_list.append(sensor_data)
        
        #sensor ID is already contained in memory sensor list
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

            #update mean sensor value and data count
            output_mean = (memory_mean * memory_mean_count + int(message.sensor_value)) / (memory_mean_count+1)
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
            
            #update list element with new sensor data
            sensor_list[index] = sensor_data

        # printing current output to stdOut
        print(f'Writing processed data: {key} - {sensor_list}')

        # producing data to output topic
        await output_topic.send(key = key, value=sensor_list)

# starting script
if __name__ == '__main__':
    app.main()