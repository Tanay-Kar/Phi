import time
a = time.time()
from math import *
b = time.time()
import math
c = time.time()
import sympy as sp
d = time.time()
import numpy as np
e = time.time()
import inspect
f = time.time()
from matplotlib import pyplot as plt
g = time.time()
import matplotlib as mpl
h = time.time()
from cycler import cycler
i = time.time()
from mpl_interactions import panhandler, zoom_factory
j = time.time()
from ing_theme_matplotlib import mpl_style
k = time.time()
from itertools import cycle
l = time.time()

print(f'from math import *: {b-a:.5f}')
print(f'import math: {c-b:.5f}')
print(f'import sympy as sp: {d-c:.5f}')
print(f'import numpy as np: {e-d:.5f}')
print(f'import inspect: {f-e:.5f}')
print(f'from matplotlib import pyplot as plt: {g-f:.5f}')
print(f'import matplotlib as mpl: {h-g:.5f}')
print(f'from cycler import cycler: {i-h:.5f}')
print(f'from mpl_interactions import panhandler, zoom_factory: {j-i:.5f}')
print(f'from ing_theme_matplotlib import mpl_style: {k-j:.5f}')
print(f'from itertools import cycle: {l-k:.5f}')
print(f'Total time: {l-a:.5f}')
