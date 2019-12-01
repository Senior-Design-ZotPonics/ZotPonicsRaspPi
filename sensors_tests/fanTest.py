#Resources:
#- https://www.electronicshub.org/raspberry-pi-servo-motor-interface-tutorial/
#- https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/

import RPi.GPIO as GPIO
import time

fan = 26 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(fan,GPIO.OUT)
# Turn on GPIO pin to run fan
# Turn off to stop fan

try:
    while True:
        GPIO.output(fan, True)
        Time.sleep(2)
        GPIO.output(fan, False)
        Time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
