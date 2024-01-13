import speech_recognition as sr
import pyttsx3

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env.local')
load_dotenv(dotenv_path=dotenv_path)
OPENAI_KEY=os.getenv("API_KEY")

import openai

openai.api_key = OPENAI_KEY

def speak_text(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()
    
r = sr.Recognizer()

def record_text():
    while 1:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source=source2, duration=0.2)
                print("Say something!")
                
                audio2 = r.listen(source=source2)
                mytext = r.recognize_google(audio_data=audio2)
                
                return mytext
        except sr.RequestError as e:
            print(f"Couldn't request results. {e}")
        except sr.UnknownValueError:
            print(f"Unknown error occurs")
    return 

def send_to_chatgpt(messages, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message
    

messages = []

while 1:
    text=record_text()
    messages.append({"role":"user", "content": text})
    response = send_to_chatgpt(messages=messages)
    speak_text(response)
    
    print(response)