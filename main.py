import tinytuya
import time
import pandas as pd
import requests


c = tinytuya.Cloud(
        apiRegion="eu", 
        apiKey="5nkgk7ymdqx8pcvqu9m3", 
        apiSecret="2e3ec86384024cda9ded1f07fdb8d490", 
        apiDeviceID="bf14abece2e472121cfe0b")

# Display list of devices
def get_device_list():
    device_list = []
    devices = c.getdevices()
    return devices
 

def get_properties():
    # Display Properties of Device
    result = c.getproperties(id)
    #print("Properties of device:\n", result)

def get_status(id):

    # Display Status of Device
    
    data = c.getstatus(id)
    #print("Status of device:\n", data)
    for item in data['result']:
        if item['code'] == 'cur_power':
            cur_power = item['value']
            break
    
    wh = round(cur_power*0.017,2) 
    
    return wh


def send_command(id, status):
# Send Command - Turn on switch
    if status == 1:
        commands = {
            "commands": [
                {"code": "switch_1", "value": True},
                {"code": "countdown_1", "value": 0},
            ]
        }
        print("Sending command...")
        result = c.sendcommand(id,commands)
        print("Results\n:", result)
    if status == 0:
        commands = {
            "commands": [
                {"code": "switch_1", "value": False},
                {"code": "countdown_1", "value": 0},
            ]
        }
        print("Sending command...")
        result = c.sendcommand(id,commands)
        print("Results\n:", result)
get_device_list()

