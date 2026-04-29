def insertion_sort_recursivo(arr, n):
    if n <= 1:
        return
    insertion_sort_recursivo(arr, n - 1)
    last = arr[n - 1]
    j = n - 2
    while j >= 0 and arr[j] > last:
        arr[j + 1] = arr[j]
        j -= 1

    arr[j + 1] = last

a = [-7, 11, 6, 0, -3, 5, 10, 2]
insertion_sort_recursivo(a, len(a))
print(a)


def IS_recursivo(array):
    return insertion_sort_recursivo(array, len(array))
