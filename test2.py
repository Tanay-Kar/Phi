from sympy import symbols, integrate,oo
from sympy import sin

f = lambda x: x**2
y = symbols('y')
x = symbols('x')

print(integrate(f(x),(x,f(0),f(1)))) 