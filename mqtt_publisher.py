import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt
import xlrd
import numpy as np
from downloadlitgrid import download_litgrid_data
import datetime
import time
import pytz
import numpy as np
import json
from main import get_status
import datetime
from datetime import date, timedelta
import requests
from datetime import datetime


# Define callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Message published with message id: " + str(mid))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))

def send_msg(curr_power):
    
                # MQTT broker configuration
        broker_url = "thingsboard.cloud"
        broker_port = 1883  # Default MQTT port
        
        username = "USERNAME"
        topic = "v1/devices/me/telemetry"
        #payload = '{"temperature"}100}'

        # Create MQTT client instance
        client = mqtt.Client()

        # Set callback functions
        client.on_connect = on_connect
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect

        # Set username and password for authentication
        client.username_pw_set(username, password=None)

        # Connect to MQTT broker
        client.connect(broker_url, broker_port, keepalive=60)

        payload = {
            
            "values": {
                "power": curr_power
            }
        }
        print (payload)
        # Convert payload to JSON string
        payload_json = json.dumps(payload)
         # Publish payload to ThingsBoard
        client.publish(topic, payload_json)
        # Wait for all messages to be sent and received
        client.loop(20)

        # Disconnect from MQTT broker
        client.disconnect()
        
#def send_price_to_thingsboard():
def download_litgrid_data(start_year, start_month, start_day, end_year, end_month, end_day):
        # Convert input integers to date objects
        # MQTT broker configuration
    broker_url = "thingsboard.cloud"
    broker_port = 1883  # Default MQTT port
    username = "26ElUyfrUdSqNeO25gBH"
    topic = "v1/devices/me/telemetry"
    #payload = '{"temperature"}100}'

    # Create MQTT client instance
    client = mqtt.Client()

    # Set callback functions
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    # Set username and password for authentication
    client.username_pw_set(username, password=None)

    # Connect to MQTT broker
    client.connect(broker_url, broker_port, keepalive=60)

    column_data = []
    datetime_values = []
    combined_array = []
    current_datetime = datetime.now()
    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = date(int(end_year), int(end_month), int(end_day))
    # Construct date strings for URL
    from_date_str = start_date.isoformat()
    print (from_date_str)
    to_date_str = end_date.isoformat()
    
    url = f"https://www.litgrid.eu/index.php/generuoti-excel-dokumenta/475?filter[from]={from_date_str}&filter[to]={to_date_str}&lines=150"
    response = requests.get(url)

    if response.status_code == 200:
        # Get content type of response
        content_type = response.headers["content-type"]

        # Check if response content is an Excel file
        if content_type == "application/vnd.ms-excel":
            # Construct file name
            #file_name = f"Litgrid_data_{from_date_str}_{to_date_str}.xls"
            file_name = f"data/Litgrid_data_{from_date_str}_{to_date_str}.xls"

            # Write response content to file
            with open(file_name, "wb") as f:
                f.write(response.content)

            print(f"File {file_name} downloaded successfully!")
        else:
            print("Error: Response content is not an Excel file.")
    else:
        print(f"Error: Could not download data. Status code: {response.status_code}")

    
    #file = xlrd.open_workbook_xls("data/Litgrid_data_2023-05-01_2023-05-05.xls", ignore_workbook_corruption=True)
    file = xlrd.open_workbook_xls(file_name, ignore_workbook_corruption=True)
    print("Reading from ", file_name)    
    litgrid_data = pd.read_excel(file, skiprows=2)

    both_Data = []
    column_data = litgrid_data.values[: , 1]
    datetime_values = litgrid_data.values[:, 0]
    combined_array = np.column_stack((datetime_values, column_data))
    
    for timest, data_point in combined_array:
        #curr_power = get_status()
        dt = datetime.strptime(timest, "%Y-%m-%d %H:%M:%S")
        dt = dt.replace(tzinfo=pytz.UTC)
        timestamp = dt.timestamp() * 1000
        payload = {
            "ts": timestamp,
            "values": {
                "Kaina": data_point/1000
            }
        }
        #print (payload)
        # Convert payload to JSON string
        payload_json = json.dumps(payload)

        # Publish payload to ThingsBoard
        client.publish(topic, payload_json)

    # Wait for all messages to be sent and received
    client.loop(80)

    # Disconnect from MQTT broker
    client.disconnect()

def download_litgrid_current():
    column_data = []
    datetime_values = []
    combined_array = []
    current_datetime = datetime.now()
    start_day = current_datetime.strftime("%d")
    start_month = current_datetime.strftime("%m")
    start_year = current_datetime.strftime("%Y")
    end_day = current_datetime.strftime("%d")
    end_month = current_datetime.strftime("%m")
    end_year = current_datetime.strftime("%Y")
    hour = current_datetime.strftime("%H")
    print("hour", hour)
    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = date(int(end_year), int(end_month), int(end_day))
    # Construct date strings for URL
    from_date_str = start_date.isoformat()
    print (from_date_str)
    to_date_str = end_date.isoformat()
    
    url = f"https://www.litgrid.eu/index.php/generuoti-excel-dokumenta/475?filter[from]={from_date_str}&filter[to]={to_date_str}&lines=150"
    response = requests.get(url)

    if response.status_code == 200:
        # Get content type of response
        content_type = response.headers["content-type"]

        # Check if response content is an Excel file
        if content_type == "application/vnd.ms-excel":
            # Construct file name
            #file_name = f"Litgrid_data_{from_date_str}_{to_date_str}.xls"
            file_name = f"data/Litgrid_data_{from_date_str}_{to_date_str}.xls"

            # Write response content to file
            with open(file_name, "wb") as f:
                f.write(response.content)

            print(f"File {file_name} downloaded successfully!")
        else:
            print("Error: Response content is not an Excel file.")
    else:
        print(f"Error: Could not download data. Status code: {response.status_code}")

    
    #file = xlrd.open_workbook_xls("data/Litgrid_data_2023-05-01_2023-05-05.xls", ignore_workbook_corruption=True)
    file = xlrd.open_workbook_xls(file_name, ignore_workbook_corruption=True)
    print("Reading from ", file_name)    
    litgrid_data = pd.read_excel(file, skiprows=2)
    

    both_Data = []
    column_data = litgrid_data.values[: , 1]
    datetime_values = litgrid_data.values[:, 0]
    combined_array = np.column_stack((datetime_values, column_data))
    print ("combined_array", combined_array)
    for timest, data_point in combined_array:
        dt = datetime.strptime(timest, "%Y-%m-%d %H:%M:%S")
        if dt.strftime("%H") == current_datetime.strftime("%H"):
            current_price = data_point
    if current_price is not None:
        return current_price
    else :
        print ("no price")
