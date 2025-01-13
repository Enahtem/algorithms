numbers = [5,2,7,12,3]

for i in range(len(numbers)-1):
    min = i
    for j in range(i,len(numbers)):
        if numbers[j]<numbers[min]:
            min = j
    numbers[min], numbers[i] = numbers[i], numbers[min]


print(numbers)
