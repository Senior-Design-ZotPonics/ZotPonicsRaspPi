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
        Time.sleep(2)
        GPIO.output(light, False)
        Time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
