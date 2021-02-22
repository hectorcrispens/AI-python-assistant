import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

#pip3 install googletrans==3.1.0a0
from googletrans import Translator

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

def speak_es(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='es')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
    
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return data

def jarvis(data):
    if "how are you" in data:
        speak("I am fine")

    elif "what time is it" in data:
        speak(ctime())

    elif "where is" in data:
        data = data.split(" ")
        location = data[2]
        speak("Hold on Frank, I will show you where " + location + " is.")
        browser = "/opt/apps/com.betanews.waterfox/files/waterfox/waterfox"
        os.system(browser + " https://www.google.nl/maps/place/" + location + "/&amp;")

    elif "translate" in data:
        translator = Translator()
        data = data.replace("translate", "", 1)
        print("translate :" + data)
        translations = translator.translate(data, "es")
        speak_es(translations.text)

        

# initialization
time.sleep(2)
speak("Hi Frank, what can I do for you?")
while 1:
    data = recordAudio()
    jarvis(data)

