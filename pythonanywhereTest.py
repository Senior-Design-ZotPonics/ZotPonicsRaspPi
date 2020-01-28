import datetime, time
import json
import requests

BASEURL = "http://okyang.pythonanywhere.com"
HEADERS = {"Content-Type": "application/json","Accept": "application/json"}


def _getAccountInfo(config_file="config.json"):
    """
    """
    data_dict = None
    with open(config_file) as json_file:
        data = json.load(json_file)
        data_dict = data["account"][0]
    return data_dict

def postSensorData(temperature,humidity,base_level,plant_height):
    """
    Adds data to mySQL
    timestamp<str>: timestamp in the format '%Y-%m-%d %H:%M:%S'
    temperature<float>: the read temperature value
    humidity<float>: the read humidity value
    base_level<float>: the read base water level value
    plant_height<float>: the read plant height value
    """
    postRequest = {"sensorData":[{"temperature":temperature,"humidity":humidity,"base_level":base_level,"plant_height":plant_height}]}

    r = requests.post(BASEURL +"/add-sensor-data", data=json.dumps(postRequest), headers=HEADERS)
    print("query status: ", r.status_code, r.text)

def postWateredData(last_watered):
    """
    Adds data to mySQL
    last_watered<str>: timestamp in the format '%Y-%m-%d %H:%M:%S'
    """
    postRequest = {"waterTime":[{"last_watered":last_watered}]}

    r = requests.post(BASEURL +"/add-lastwatered-data", data=json.dumps(postRequest), headers=HEADERS)
    print("query status: ", r.status_code, r.text)

if __name__ == "__main__":
    #print(_getAccountInfo())
    postSensorData(50,50,2,2)
    #last_watered = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    #postWateredData(last_watered)
