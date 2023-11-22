
from math import *
import math
import sympy as sp
import numpy as np
import inspect
from matplotlib import pyplot as plt
import matplotlib as mpl
from cycler import cycler
from mpl_interactions import panhandler, zoom_factory
from ing_theme_matplotlib import mpl_style

table_used = False
mpl_style(dark=False,minor_ticks=True)
mpl.rcParams['axes.prop_cycle'] = cycler('color', ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4'])

i = sp.I if False else 1j

with plt.ioff() :
    fig, ax = plt.subplots()
    
def __plot__(func,name):
    global table_used
    table_used = True
    x = np.linspace(-15, 15, 3000)
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
          
         
def ___solve___(func,func_name,func_str):
    roots = sp.solve(func)
    
    # Separate real and complex roots during iteration
    real_roots = []
    complex_roots = []

    for root in roots:
        if root.is_real:
            real_roots.append(root)
        else:
            complex_roots.append(root)

    # Print the results
    print(f'\nSolving {func_str} = {func}')
    
    if not roots:
        print('No solutions found')
    else:
        if real_roots:
            print("\nReal Roots:")
            for root in real_roots:
                print(f"x = {root:.2f}")

        if complex_roots:
            print("\nComplex Roots:")
            for root in complex_roots:
                real_part = sp.re(root)
                imag_part = sp.im(root)
                print(f"x = {real_part:.2f} + {imag_part:.2f}i")
       
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
    plt.yscale('linear')
    disconnect_zoom = zoom_factory(ax)
    pan_handler = panhandler(fig)
    if True:
        if True:
            plt.axis([-15, 15, -15, 15])
        else:
            plt.axis([0, 15, 0, 15])
    plt.show()
