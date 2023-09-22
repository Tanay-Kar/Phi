import time

# Split the selection into individual lines
lines = ["from math import *", "import math", "from sympy import solve,im,re", "import numpy as np", "from matplotlib import pyplot as plt", "from mpl_interactions import panhandler, zoom_factory", "from ing_theme_matplotlib import mpl_style"]

# Loop through each line and measure the time taken
for line in lines:
    start_time = time.time()
    exec(line)
    end_time = time.time()
    print(f"Time taken for '{line}': {end_time - start_time} seconds")