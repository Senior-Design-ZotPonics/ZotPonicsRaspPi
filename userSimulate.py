import time
import datetime
import sqlite3
from random import randint

def UserInputFactor(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,nutrientratio=80):
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
            "NUTRIENTRATIO" REAL
        );
        ''')
        conn.commit()
        conn.execute("INSERT INTO CONTROLFACTORS (TIMESTAMP,LIGHTSTARTTIME,LIGHTENDTIME,HUMIDITY,TEMPERATURE,WATERINGFREQ,NUTRIENTRATIO)\nVALUES ('{}',{},{},{},{},{},{})".format(timestamp,lightstart,lightend,humidity,temp,waterfreq,nutrientratio))

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
        wateringFreq = randint(0,300)
        wateringDuration = randint(0,500)

        #input the random integers into the data base
        UserInputFactor(lightStart,lightEnd,humidityMax,tempMax,wateringFreq,wateringDuration)

        #add some delay
        time.sleep(sleepTime)

if __name__ == "__main__":
    randomUserInputFactors()
