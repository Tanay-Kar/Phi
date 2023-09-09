
from math import *
from matplotlib import pyplot as plt

def __plot__(func,name):
    x = [i/10 for i in range(-100, 100, 1)]
    y = [func(i) for i in x]
    plt.plot(x, y)
    plt.legend([name])
    plt.title('Plot of function "' + name + '"')


__plot__(sin,'sin')
__plot__(cos,'cos')

plt.show()