import sys
import Adafruit_DHT
import time
import pyrebase
import RPi.GPIO as GPIO
from time import sleep


config = {
  "apiKey": "AIzaSyDhinRkAu5k-3aL83EIe_thcTwhmu1fVvU",
  "authDomain": "baby-156b1.firebaseapp.com",
  "databaseURL": "https://baby-156b1.firebaseio.com",
  "storageBucket": "baby-156b1.appspot.com",
   "serviceAccount": "firebase.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
#data = {"tem": "",
 #       "hum": ""}
#db.child("status").set(data)

while True:

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} '.format(temperature, humidity)
    time.sleep(1)
    
    data = {"Humidity": ' %.1f ' % humidity,
            "Temperature": ' %.1f ' % temperature}
    db.child("Status").set(data)

    
  