#!/bin/bash

sudo apt-get install xterm -y

echo Setting up running the program on startup.
mkdir /home/pi/.config/autostart
cp zotponics.desktop /home/pi/.config/autostart/zotponics.desktop
echo Finished setting up running the program on startup completed.
echo

echo Setup dependencies for Adafruit_DHT11...
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl git
cd
git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
sudo python setup.py install
echo Finished setting up dependencies for Adafruit_DHT11...
