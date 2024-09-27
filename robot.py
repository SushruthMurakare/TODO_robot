#! /usr/bin/env python
# -*- encoding: UTF-8 -*-


import qi
import time
import sys
import argparse
from subprocess import call
from naoqi import ALProxy # for having the robot sit
import atexit


class HumanGreeter(object):  

    def __init__(self, app, ip):
        #used to have the robot sit down and stay still
        
        super(HumanGreeter, self).__init__()
        app.start()
        session = app.session
        self.awake = True

        # Get the service ALMemory.
        self.memory = session.service("ALMemory")

        #creates an event listener for the justArrived flag and calls on_human_tracked when it is flagged
        self.subscriber = self.memory.subscriber("PeoplePerception/JustArrived")
        self.subscriber.signal.connect(self.on_human_tracked)

        #creates an event listener for the justLeft flag and calls on_human_tracked2 when it is flagged
        self.subscriber2 = self.memory.subscriber("PeoplePerception/JustLeft")
        self.subscriber2.signal.connect(self.on_human_tracked2)

        motionProxy  = ALProxy("ALRobotPosture", self.ip, 9559)
        motionProxy.goToPosture("StandInit", 1.0)

        # Get the services ALTextToSpeech and ALFaceDetection.
        self.tts = session.service("ALTextToSpeech")
        self.tts.setVolume(0.5)
        print(self.tts.getAvailableVoices())
        time.sleep(10)
        self.tts.setVoice("Kenny22Enhanced")

        self.face_detection = session.service("ALPeoplePerception")
        self.face_detection.subscribe("HumanGreeter")
        self.got_face = False

        self.name = "" # used to store the name that it hears

        

        responce = ""
        while(self.awake):
            call("python ./robotGPT_call.py", shell=True)
            with open("response.txt", "w") as f:
                responce = f.read()
            
            match responce:
                # case x:
                #     pass
                case _:
                    self.tts.say(responce)
        

    def sleep(self):
        motionProxy  = ALProxy("ALRobotPosture", self.ip, 9559)
        motionProxy.goToPosture("Crouch", 1.0)


    """def on_human_tracked(self, value):
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
            self.tts.say("Good Bye "+self.name+"!")"""


    def run(self):
        print("Starting HumanGreeter")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print( "Interrupted by user, stopping HumanGreeter")
            self.awake = False
            self.face_detection.unsubscribe("HumanGreeter")
            #stop
            sys.exit(0)
  

if __name__ == "__main__":
    ip = "10.60.238.195"
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default=ip,
                        help=f"Robot IP address. On robot or Local Naoqi: use {ip}.")
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

    def goodbye(human_greeter):
        human_greeter.sleep()
    
    human_greeter = HumanGreeter(app,ip)
    atexit.register(goodbye(human_greeter))
    human_greeter.run()