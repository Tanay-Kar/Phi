'''
Phi - Programmation Heuristique Interface

read.py - Reads a file and prints the AST
----------------
Author: Tanay Kar
----------------
'''

from basic import Interpreter
from exceptions import ParseError

FILE_NAME = 'main.phi'
OUT_FILE_NAME = 'out.txt'

out = ''

with open(FILE_NAME, 'r') as f:
    lines = f.read()
    
lines = lines.split('\n')

for line in lines:
    if line == '': continue
    try:
        ast = Interpreter(line).ast()
        out += str(ast) + '\n'
        print(ast.tokens)
    except ParseError as e:
        print(e)
        
with open(OUT_FILE_NAME, 'w') as f:
    f.write(out)