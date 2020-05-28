import pygame
import pyrebase
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

pygame.mixer.init()
s=pygame.mixer.music

def play():
    voice = db.child("Voices/voice").get()
    if (voice.val()==1):
        s.load("/home/pi/m7med/importt/files/1.mp3")
        s.play()
        db.child("Voices/voice").set(5)
        if (voice.val()==5):
            pygame.mixer.music.get_busy()
    elif (voice.val()==2):
        s.load("/home/pi/m7med/importt/files/2.mp3")
        s.play()
        db.child("Voices/voice").set(5)
        if (voice.val()==5):
            pygame.mixer.music.get_busy()
    elif (voice.val()==0):
        pygame.mixer.music.stop()
    
            
    #elif (play.val()==0):
        #pygame.mixer.music.stop()

#while pygame.mixer.music.get_busy() == True:
   # continue

#while True:
#    play = db.child("play").get()
#   if (play.val()==1):
#        pygame.mixer.music.load("1.mp3")
 #       pygame.mixer.music.play()
  #      #time.sleep(20)
   #     if (play.val()==1):
    #        pygame.mixer.music.get_busy()
     #       time.sleep(20)
  #  elif (play.val()==0):
   #     pygame.mixer.music.stop()
   
   

#while True:
#    play = db.child("play").get()
 #   if (play.val()==1):
  #      s.load("1.mp3")
   #     s.play()
    #    while True:
     #       s.get_busy()
      #      time.sleep(20)
       #     break
    #elif (play.val()==0):
     #   pygame.mixer.music.stop()

