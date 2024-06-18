# data_simulator.py
#
# This python script simulates the smartwatch sensor. 
# It generates random sensor values every second and posts them to a *.csv file 
# which is observed by the kafka cluster as sensor input data.

# importing necessary packages
import csv
import random
import datetime
import time 

# get current UTC time
timestamp = datetime.datetime.today()

# start endless loop for generating sensor data
while 1:
    # defining random values in specific ranges for ID and heartbeat beat value
    sensor_id = random.randint(1,10)
    heartbeat = random.randint(60,80)

    # incrementing timestamp in steps of one second
    timestamp = timestamp + datetime.timedelta(seconds=1)

    # combining new sensor values to an array
    new_row = [[sensor_id, "heart_rate", timestamp, heartbeat]]

    # pasting sensor value array to *.csv file
    with open('smartwatch_heartrate_source_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_row)
    
    # printing generated sensor values to stdOut and wait for generation of next sensor value
    print(new_row)
    time.sleep(1)