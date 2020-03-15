# ZotPonicsRaspPi Quick Start for Local Version
This is the code for the raspberry pi systems designs of the Smart Hydroponics System, ZotPonics.
## Authors
Sidney Lau: B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine

[Owen Yang](https://www.linkedin.com/in/owen-yang-200989138/): B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine
*********************
# Sections
1. [Set-Up](#set-up)
2. [Running ZotPonics Raspberry Pi Code](#running-zotponics-raspberry-pi-code)
3. [Testing](#testing)
4. [Documentation on Important Functions](#documentation-on-important-functions)
5. [Wiki](#wiki)



# Set-Up
This code was developed with Python 3.7.2
This code is for the local version of ZotPonics. That means that the database is hosted locally with SQLITE. All the code this guide is referring to is in the `local_version` folder.

Make sure that you have the following Python libraries installed:
1. sqlite3
2. Adafruit_DHT
3. Flask

Make sure you also set up the `zotponics.db` database (see below for more details)

**Set up Flask**

To get the Flask library run this in the terminal:
```
pip install flask
```

**Set up Adafruit_DHT11 (Temperature and Humidity Sensor)**

To get the Adafruit_DHT library run this in the terminal:
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
```

**Setting up PythonAnywhere**

Python Anywhere is an online service where users can host their Python websites. We used Python Anywhere to host our API's.

Please see the ZotPonics API Documentation for Set-up [here](https://github.com/Senior-Design-ZotPonics/ZotPonicsRaspPi/wiki/ZotPonics-API-Documentation)

**Deprecated Section**

To set up the database locally, we use the files in the `local_version` folder. It uses sqlite3, a local database. You can run `userSimulate.py` to quickly set up the zotponics database with random values generated for the database [tables](wiki_content/database_relation.png): USERDEMO, and CONTROLFACTORS. The other tables, SENSOR_DATA and LAST_WATERED will be populated once you run `ZotPonics_raspi_sqlite_version.py`


# Running ZotPonics Raspberry Pi Code
To run it on the Raspberry Pi just run the following command:
```
python3 ZotPonics_raspi_sqlite_version.py
```
# Testing
For you can use the `userSimulate.py` file.

There are two main functions you can use `randomUserInputFactor` and `UserActivateControl` to test pushing daata to the datbase.

# Documentation on Important Functions
### ZotPonics.run
#### ZotPonics.run(*self,simulateAll=False,temperSim=False,humidSim=False,baseLevelSim=False,ecSim=False*)
This function helps run the main control block logic for your ZotPonics hydroponics system.

> ### Parameters
>
> **simulateAll[bool]**: If True, It turns all the other boolean parameters to True.
>
> **temperSim[bool]**: If True, just return 0.0 for the the temperature data.
>
> **humidSim[bool]**: If True, just return 0.0 for the the humidity data.
>
> **baseLevelSim[bool]**: If True, just return 0.0 for the the base level data.

> ### Returns
> *None*

## userSimulate.randomUserInputFactor
#### randomUserInputFactors(n=10,sleepTime=5)
This function is located in the `userSimulate.py` file. You can run the function by calling the function in the `if __name__ == "__main__"`

> ### Parameters
>
> **n[int]**: default is 10 for convenience. This is the number of times that random user input factors will be pushed to the database.
>
> **sleepTime[int]**: default is 5 seconds for convenience. This will determine the rate at which the user input factor is updated to the database.

> ### Returns
> *None*

## userSimulate.UserActivateControl
#### UserActivateControl(fans=0,vents=1,lights=0,water=1,notify=1)
This function is located in the `userSimulate.py` file. You can run the function by calling the function in the `if __name__ == "__main__"` block. This function allows you to simulate activate the actuators. The actuators includes the fans, the vent flaps, the lights, the water pump, and a notification system.

> ### Parameters
>
> **fans[int]**: default is 0 for convenience. Toggle between 0 or 1. 1 activates the fans, 0 keeps it off.
>
> **vents[int]**: default is 1 for convenience. Toggle between 0 or 1. 1 opens the vents, 0 keeps it off.
>
> **lights[int]**: default is 0 for convenience. Toggle between 0 or 1. 1 turns on the lights, 0 keeps it off.
>
> **water[int]**: default is 1 for convenience. Toggle between 0 or 1. 1 turns on the water pump, 0 keeps it off.
>
> **notify[int]**: default is 1 for convinience. Toggle between 0 or 1. 1 notifies the users, 0 doesn't send any notifications

> ### Returns
> *None*

# Wiki
Read our wiki for more information: [ZotPonics Wiki](https://github.com/Senior-Design-ZotPonics/ZotPonicsRaspPi/wiki)
