import RPi.GPIO as GPIO
import time
pump = 6 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(pump,GPIO.OUT)
# Turn on GPIO pin to turn on lights
# Turn off to off lights

try:
    GPIO.output(pump, True)

except KeyboardInterrupt:
    GPIO.cleanup()
