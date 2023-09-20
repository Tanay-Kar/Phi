'''
Phi - Programmation Heuristique Interface

header.py - Header text for compiled phi files
----------------
Author: Tanay Kar
----------------
'''

___plot_limit___ =  1.5# Change this to change the plot domain
___resolution_factor___ = 10 # Change this to change the resolution of the plot
___graph_theme___ = 'dark3' # Change this to change the theme of the plot

header = f'''
from math import *
import numpy as np
from matplotlib import pyplot as plt
from qbstyles import mpl_style

table_used = False
mpl_style(dark={True if ___graph_theme___ == 'dark' else False},minor_ticks=True)

    
def __plot__(func,name):
    global table_used
    table_used = True
    x = np.linspace({-___plot_limit___}, {___plot_limit___}, {round(2*___plot_limit___*___resolution_factor___)})
    try:
        y = np.vectorize(func)(x)
        
    except Exception as e:
        y = np.empty_like(x)
        
        # Calculate the function values and handle points outside the domain
        for i, x_val in enumerate(x):
            try:
                y[i] = func(x_val)
            except Exception as e:
                y[i] = np.nan
    plt.plot(x, y,label=name)
    
    
'''


footer = '''
if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.axis('auto')
    plt.grid(linestyle=':')
    plt.legend()
    plt.show()
'''

