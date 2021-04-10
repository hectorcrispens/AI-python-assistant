from gtts import gTTS
import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import pyttsx3

# imports to Mozilla/TTS
import string
from pathlib import Path
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

# import to play
import pyaudio  
import wave
import time

def play():
    #define stream chunk   
    chunk = 1024  
    
    #open a wav format music  
    f = wave.open(r"audio.wav","rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  

    #stop stream  
    stream.stop_stream()  
    stream.close()  

    #close PyAudio  
    p.terminate()  

def text_to_wav(text):
    tts_checkpoint = "/home/hector/.local/share/tts/tts_models--en--ljspeech--speedy-speech-wn/model_file.pth.tar"
    tts_config = "/home/hector/.local/share/tts/tts_models--en--ljspeech--speedy-speech-wn/config.json"

    synthesizer = Synthesizer(tts_checkpoint, tts_config)

    # kick it
    wav = synthesizer.tts(text)

    # save the results
    file_name = 'audio.wav'
    #print(" > Saving output to {}".format(file_name))
    synthesizer.save_wav(wav, file_name)

q = queue.Queue()

# Funcion encargada del audio, recibe un texto y lo envia como audio al altavoz
def speak_from_gtts(audioString, l='en'):
    print(audioString)
    
    tts = gTTS(text=audioString, lang=l)
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")

# Funcion de speak offline
def speak_from_pytts(text):
    print(text)
    # initialize Text-to-speech engine
    engine = pyttsx3.init()
    engine.setProperty("rate", 120)
    engine.say(text)
    # play the speech
    engine.runAndWait()

def speak(text, sound=True):
    if sound:
        text_to_wav(text)
        play()
    else:
        print(text)

# Funcion que utiliza vosk, no deberia tocarla 
def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


# Funcion para grabar audio y decodificar su contenido
def recordAudio():    
    try:
        device_info = sd.query_devices(None, 'input')
        # soundfile expects an int, sounddevice provides a float:
        samplerate = int(device_info['default_samplerate'])
        
        model = vosk.Model("model")   
        dump_fn = None
        with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype='int16', channels=1, callback=callback):
            # print('#' * 80)
            # print('Press Ctrl+C to stop the recording')
            # print('#' * 80)
            
            rec = vosk.KaldiRecognizer(model, samplerate)
            band = True
            while band:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    band = False
                    value = json.loads(result)
                    print("Recorded text: {0}".format(value["text"]))
                    time.sleep(2)
                    return value["text"]
                else:
                    print(rec.PartialResult())
                    # if dump_fn is not None:
                    #     dump_fn.write(data)
    except Exception as e:
        return "error"
 
