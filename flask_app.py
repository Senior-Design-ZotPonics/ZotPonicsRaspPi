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

    lightStartTime, lightEndTime = _getLightStartEnd()
    hour = datetime.datetime.now().hour #returns hour in 24hr format int
    if (hour >= lightStartTime and hour < lightEndTime):
        lightOn = True
    else:
        lightOn = False

    readings[0]['lastWateredTimestamp'] = wateredTimestamp
    readings[0]['timestamp'] = timestamp
    readings[0]['temperature'] = temperature
    readings[0]['humidity'] = humidity
    readings[0]['baseLevel'] = baseLevel
    readings[0]['plantHeight'] = plantHeight
    readings[0]['lightStatus'] = str(lightOn)

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
        return "No GET Method"

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
        readings = [
            {
                'lastwatered': None
            },
        ]

        last_watered = None
        account = _getAccountInfo("/home/okyang/config.json")
        try:
            db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
            conn = db.cursor()
            conn.execute("SELECT * FROM LAST_WATERED ORDER BY TIMESTAMP LIMIT 1")
            last_watered = conn.fetchone()
            conn.close()
        except StopIteration:
            #this means that the table is empty, don't do anything
            pass
        except Exception as e:
            return e

        readings[0]['last_watered'] = last_watered

        return jsonify({'readings': readings})

@app.route('/usercontrolgrowth', methods=['GET', 'POST'])
def control_factors():
    if request.method == 'POST':
        if not request.json:
            abort(400)
        postData = request.json["controlfactors"]
        for row in postData:
            lightstart = row["lightstart"]
            lightend = row["lightend"]
            humidity = row["humidity"]
            temp = row["temp"]
            waterfreq = row["waterfreq"]
            waterdur = row["waterdur"]
            nutrientratio = row["nutrientratio"]
            baselevel = row["baselevel"]
            _UserInputFactor(lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel)

        return "Created: " + str(request.json), 201
    else:
        readings = [
            {
                'timestamp': None,
                'lightStartTime': None,
                'lightEndTime': None,
                'humidity': None,
                'temperature': None,
                'waterFreq': None,
                'waterDuration': None,
                'nutrientRatio': None,
                'baseLevel': None
            },
        ]

        timestamp, lightStartTime, lightEndTime, humidity, temperature, waterFreq, waterDuration, nutrientRatio, baseLevel = None, None, None, None, None, None, None, None, None

        account = _getAccountInfo("/home/okyang/config.json")
        try:
            db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
            conn = db.cursor()
            conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")
            timestamp, lightStartTime, lightEndTime, humidity, temperature, waterFreq, waterDuration, nutrientRatio, baseLevel = conn.fetchone()
            conn.close()
        except StopIteration:
            #this means that the table is empty, don't do anything
            pass
        except Exception as e:
            return e

        readings[0]['timestamp'] = timestamp
        readings[0]['lightStartTime'] = lightStartTime
        readings[0]['lightEndTime'] = lightEndTime
        readings[0]['humidity'] = humidity
        readings[0]['temperature'] = temperature
        readings[0]['waterFreq'] = waterFreq
        readings[0]['waterDuration'] = waterDuration
        readings[0]['nutrientRatio'] = nutrientRatio
        readings[0]['baseLevel'] = baseLevel

        return jsonify({'readings': readings})

