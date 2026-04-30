def insertion_sort_recursivo(arr, n):
    if n <= 1:
        return arr
    insertion_sort_recursivo(arr, n - 1)
    last = arr[n - 1]
    j = n - 2
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1

    arr[j + 1] = last
    return arr

def IS_recursivo(array):
    return insertion_sort_recursivo(array, len(array))
