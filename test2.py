from sympy import symbols, integrate,oo
from sympy import sin

f = lambda x,y: x+y
y = symbols('y')
x = symbols('x')

print(integrate(f(x,y),(y,0,1))) 