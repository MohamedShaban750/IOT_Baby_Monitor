import pyrebase
import RPi.GPIO as GPIO
from time import sleep

config = {
  "apiKey": "AIzaSyDhinRkAu5k-3aL83EIe_thcTwhmu1fVvU",
  "authDomain": "baby-156b1.firebaseapp.com",
  "databaseURL": "https://baby-156b1.firebaseio.com",
  "storageBucket": "baby-156b1.appspot.com",
   "serviceAccount": {
  "type": "service_account",
  "project_id": "baby-156b1",
  "private_key_id": "258dd9523bed9dbe6ffe459214dc655ccd0f7d18",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC8SL4qtmkG1C7i\ntAfp9krNgLNNtVJ2sGTJnh1eXjIgiZYXjzRu/UYdsNu2QBjhBpycx88+FjR7sR+h\nj/68BqXGWGf7fIYsj06CEUfjWMZS7kB5hWSSvimAidRzLfF1FzZRYrhqs5ICcL11\n1iKgZF4HMwCjB5hBn6VO3OZUhkRx+ELXYkedHnKBkUnrct6gl2+0jEYwEac5OhGS\nNQgG40fg6KO7Mk407gzO1D2h8Od0dnJebaSWSlpFGG0u5QROEl4qeiCIX7kDILT1\nEPSlqFHhqrQ30WsHVeNmr4YSR5mQZ9Da3sm/x7lhKPXhnyIC4IsxqabQPxF9ygDU\ncz6sgjVZAgMBAAECggEARFNngyt/0IUWYJlxV8NTYODn8Haw7rZTVOEGilTHfww+\nxdzna7GIjMS97pSzEpHqKnDN8ZtwP0THFEOjbstAxEoXrekB7dCxbjzkKAnyqmyg\nRBkWprPQbr9Vs9iDy3h5cy5OexYgEbek4UqsdSUHBDjLbd4XMBVFkWlTQnAZDXwo\nisY4XKMaMrbVMDoYF9EWu9SdjwooNog2fNckeyvKU/RpHI4e541DG0piQTdgAdIY\nig9gkvO3l6og5YOGfusZpL8FoZR6/wBzZPJotg+L6omB3XTVtWq/msphBAfDBPoT\nInWkoL5eTa+lmqWmbPox5zhX/Gstvv0doVykjRfqkwKBgQDw1An7KHQ8xeMFJzQv\n8qInRDQRni4L2POH9WjdFlUSKh0VLZ2KSf5OpDDbbbKtkxG2gzLTZPG9rusBxwhb\nVJoxTSekGlWXve/EoINDdQKAZbNNelwdTWX73DYqrRJesknWnegaxR4h0VeSaudI\n8/nFUoyMG4RzkxdoCx9IYTd1BwKBgQDIJUw9w5wrdIzqr4KKul4IzpphK3RYY2ii\nC/PsAjjYHdVClF7vEzLA9vWVhXquUJu4DK50qPXa2R+C825/u2QjEh0QhzoE5sB7\nEkZiBQBd/RmkswUpBIMYGQ6a33cFMzfOFpzzud4Hh9TXOW9Kd/g9OeFa9cwBMuDr\nWoYIZD/KnwKBgAVdc+t4dz5zWh9fRDZdPWeKiW5rC7OP3b0FppRmTvbcoVE7dusB\nwvyVg9EfnH9pa1eZjKRQ92G2Z93eRT1joRvAEEYDoCyFOrYyrTnvfWLG4Tu0oiC0\n/LSjr0E8IdCiQCrb0bPm+EjglQbaAtUJOmM+94qXglfgywCyXrwKDmY5AoGAC0KF\n6oehtpQlBWMAXhukBKzS5JqUPhDBpzQy8dkiJ45uHAPK33peBZsfL91FjJ7+U7lq\n6ydCRaCndC+LzOXW+V4ggniJHBN7SrE5gnQzlBYUJj7oEGmvkmB+gNoHkSRThGWj\nSNbxFc1ffQg/KZpcPd2OvxZK9tpM6xC5r6ksKZMCgYEAsfZIfUN5bQSUdXHxBDpX\nchJF9AM2toawv6WXDJYIguYh4eWWt8xcRTB/kjDYhvbmwpFriAPLSkcOa8xVwAxs\notvqebrGBnVZJCzJGPyKbMBcMHOXO4OdQmDirqVnkfsYfn2D+6PH3s//MpK/X7LO\nip7DIVoeY54W+p9SXVZNugA=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-4hrde@baby-156b1.iam.gserviceaccount.com",
  "client_id": "102608346635458570366",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-4hrde%40baby-156b1.iam.gserviceaccount.com"
}
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


while True:
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
            
GPIO.cleanup() 




