
from math import *
import math
import sympy as sp
import numpy as np
import inspect
from matplotlib import pyplot as plt
from mpl_interactions import panhandler, zoom_factory
from ing_theme_matplotlib import mpl_style

table_used = False
mpl_style(dark=True,minor_ticks=True)

with plt.ioff() :
    fig, ax = plt.subplots()
    
def __plot__(func,name):
    global table_used
    table_used = True
    x = np.linspace(-10, 10, 200)
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
    
def ___create_namespace___():
    # This is just a helper function to create/destroy a namespace for sympy functions
    # In other words , this is just a tranquilizer for sympy's overly sensitive namespace
    # conflict. It encloses all the sympy dependent functions and forms a blanket namespace
    # for them.
    sympy_names = [name for name in dir(sp)]
    # Filter the list to include only the names also present in the math module
    joint_names = [name for name in sympy_names if hasattr(math, name)]
    # Import the matching SymPy names
    for name in joint_names:
        globals()[name] = getattr(sp, name) 
          
         
def ___solve___(func,func_name):
    print(sp.solve(func))
       
x = sp.symbols('x')

___create_namespace___()
___solve___(sin(x),'sin')
from math import *
print((3 + sin(8)))

if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.axis('auto')
    plt.grid(linestyle=':')
    plt.legend()
    disconnect_zoom = zoom_factory(ax)
    pan_handler = panhandler(fig)
    plt.show()
