"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Notes:
- Database is "zotponics.db" for now.
"""

import sqlite3
import datetime
import time

class ZotPonics():
    def __init__(self):
        #======Variables that should not be changed=======
        self.tempMin = 60 #Fahrenheit
        #======Data base variables======
        self.sensorFreq = 300 #seconds

        self.lightStartTime = 8 #int in 24hr format
        self.lightEndTime = 18 #int in 24hr format

        self.humidityMax = 80 #percentage

        self.tempMax = 100 #Fahrenheit

        self.wateringFreq = 300 #seconds
        self.wateringDuration = 100 #seconds

        self.startNutrientRatio = 30 #percentage

        #=======User Activated Variables========
        self.lightOn = False
        self.vent = False
        self.fan = False
        self.water = False

        #======control Logic Variables======
        self.lightTimer = time.time()

    def run(self):
        while True:
            #======DATA COLLECTION=======
            sensorData = self.sensorCollect() #this is a list  of (timestamp,temperature,humidity,baseLevel)

            #======CONTROL GROWTH FACTORS=====
            self.controlGrowthFactors(sensorData)

            #======READ USER ACTIVIATED CONTROLS=========
            self.readUserActControls()
            #=======IDLE STATE=========
            break #just for testing

    def controlGrowthFactors(self,sensorData):
        """
        sensorData<tuple>: this is a list  of (timestamp,temperature,humidity,baseLevel)
        """
        #----Check temp and fan control vent control------
        #----Check humidity and vent control-----
        #----Check base level and dispense reserves-------
        #----Check reserves and notify--------
        pass
    def readUserActControls(self):
        """
        This will be determined later by how we interface the mobile app.
        """
        pass
    def readUserControlFactors(self):
        """
        """
        pass
    def sensorCollect(self,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False):
        """
        This is the main function for sensor data collections
        temperSim<bool>: If True, just return 0.0 for the the temperature data.
        humidSim<bool>: If True, just return 0.0 for the the humidity data
        baseLevelSim<bool>: If True, just return 0.0 for the the base level data
        """
        #===========Data Collection=============
        #------Temperature Data (C)--------
        temperature = self.temperData(temperSim)

        #------Humidity Data (%)--------
        humidity = self.humidData(humidSim)

        #------Base Reservoir Water Level Data (cm)--------
        baseLevel = self.baseLevelData(baseLevelSim)

        #-----------Add to Database----------
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        self.updateDatabase(timestamp,temperature,humidity,baseLevel)
        return (timestamp,temperature,humidity,baseLevel)

    def temperData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def humidData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def baseLevelData(self,simulate):
        """
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def updateDatabase(self,timestamp,temperature,humidity,base_level):
        """
        Temporarily adding to sqlite, will add to MySQL
        """
        conn = sqlite3.connect("zotponics.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS "SENSOR_DATA" (
            "TIMESTAMP"	TEXT NOT NULL,
            "TEMPERATURE"	REAL,
            "HUMIDITY"	REAL,
            "BASE_LEVEL" REAL
        );
        ''')
        conn.execute("INSERT INTO SENSOR_DATA (TIMESTAMP,TEMPERATURE,HUMIDITY,BASE_LEVEL)\nVALUES ('{}',{},{},{})".format(timestamp,temperature,humidity,base_level))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    zot = ZotPonics()
    zot.run()
