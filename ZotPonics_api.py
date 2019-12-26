"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Dependencies:
    - pip install Flask
Resources:
    - https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""
#!flask/bin/python
from flask import Flask, jsonify, make_response
import sqlite3
import datetime

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

@app.route('/recentsensordata', methods=['GET'])
def get_recentSensorData():

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

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0') # TODO: make server exclusive
