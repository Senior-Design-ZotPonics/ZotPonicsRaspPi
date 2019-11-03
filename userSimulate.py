import time
import datetime
import sqlite3
from random import randint

def UserInputFactor(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,nutrientratio=80,baselevel=10):
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
            "NUTRIENTRATIO" REAL,
            "BASELEVEL" REAL
        );
        ''')
        conn.execute("INSERT INTO CONTROLFACTORS (TIMESTAMP,LIGHTSTARTTIME,LIGHTENDTIME,HUMIDITY,TEMPERATURE,WATERINGFREQ,NUTRIENTRATIO,BASELEVEL)\nVALUES ('{}',{},{},{},{},{},{},{})".format(timestamp,lightstart,lightend,humidity,temp,waterfreq,nutrientratio,baselevel))

        conn.commit()
    finally:
        conn.close()

def randomUserInputFactors(n=10,sleepTime=5):
    """
    n<int>: the number of times we want to imput
    sleepTime<int>: the duration of sleeping between each post
    """
    for i in range(n):
        #generate the random integers
        lightStart = randint(0,12)
        lightEnd   = randint(13,23)
        humidityMax = randint(0,100)
        tempMax = randint(0,100)
        wateringDuration = randint(0,500)

        wateringFreq = randint(0,300)
        baseLevel = randint(0,20)
        #input the random integers into the data base
        UserInputFactor(lightStart,lightEnd,humidityMax,tempMax,wateringFreq,wateringDuration,baseLevel)

        #add some delay
        time.sleep(sleepTime)

def UserActivateControl(fans=0,vents=1,lights=0,water=1,notify=1):
    """
    This function is for the demo mode where users can activate the control
    growth factors
    """
    try:
        conn = sqlite3.connect("zotponics.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS "USERDEMO" (
            "FAN" BIT,
            "VENTS" BIT,
            "LIGHTS" BIT,
            "WATER" BIT,
            "BASELEVELNOTIFY" BIT
        );
        ''')
        conn.execute("INSERT INTO USERDEMO (FAN,VENTS,LIGHTS,WATER,BASELEVELNOTIFY)\nVALUES ({},{},{},{},{})".format(fans,vents,lights,water,notify))
        conn.commit()
    finally:
        conn.close()

if __name__ == "__main__":
    randomUserInputFactors()
    UserActivateControl()
