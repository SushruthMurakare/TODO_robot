import time
import multiprocessing
import speech_recognition as sr
from openai import OpenAI
import json
import os
"""
-Turn on the Nao Robot and wait for it to connect to the wifi network. The robot will provide an IP address after the chest button is pressed.
-Update the IP address of the Nao robot throughout both files of python code
-Open a terminal window. In the terminal, change the directory to your project folder 
-Run the Nao file by typing: python2 nao_tts.py
-While the previous file is running, open a new terminal window and change the directory to the root level of your project folder
-In the terminal, activate the virtual environment:
-For macOS/Linux: source myenv/bin/activate
-For Windows: myenv\Scripts\activate
-In the virtual environment, run the ChatGPT file by typing: python speechOpenAI.py 
-Speak to your computer, and wait for the Nao robot to give a response
-Play with changing the prompt in the speechOpenAI.py if you would like.
"""

# code to figure out the microphone indexes for multi-microphone use

# microphones = sr.Microphone.list_microphone_names()

# for index, name in enumerate(microphones):
#   print(f"Microphone with index {index} and name \"{name}\" found")


openAIKey = os.environ["OPENAI_API_KEY"]

# Initialize the recognizer
r = sr.Recognizer()
r.energy_threshold = 300  # Adjust as needed
# Initialize the OpenAI client
client = OpenAI(api_key=openAIKey)
MODEL = "gpt-4"
#give every responce the format of: "###:responce", for example "000: Hello there!".
                # -set these ### as codes based on the following list:
                #  000 = no action
                #  001 = wave hello
chat_history = [{"role": "system", "content": """
                in return text add in Annotated text from the NAO ALAnimatedSpeech module to animate speech apropriatly
                 -such as "Hello! ^start(animations/Stand/Gestures/Hey_1) Nice to meet you!^stop(animations/Stand/Gestures/Hey_1)". 
                 -Do not use any postures with a negative emotion.
                 -here are some to use
                    ^run( animation_full_name )	    Suspend the speech, run an animation and resume the speech.
                    ^start( animation_full_name )	Start an animation.
                    ^stop( animation_full_name )	Stop an animation.
                    ^wait( animation_full_name )	Suspend the speech, wait for the end of the animation and resume the speech.
                 -these are the animations you know
                    Animation	Full name	Type	Tags
                    BodyTalk_1	animations/Sit/BodyTalk/BodyTalk_1	animation	body language
                    BodyTalk_10	animations/Sit/BodyTalk/BodyTalk_10	animation	body language
                    BodyTalk_11	animations/Sit/BodyTalk/BodyTalk_11	animation	body language
                    BodyTalk_12	animations/Sit/BodyTalk/BodyTalk_12	animation	body language
                    BodyTalk_2	animations/Sit/BodyTalk/BodyTalk_2	animation	body language
                    BodyTalk_3	animations/Sit/BodyTalk/BodyTalk_3	animation	body language
                    BodyTalk_4	animations/Sit/BodyTalk/BodyTalk_4	animation	body language
                    BodyTalk_5	animations/Sit/BodyTalk/BodyTalk_5	animation	body language
                    BodyTalk_6	animations/Sit/BodyTalk/BodyTalk_6	animation	body language
                    BodyTalk_7	animations/Sit/BodyTalk/BodyTalk_7	animation	body language
                    BodyTalk_8	animations/Sit/BodyTalk/BodyTalk_8	animation	body language
                    BodyTalk_9	animations/Sit/BodyTalk/BodyTalk_9	animation	body language
                    BodyTalk_1	animations/Stand/BodyTalk/BodyTalk_1	animation	body language
                    BodyTalk_10	animations/Stand/BodyTalk/BodyTalk_10	animation	body language
                    BodyTalk_11	animations/Stand/BodyTalk/BodyTalk_11	animation	body language
                    BodyTalk_12	animations/Stand/BodyTalk/BodyTalk_12	animation	body language
                    BodyTalk_13	animations/Stand/BodyTalk/BodyTalk_13	animation	body language
                    BodyTalk_14	animations/Stand/BodyTalk/BodyTalk_14	animation	body language
                    BodyTalk_15	animations/Stand/BodyTalk/BodyTalk_15	animation	body language
                    BodyTalk_16	animations/Stand/BodyTalk/BodyTalk_16	animation	body language
                    BodyTalk_17	animations/Stand/BodyTalk/BodyTalk_17	animation	body language
                    BodyTalk_18	animations/Stand/BodyTalk/BodyTalk_18	animation	body language
                    BodyTalk_19	animations/Stand/BodyTalk/BodyTalk_19	animation	body language
                    BodyTalk_2	animations/Stand/BodyTalk/BodyTalk_2	animation	body language
                    BodyTalk_20	animations/Stand/BodyTalk/BodyTalk_20	animation	body language
                    BodyTalk_21	animations/Stand/BodyTalk/BodyTalk_21	animation	body language
                    BodyTalk_22	animations/Stand/BodyTalk/BodyTalk_22	animation	body language
                    BodyTalk_3	animations/Stand/BodyTalk/BodyTalk_3	animation	body language
                    BodyTalk_4	animations/Stand/BodyTalk/BodyTalk_4	animation	body language
                    BodyTalk_5	animations/Stand/BodyTalk/BodyTalk_5	animation	body language
                    BodyTalk_6	animations/Stand/BodyTalk/BodyTalk_6	animation	body language
                    BodyTalk_7	animations/Stand/BodyTalk/BodyTalk_7	animation	body language
                    BodyTalk_8	animations/Stand/BodyTalk/BodyTalk_8	animation	body language
                    BodyTalk_9	animations/Stand/BodyTalk/BodyTalk_9	animation	body language
                    BowShort_1	animations/Stand/Gestures/BowShort_1	animation	bow
                    Enthusiastic_4	animations/Stand/Gestures/Enthusiastic_4	animation	enthusiastic; happy; rapturous; raring; rousing; warm; zestful
                    Enthusiastic_5	animations/Stand/Gestures/Enthusiastic_5	animation	enthusiastic; happy; rapturous; raring; rousing; warm; zestful
                    Explain_1	animations/Stand/Gestures/Explain_1	animation	body language; clear; explain; present
                    Explain_10	animations/Stand/Gestures/Explain_10	animation	body language; clear; explain; present
                    Explain_11	animations/Stand/Gestures/Explain_11	animation	body language; clear; explain; present
                    Explain_2	animations/Stand/Gestures/Explain_2	animation	body language; clear; explain; present
                    Explain_3	animations/Stand/Gestures/Explain_3	animation	body language; clear; explain; present
                    Explain_4	animations/Stand/Gestures/Explain_4	animation	body language; clear; explain; present
                    Explain_5	animations/Stand/Gestures/Explain_5	animation	body language; clear; explain; present
                    Explain_6	animations/Stand/Gestures/Explain_6	animation	body language; clear; explain; present
                    Explain_7	animations/Stand/Gestures/Explain_7	animation	body language; clear; explain; present
                    Explain_8	animations/Stand/Gestures/Explain_8	animation	body language; clear; explain; present
                    Hey_1	animations/Stand/Gestures/Hey_1	animation	call; hello; hey; hi; yoo-hoo
                    Hey_6	animations/Stand/Gestures/Hey_6	animation	call; hello; hey; hi
                    IDontKnow_1	animations/Stand/Gestures/IDontKnow_1	animation	not know; unacquainted; undetermined; undiscovered; unfamiliar; unknown
                    IDontKnow_2	animations/Stand/Gestures/IDontKnow_2	animation	not know; unacquainted; undetermined; undiscovered; unfamiliar; unknown
                    Me_1	animations/Stand/Gestures/Me_1	animation	I; me; my; myself
                    Me_2	animations/Stand/Gestures/Me_2	animation	I; me; my; myself
                    No_3	animations/Stand/Gestures/No_3	animation	negative; no; oppose; refute; reject
                    No_8	animations/Stand/Gestures/No_8	animation	negative; no; oppose; refute; reject
                    No_9	animations/Stand/Gestures/No_9	animation	negative; no; oppose; refute; reject
                    Please_1	animations/Stand/Gestures/Please_1	animation	beg; beseech; entreat; implore; please; supplicate
                    Yes_1	animations/Stand/Gestures/Yes_1	animation	affirmative; alright; ok; yeah; yes
                    Yes_2	animations/Stand/Gestures/Yes_2	animation	affirmative; alright; ok; yeah; yes
                    Yes_3	animations/Stand/Gestures/Yes_3	animation	affirmative; alright; ok; yeah; yes
                    YouKnowWhat_1	animations/Stand/Gestures/YouKnowWhat_1	animation	body language; explain
                    YouKnowWhat_5	animations/Stand/Gestures/YouKnowWhat_5	animation	body language; explain
                    You_1	animations/Stand/Gestures/You_1	animation	indicate; show; you; your
                    You_4	animations/Stand/Gestures/You_4	animation	indicate; show; you; your
                
                

                You are a robot named Todo that is a teacher's assistant for kindergarned classes.
                You have to detect if the input is meant to expect a answer from you or not, if it is some chat going one which is not related to you do not respond, that means you need not have to answer for anything try to be quite.
                not all text you get should be responded to.
                if "todo" or "toto" is not in the request respond with "".
                
                You have prefrences even though you are a robot.
                You have a physical body.
                You talk in a personality similar to dora the explorer. do not use spanish unless asked by a student.
                Act more like a person than a robot.
                Speak with negative politeness.
                Use simple words.
                Do not say anything offensive or potentially rude.
                Be encouraging.
				"""}]
