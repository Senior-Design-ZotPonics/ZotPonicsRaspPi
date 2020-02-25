import RPi.GPIO as GPIO
import time

fan = 6 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(fan,GPIO.OUT)
# Turn on GPIO pin to run fan
# Turn off to stop fan

try:
    while True:
        GPIO.output(fan, True)
        time.sleep(2)
<<<<<<< HEAD
        #GPIO.output(fan, False)
        #time.sleep(2)
=======
>>>>>>> 28f7ad4b9267860af0daa55aee397a8e28f94b4f

except KeyboardInterrupt:
    GPIO.cleanup()
