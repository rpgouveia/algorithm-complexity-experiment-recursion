def merge(S, temp, From, mid, to):

    a = From
    b = From
    c = mid + 1

    while b <= mid and c <= to:
        if S[b] < S[c]:
            temp[a] = S[b]
            b = b + 1
        else:
            temp[a] = S[c]
            c = c + 1
        a = a + 1

    # remaining elements
    while b < len(S) and b <= mid:
        temp[a] = S[b]
        a = a + 1
        b = b + 1

    # copy back
    for b in range(From, to + 1):
        S[b] = temp[b]


# Iterative sort
def Merge_Sort(S):

    low = 0
    high = len(S) - 1

    # sort list
    temp = S.copy()

    d = 1
    while d <= high - low:

        for b in range(low, high, 2*d):
            From = b
            mid = b + d - 1
            to = min(b + 2*d - 1, high)
            merge(S, temp, From, mid, to)

        d = 2*d
    return S

def Merge_Sort_interativo_wapper(A):
    return Merge_Sort(A)

#X = [58, 30, 97, 21, 81, 35, 48, 59, 24, 2, -1]
#print('ANTES',X)
#QQ = Merge_Sort_interativo_wapper(X)
#print('DEPOIS',QQ)
