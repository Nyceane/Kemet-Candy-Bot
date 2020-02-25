import time
import os
import grovepi
from grovepi import *

#Sensor connected to A0 Port 
sensor = 14		# Pin 14 is A0 Port.
led = 4

grovepi.pinMode(sensor,"INPUT")
pinMode(led,"OUTPUT")

count = 0
last_value = 0

while True:
    try:
        sensor_value = grovepi.analogRead(sensor)
        print ("sensor_value = %d" %sensor_value)

        if sensor_value > 200:
        	count += 1

        if sensor_value <= 200 and last_value > 200:
        	count = 0 #reset the count

        if count > 2:
            count = 0
            digitalWrite(led,1)		# Send HIGH to switch on LED
            print('called robotic arm')
            os.system('python3 Script.py --Json candybot.json')
            digitalWrite(led,0)		# Send LOW to switch off LED
        
        last_value = sensor_value
        
        time.sleep(.5)

    except IOError:
        print ("Error")