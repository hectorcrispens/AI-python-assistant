import numpy as np
import scipy as sc
import os
import time
import json


#from sklearn.datasets import make_circles

# CREAR DATASET
n = 10 # FILAS DEL DATASET
p = 2 # COLUMNAS DEL DATASET


# # CLASE DE LA CAPA DE LA RED
class neural_layer():
    def __init__(self, w, b, act_f):
        self.act_f = act_f
        # vector de bias, se puede multiplicar porque type es numpy.ndarray
        # multiplica por 2 - 1, para que los valores de rand vayan de -1 < x < 1 pero el shape es [1, n_neur] y [n_conn, n_neur]
        self.b = b
        self.w = w
              
# Funciones de activacion
sigm = (lambda x: 1 / (1 + np.e ** ( - x )),
        lambda x: x * (1 - x))

relu = (lambda x: np.maximum(0, x),
        lambda x: np.maximum(0, x))


#print(red)
# ERROR CUADRATICO MEDIO
l2_cost = (lambda Yp, Yr: np.mean((Yp-Yr) ** 2),
           lambda Yp, Yr: (Yp-Yr))

def train(neural_net, x, y, l2_cost, rate = 0.5):

    out = [(None,x) ]
    zetas = [x]
    alphas = [None]
    #FORWARD PASS
    for l, layer in enumerate(neural_net):
        z = np.dot(out[-1][1], neural_net[l].w) + neural_net[l].b
        a = neural_net[l].act_f[0](z)       
        zetas.append(z)
        alphas.append(a)
        out.append((z,a))

    
    deltas = []
    # neural_net[0-6]
    for l in reversed(range(0, len(neural_net))):
        # los indices out[l+1] son porque en out[0] hemos guardado los datos que provienen del dataset
        z = out[l+1][0]
        a = out[l+1][1]
        
        # BACKWARD PASS
        if l == len(neural_net)-1:           
           # calcular delta en ultima capas (derivada del costo* derivada de la activacion)
           deltas.insert(0, l2_cost[1](a, y) * neural_net[l].act_f[1](a))

        else:
            deltas.insert(0, np.dot(deltas[0],_W.T) * neural_net[l].act_f[1](a))

        _W =  neural_net[l].w
        
        # GRADIENT DESCENT
        neural_net[l].b = neural_net[l].b - np.mean(deltas[0], axis = 0, keepdims=True) * rate
        neural_net[l].w = neural_net[l].w - np.dot(out[l][1].T,deltas[0]) * rate
    time.sleep(0.1)
    os.system('clear')

    # Como la funcion de activacion es continua y nosotros necesitamos valores discretos
    # primero redondeamos todos los valores obtenidos de la activacion de la ultima capa
    # finalmente convertimos esos valores a numeros enteros y comparamos con la salida esperada
    result = np.around(out[-1][1])
    result = result.astype(int)
    print(result)
    print("Error cuadratico medio {cost}".format(cost = l2_cost[0](y, out[-1][1])) )
    compare = result == y
    return compare.all()
    # print("\n Salida Esperada")
    # print(y)

def forward_pass(neural_net, x):
    out = [(None,x) ]
    zetas = [x]
    alphas = [None]
    #FORWARD PASS
    for l, layer in enumerate(neural_net):
        z = np.dot(out[-1][1], neural_net[l].w) + neural_net[l].b
        a = neural_net[l].act_f[0](z)       
        out.append((z,a))
    return at_discrete(out[-1][1])

def at_discrete(out):
    # Como la funcion de activacion es continua y nosotros necesitamos valores discretos
    # primero redondeamos todos los valores obtenidos de la activacion de la ultima capa
    # finalmente convertimos esos valores a numeros enteros y comparamos con la salida esperada
    result = np.around(out)
    result = result.astype(int)
    return result

def get_state(neural_net):
    layers = []
    for n in neural_net:
        dic = {"w": n.w.tolist(), "b": n.b.tolist()}
        layers.append(dic)
    return list(layers)

# Funcion que crea la red con todas las capaz
def create_nn(topology, act_f):
    nn = []
    for l, value in enumerate(topology[:-1]):
        w = np.random.randn(value,topology[l+1])
        b = np.random.randn(1, topology[l+1])
        nn.append(neural_layer(w, b, act_f))
    return nn

def build_nn(layers, act_f):
    nn = []
    for layer in layers:
        nn.append(neural_layer(np.array(layer["w"]), np.array(layer["b"]), act_f))
    return nn
