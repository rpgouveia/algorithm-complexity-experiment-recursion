import sys

from algorithms.quick_sort_recursivo import quick_sort_recursivo_wapper
from algorithms.quick_sort_random import quick_sort_recursivo_random_wapper
from algorithms.merge_sort_interativo import Merge_Sort_interativo_wapper
from algorithms.merge_sort_recursivo import merge_sort__recursivo_wapper
from algorithms.merge_sort_recursivo_random import merge_sort_recursivo_random_wapper
from algorithms.select_sort_recursivo import select_sort_recursivo_wapper
from algorithms.select_sort_recursivo_random import select_sort_recursivo_random_wapper
from algorithms.sellSort_base_line import shellSort_Wapper
from algorithms.Insertion_sort_interativo import insertion_sort_interativo
from algorithms.insertion_sort_recursivo import IS_recursivo
from gerador import gerar_dados_crescente
from gerador import gerar_dados_random
from gerador import gerar_dados_decrescente
from gerador import agora
from gerador import dif_time


def teste():
    X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
    print(f'X : {X}')

    QS1 = quick_sort_recursivo_wapper(X.copy())
    QS2 = quick_sort_recursivo_random_wapper(X.copy())
    print(f'Quick sort recursivo: {QS1}')
    print(f'Quick sort recursivo randomizado: {QS2}')

    MS1 = Merge_Sort_interativo_wapper(X.copy())
    MS2 = merge_sort__recursivo_wapper(X.copy())
    MS3 = merge_sort_recursivo_random_wapper(X.copy())
    print(f'Merge sort interativo: {MS1}')
    print(f'Merge sort recursivo: {MS2}')
    print(f'Merge sort recursivo randomizado: {MS3}')

    SS1 = select_sort_recursivo_wapper(X.copy())
    SS2 = select_sort_recursivo_random_wapper(X.copy())
    print(f'Select sort recursivo: {SS1}')
    print(f'Select sort recursivo randomizado: {SS2}')

    BASE_LINE = shellSort_Wapper(X.copy())
    print(f'Sell Sort [Baseline]: {BASE_LINE}')

    IS1 = insertion_sort_interativo(X.copy())
    IS2 = IS_recursivo(X.copy())
    print(f'Insertion sort interativo: {IS1}')
    print(f'Insertion sort recursivo: {IS2}')

def execucao(X, i):
    D = []

    a = agora()
    QS1 = quick_sort_recursivo_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    QS2 = quick_sort_recursivo_random_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    MS1 = Merge_Sort_interativo_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    MS2 = merge_sort__recursivo_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    MS3 = merge_sort_recursivo_random_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    SS1 = select_sort_recursivo_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    SS2 = select_sort_recursivo_random_wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    BASE_LINE = shellSort_Wapper(X.copy())
    b = agora()
    D.append(dif_time(b,a))
    

    a = agora()
    S1 = insertion_sort_interativo(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    a = agora()
    S2 = IS_recursivo(X.copy())
    b = agora()
    D.append(dif_time(b,a))

    return D

limite = sys.getrecursionlimit()
print('Limite de memória: ', limite)
sys.setrecursionlimit(100000)
limite = sys.getrecursionlimit()
print('Limite de memória: ', limite)

T = 250
N = 20
L = []

for i in range(1, N+1, 1):
    print('O tamanho do problema',i, ' é ', i * T)
    # X = gerar_dados_decrescente( i * T )
    X = gerar_dados_crescente( i * T )
    # X = gerar_dados_random( i * T )
    L.append( execucao(X, i) )

print('QS1,QS2,MS1,MS2,MS3,SS1,SS2,BASE_LINE,IS1,IS2')
for x in L:
    c = len(x) - 1
    i = 0
    for y in x:
        if (i < c):
            print(y, end=',')
        else:
            print(y, end='')
        i +=1
    print()

