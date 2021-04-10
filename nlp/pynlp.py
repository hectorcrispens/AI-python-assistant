from numpy import argmax
import numpy as np
import re
import json
import os
import pandas as pd

        
#Esta funcion elimina todos los caracteres que no son alfanumericos o espacios
def only_alphanumeric(sentence):
    new_sentence = ''
    for alphabet in sentence:
        if alphabet.isalpha() or alphabet == ' ':
            new_sentence += alphabet
    return new_sentence

#Esta funcion recibe una lista de sentencias, y las procesa una a una haciendo los siguientes cambios:
# - convierte todas las sentencias a minuscula
# - Elimina todos los caracteres de simbolos y demas que no sean alfanumericos o espacio
# - Luego convierte cada sentencia a una lista de palabras
# - finalmente elimina los espacios sucesivos
def preprocess_data(X):
    X = [data_point.lower() for data_point in X]
    X = [only_alphanumeric(sentence) for sentence in X]
    X = [data_point.strip() for data_point in X]
    X = [re.sub(' +', ' ', data_point) for data_point in X]
    return X

def stopwords():
    with open(os.path.dirname(__file__)+'/stopwords.json', 'r') as f:
        stopw = f.read()
        return json.loads(stopw)


def fetch_dataset(intents):
    tags = []
    patterns = []
    for ob in intents:
        for pat in ob["patterns"]:
            patterns.append(pat)
            tags.append(ob["tag"])
    di = {"intents": tags, "patterns": patterns}
    return pd.DataFrame(di)
    
        
#Esta funcion recibe una sentencia y devuelve una lista de ceros y unos acordes las palabras
#se encuentren en el vocabulio
def encode_sentence(sentence, vocabulary):
    sentence = preprocess_data([sentence])[0]
    sentence_encoded = [0] * len(vocabulary)
    for i in range(len(vocabulary)):
        if vocabulary[i] in sentence.split(' '):
            sentence_encoded[i] = 1
    return sentence_encoded

#La salida de la red neuronal se corresponde con cada una de las classes
#se recibe por cada sentencia 
def encode_intents(Y, classes):
    Y_encoded = []
    for data_point in Y:
        data_point_encoded = [0] * len(classes)
        for i in range(len(classes)):
            if classes[i] == data_point:
                data_point_encoded[i] = 1
        Y_encoded.append(data_point_encoded)
    return Y_encoded

#Siendo X una lista de sentencias, crea devuelve una lista normalizada con todas las palabras distintas contenidas en la lista
#Devuelve un vocabulario
def make_vocabulary(X):
    X = preprocess_data(X)    
    vocabulary = set()
    for data_point in X:
        for word in data_point.split(' '):
            if word not in vocabulary:
                vocabulary.add(word)

    vocabulary = list(vocabulary)
    return vocabulary
