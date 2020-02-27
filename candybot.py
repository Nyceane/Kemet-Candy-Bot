import time
import os
import grovepi
from grovepi import *
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("/path/to/your_account-service_key")

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your_candy_bot.firebaseio.com/'
})

ref = db.reference('/candy')

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
            ref.set({'count': 1, 'time': datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")})
        last_value = sensor_value
        
        time.sleep(.5)

    except IOError:
        print ("Error")
