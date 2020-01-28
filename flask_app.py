"""
Authors: Owen Yang and Sid Lau
Organization: ZotPonics Inc.
Python Version: 3.7
Dependencies:
Resources:
- https://help.pythonanywhere.com/pages/UsingMySQL
- https://mysqlclient.readthedocs.io/
Notes:
- This file is for the pythonanywhere.com website
- for pythonanywhere console: pip install mysqlclient
"""

from flask import Flask, jsonify, make_response, request
import MySQLdb
import datetime, time
import json


app = Flask(__name__)

def _getAccountInfo(config_file="/home/okyang/config.json"):
    """
    """
    data_dict = None
    with open(config_file) as json_file:
        data = json.load(json_file)
        data_dict = data["account"][0]
    return data_dict

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/recentsensordata', methods=['GET'])
def get_recentSensorData():
    """
    This is the GET API for the ZotPonics system that will retrieve all the
    sensor data and return it as a json object.
    The data it will send back will include: last wateredTimestamp, timestamp,
    temperature, humidity, baseLevel, plantHeight, lightStatus
    """
    readings = [
        {
            'lastWateredTimestamp': None,
            'timestamp': None,
            'temperature': None,
            'humidity': None,
            'baseLevel': None,
            'plantHeight': None,
            'lightStatus': None
        },
    ]

    wateredTimestamp, timestamp, temperature, humidity, baseLevel, plantHeight = None, None, None, None, None, None
    try:
        account = _getAccountInfo()
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        conn.execute("SELECT * FROM LAST_WATERED ORDER BY TIMESTAMP DESC LIMIT 1;")
        wateredTimestamp = conn.fetchone() #converting it back into a datetime object
        cursor = conn.execute("SELECT * FROM SENSOR_DATA ORDER BY TIMESTAMP DESC LIMIT 1;")
        timestamp, temperature, humidity, baseLevel, plantHeight = conn.fetchone()
        conn.close()
    except StopIteration:
        #this means that the table is empty, don't do anything
        pass

    # lightStartTime, lightEndTime = _getLightStartEnd()
    # hour = datetime.datetime.now().hour #returns hour in 24hr format int
    # if (hour >= lightStartTime and hour < lightEndTime):
    #     lightOn = True
    # else:
    #     lightOn = False

    readings[0]['lastWateredTimestamp'] = wateredTimestamp
    readings[0]['timestamp'] = timestamp
    readings[0]['temperature'] = temperature
    readings[0]['humidity'] = humidity
    readings[0]['baseLevel'] = baseLevel
    readings[0]['plantHeight'] = plantHeight
    readings[0]['lightStatus'] = "True"#str(lightOn) # TODO:

    return jsonify({'readings': readings})

@app.route('/add-sensor-data', methods=['GET', 'POST'])
def add_sensor_data():
    """
    Adds sensor data to mySQL
    timestamp<str>: timestamp in the format '%Y-%m-%d %H:%M:%S'
    temperature<float>: the read temperature value
    humidity<float>: the read humidity value
    base_level<float>: the read base water level value
    plant_height<float>: the read plant height value
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        postData = request.json["sensorData"]
        for row in postData:
            temperature = row["temperature"]
            humidity = row["humidity"]
            base_level = row["base_level"]
            plant_height = row["plant_height"]

            #updates the SensorTable
            _updateSensorTable(temperature,humidity,base_level,plant_height)

        return "Created: " + str(request.json), 201
    else:
        return "Error"

@app.route('/add-lastwatered-data', methods=['GET','POST'])
def add_lastwatered():
    """
    Adds the lastwatered timestamp to the database
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        postData = request.json["waterTime"]
        for row in postData:
            last_watered = row["last_watered"]

            #updates the SensorTable
            _updateWateredTable(last_watered)

        return "Created: " + str(request.json), 201
    else:
        return "Error"
def _updateWateredTable(last_watered):
    """
    Adds the lastwatered timestamp to the database
    last_watered[str]: timestamp in the format '%Y-%m-%d %H:%M:%S'
    """
    account = _getAccountInfo("config.json")
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS "LAST_WATERED" (TIMESTAMP varchar(255) not null);''')
        conn.execute("INSERT INTO LAST_WATERED (TIMESTAMP)\nVALUES ('{}')".format(last_watered))
        db.commit()
        conn.close()
    except Exception as e:
        return e

def _updateSensorTable(temperature,humidity,base_level,plant_height):
    """
    Adds data to mySQL
    timestamp<str>: timestamp in the format '%Y-%m-%d %H:%M:%S'
    temperature<float>: the read temperature value
    humidity<float>: the read humidity value
    base_level<float>: the read base water level value
    plant_height<float>: the read plant height value
    """
    account = _getAccountInfo("config.json")
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS SENSOR_DATA (TIMESTAMP varchar(255) not null, TEMPERATURE float(24), HUMIDITY float(24),BASE_LEVEL float(24), PLANTHEIGHT float(24));''')
        conn.execute("INSERT INTO SENSOR_DATA (TIMESTAMP,TEMPERATURE,HUMIDITY,BASE_LEVEL,PLANTHEIGHT)\nVALUES ('{}',{},{},{},{})".format(timestamp,temperature,humidity,base_level,plant_height))
        db.commit()
        conn.close()
    except Exception as e:
        return e

def _getLightStartEnd():
    """
    This function gets the lightStartTime and the lightendTime
    """
    lightStartTime, lightEndTime = 0,0
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")

        _, lightStartTime, lightEndTime, _, _, _, _, _, _ = conn.fetchone()
        conn.commit()
    except Exception as e:
        return e
    return lightStartTime, lightEndTime
