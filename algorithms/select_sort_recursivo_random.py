from random import randrange

def partition(x, indice_do_pivo=0):
    i = 0
    if indice_do_pivo != 0:
        x[0], x[indice_do_pivo] = x[indice_do_pivo], x[0]
    for j in range(len(x) - 1):
        if x[j + 1] < x[0]:
            x[j + 1], x[i + 1] = x[i + 1], x[j + 1]
            i += 1
    x[0], x[i] = x[i], x[0]
    return x, i

def select_sort_random(x, k):
    if len(x) == 1:
        return x[0]
    x, j = partition(x, randrange(len(x)))
    if j == k:
        return x[j]
    elif j > k:
        return select_sort_random(x[:j], k)
    else:
        return select_sort_random(x[(j + 1):], k - j - 1)

def select_sort_recursivo_random_wapper(x, contador=0, Q=None):
    if Q is None:
        Q = []
    if contador == len(x):
        return Q
    Q.append(select_sort_random(x, contador))
    return select_sort_recursivo_random_wapper(x, contador + 1, Q)