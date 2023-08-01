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
# Define callback functions for MQTT events
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print("Message published with message id: " + str(mid))

def on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker with result code: " + str(rc))
def send_Thingsboard_price(price,curr_power,id):       
        # MQTT broker configuration
        broker_url = "thingsboard.cloud"
        broker_port = 1883  # Default MQTT port
        #username = "2EO0t4sN6Dh7ksz6Iwz4"
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
       
        if id == 'bf2a3f11b3656f64b6m3j0':
            name = 'Projektorius kaina'
            payload = {
                
                name: ((curr_power/60/1000)*(price/1000))
        }
            
        if id =='bf14abece2e472121cfe0b':
            name = 'Wifi Plug kaina'
            payload = {
                name: ((curr_power/60/1000)*(price/1000))
        }
        if id == 'bf485e5cbfd699d6e55hkk':
            name = 'Nous A1 3 kaina'
            payload = {
                name: ((curr_power/60/1000)*(price/1000))
        }

        #payload = {
         #       "id": id,
        #        "power": curr_power
        #}
        print (payload)
        # Convert payload to JSON string
        payload_json = json.dumps(payload)
         # Publish payload to ThingsBoard
        client.publish(topic, payload_json)
        # Wait for all messages to be sent and received
        client.loop(20)
def send_Thingsboard(curr_power,id):       
        # MQTT broker configuration
        broker_url = "thingsboard.cloud"
        broker_port = 1883  # Default MQTT port
        #username = "2EO0t4sN6Dh7ksz6Iwz4"
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
        if id == 'bf2a3f11b3656f64b6m3j0':
            name = 'Projektorius'
            payload = {
                
                name: curr_power
        }
            
        if id =='bf14abece2e472121cfe0b':
            name = 'Wifi Plug'
            payload = {
                name: curr_power
        }
        if id == 'bf485e5cbfd699d6e55hkk':
            name = 'Nous A1 3'
            payload = {
                name: curr_power
        }

        #payload = {
         #       "id": id,
        #        "power": curr_power
        #}
        print (payload)
        # Convert payload to JSON string
        payload_json = json.dumps(payload)
         # Publish payload to ThingsBoard
        client.publish(topic, payload_json)
        # Wait for all messages to be sent and received
        client.loop(20)
import requests
import datetime
from datetime import date, timedelta

def download_litgrid_data(start_year, start_month, start_day, end_year, end_month, end_day):
    # Convert input integers to date objects
    start_date = date(start_year, start_month, start_day)
    end_date = date(end_year, end_month, end_day)
    # Construct date strings for URL
    from_date_str = start_date.isoformat()
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

# Example usage: download data from May 1st to May 5th 2023