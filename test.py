import math
import random


#f: function, x0, x1, N: num points
def data_generation(f, x0, x1, N):
    x = [x0+(x1-x0)/(N-1)*x for x in range(N)]
    return [[x,f(x)] for x in x]


### GENERATING SAMPLE DATA
#x: input
def f(x):
    return math.sin(x)
x0 = 0
x1 = math.pi
N = 100

print(data_generation(f, x0, x1, N))

### ADD BAYESIAN STUFF HERE
