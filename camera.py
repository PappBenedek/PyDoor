# import packages
from picamera import PiCamera
import time
import qrcode
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #Set the GPIO numbering
GPIO.setup(14,GPIO.OUT) #Set the output pin wich will trigger the relay

cam = PiCamera() # Init camre
decoder = qrcode.Decoder() # Init decoder
try:
    while True:
        cam.capture('/home/pi/Desktop/im.jpg') # Take a picture
        if decoder.decode('/home/pi/Desktop/im.jpg'): # If it can be decoded as a qr-code
            with open('/home/pi/Desktop/pydoor/secret.key','r') as f: # open the current secret key
                if decoder.result == f.readline(): # If the decoded str == the secret key
                    GPIO.output(14,GPIO.HIGH)
                    time.sleep(5)               # Trigger a relay wich opens the eletric door for 5 sec
                    GPIO.output(14,GPIO.LOW)
        time.sleep(2)
# Cleanup the GPIO pins
finally:
    GPIO.cleanup()