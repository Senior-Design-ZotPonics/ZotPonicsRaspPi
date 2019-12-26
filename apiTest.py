"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
"""
import datetime, time
import json
import requests

HEADERS = {
		"Content-Type": "application/json",
		"Accept": "application/json"
	}

def simplePost(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,nutrientratio=80,baselevel=10):
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    postRequest = {"controlfactors": [{"timestamp":timestamp, "lightstart":lightstart, "lightend":lightend, "humidity":humidity, "temp":temp, "waterfreq":waterfreq, "nutrientratio":nutrientratio, "baselevel":baselevel}]}

    r = requests.post("http://127.0.0.1:5000/userControlGrowth", data=json.dumps(postRequest), headers=HEADERS)
    print("query status: ", r.status_code, r.text)

if __name__ == "__main__":
    simplePost()
