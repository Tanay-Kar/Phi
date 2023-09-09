'''
Phi - Programmation Heuristique Interface

header.py - Header text for compiled phi files
----------------
Author: Tanay Kar
----------------
'''

___plot_limit___ = 100 # Change this to change the plot domain
___resolution_factor___ = 10 # Change this to change the resolution of the plot

header = f'''
from math import *
from matplotlib import pyplot as plt

def __plot__(func,name):
    x = [i/{___resolution_factor___} for i in range({-___plot_limit___}, {___plot_limit___})]
    y = [func(i) for i in x]
    plt.plot(x, y)
    plt.legend([name])
    plt.title('Function Plot')
    


'''

footer = '''
plt.show()
'''