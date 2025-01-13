numbers = [2,3,5,8,1,9]

for i in range(1,len(numbers)):
    val = numbers[i]
    for j in reversed(range(i)):
        numbers[j+1] = numbers[j]
        if (numbers[j]<=val):
            numbers[j+1]=val
            break
        elif (j==0):
            numbers[0]=val

print(numbers)
