
from math import *
from matplotlib import pyplot as plt
from qbstyles import mpl_style
table_used = True
mpl_style(dark=True,minor_ticks=True)

plt.yscale('linear')
import numpy as np

f = lambda x: (sin(x)/x) 
# Creating vectors X and Y
x = np.linspace(-100, 100, 1000)
y = np.vectorize(f)(x)
 
fig = plt.figure(figsize = (10, 5))
# Create the plot
plt.plot(x, y)
    

if table_used:
    plt.axhline(y=0, color='grey')
    plt.axvline(x=0, color='grey')
    plt.show()
