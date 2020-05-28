import pyrebase
import RPi.GPIO as GPIO
import time
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


in1 = 17
en1 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(en1,GPIO.OUT)

GPIO.setup(in1,GPIO.OUT)

p1=GPIO.PWM(en1,1000)
p1.start(50)
#motor
def motor():
    control1 = db.child("Motor/run").get()
    level1 = db.child("Motor/level").get()
    
    if (control1.val()==0):
        GPIO.output(in1, 0)
        
    elif (level1.val()==1):
        p1.ChangeDutyCycle(50)
        GPIO.output(in1, 1)
        
    elif (level1.val()==2):
        p1.ChangeDutyCycle(75)
        GPIO.output(in1, 1)
        
    elif (level1.val()==3):
        p1.ChangeDutyCycle(100)
        GPIO.output(in1, 1)
    