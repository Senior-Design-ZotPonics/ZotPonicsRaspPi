"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Dependencies:
    - pip install Flask
Resources:
    - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
#!flask/bin/python
from flask import Flask, jsonify, make_response, request
import sqlite3

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
    readings[0]['lastWateredTimestamp'] = wateredTimestamp
    readings[0]['timestamp'] = timestamp
    readings[0]['temperature'] = temperature
    readings[0]['humidity'] = humidity
    readings[0]['baseLevel'] = baseLevel
    readings[0]['plantHeight'] = plantHeight
    #readings['lightStatus'] =  # TODO:

    return jsonify({'readings': readings})

@app.route('/usercontrolgrowth', methods=['POST'])
def create_task():
    if not request.json:
        abort(400)
    return "Created: " + str(request.json), 201

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0') # TODO: make server exclusive
