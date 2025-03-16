numbers = [5, 2, 3, 4, 1]

for i in range(len(numbers) - 1):
    for j in range(i, len(numbers)):
        if numbers[i] > numbers[j]:
            numbers[i], numbers[j] = numbers[j], numbers[i]

print(numbers)
