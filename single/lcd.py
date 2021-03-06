#import
import RPi.GPIO as GPIO
import time
import smbus
import sys
import Adafruit_DHT
import pyrebase
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

# Define GPIO to LCD mapping
LCD_RS = 23
LCD_E  = 24
LCD_D4 = 5
LCD_D5 = 6
LCD_D6 = 13
LCD_D7 = 19
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():
  # Main program block
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
 
  # Initialise display
  lcd_init()
 
  while True:
     
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    
    # Send some test
    lcd_string("IOT Baby",LCD_LINE_1)
    lcd_string("Monitor",LCD_LINE_2)
    time.sleep(2)
 
 
    # Send some more text
    lcd_string(  'Temp= %.1f C' % temperature  ,LCD_LINE_1)
    lcd_string( 'Hum = %.1f %%' % humidity ,LCD_LINE_2)
    #time.sleep(5)

    data = {"Humidity": ' %.1f ' % humidity,
            "Temperature": ' %.1f ' % temperature}
    db.child("Status").set(data)
    
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  time.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
 
  GPIO.output(LCD_RS, mode) # RS
 
  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  message = message.ljust(LCD_WIDTH," ")
 
  lcd_byte(line, LCD_CMD)
 
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)
    GPIO.cleanup()