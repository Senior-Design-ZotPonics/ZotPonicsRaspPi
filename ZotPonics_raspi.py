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

        #=======User and sensor activated Variables========
        self.lightOn = False
        self.vent = False
        self.fan = False
        self.water = False

        #======control Logic Variables======
        self.lightTimer = time.time()

    def run(self):
        while True:
            #======DATA COLLECTION=======
            sensorData = self.sensorCollect() #this is a list  of (timestamp,temperature,humidity,baseLevel) #also updates the database

            #======CONTROL GROWTH FACTORS=====
            self.controlGrowthFactors(sensorData)

            #======READ USER ACTIVIATED CONTROLS=========
            ## Skip this for now
            # self.readUserActControls()

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
        <oky>: FOCUS ON THIS LATER
        This will be determined later by how we interface the mobile app.
        Right now to simulate this we will just have another table in
        zotbins.db
        Immediate Control Values will include:
        - fan+vents
        - just vents
        - lights
        - water

        There will be only 2 options that can be entered
        There will be 3 options that can be entered in as a value for the
        other variables.
        - NULL: No Action
        - 1: Turn On
        - 2: Turn Off

        The table must also include only one row.
        """
        conn = sqlite3.connect("zotponics.db")
        conn.execute('''CREATE TABLE IF NOT EXISTS "IMMEDIATE_INPUTS" (
            "ISCHANGED" BIT,
            "FAN" BIT,
            "VENTS" BIT,
            "LIGHTS" BIT,
            "WATER" BIT
        );
        ''')
        conn.execute("INSERT INTO SENSOR_DATA (TIMESTAMP,TEMPERATURE,HUMIDITY,BASE_LEVEL)\nVALUES ('{}',{},{},{})".format(timestamp,temperature,humidity,base_level))
        conn.commit()
        conn.close()

    def readUserControlFactors(self):
        """
        This will read the user control growth factors.

        The table used for this must only include one row and include
        the following columns:
        - "LIGHTSTARTTIME" REAL,
        - "LIGHTENDTIME" REAL,
        - "HUMDITY" REAL,
        - "TEMPERATURE" REAL,
        - "WATERINGFREQ" REAL,
        - "NUTRIENTRATIO" REAL
        """
        # conn = sqlite3.connect("zotponics.db")
        #
        # # conn.execute('''CREATE TABLE IF NOT EXISTS "CONTROLFACTORS" (
        # #     "LIGHTSTARTTIME" REAL,
        # #     "LIGHTENDTIME" REAL,
        # #     "HUMDITY" REAL,
        # #     "TEMPERATURE" REAL,
        # #     "WATERINGFREQ" REAL,
        # #     "NUTRIENTRATIO" REAL
        # # );
        # # ''')
        # # conn.execute()
        # # conn.commit()
        # # conn.close()

    def sensorCollect(self,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False):
        """
        This is the main function for sensor data collections. It updates the database and
        returns the outputs as a tuple.
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
