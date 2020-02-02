import RPi.GPIO as GPIO
import time
pump = 6 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(pump,GPIO.OUT)
# Turn on GPIO pin to turn on lights
# Turn off to off lights

try:
    while True:
        GPIO.output(pump, True)
        time.sleep(2)
        GPIO.output(pump, False)
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
