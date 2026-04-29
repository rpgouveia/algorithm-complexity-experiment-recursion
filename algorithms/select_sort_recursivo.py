
def min_indice(A, i, j):
    if i == j:
        return i
    k = min_indice(A, i + 1, j)
    return i if A[i] < A[k] else k

def select_sort(A, n, indice = 0):
    if indice == n:
       return
    k = min_indice(A, indice, n-1)
    if k != indice:
        A[k], A[indice] = A[indice], A[k]
    select_sort(A, n, indice + 1)
    return A

def select_sort_recursivo_wapper(X):
    return select_sort(X, len(X))

#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = select_sort_recursivo_wapper(X)
#print('DEPOIS',QQ)
