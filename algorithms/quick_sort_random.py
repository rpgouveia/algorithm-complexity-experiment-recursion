from random import randint

def swap_r(A, i, j):
    aux = A[ i ]
    A[ i ] = A[ j ]
    A[ j ] = aux

def partition_r(A, p, r):
    x = randint(p, r)
    swap_r(A, x, r)
    x = A[ r ]
    i = p - 1
    for j in range(p, r, 1):
        if A[ j ] <= x:
            i = i + 1
            swap_r(A, i, j)
    swap_r(A, i + 1, r)
    return i + 1

def quick_sort_r(A, p, r):
    if p < r:
        q = partition_r(A, p, r)
        quick_sort_r(A, p, q - 1)
        quick_sort_r(A, q + 1, r)

def quick_sort_recursivo_random_wapper(A):
    N = len(A) - 1
    quick_sort_r(A, 0, N)
    return A

#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = quick_sort_recursivo_random_wapper(X)
#print('DEPOIS',QQ)
