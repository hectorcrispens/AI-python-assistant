#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


try:
    if not os.path.exists("model"):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    
    device_info = sd.query_devices(None, 'input')
    # soundfile expects an int, sounddevice provides a float:
    samplerate = int(device_info['default_samplerate'])

    model = vosk.Model("model")

   
    dump_fn = None

    with sd.RawInputStream(samplerate=samplerate, blocksize = 8000, device=None, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    value = json.loads(rec.Result()) 
                    print(value["text"])
                # else:
                #     print(rec.PartialResult())
                # if dump_fn is not None:
                #     dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')  
