numbers = [2, 6, 1, 7, 2]


# heapify recursively swap around parent and child to ensure parent is larger than both.
# if a swap occurs, recursively ensure that all the previous children of the new largest value still remains larger.
def heapify(numbers, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and numbers[left] > numbers[largest]:
        largest = left

    if right < n and numbers[right] > numbers[largest]:
        largest = right

    if largest != i:
        numbers[i], numbers[largest] = numbers[largest], numbers[i]
        heapify(numbers, n, largest)


def heap_sort(numbers):
    n = len(numbers)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        heapify(numbers, n, i)

    # Slowly decrease the size of the heap one by one, adding the values to the array, while maintaining heap
    for i in range(n - 1, 0, -1):
        numbers[i], numbers[0] = numbers[0], numbers[i]  # Swap
        heapify(numbers, i, 0)

    return numbers


print(heap_sort(numbers))
