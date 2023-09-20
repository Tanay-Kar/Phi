
from math import *
import numpy as np
from matplotlib import pyplot as plt
from qbstyles import mpl_style

table_used = False
mpl_style(dark=False,minor_ticks=True)

    
def __plot__(func,name):
    global table_used
    table_used = True
    x = np.linspace(-1.5, 1.5, 30)
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
    
    
f = lambda x: x
__plot__(sin,'sin')
__plot__(cos,'cos')
__plot__(f,'f')

if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.axis('auto')
    plt.grid(linestyle=':')
    plt.legend()
    plt.show()
