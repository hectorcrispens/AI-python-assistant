import re
import pprint
#import gtts
import json
import random
import time
#from pynlp import PyNLP
import pandas as pd
import numpy as np

import speak.pyio as spk
import neural.neural as ia
import nlp.pynlp as nlp

import features.translate as trl
import features.weather as wtr
import features.datetime as dtm


import tensorflow as tf
from tensorflow import keras

## CARGAR ARCHIVOS DEL DATASET E INTENTS

# Cargamos el dataset que nos proveera los datos para el entrenamiento de la red  
#df = pd.read_csv('neural/dataset.csv', index_col=0)

# Cargamos el archivo intents.json que nos provee respuestas y las classes
intent = None
with open('nlp/intent.json', 'r') as f:
    try:
        data = f.read()
        intent = json.loads(data)
        intent = intent["intents"]
    except Exception as e:
        print(e)
    


# Procesador de operaciones
#opp = ModeloIA()




## PREPARAR PARA ENTRENAR A LA RED NEURONAL
df = nlp.fetch_dataset(intent)

#stopwords = nlp.stopwords()
# Creacion de un vocabulario a partir del dataset para codificar las entradas
vocabulary = nlp.make_vocabulary(df.patterns)

# Obtener la lista de classes del intent para codificar las salidas
classes = [X['tag'] for X in intent]

# Codificar datos de entrada para la red neuronal usando el vocabulario
encoded_x = [nlp.encode_sentence(x, vocabulary) for x in df.patterns]
encoded_x = np.array(encoded_x)

# Codificar las salida de la red usando las classes
encoded_y = nlp.encode_intents(df.intents, classes)
encoded_y = np.array(encoded_y)





### ENTRENAMIENTO DE LA RED NEURONAL


# Definicion de la topologia, el numero de entradas es igual al tamaño de los vectores de entrada, es decir es igual al vocabulario y el de salida es igual al tamaño del vector de clases
topology=[len(encoded_x[0]), 60, 60, 30, len(encoded_y[0])]

# Creamos la red neuronal usando la funcion _create_nn
#neural_net = ia.create_nn(topology,ia.sigm)



# CREAMOS LA RED NEURONAL CON KERAS
model = keras.models.load_model('model.h5')

# # Compilamos el modelo, definiendo la función de coste y el optimizador.
# model.compile(loss='mse', optimizer=keras.optimizers.SGD(lr=0.05), metrics=['acc'])

# print(topology)


# # Y entrenamos al modelo. Los callbacks 
# model.fit(encoded_x, encoded_y, epochs=100)
# model.summary()
#neural_net = ia.build_nn(layers, ia.sigm)
#Error cuadratico recomendado < 0.00178476
# Entrenamos mientras el error mientras train devuelve False, train esta redondeando y discretizando los valores, al igual que compara con la salida
# trained = False
# epochs = 1
# while not trained:
#     trained=ia.train(neural_net, encoded_x, encoded_y, ia.l2_cost, 0.07)
#     epochs = epochs + 1

# print("Total de epochs: {0}".format(epochs))

## INICIAR EL ASISTENTE VIRTUAL

# El asistente informa que esta listo
spk.speak("virtual assistant is ready")


# Algunas variables necesarios
context = "conversation"
sound = True

# Escaneo continuo de audio
while True:
    hope = True
    # Obtenemos un texto a partir del microfono
    data = spk.recordAudio()
    intent_get = []

    # Procesamos data con la red neuronal y decodifcamos el intents
    try:       
        if hope and context in ["conversation"]:
            hope = False

            # Toda la logica de codificar el dato obtenido, procesar el dato codificado por la red neuronal,
            # obterner la salida codificada y decodificar la salida.
            encoded_s = [nlp.encode_sentence(data, vocabulary)]
            #encoded_r = ia.forward_pass(neural_net, np.array(encoded_s))

            # En caso de usar keras
            encoded_r = model.predict(encoded_s)
            print(encoded_r)
            encoded_r = ia.at_discrete(encoded_r)
            print(encoded_r)

            b = [x==1 for x in encoded_r[0]]
            np_classes = np.array(classes)
            intent_get = np_classes[b]
            intent_get = intent_get[0]

            print("#" * 50)
            print("\t Context: {0}".format(context))
            print("\t Hope: {0}".format(hope))
            print("#" * 50)
            
            for n in intent:
                if intent_get in n["tag"]:
                    resp = n["responses"][random.randint(0, len(n["responses"]) -1)]
                    spk.speak(resp, sound)
                    context = n["context"][0]

                    # Empezamos a listar las operaciones contextuales del Asistente
                    # Poner en silencio el asistente
                    if intent_get in ["shutup"]:
                        sound = False
                        
                    # Habilitar el sonido del asistente
                    if intent_get in ["speak"]:
                        sound = True
                    
                    # Pronostico del tiempo
                    if intent_get in ["weather"]:
                        datos = wtr.weather_app()
                        pprint(datos)

                    # Hora del dia
                    if intent_get in ["time"]:
                        spk.speak(dtm.time())

        if hope and context in ["translate"]:
            hope = False
            text = trl.translate(data)
            print(text)
            time.sleep(10)
            context = "conversation"
            

    except Exception:
        print("not decode intents...")
        time.sleep(2)
        continue

                    

    
    # if re.search('weather|temperature', data):
    #     #city = data.split(' ')[-1]
    #     city = 'Santa Fe, AR'
    #     weather_data = spk.weather(city=city)
    #     print(weather_data)
    #     t2s(weather_data)
    #     continue
    # if re.search('news', data):
    #     news_data = spk.news()
    #     pprint.pprint(news_data)
    #     t2s(f"I have found {len(news_data)} news. You can read it. Let me tell you first 2 of them")
    #     t2s(news_data[0])
    #     t2s(news_data[1])
    #     break

    # if re.search('tell me about', data):
    #     topic = data[14:]
    #     wiki_data = spk.wikipedia(topic)
    #     print(wiki_data)
    #     t2s(wiki_data)
    #     break

    # if re.search('date', data):
    #     date = spk.tell_me_date()
    #     print(date)
    #     print(t2s(date))
    #     break

    # if re.search('time', data):
    #     time = spk.tell_me_time()
    #     print(time)
    #     t2s(time)
    #     break

    # if re.search('open', data):
    #     domain = data.split(' ')[-1]
    #     open_result = spk.website_opener(domain)
    #     print(open_result)
    #     break
            
    # else:
    #     t2s(data, 'en')
    #     continue
