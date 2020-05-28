import os
import sys
sys.path.append('/home/pi/m7med/importt/files')
import motor
import fan
import play
import sound
#sys.path.insert(1, '/home/pi/m7med/importt/motor')
#sys.path.insert(2, '/home/pi/m7med/importt/fan')
#sys.path.append('/home/pi/m7med/importt/motor')
#sys.path.append('/home/pi/m7med/importt/fan')
#import motor1
#import fan1
import lcd
#import dht11

while True:
    motor.motor()
    fan.fan()
    sound.sound()
    play.play()
    #motor1.motor()
    #fan1.fan()
    
    #dht11.dht11()
    lcd.main()
     
GPIO.cleanup()
