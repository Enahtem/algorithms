numbers = [2,3,0,5,8,1,9]

for i in range(len(numbers)):
    value = numbers[i]
    j = i
    while j>0 and numbers[j-1]>value:
        numbers[j]=numbers[j-1]
        j-=1
    numbers[j] = value

print(numbers)

