
def shellSort(array, a):
    mid = a // 2
    h = 1
    n = a
    while (h < n):
        h = 3 * h + 1
    mid = h
    k1 = 1
    while mid > 0:
        mid = int ((mid - 1)/3)
        k2 = 1
        for i in range(mid, a):
            chave = array[i]
            j = i
            k3 = 3
            while j >= mid and array[j - mid] > chave:
                print(k1,k2,k3, mid)
                array[j] = array[j - mid]
                j = j - mid
            array[j] = chave
        print()
    return array

def shellSort_Wapper(array):
    return shellSort(array, len(array))

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
