import csv
import random
import datetime
import time 

timestamp = datetime.datetime.today()

while 1:
    sensor_id = random.randint(1,10)
    timestamp = timestamp + datetime.timedelta(seconds=1)
    heartbeat = random.randint(60,80)
    new_row = [[sensor_id, "heart_rate", timestamp, heartbeat]]

    with open('smartwatch_heartrate_source_data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_row)
    print(new_row)
    time.sleep(1)