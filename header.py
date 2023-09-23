'''
Phi - Programmation Heuristique Interface

header.py - Header text for compiled phi files
----------------
Author: Tanay Kar
----------------
'''

___plot_limit___ = 15 # Change this to change the plot domain
___resolution_factor___ = 100 # Change this to change the resolution of the plot
___graph_theme_dark___ = True # Change this to change the theme of the plot
___bidirectional___ = True # Change this to chose whether to plot the function in negative domain or not
___y_scale___ = 'linear' # Change this to change the y scale of the plot
___equiscaled___ = True # Change this to make the plot scaled equally in both axes
___define_iota___ = False # Change this to define iota as a constant
header = f'''
from math import *
import math
import sympy as sp
import numpy as np
import inspect
from matplotlib import pyplot as plt
from mpl_interactions import panhandler, zoom_factory
from ing_theme_matplotlib import mpl_style

table_used = False
mpl_style(dark={___graph_theme_dark___},minor_ticks=True)

i = sp.I if {___define_iota___} else 1j

with plt.ioff() :
    fig, ax = plt.subplots()
    
def __plot__(func,name):
    global table_used
    table_used = True
    x = np.linspace({-___plot_limit___ if ___bidirectional___ else 0}, {___plot_limit___}, {round(2*___plot_limit___*___resolution_factor___)})
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
    print(f'\\nSolving {{func_str}} = {{func}}')
    
    if not roots:
        print('No solutions found')
    else:
        if real_roots:
            print("\\nReal Roots:")
            for root in real_roots:
                print(f"x = {{root:.2f}}")

        if complex_roots:
            print("\\nComplex Roots:")
            for root in complex_roots:
                real_part = sp.re(root)
                imag_part = sp.im(root)
                print(f"x = {{real_part:.2f}} + {{imag_part:.2f}}i")
       
'''


footer = f'''
if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.axis('auto')
    plt.grid(linestyle=':')
    plt.legend()
    plt.yscale(\'{___y_scale___}\')
    disconnect_zoom = zoom_factory(ax)
    pan_handler = panhandler(fig)
    if {___equiscaled___}:
        if {___bidirectional___}:
            plt.axis([{-___plot_limit___}, {___plot_limit___}, {-___plot_limit___}, {___plot_limit___}])
        else:
            plt.axis([0, {___plot_limit___}, 0, {___plot_limit___}])
    plt.show()
'''

