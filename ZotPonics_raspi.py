"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Notes:
- Database is "zotponics.db" for now.
Resources:
- Controlling a Servo
    - https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/
"""

import sqlite3
import datetime
import time


class ZotPonics():
    def __init__(self):
        #======Variables that should not be changed==========
        self.tempMin = 60 #Fahrenheit #<oky>: Not used, because we don't have heating element

        #======GPIO Variables that should not be changed=====

        #======Data base variabxles======
        self.sensorFreq = 300 #seconds #<oky>: Not used yet

        self.lightStartTime = 8 #int in 24hr format
        self.lightEndTime = 18 #int in 24hr format

        self.humidityMax = 80 #percentage

        self.tempMax = 100 #Fahrenheit

        self.wateringFreq = 300 #seconds
        self.wateringDuration = 100 #seconds

        self.startNutrientRatio = 30 #percentage

        self.baseLevelMin = 40 #centimeters

        #=======User and sensor activated Variables========
        self.lightOn = False
        self.vent = False
        self.fan = False
        self.water = False

        #======control Logic Variables======
        self.lightTimer = time.time()


    def setupGPIO(self,simulateAll=False):
        """
        Function to help simulate the sensors and manage GPIO import
        """
        if simulateAll:
            pass
        else:
            import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

            #====Set pin numbers====
            self.SERVO_PIN = 25
            self.FAN_PIN = 26

            #====Setup pins====
            GPIO.setup(self.SERVO_PIN,GPIO.OUT)
            GPIO.setup(self.FAN_PIN,GPIO.OUT)

            #====Setup servo motor====
            self.servo = GPIO.PWM(self.SERVO_PIN,50)
            self.servo.start(2.5)
            self.closeVent()



    def run(self,simulateAll=False,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False):
        """
        This is the main function for running all the data collection logic,
        data base reading, control growth logic, and idle state logic.

        temperSim<bool>: If True, just return 0.0 for the the temperature data.
        humidSim<bool>: If True, just return 0.0 for the the humidity data
        baseLevelSim<bool>: If True, just return 0.0 for the the base level data
        """
        #========== GPIO and/or Simulation Logic Setup=============
        if (simulateAll==True): temperSim, humidSim, baseLevelSim = True, True, True
        self.setupGPIO(simulateAll)

        #========== Main Loop ================
        while True:
            #======DATA COLLECTION=======
            sensorData = self.sensorCollect() #this is a list  of (timestamp,temperature,humidity,baseLevel) #also updates the database

            #======READ CONTROl GROWTH FACTORS====
            _, self.lightStartTime, self.lightEndTime, self.humidityMax, self.tempMax, self.wateringFreq, self.wateringDuration, self.baseLevelMin = self.readUserControlFactors()

            print(self.lightStartTime, self.lightEndTime, self.humidityMax, self.tempMax, self.wateringFreq, self.wateringDuration)

            #====== APPLY CONTROL GROWTH FACTORS LOGIC=====
            self.controlGrowthFactors(sensorData) #<sid>

            #======READ USER ACTIVIATED CONTROLS=========
            userAct = self.readUserActControls()
            print(userAct)

            #=======IDLE STATE=========
            break #just for testing

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
        Collects temperature data. User has the option to simulate the data
        if no physical sensor exists.
        simulate<bool>: If True, just return 0.0 for the the temperature data.
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def humidData(self,simulate):
        """
        Collects humidity data. User has the option to simulate the data if
        no physical sensor exists.
        simulate<bool>: If True, just return 0.0.
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def baseLevelData(self,simulate):
        """
        Collects the base water level Data. User has the option to simulate the
        data if no physical sensor exits.
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #this would be where we implement sensor GPIO logic
            return 0.0 #temporary

    def updateDatabase(self,timestamp,temperature,humidity,base_level):
        """
        Temporarily adding to sqlite, will add to MySQL.
        timestamp<str>: timestamp in the format '%Y-%m-%d %H:%M:%S'
        temperature<float>: the read temperature value
        humidity<float>: the read humidity value
        base_level<float>: the read base water level value
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

    def controlGrowthFactors(self,sensorData):
        """
        sensorData<tuple>: this is a list  of (timestamp,temperature,humidity,baseLevel)
        """
        #----Check temp/humidity and fan/vent control------
        if (sensorData[1] > self.tempMax):
            if (not self.fan):
                self.runFan()
            self.fan = True
            print("FAN IS ON")
        else:
            if (self.fan):
                self.stopFan()
            self.fan = False

        if (sensorData[1] > self.tempMax or sensorData[2] > self.humidityMax):
            if (not self.vent):
                self.openVent()
            self.vent = True
            print("VENT IS OPEN")
        else:
            if (self.vent):
                self.closeVent()
            self.vent = False

        #----Check base level and dispense reserves-------
        if (sensorData[3] <= self.baseLevelMin):
            self.water = True
            print("DISPENSE WATER")
        else:
            self.water = False

        #----Check hour and light control-------
        hour = datetime.datetime.now().hour #returns hour in 24hr format int
        if (hour >= self.lightStartTime and hour < self.lightEndTime):
            if (not self.lightOn):
                self.turnOnLight()
            self.lightOn = True
        else:
            if (self.lightOn):
                self.turnOffLight()
            self.lightOn = False

        #----Activate actuators------
        if (self.water):
            self.dispenseWater()

        #----Check reserves and notify--------
            #calculate depending on how much reserves are dispensed

    def runFan(self):
        """
        Run fan by setting fan GPIO pin to true
        """
        GPIO.output(fan, True)

    def stopFan(self):
        """
        Stop fan by setting fan GPIO pin to false
        """
        GPIO.output(fan, False)

    def openVent(self):
        """
        Set servo to 180 degree to open vent
        Duty cycle for 180 degree = 12%
        """
        self.servo.ChangeDutyCycle(12)

    def closeVent(self):
        """
        Set servo to 0 degree to close vent
        Duty cycle for 0 degree = 3%
        """
        self.servo.ChangeDutyCycle(3)

    def dispenseWater(self):
        """
        """
        #spit out water
        pass

    def turnOnLight(self):
        """
        """
        pass

    def turnOffLight(self):
        """
        """
        pass

    def readUserControlFactors(self):
        """
        This will read the user control growth factors and return the values
        sepcified in the table "CONTROLFACTORS".

        The table ("CONTROLFACTORS") contains the following columns:
        - "TIMESTAMP" TEXT NOT NULL,
        - "LIGHTSTARTTIME"    REAL,
        - "LIGHTENDTIME"  REAL,
        - "HUMIDITY"   REAL,
        - "TEMPERATURE"   REAL,
        - "WATERINGFREQ"  REAL,
        - "NUTRIENTRATIO" REAL,
        - "BASELEVEL" REAL
        """
        row = (None,self.lightStartTime,self.lightEndTime,self.humidityMax,self.tempMax,self.wateringFreq,self.wateringDuration,self.baseLevelMin)
        try:
            conn = sqlite3.connect("zotponics.db")
            cursor = conn.execute("SELECT * FROM CONTROLFACTORS ORDER BY TIMESTAMP DESC LIMIT 1")
            row = next(cursor)
        except StopIteration:
            #this means that the table is empty, don't do anything
            pass
        finally:
            conn.close()
        return row

    def readUserActControls(self):
        """
        <oky>: FOCUS ON THIS LATER
        This will be determined later by how we interface the mobile app.
        Right now to simulate this we will just have another table in
        zotbins.db

        Immediate Control Values will include:
        - fan+vents for (for 10 seconds)
        - just vents (for 10 seconds)
        - lights (for 10 seconds)
        - water (for 10 seconds)
        - baselevelnotify (notify)

        The table must also include only one row.
        """
        row=(0,0,0,0,0)
        try:
            conn = sqlite3.connect("zotponics.db")
            cursor = conn.execute("SELECT * FROM USERDEMO LIMIT 1")
            row = next(cursor)

            #delete all rows in the table so it doesn't activate again
            conn.execute("DELETE FROM USERDEMO")
            conn.commit()

        except StopIteration:
            #this means that the table is empty, nothing should be activated
            pass

        finally:
            conn.close()
        return row



if __name__ == "__main__":
    zot = ZotPonics()
    zot.run(simulateAll=True,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False)
