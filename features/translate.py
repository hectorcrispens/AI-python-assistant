#pip3 install googletrans==3.1.0a0
from googletrans import Translator

def translate(data):
    translator = Translator()
    try:
        translations = translator.translate(data, "es")
        return translations.text
    except Exception as e:
        return "I'm sorry, something has gone wrong"
    
