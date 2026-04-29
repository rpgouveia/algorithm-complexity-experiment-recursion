
def swap(A, i, j):
    aux = A[ i ]
    A[ i ] = A[ j ]
    A[ j ] = aux

def partition(A, p, r):
    x = A[ r ]
    i = p - 1
    for j in range(p, r, 1):
        if A[ j ] <= x:
            i = i + 1
            swap(A, i, j)
    swap(A, i + 1, r)
    return i + 1

def quick_sort(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quick_sort(A, p, q - 1)
        quick_sort(A, q + 1, r)

def quick_sort_recursivo_wapper(A):
    N = len(A) - 1
    quick_sort(A, 0, N)
    return A

#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = quick_sort_recursivo_wapper(X)
#print('DEPOIS',QQ)
