
def merge(A, parte_esq, parte_dir):
    i, j, k = 0, 0, 0
    while i < len(parte_esq) and j < len(parte_dir):
        if parte_esq[ i ] <= parte_dir[ j ]:
            A[ k ] = parte_esq[ i ]
            i = i + 1
        else:
            A[ k ] = parte_dir[ j ]
            j = j + 1
        k = k + 1

    while i < len(parte_esq):
        A[ k ] = parte_esq[ i ]
        i = i + 1
        k = k + 1

    while j < len(parte_dir):
        A[ k ] = parte_dir[ j ]
        j = j + 1
        k = k + 1

def merge_sort(A):
    if len(A)>1:
        divide = len(A)//2
        parte_esq = A[:divide]
        parte_dir = A[divide:]

        merge_sort(parte_esq)
        merge_sort(parte_dir)

        merge(A, parte_esq, parte_dir)

def merge_sort__recursivo_wapper(A):
    merge_sort(A)
    return A

#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = merge_sort__recursivo_wapper(X)
#print('DEPOIS',QQ)