@app.route('/userdemo', methods=['GET', 'POST'])
def user_demo():
    """
    Immediate Control Values will include:
    - fan+vents for (for 10 seconds)
    - just vents (for 10 seconds)
    - lights (for 10 seconds)
    - water (for 10 seconds)
    - baselevelnotify (notify)

    The table must also include only one row.
    """
    if request.method == 'POST':
        if not request.json:
            abort(400)
        postData = request.json["user_demo"]
        for row in postData:
            fanvents = row["fanvents"]
            vents = row["vents"]
            lights = row["lights"]
            water = row["water"]
            baselevelnotify = row["baselevelnotify"]

            #updates the SensorTable
            _updateDemoTable(fanvents,vents,lights,water,baselevelnotify)

        return "Created: " + str(request.json), 201
    else:
        readings = [
            {
                'fanvents': None,
                'vents': None,
                'lights': None,
                'water': None,
                'baselevelnotify': None
            },
        ]

        fanvents,vents,lights,water,baselevelnotify = None, None, None, None, None
        account = _getAccountInfo("/home/okyang/config.json")
        try:
            db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
            conn = db.cursor()
            conn.execute("SELECT * FROM USERDEMO LIMIT 1")
            fanvents,vents,lights,water,baselevelnotify = conn.fetchone()

            #delete all rows in the table so it doesn't activate again
            conn.execute("DELETE FROM USERDEMO;")
            #
            # #commit and close
            db.commit()
            conn.close()

        except StopIteration:
            #this means that the table is empty, don't do anything
            pass
        except Exception as e:
            return e

        readings[0]['fanvents'] = fanvents
        readings[0]['vents'] = vents
        readings[0]['lights'] = lights
        readings[0]['water'] = water
        readings[0]['baselevelnotify'] = baselevelnotify

        return jsonify({'readings': readings})

def _updateDemoTable(fanvents,vents,lights,water,baselevelnotify):
    """
    """
    account = _getAccountInfo("/home/okyang/config.json")
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS USERDEMO (
            FAN TINYINT,
            VENTS TINYINT,
            LIGHTS TINYINT,
            WATER TINYINT,
            BASELEVELNOTIFY TINYINT
        );
        ''')
        conn.execute("INSERT INTO USERDEMO (FAN,VENTS,LIGHTS,WATER,BASELEVELNOTIFY)\nVALUES ({},{},{},{},{})".format(fanvents,vents,lights,water,baselevelnotify))
        db.commit()
        conn.close()
    except Exception as e:
        return e


def _UserInputFactor(lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel):
    """
    This function is to help with inputing the control growth factors data.
    lightstart<int>
    lightend<int>
    humidity<int>
    temp<int>
    waterfreq<int>
    nutrientratio<int>
    """
    account = _getAccountInfo("/home/okyang/config.json")
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('''CREATE TABLE IF NOT EXISTS CONTROLFACTORS (
            TIMESTAMP varchar(255) not null,
            LIGHTSTARTTIME    float(24),
            LIGHTENDTIME  float(24),
            HUMIDITY   float(24),
            TEMPERATURE   float(24),
            WATERINGFREQ  float(24),
            WATERINGDURATION float(24),
            NUTRIENTRATIO float(24),
            BASELEVEL float(24)
        );
        ''')
        db.commit()
        conn.execute("INSERT INTO CONTROLFACTORS (TIMESTAMP,LIGHTSTARTTIME,LIGHTENDTIME,HUMIDITY,TEMPERATURE,WATERINGFREQ,WATERINGDURATION,NUTRIENTRATIO,BASELEVEL)\nVALUES ('{}',{},{},{},{},{},{},{},{})".format(timestamp,lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel))
        db.commit()
        conn.close()
    except Exception as e:
        return e

def _updateWateredTable(last_watered):
    """
    Adds the lastwatered timestamp to the database
    last_watered[str]: timestamp in the format '%Y-%m-%d %H:%M:%S'
    """
    account = _getAccountInfo("/home/okyang/config.json")
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
    account = _getAccountInfo("/home/okyang/config.json")
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
    account = _getAccountInfo("/home/okyang/config.json")
    try:
        db = MySQLdb.connect(host="okyang.mysql.pythonanywhere-services.com",user=account["username"],passwd=account["password"],db=account["database"])
        conn = db.cursor()
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")

        _, lightStartTime, lightEndTime, _, _, _, _, _, _ = conn.fetchone()
        db.commit()
    finally:
        return (lightStartTime, lightEndTime)
