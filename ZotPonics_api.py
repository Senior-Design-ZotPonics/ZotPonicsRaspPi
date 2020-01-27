"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Python Version 3.7
Dependencies:
    - pip install Flask
Resources:
    - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
#!flask/bin/python
from flask import Flask, jsonify, make_response, request
import sqlite3
import datetime, time

app = Flask(__name__)

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
        conn = sqlite3.connect("zotponics.db")
        cursor = conn.execute("SELECT * FROM LAST_WATERED ORDER BY TIMESTAMP DESC LIMIT 1")
        wateredTimestamp = next(cursor)[0] #converting it back into a datetime object
        cursor = conn.execute("SELECT * FROM SENSOR_DATA ORDER BY TIMESTAMP DESC LIMIT 1")
        timestamp, temperature, humidity, baseLevel, plantHeight = next(cursor)
    except StopIteration:
        #this means that the table is empty, don't do anything
        pass
    finally:
        conn.close()

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
    readings[0]['lightStatus'] = str(lightOn) # TODO:

    return jsonify({'readings': readings})

@app.route('/usercontrolgrowth', methods=['GET', 'POST'])
def create_task():
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
            UserInputFactor(lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel)

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
        try:
            conn = sqlite3.connect("zotponics.db")
            cursor = conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")
            timestamp, lightStartTime, lightEndTime, humidity, temperature, waterFreq, waterDuration, nutrientRatio, baseLevel = next(cursor)
        except StopIteration:
            #this means that the table is empty, don't do anything
            pass
        finally:
            conn.close()

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

def UserInputFactor(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,waterdur=60,nutrientratio=80,baselevel=10):
    """
    lightstart<int>
    lightend<int>
    humidity<int>
    temp<int>
    waterfreq<int>
    nutrientratio<int>
    """
    try:
        conn = sqlite3.connect("zotponics.db")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('''CREATE TABLE IF NOT EXISTS "CONTROLFACTORS" (
            "TIMESTAMP" TEXT NOT NULL,
            "LIGHTSTARTTIME"    REAL,
            "LIGHTENDTIME"  REAL,
            "HUMIDITY"   REAL,
            "TEMPERATURE"   REAL,
            "WATERINGFREQ"  REAL,
            "WATERINGDURATION" REAL,
            "NUTRIENTRATIO" REAL,
            "BASELEVEL" REAL
        );
        ''')
        conn.execute("INSERT INTO CONTROLFACTORS (TIMESTAMP,LIGHTSTARTTIME,LIGHTENDTIME,HUMIDITY,TEMPERATURE,WATERINGFREQ,WATERINGDURATION,NUTRIENTRATIO,BASELEVEL)\nVALUES ('{}',{},{},{},{},{},{},{},{})".format(timestamp,lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel))

        conn.commit()
    finally:
        conn.close()

def _getLightStartEnd():
    lightStartTime, lightEndTime = 0,0
    try:
        conn = sqlite3.connect("zotponics.db")
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        cursor = conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")
        _, lightStartTime, lightEndTime, _, _, _, _, _, _ = next(cursor)
        conn.commit()
    finally:
        conn.close()
    return lightStartTime, lightEndTime


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0') # TODO: make server exclusive
