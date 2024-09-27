#!/usr/bin/env python3.11
import time
import multiprocessing
import speech_recognition as sr
import json
import os

# code to figure out the microphone indexes for multi-microphone use

microphones = sr.Microphone.list_microphone_names()


#finding the microphone that you want to use
#for index, name in enumerate(microphones):
#    print(f"Microphone with index {index} and name \"{name}\" found")



# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 300  # Adjust volume threshold

def speak(mic,person):
	while True:
		with sr.Microphone(device_index=mic) as source:

			r.adjust_for_ambient_noise(source,duration=1)
			
			print("Listening...")
			audio = r.listen(source)
			print("Stop Listening")
			
			try:
				# using google to transcribe the audio file to text
				text = r.recognize_google(audio)
				print("mic " + str(mic) + " " + person + " said: " + text)

				with open("input.txt", "w") as f:
					f.write(text) # writes the words that it heard to input file
					#will overwrite
				break

			except Exception as e:
				print(f"An error occurred: {e}")

		time.sleep(1)		
		

speak(2,"Human")
#1 for headset
#2 for headphones

