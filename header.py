'''
Phi - Programmation Heuristique Interface

header.py - Header text for compiled phi files
----------------
Author: Tanay Kar
----------------
'''

___plot_limit___ = 100 # Change this to change the plot domain
___resolution_factor___ = 10 # Change this to change the resolution of the plot
___graph_theme___ = 'dark' # Change this to change the theme of the plot
header = f'''
from math import *
from matplotlib import pyplot as plt
from qbstyles import mpl_style
table_used = False
mpl_style(dark={True if ___graph_theme___ == 'dark' else False},minor_ticks=True)

plt.yscale('linear')
def __plot__(func,name):
    table_used = True
    x = [i/{___resolution_factor___} for i in range({-___plot_limit___}, {___plot_limit___})]
    y = []
    for i in x:
        try:
            y.append(func(i))
        except ValueError:
            y.append(0)
    plt.legend([name])
    plt.plot(x, y)
    
'''


footer = '''
if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.show()
'''