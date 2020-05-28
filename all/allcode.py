#import
import RPi.GPIO as GPIO
import time
import smbus
import sys
import Adafruit_DHT
import pyrebase
from time import sleep
import pygame

#firebase connection
config = {
  "apiKey": "AIzaSyDhinRkAu5k-3aL83EIe_thcTwhmu1fVvU",
  "authDomain": "baby-156b1.firebaseapp.com",
  "databaseURL": "https://baby-156b1.firebaseio.com",
  "storageBucket": "baby-156b1.appspot.com",
   "serviceAccount": "/home/pi/m7med/m/firebase.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

#motor
in1 = 17
en1 = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(en1,GPIO.OUT)

GPIO.setup(in1,GPIO.OUT)

p1=GPIO.PWM(en1,1000)
p1.start(50)

#fan
in2 = 20
en2 = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(en2,GPIO.OUT)

GPIO.setup(in2,GPIO.OUT)

p2=GPIO.PWM(en2,1000)
p2.start(50)

#voices
pygame.mixer.init()
s=pygame.mixer.music

#sound
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
        

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=30) 
GPIO.add_event_callback(channel, callback) 

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
        
        #motor
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
            
        #fan
        control2 = db.child("Fan/run").get()
        level2 = db.child("Fan/level").get()
        
        if (control2.val()==0):
            GPIO.output(in2, 0)
            
        elif (level2.val()==1):
            p2.ChangeDutyCycle(50)
            GPIO.output(in2, 1)
            
        elif (level2.val()==2):
            p2.ChangeDutyCycle(75)
            GPIO.output(in2, 1)
            
        elif (level2.val()==3):
            p2.ChangeDutyCycle(100)
            GPIO.output(in2, 1)

        #sound
        sound = db.child("Sound Detection/detected").get()    
        if (sound.val()=="yes"):   
            time.sleep(5)
            db.child("Sound Detection/detected").set("no")
            
        #voices
        voice = db.child("Voices/voice").get()
        if (voice.val()==1):
            s.load("1.mp3")
            s.play()
            db.child("Voices/voice").set(5)
            if (voice.val()==5):
                pygame.mixer.music.get_busy()
        elif (voice.val()==2):
            s.load("2.mp3")
            s.play()
            db.child("Voices/voice").set(5)
            if (voice.val()==5):
                pygame.mixer.music.get_busy()
        elif (voice.val()==0):
            pygame.mixer.music.stop()                    
                
    GPIO.cleanup()
    
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