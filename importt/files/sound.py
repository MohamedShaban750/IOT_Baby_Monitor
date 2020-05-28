import RPi.GPIO as GPIO
import time
import pyrebase
from time import sleep

config = {
  "apiKey": "AIzaSyDhinRkAu5k-3aL83EIe_thcTwhmu1fVvU",
  "authDomain": "baby-156b1.firebaseapp.com",
  "databaseURL": "https://baby-156b1.firebaseio.com",
  "storageBucket": "baby-156b1.appspot.com",
   "serviceAccount": "/home/pi/m7med/importt/files/firebase.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#GPIO SETUP
channel = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def callback(channel):
    if GPIO.input(channel):
        print "Sound Detected!"
        db.child("Sound Detection/detected").set("yes")
        
    else:
        print "Sound Detected!"
        db.child("Sound Detection/detected").set("yes")
        
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

# infinite loop
def sound():
    sound = db.child("Sound Detection/detected").get()    
    if (sound.val()=="yes"):   
        time.sleep(5)
        db.child("Sound Detection/detected").set("no")
            
