numbers = [8, 3, 1, 7, 0, 10, 2]

"""
Partition works by selecting a pivot value, 
looping from low to high,
and creating a ctack of numbers less than pivot, 
then adding the pivot value at the end.
"""


def partition(numbers, low, high):
    pivot = numbers[high]
    i = low - 1
    for j in range(low, high):
        if numbers[j] <= pivot:
            i += 1
            numbers[i], numbers[j] = numbers[j], numbers[i]
    numbers[i + 1], numbers[high] = numbers[high], numbers[i + 1]
    return i + 1


def quick_sort(numbers, low=0, high=None):
    if high == None:
        high = len(numbers) - 1
    if low >= high:
        return numbers
    pivot = partition(numbers, low, high)
    quick_sort(numbers, low, pivot - 1)
    quick_sort(numbers, pivot + 1, high)
    return numbers


print(quick_sort(numbers))
