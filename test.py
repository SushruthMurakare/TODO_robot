"""import naoqi
from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "10.60.88.243", 9559)
tts.say("This is a test")
""""""
import speech_recognition as sr

r=sr.Recognizer()
print(sr.Microphone.list_microphone_names())
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source,duration=1)
    # r.energy_threshold()
    print("say anything : ")
    audio= r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(text)
    except:
        print("sorry, could not recognise")
"""
#ctrl?
# from naoqi import *
# import time
# check = 0


# # create python module
# class myModule(ALModule):
#   """python class myModule test auto documentation: comment needed to create a new python module"""


#   def pythondatachanged(self, strVarName, value):
#     """callback when data change"""
#     print("data changed")
#     global check
#     check = 1

#   def _pythonPrivateMethod(self, param1, param2, param3):
#     global check


# broker = ALBroker("pythonBroker","10.0.252.184",9999,"naoverdose.local",9559)


# # call method
# try:

#   pythonModule = myModule("pythonModule")
#   prox = ALProxy("ALMemory")
#   #prox.insertData("val",1) # forbidden, data is optimized and doesn't manage callback
#   prox.subscribeToEvent("FaceDetected","pythonModule", "pythondatachanged") #  event is case sensitive !

# except Exception,e:
#   print "error"
#   print e
#   exit(1)

# while (1):
#   time.sleep(2)
print("waiting")
from subprocess import call
exit_code = call("python .\input_words.py", shell=True)
with open("input.txt", "r") as f:
    input = f.read()
print(input)

