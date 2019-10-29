import time
import datetime
import sqlite3

def UserInputFactor(lightstart=8,lightend=22,humidity=80,temp=100,waterfreq=300,nutrientratio=80):
    """
    lightstart<int>
    lightend<int>
    humidity<int>
    temp<int>
    waterfreq<int>
    nutrientratio<int>
    """
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
    conn.close()

if __name__ == "__main__":
    UserInputFactor()
