numbers = [1, 2, 3, 4, 5, 6]


def binary_search(number):
    low = 0
    high = len(numbers) - 1
    while low <= high:
        index = (low + high) // 2
        if numbers[index] < number:
            low = index - 1
        elif numbers[index] > number:
            high = index + 1
        else:
            return index
    return -1


print(binary_search(4))
