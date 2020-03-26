#!/bin/bash

sudo apt-get install xterm -y

echo Setting up running the program on startup.
mkdir /home/pi/.config/autostart
cp zotponics.desktop /home/pi/.config/autostart/zotponics.desktop


