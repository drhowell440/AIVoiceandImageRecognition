from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

def lookupfull():
 kit.servo[12].angle =90  #Bottom Eye Lid
 kit.servo[13].angle =80 #Top Eye Lid
 kit.servo[15].angle =90 #Up and Down Eye Ball
 sleep(.5)

def lookuphalf():
 #kit.servo[12].angle = 0 #Bottom Eye Lid
 kit.servo[13].angle =110 #Top Eye Lid
 sleep(.5)
 
def lookdownfull():
 kit.servo[12].angle =90  #Bottom Eye Lid
 kit.servo[13].angle =150 #Top Eye Lid
 kit.servo[15].angle = 90 #Up and Down Eye Ball
 sleep(.5)

def lookdownhalf():
 #kit.servo[12].angle = 0 #Bottom Eye Lid
 sleep(.5) 

def lookstraight():
 #kit.servo[12].angle = 0 #Bottom Eye Lid
 sleep(.5) 

def closeeyes():
 #kit.servo[12].angle = 90 #Bottom Eye Lid
 kit.servo[13].angle = 180 #Top Eye Lid   
 sleep(.5)
 
def openeyes():
 kit.servo[13].angle = 120 #Top Eye Lid
 sleep(.5)
 
def lookleftfull():
  kit.servo[14].angle = 115 #Left to Right Eye Ball
  
def lookrightfull():
  kit.servo[14].angle = 60 #Left to Right Eye Ball
  
def centereyeball  ():
  kit.servo[14].angle = 89 #Left to Right Eye Ball
  

openeyes()
sleep(1)
lookuphalf()
sleep(1)
lookupfull()
sleep(1)
#lookdownhalf()
#sleep(1)
#lookdownfull()
#sleep(1) 
#lookstraight()
#sleep(1)
closeeyes()
#sleep(3)
  
#openeyes()
#sleep(1)
#looklefthalf()
#sleep(1)
#lookleftfull()
#sleep(1)
#lookrighthalf()
#sleep(1)
#lookrightfull()
#sleep(1)
#centereyeball()
#sleep(1)
#closeeyes()

