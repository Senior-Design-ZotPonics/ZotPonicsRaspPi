import RPi.GPIO as GPIO
import time
light = 5 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(light,GPIO.OUT)
# Turn on GPIO pin to turn on lights
# Turn off to off lights

try:
    while True:
        GPIO.output(light, True)
        time.sleep(.5)
        #GPIO.output(light, False)
        #time.sleep(.5)

except KeyboardInterrupt:
    GPIO.cleanup()
