"""
Authors: Sid Lau, Jason Lim, Kathy Nguyen, Owen Yang
Organization: ZotPonics Inc.
Python Version 3.7
Notes:
- Database is set up on pythonanywhere.com

Resources:
- https://stackoverflow.com/questions/366682/how-to-limit-execution-time-of-a-function-call-in-python


"""

import sqlite3
import datetime
import time
import signal
from contextlib import contextmanager
import Adafruit_DHT
import RPi.GPIO as GPIO
import json
import requests

BASEURL = "http://okyang.pythonanywhere.com"
HEADERS = {"Content-Type": "application/json","Accept": "application/json"}

class Timeout(Exception):
    """
    This is for the timed signal excpetion
    """
    pass

class ZotPonics():
    def __init__(self):
        #======Variables that should not be changed==========
        self.tempMin = 60 #Fahrenheit #<oky>: Not used, because we don't have heating element

        #======Data base variables======
        self.sensorFreq = 10 #900 #seconds #<oky>: Not used yet

        self.lightStartTime = 8 #int in 24hr format
        self.lightEndTime = 18 #int in 24hr format

        self.humidityMax = 80 #percentage

        self.tempMax = 28 #Celsius

        self.wateringFreq = 300 #seconds
        self.wateringDuration = 100 #seconds

        self.nutrientRatio = 30 #percentage

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
        #print("setting up")
        if simulateAll:
            pass
        else:
            #import Adafruit_DHT
            #import RPi.GPIO as GPIO
            GPIO.setmode(GPIO.BCM)

            #====Set pin numbers====
            self.SERVO_PIN = 25 #GPIO 25
            self.FAN_PIN = 6 #GPIO 26
            self.ULTRASONIC_TRIG = 23 #GPIO 23
            self.ULTRASONIC_ECHO = 24 #GPIO 24
            self.DHT11 = 4 #GPIO 4, for the temperature and humidity sensor
            self.LIGHT = 5 #GPIO 5
            self.PUMP = 26 #GPIO 6

            #====Setup pins====
            GPIO.setup(self.SERVO_PIN,GPIO.OUT)
            GPIO.setup(self.FAN_PIN,GPIO.OUT)
            GPIO.setup(self.ULTRASONIC_TRIG,GPIO.OUT)
            GPIO.setup(self.ULTRASONIC_ECHO,GPIO.IN)
            GPIO.setup(self.LIGHT,GPIO.OUT)
            GPIO.setup(self.PUMP,GPIO.OUT)


            #====Set pins as False======
            GPIO.output(self.FAN_PIN, False)
            GPIO.output(self.LIGHT, False)
            GPIO.output(self.PUMP, False)


            #====Set up the Temp and Humidity Sensor=====
            self.dht11_sensor = Adafruit_DHT.DHT11

            #====Setup servo motor====
            #self.servo = GPIO.PWM(self.SERVO_PIN,50)
            #self.servo.start(2.5)
            #self.closeVent()

    def run(self,simulateAll=False,temperSim=False,humidSim=False,baseLevelSim=False,plantHeightSim=False,demoMode=False):
        """
        This is the main function for running all the data collection logic,
        data base reading, control growth logic, and idle state logic.

        simulateAll<bool>: If True, It turns all the other boolean parameters to True.
        temperSim<bool>: If True, just return 0.0 for the the temperature data.
        humidSim<bool>: If True, just return 0.0 for the the humidity data
        baseLevelSim<bool>: If True, just return 0.0 for the the base level data
        plantHeightSim<bool>: If True, just return 0.0 for the plant height data
        demoMode<bool>: If True, the program will not collect sensor data or run "APPLY GROWTH FACTORS LOGIC"
        """
        #========== GPIO and/or Simulation Logic Setup=============
        if (simulateAll==True): temperSim, humidSim, baseLevelSim, plantHeightSim = True, True, True, True
        self.setupGPIO(simulateAll)

        #========== Main Loop ================
        while True:
            if not demoMode:
                #======DATA COLLECTION=======
                sensorData = self.sensorCollect(temperSim, humidSim, baseLevelSim, plantHeightSim) #this is a list  of (timestamp,temperature,humidity,baseLevel) #also updates the database

                #======READ CONTROl GROWTH FACTORS====
                _, self.lightStartTime, self.lightEndTime, self.humidityMax, self.tempMax, self.wateringFreq, self.wateringDuration, self.nutrientRatio, self.baseLevelMin = self.readUserControlFactors()

                print("Control Growth Factors:", "light start:",self.lightStartTime, "| light end:", self.lightEndTime, "| humidity:", self.humidityMax, "| tempMax: ",
                      self.tempMax, "| watering frequency:", self.wateringFreq, "| watering duration:", self.wateringDuration)

                #====== APPLY CONTROL GROWTH FACTORS LOGIC=====
                self.controlGrowthFactors(sensorData)

                #=======IDLE STATE=========
                time.sleep(self.sensorFreq) #just for testing

            if (demoMode):
                #======READ USER ACTIVIATED CONTROLS=========
                userAct = self.readUserActControls()
                print("User Activated Controls:", userAct)

    def sensorCollect(self,temperSim=False,humidSim=False,baseLevelSim=False,plantHeightSim=False):
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

        #------Plant Height (cm)-----------------
        plantHeight = self.plantHeightData(plantHeightSim)

        #-----------Add to Database----------
        self.updateDatabase(temperature,humidity,baseLevel,plantHeight)
        return (None,temperature,humidity,baseLevel,plantHeight)

    def temperData(self,simulate):
        """
        Collects temperature data. User has the option to simulate the data
        if no physical sensor exists.
        simulate<bool>: If True, just return 0.0 for the the temperature data.
        """
        if simulate:
            return 0.0
        else:
            try:
                with self.time_limit(10):
                    _, temperature = Adafruit_DHT.read_retry(self.dht11_sensor,self.DHT11)
                    return temperature #temporary
            except Timeout:
                return -1 #we know it failed

    def humidData(self,simulate):
        """
        Collects humidity data. User has the option to simulate the data if
        no physical sensor exists.
        simulate<bool>: If True, just return 0.0.
        """
        if simulate:
            return 0.0
        else:
            try:
                with self.time_limit(10):
                    humidity, _ = Adafruit_DHT.read_retry(self.dht11_sensor,self.DHT11)
                    return humidity #temporary
            except Timeout:
                return -1 #wee know it failed

    def baseLevelData(self,simulate):
        """
        Collects the base water level Data. User has the option to simulate the
        data if no physical sensor exits.
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            return -1 #<oky>: need to discuss with teammates, but we can ignore baseLevelData for now

    def plantHeightData(self,simulate):
        """
        Collects the base water level Data. User has the option to simulate the
        data if no physical sensor exits.
        simulate<bool>:
        """
        if simulate:
            return 0.0
        else:
            #set the Trigger to HIGH
            GPIO.output(self.ULTRASONIC_TRIG, True)

            #set the Trigger after 0.01 ms to LOW
            time.sleep(0.00001)
            GPIO.output(self.ULTRASONIC_TRIG, False)

            StartTime = time.time()
            StopTime = time.time()

            try:
                with self.time_limit(5):
                    while GPIO.input(self.ULTRASONIC_ECHO ) == 0:
                        StartTime = time.time()
                    while GPIO.input(self.ULTRASONIC_ECHO) == 1:
                        StopTime = time.time()
            except Timeout:
                return -1 #we know it failed

            TimeElapsed = StopTime - StartTime
            distance = (TimeElapsed*34300)/2
            return distance

    def updateDatabase(self,temperature,humidity,base_level,plant_height):
        """
        timestamp<str>: timestamp is automatically generated by the pythonanywhere API, so this variable is not needed

        temperature<float>: the read temperature value
        humidity<float>: the read humidity value
        base_level<float>: the read base water level value
        plant_height<float>: the read plant height value

        TODO: Test this.
        """
        postRequest = {"sensorData":[{"temperature":temperature,"humidity":humidity,"base_level":base_level,"plant_height":plant_height}]}
        r = requests.post(BASEURL +"/add-sensor-data", data=json.dumps(postRequest), headers=HEADERS)

        print("query status: ", r.status_code, r.text)

    def LastWateredTimestamp(self):
        """
        This function returns the most recent timestamp from the sql database.
        Output:
            - None (that means the table was empty)
            - timestamp in the form '%Y-%m-%d %H:%M:%S'

        TODO: test this
        """
        timestamp = None
        try:
            r = requests.get(BASEURL+"/add-lastwatered-data")
            s = r.json()
            r.close()
            timestamp = datetime.datetime.strptime(s['readings'][0]['last_watered'],'%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(e)

        return timestamp

    def updateLastWateredTable(self):
        """
        TODO: test this
        """
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        postRequest = {"waterTime":[{"last_watered":timestamp}]}
        r = requests.post(BASEURL +"/add-lastwatered-data", data=json.dumps(postRequest), headers=HEADERS)

        print("query status: ", r.status_code, r.text)

    #TODO: Fix the logic of this function
    def controlGrowthFactors(self,sensorData):
        """
        sensorData<tuple>: this is a list  of (timestamp,temperature,humidity,baseLevel)
        """
        #----Check temp/humidity and fan/vent control------
        if (sensorData[1] > self.tempMax):
            if (not self.fan):
                self.openVent()
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

        #----Check base level and notify-------
        #<oky> need to change logic here
        if (sensorData[3] <= self.baseLevelMin and sensorData[3]>0):
            print("REFILL NUTRIENT WATER")
        else:
            pass

        #------check watering frequency and water----------
        lastWateredTimestamp = self.LastWateredTimestamp()
        if (lastWateredTimestamp == None):
            self.water = True
        else:
            print("CHECKING WATERING CALCULATION:",lastWateredTimestamp,datetime.datetime.now())
            timeDifference = (datetime.datetime.now() - lastWateredTimestamp).total_seconds()
            print("timeDifference:", timeDifference)
            if ( timeDifference > self.wateringFreq ):
                self.water = True
            else:
                self.water = False

        #----Check hour and light control-------
        hour = datetime.datetime.now().hour #returns hour in 24hr format int
        if (hour >= self.lightStartTime and hour < self.lightEndTime):
            if not self.lightOn:
                self.turnOnLight()
        elif (self.lightStartTime > self.lightEndTime and (hour >= self.lightStartTime or hour < self.lightEndTime)):
            if not self.lightOn:
                self.turnOnLight()
            self.lightOn = True
        else:
            if (self.lightOn):
                self.turnOffLight()
            self.lightOn = False

        #----Activate actuators------
        if (self.water):
            print("WATERING")
            self.dispenseWater()
            self.updateLastWateredTable()

    def readUserControlFactors(self):
        """
        This will read the user control growth factors and return the values
        specified in the table "CONTROLFACTORS".

        The table ("CONTROLFACTORS") contains the following columns:
        - "TIMESTAMP" TEXT NOT NULL,
        - "LIGHTSTARTTIME"    REAL,
        - "LIGHTENDTIME"  REAL,
        - "HUMIDITY"   REAL,
        - "TEMPERATURE"   REAL,
        - "WATERINGFREQ"  REAL,
        - "WATERINGDURATION" REAL,
        - "NUTRIENTRATIO" REAL,
        - "BASELEVEL" REAL

        TODO: toggle option to pythonanywhere
        """
        row = (None,self.lightStartTime,self.lightEndTime,self.humidityMax,self.tempMax,self.wateringFreq,self.wateringDuration,self.nutrientRatio,self.baseLevelMin)
        try:
            r = requests.get(BASEURL+"/usercontrolgrowth")
            s = r.json()["readings"][0]
            r.close()
            lightstart = s["lightStartTime"]
            lightend = s["lightEndTime"]
            humidity = s["humidity"]
            temp = s["temperature"]
            waterfreq = s["waterFreq"]
            waterdur = s["waterDuration"]
            nutrientratio = s["nutrientRatio"]
            baselevel = s["baseLevel"]
            row = (None,lightstart,lightend,humidity,temp,waterfreq,waterdur,nutrientratio,baselevel)
        except Exception as e:
            print(e)

        return row

    def readUserActControls(self):
        """
        This function is for the user demo feature.
        Immediate Control Values will include:
        - fan+vents for (for 10 seconds)
        - just vents (for 10 seconds)
        - lights (for 10 seconds)
        - water (for 10 seconds)
        - baselevelnotify (notify)

        The table must also include only one row.

        TODO: toggle option to pythonanywhere
        """
        row=(0,0,0,0,0)
        try:
            r = requests.get(BASEURL+"/userdemo")
            s = r.json()["readings"][0]
            r.close()
            fanvents = s["fanvents"]
            vents = s["vents"]
            lights = s["lights"]
            water = s["water"]
            baselevelnotify = s["baselevelnotify"]
            row = (fanvents,vents,lights,water,baselevelnotify)
        except Exception as e:
            print(e)

        return row

    def runFan(self):
        """
        Run fan by setting fan GPIO pin to true
        """
        GPIO.output(self.FAN_PIN, True)

    def stopFan(self):
        """
        Stop fan by setting fan GPIO pin to false
        """
        GPIO.output(self.FAN_PIN, False)

    def ventMove(self,cycle):
        """
        cylcle<int>: the duty cycle to specify the servo motor's position. 0 degrees = 3% duty cycle and 180 degrees = 12% duty cycle
        """
        p=GPIO.PWM(self.SERVO_PIN,50)
        p.start(2.5)
        p.ChangeDutyCycle(cycle)
        time.sleep(1)
        p.stop
        
    def openVent(self):
        """
        Set servo to 180 degree to open vent
        Duty cycle for 180 degree = 12%
        """
        self.ventMove(12)

    def closeVent(self):
        """
        Set servo to 0 degree to close vent
        Duty cycle for 0 degree = 3%
        """
        self.ventMove(3)

    def dispenseWater(self):
        #spit out water
        GPIO.output(self.PUMP, True)
        time.sleep(self.wateringDuration)
        GPIO.output(self.PUMP, False)

    def turnOnLight(self):
        GPIO.output(self.LIGHT, True)

    def turnOffLight(self):
        GPIO.output(self.LIGHT, False)

    @contextmanager
    def time_limit(self,seconds):
        """
        This is for the timed signal to limit the amount of time it takes for
        a function to run.
        """
        def signal_handler(signum, frame):
            raise TimeoutException("Timed out!")
        signal.signal(signal.SIGALRM, self._handler)
        signal.alarm(seconds)
        try:
            yield
        finally:
            signal.alarm(0)

    def _handler(self,sig,frame):
        """
        This is for the timed signal to limit the amount of time it takes for
        a function to run.
        """
        raise Timeout

if __name__ == "__main__":
    try:
        zot = ZotPonics()
        zot.run(simulateAll=False)
    except Exception as e:
        GPIO.cleanup()
        raise e
