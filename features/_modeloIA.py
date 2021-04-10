import pyaudio
import speech_recognition as sr
import pprint
import os
from gtts import gTTS
import time

import features.weather as wea
import features.wikipedia as wik
import features.news as nw
import features.datetime as dtime
import features.website as ws
import features.translate as tl

class ModeloIA():
    def __init__(self):
        self.silence = False

    # Funcion encargada del audio, recibe un texto y lo envia como audio al altavoz
    def speak(self, audioString, l='en'):
        print(audioString)
        if not self.silence:
            tts = gTTS(text=audioString, lang=l)
            tts.save("audio.mp3")
            os.system("mpg321 audio.mp3")

    def recordAudio(self):
        microphone = sr.Microphone()
        recognizer = sr.Recognizer()
        
        with microphone as micro_audio:
            print("Start Speaking ...")
            
            recognizer.adjust_for_ambient_noise(micro_audio)
            audio = recognizer.listen(micro_audio)
            data = ""
            try:
                print("Converting your speech to text...")
                data = recognizer.recognize_google(audio)
                return data
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def wheater(self, city='Santa Fe, AR'):
        try:
            res = wea.weather_app(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def news(self):
        return nw.news()

    def wikipedia(self, topic='tell me about earth planet'):
        return wik.tell_me_about(topic)

    def date(self):
        return dtime.date()

    def time(self):
        return dtime.time()

    def open(self, domain):
        return ws.website(domain)

    def translate(self, text):
        return tl.translate(text)
        
