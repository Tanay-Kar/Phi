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

def read_file(path,outpath='log.txt',verbose=False) -> None:
    path = path
    outpath = outpath
    ast_list = []
    out = ''
    log = lambda *args: print(*args) if verbose else None
    
    with open(path, 'r') as f:
        lines = f.read()
        
    lines = lines.split('\n')
    for line in lines:
        if line == '': continue
        try:
            ast = Interpreter(line).ast()
            out += str(ast) + '\n'
            ast_list.append(ast)
            log(ast)
        except ParseError as e:
            raise e
            
    with open(outpath, 'w') as f:
        f.write(out)
    return ast_list
            

            
if __name__ == '__main__':
    rd = read_file(FILE_NAME,OUT_FILE_NAME)
    print()
    print(rd)