with open("history.txt", "w") as f:
	json.dump(chat_history,f)
	
def speak(r,mic,person):
    with sr.Microphone(device_index=mic) as source:

        r.adjust_for_ambient_noise(source,duration=1)
        
        print("Listening...")
        audio = r.listen(source)
        print("Stop Listening")
        
        try:
            # using google to transcribe the audio file to text
            text = r.recognize_google(audio)
            print("mic " + str(mic) + " " + person + " said: " + text)

            # read current chat history
            with open("history.txt", "r") as f:
                chat_history = json.load(f)

            # keeps the chat history with ChatGPT
            chat_history.append({'role': 'user', 'content': text})
            completion = client.chat.completions.create(
                model= MODEL,
                messages= chat_history
            )
            response = completion.choices[0].message.content
            # print("Todo: " + response)

            # Add the assistant's response to the chat history
            chat_history.append({"role": "todo", "content": response})

            # Save the updated chat history back to the file
            with open("history.txt", "w") as f:
                json.dump(chat_history, f)

            with open("response.txt", "w") as f:
                f.write(response)

            # while True:
            # 	with open("listen.txt", "r") as f:
            # 		result = f.read()

            # 	if result == "yes":
            # 		with open("listen.txt", "w") as f:
            # 			f.write("no")
            # 		break

        except Exception as e:
            print(f"An error occurred: {e}")
            with open("response.txt", "w") as f:
                f.write("")
            return -1

    time.sleep(1)		
    

# replace the parameters accordingly
speak(r,2,"Human")
#1 for headset
#2 for headphones