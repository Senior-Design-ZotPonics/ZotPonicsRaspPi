# ZotPonicsRaspPi Quick Start
This is the code for the Raspberry Pi Systems Design portion of the Smart Hydroponics System, ZotPonics.

## Authors
[Sidney Lau](https://www.linkedin.com/in/sidney-lau/): B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine

[Owen Yang](https://www.linkedin.com/in/owen-yang-200989138/): B.S. Computer Science and Engineering Major, Class of 2020, University of California, Irvine
*********************
# Table of Contents
1. [Set-Up](#set-up)
2. [Running ZotPonics Raspberry Pi Code](#running-zotponics-raspberry-pi-code)
3. [Testing](#testing)
4. [Documentation on Important Functions](#documentation-on-important-functions)
5. [Wiki](#wiki)

# Set-Up
This code was developed with Python 3.7.2

The code for the non-local version is included in this root folder. It uses PythonAnywhere to store our database and manage our APIs.

**0. Run the Bash Script for Setup**
There is a bash script that you can run to automatically set-up this repository. If you run it successfully, you can skip steps 1 and 2. To run the bash script open the terminal on the Raspberry Pi and run:
```
./setup.sh
```

**1. Set up Adafruit_DHT11 (Temperature and Humidity Sensor)**

To get the Adafruit_DHT library run this in the terminal:
```
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
```

**2. Running the ZotPonics Code on Startup on the Raspberry Pi**

To make the ZotPonics Code run when the Raspberry Pi is turned run this in the terminal:
```
mkdir /home/pi/.config/autostart
cp zotponics.desktop /home/pi/.config/autostart/zotponics.desktop
```

The `zotponics.desktop` file is the main file used to make sure the program runs on startup.

**3. Setting up PythonAnywhere**

Python Anywhere is an online service where users can host their Python websites. We used Python Anywhere to host our API's.

Please see the ZotPonics API Documentation for Set-up [here](https://github.com/Senior-Design-ZotPonics/ZotPonicsRaspPi/wiki/ZotPonics-API-Documentation#pythonanywhere-setup)

After setting up your Python Anywhere website. Make sure you change the `BASE_URL` global value in the `ZotPonics_raspi.py` file to your URL.

# Running ZotPonics Raspberry Pi Code
If you set up running your code on start up, you can just reboot the Raspberry Pi and it should run on start up. You can use `htop` on the terminal to see if your code is running on startup.  

If you didn't set up running the code on start up run the following command in the terminal:
```
python3 ZotPonics_raspi.py
```

# Testing the API's
For testing you can run the `pythonanywhereTest.py` script in the terminal:
```
python3 pythonanywhereTest.py
```
This script will run the `pythonanywhereTest.testAll` function to test the following API's:
- add-sensor-data
- add-lastwatered-data
- usercontrolgrowth
- userdemo

*We have more documentation on other testing here: [ZotPonics-Testing-Verification](https://github.com/Senior-Design-ZotPonics/Documentation/wiki/ZotPonics-Testing-Verification)*

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
>
> ### Returns
>
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
>
> ### Returns
>
> *None*

# Wiki
Read our wiki for more information: [ZotPonics Wiki](https://github.com/Senior-Design-ZotPonics/ZotPonicsRaspPi/wiki)
