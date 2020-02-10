#Resources:
#- https://www.electronicshub.org/raspberry-pi-servo-motor-interface-tutorial/
#- https://www.learnrobotics.org/blog/raspberry-pi-servo-motor/

import RPi.GPIO as GPIO
import time

control = [3,12]

servo = 25 #GPIO pin

GPIO.setmode(GPIO.BCM)

GPIO.setup(servo,GPIO.OUT)
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%

#<oky>: however, servo motors are not perfect
# after testing:
# duty cycle for 0 degree = 3%
# duty cycle for 180 degree = 12%


p=GPIO.PWM(servo,50)# 50hz frequency

p.start(2.5)# starting duty cycle ( it set the servo to 0 degree )


try:
       while True:
           usern = input("Enter a number")
           #for x in range(2):
           if usern == 1: #open logic
                  print("open!")
                  p.ChangeDutyCycle(12)
           elif usern == 2: #close logic
                  print("close!")
                  p.ChangeDutyCycle(3)
           else:
                  pass
           #p.ChangeDutyCycle(control[x])
           #print(control[x])
           #time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
