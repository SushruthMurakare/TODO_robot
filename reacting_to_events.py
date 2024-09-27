#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import time
import sys
import argparse
from subprocess import call
# from naoqi import ALProxy # for having the robot sit

class HumanGreeter(object):
    """
    A simple class to react to face detection events.
    """
    

    def __init__(self, app):
        #used to have the robot sit down and stay still
        #motionProxy  = ALProxy("ALMotion", "10.60.238.195", 9559)
        #motionProxy.rest()
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session

        # Get the service ALMemory.
        self.memory = session.service("ALMemory")

        #creates an event listener for the justArrived flag and calls on_human_tracked when it is flagged
        self.subscriber = self.memory.subscriber("PeoplePerception/JustArrived")
        self.subscriber.signal.connect(self.on_human_tracked)

        #creates an event listener for the justLeft flag and calls on_human_tracked2 when it is flagged
        self.subscriber2 = self.memory.subscriber("PeoplePerception/JustLeft")
        self.subscriber2.signal.connect(self.on_human_tracked2)

        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.face_detection = session.service("ALPeoplePerception")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False

        self.name = "" # used to store the name that it hears

    def on_human_tracked(self, value):
        self.tts.say("Hello, you! Whats your name?")
        print("waiting")
        
        call("python .\input_words.py", shell=True) # calls python 3 file

        with open("input.txt", "r") as f:
            input = f.read() # opens and reads what the python file outputs
        print(input)
        self.name = input
        self.tts.say("Hello, "+self.name+"!")

    def on_human_tracked2(self, value):
        if self.name == "":
            self.tts.say("Good Bye!")
        else:
            self.tts.say("Good Bye "+self.name+"!")

    def run(self):
        print("Starting HumanGreeter")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print( "Interrupted by user, stopping HumanGreeter")
            self.face_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)
  

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="10.60.238.195",
                        help="Robot IP address. On robot or Local Naoqi: use '10.60.238.195'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["HumanGreeter", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    human_greeter = HumanGreeter(app)
    human_greeter.run()
