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

def postControlFactors(lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel):
    """
    """
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    postRequest = {"controlfactors":[{"timestamp":timestamp,
                                    "lightstart":lightstart,
                                    "lightend": lightend,
                                    "humidity": humidity,
                                    "temp": temp,
                                    "waterfreq":waterfreq,
                                    "waterdur":waterdur,
                                    "nutrientratio":nutrientratio,
                                    "baselevel":baselevel
                                    }]}

    r = requests.post(BASEURL +"/usercontrolgrowth", data=json.dumps(postRequest), headers=HEADERS)
    print("query status: ", r.status_code, r.text)

def postUserDemo(fanvents,vents,lights,water,baselevelnotify):
    postRequest = {"user_demo":[{"fanvents":fanvents,
                                    "vents":vents,
                                    "lights": lights,
                                    "water": water ,
                                    "baselevelnotify": baselevelnotify
                                    }]}

    r = requests.post(BASEURL +"/userdemo", data=json.dumps(postRequest), headers=HEADERS)
    print("query status: ", r.status_code, r.text)

if __name__ == "__main__":
    #postSensorData(12,50,None,1)

    # last_watered = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    # postWateredData(last_watered)

    #postControlFactors(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,waterdur=10,nutrientratio=80,baselevel=10)
    postUserDemo(1,1,1,1,1)
