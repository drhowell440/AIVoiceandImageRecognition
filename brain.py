import speech_recognition as sr
import subprocess
import random
import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

def blinkeyes():
    kit.servo[15].angle = 40
    kit.servo[12].angle = 120

    kit.servo[13].angle = 140
    kit.servo[14].angle = 120

    time.sleep(.35)

    kit.servo[15].angle = 40
    kit.servo[12].angle = 90

    kit.servo[13].angle = 0
    kit.servo[14].angle = 90

    time.sleep(.25)

    kit.servo[15].angle = 40
    kit.servo[12].angle = 120

    kit.servo[13].angle = 160
    kit.servo[14].angle = 120

    time.sleep(1)
    
def lookright():
    kit.servo[15].angle = 120
    
def lookleft():
    kit.servo[15].angle = 0
    
def closeeyes():
    kit.servo[15].angle = 40
    kit.servo[12].angle = 90

    kit.servo[13].angle = 0
    kit.servo[14].angle = 90
    
def openeyes():    
    kit.servo[15].angle = 40
    kit.servo[12].angle = 120

    kit.servo[13].angle = 160
    kit.servo[14].angle = 120

def eyesup():    
    kit.servo[15].angle = 40
    kit.servo[12].angle = 160

    kit.servo[13].angle = 160
    kit.servo[14].angle = 120

def eyesdown():    
    kit.servo[15].angle = 40
    kit.servo[12].angle = 60

    kit.servo[13].angle = 160
    kit.servo[14].angle = 120

def speak_with_flite(text, voice="kal16"):
    subprocess.run(["flite", "-voice", voice, "-t", text])

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
        speak_with_flite("Stop mumbling")
    return response
    

if __name__ == "__main__":
 
    NUM = 100
    greeting = [
    "hello", "hey", "hi",  "yo", "what's good", "what's poppin",
    "howdy", "how's it going", "hi there", "good day", "hiya", "g'day", "hi folks",
    "hi friend", "hi everyone", "hi folks", "how's everything", "hi mate", "greetings",
    "hi ya'll", "hi darling", "hi beautiful", "hi handsome", "hi sweetie", "hi love",
    "hi honey", "hi dear", "hi buddy", "hi pal"]

    howareyou = [
    "what's up", "how are you","are you okay","how are things",
    "how is life","how are you doing"]
    
    whatisyourname = [
    "what is your name","what's up dog", "what's your name",
    "what do you call yourself","what do they call you"]
    
    good = [
    "good","i am good", "i'm good", "great", "i am great", "i'm great",
    "pretty good", "I am pretty good", "I'm pretty good", ]
    
    bad = [
    "bad","i am bad", "i'm bad", "not good", "i am not good",
    "i'm not good", "not great", "i am not great" , "i'm not great",
    "not so good", "not so great"]
    
    choad = [
    "choad", "hey choad", "choader","chode", "hey chode",
    "hey chowder", "hegehod", "hey chad", "play chode",
    "hey chodie", "hey jody", "hey jode", "whoa chode",
    "whoa choad", "woah chode", "woah choad", "wow chode",
    "wow choad", "wobe toad", "hi chode", "hydro"]
    
    #list of verbal commands for movement
    blink = [
    "blink your eyes", "blink", "blank", "blink eyes", "blank eyes"]
    
    looktotheright = "look right"
    looktotheleft = "look left"
    closeyoureyes= "close your eyes"
    openyoureyes= "open your eyes"
    lookupeyes= "look up"
    lookdowneyes= "look down"
    
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
        
#blinkeyes()
speak_with_flite("Whoa Choad, im back")
for i in range(NUM):
        spoken = recognize_speech_from_mic(recognizer, microphone)

        if spoken["transcription"]:
           # show the user the transcription
           print("You said: {}".format(spoken["transcription"]))
       
           prompt = spoken["transcription"].lower()
       
           if prompt in greeting:
              speak_with_flite("Whats up dog")
              time.sleep(1)
           elif prompt in howareyou:
              speak_with_flite("Everything is dope. How are you?")
              spoken = recognize_speech_from_mic(recognizer, microphone)
              if spoken["transcription"]:
                 # show the user the transcription
                 print("You said: {}".format(spoken["transcription"]))
       
                 prompt = spoken["transcription"].lower()
       
                 if prompt in good:
                    speak_with_flite("That's great!")
                    
                 elif prompt in bad:
                     speak_with_flite("Oh no.")
                     speak_with_flite("Don't worry")
                     speak_with_flite("it'll be okay")  
              time.sleep(1)
           elif prompt in whatisyourname:
              speak_with_flite("They call me Choadie.")
              speak_with_flite("Choadie Mac choaderson")
              time.sleep(1)
           elif prompt in choad:
              speak_with_flite("Choad for life")
              speak_with_flite("for life")
              speak_with_flite("for life")
              speak_with_flite("for life")
              time.sleep(1)       
           elif prompt in blink:
              blinkeyes()
              time.sleep(1)
           elif prompt == looktotheright:
              lookright()
              time.sleep(1)   
           elif prompt == looktotheleft:
              lookleft()
              time.sleep(1)
           elif prompt == closeyoureyes:
              closeeyes()
              time.sleep(1)
           elif prompt == openyoureyes:
              openeyes()
              time.sleep(1)
           elif prompt == lookupeyes:
              eyesup()
              time.sleep(1)
           elif prompt == lookdowneyes:
              eyesdown()
              time.sleep(1)
              
            
              
       
   
      


       

        