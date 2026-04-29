from random import randrange

def partition(x, indice_do_pivo = 0):
    i = 0
    
    if indice_do_pivo != 0: 
        x[0],x[indice_do_pivo] = x[indice_do_pivo],x[0]
        
    for j in range(len(x) - 1):
        if x[j + 1] < x[0]:
            x[j + 1], x[i +1 ] = x[i + 1], x[j + 1]
            i += 1
            
    x[0], x[i] = x[i], x[0]
    return x, i

def select_sort_random(x, k):
    if len(x) == 1:
        return x[0]
    else:
        parte_do_x = partition(x, randrange(len(x)))
        x = parte_do_x[ 0 ] # arranjo particionado
        j = parte_do_x[ 1 ] # indice do pivo
        if j == k:
            return x[ j ]
        elif j > k:
            return select_sort_random(x[:j], k)
        else:
            k = k - j - 1
            return select_sort_random(x[(j+1):], k)

def select_sort_recursivo_random_wapper(x, contador = 0, Q = []):
    if contador == len(x):
        return Q
    else:
        Q.append(select_sort_random(x, contador))
        select_sort_recursivo_random_wapper(x, contador + 1, Q)
    return Q


#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = select_sort_recursivo_random_wapper(X)
#print('DEPOIS',QQ)

