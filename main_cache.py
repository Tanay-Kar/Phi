
from math import *
import math
import sympy as sp
import numpy as np
import inspect
from matplotlib import pyplot as plt
import matplotlib as mpl
from cycler import cycler
from mpl_interactions import panhandler, zoom_factory
try:
    from ing_theme_matplotlib import mpl_style
except ImportError:
    from qbstyles import mpl_style



mpl_style(dark=True,minor_ticks=False)
mpl.rcParams['axes.prop_cycle'] = cycler('color', ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf','#1f77b4'])

with plt.ioff() :
    fig, ax = plt.subplots()
    
table_used = False

i = sp.I if False else 1j
    
def __plot__(func,name,integration=False,integration_limits=[0,0]):
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
    if integration:
        if integration_limits == "calculated":
            integration_limits = [min(x),max(x)]
        plt.fill_between(x, y, where=((x>integration_limits[0]) & (x<integration_limits[1])), alpha=0.5)

def __create_namespace__():
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
          
         
def __solve__(func,func_name,func_str):
    
    print(f'\nSolving {func_str} = {func} ...')

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

def __integrate__(func,func_name,func_str,var,indefinite=True,integration_limits=[0,0]):
    print(f'\nIntegrating {func_str} = {func} with respect to {var} ...')
    var = sp.Symbol(var)
    if indefinite:
        func_integral = sp.integrate(func,var)
        print(f'\nIntegral of {func_str} = {func_integral}')
    else:
        func_integral = sp.integrate(func,(var,integration_limits[0],integration_limits[1]))
        print(f'\nIntegral of {func_str} from {integration_limits[0]} to {integration_limits[1]} = {func_integral}')

def __eqsolve__(eq_set,var_set): 
    print(f'\nSolving {len(eq_set)} equation{"s" if len(eq_set)>1 else ""} for {var_set} ...')
    for i in eq_set:
        print(i.lhs,'=',i.rhs)
    roots = sp.solve(eq_set,var_set,dict=True)
    if not roots:
        print('No solutions found')
        return
    print('\nSolution set:')
    if type(roots) == dict:
        for i in roots:
            print(f'{i} = {roots[i]}',end=' , ')
    
    elif type(roots) == list and len(roots) == 1:
        for i in roots[0]:
            print(f'{i} = {roots[0][i]}',end=' , ')
            
        print()
    else:
        for i in roots:
            for j in i:
                print(f'{j} = {i[j]}',sep=' , ')
            print()


def add(x,y):
	
	a = (x + y)
	
	return 0

print(add(1,2))

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
