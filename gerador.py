from datetime import datetime
import time
from random import randint

def gerar_dados_crescente(N):
    L=[]
    for i in range(0,N,1):
        L.append(i + 17)
    return L

def gerar_dados_decrescente(N):
    L=[]
    for i in range(N,0, -1):
        L.append(i + 17)
    return L

def gerar_dados_random(N):
    L=[]
    for i in range(0,N,1):
        L.append(randint(0,N))
    return L

def agora():
    return int(round(time.time() * 1000))
    #return datetime.now()

def dif_time(a, b):
    #return b.second - a.second
    return a - b

