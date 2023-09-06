'''
Phi - Programmation Heuristique Interface

compiler.py - Compiler for Phi
----------------
Author: Tanay Kar
----------------
'''

from analyser import SpecificAnalyser
from read import read_file
import typing

func_comp_type = typing.Literal['DCLR','CALL']

class Compiler:
    def __init__(self,file,repr=False) -> None:
        analyse = SpecificAnalyser(read_file(file))
        self.ast = analyse.specicific_ast
        self.precompiled_code = ''
        self.as_repr = repr
        self.precompile_temp = file.split('.')[0] + '.phicache'
        self.line_no = -1
        self.current_line = None
        self.advance()
    
    def advance(self):
        while self.line_no + 1 < len(self.ast):
            self.line_no += 1
            self.current_line = self.ast[self.line_no]
            break
        else:
            self.current_line = None
        
        
    def compile(self):
        while self.current_line:
            match self.current_line.type:
                case 'ASSIGN':
                    self.compile_assignment()
                case 'FUNCDCLR':
                    self.compile_function_direct()
            self.advance()
        
        with open(self.precompile_temp,'w') as f:
            f.write(self.precompiled_code)
    
    def compile_assignment(self):
        variable = self.current_line.variable.value
        value = self.current_line.value
        code = f'{variable} = {value}\n'
        self.precompiled_code += code
        
    def compile_function_direct(self):
        function = self.current_line.function
        command = self.current_line.commands
        args = function.args.values
        code = f'{self.compile_function(function,"DCLR")}:{command}\n'
        self.precompiled_code += code
    
    def compile_function(self,func,type:func_comp_type):
        name = func.function_name
        args = func.args.values
        # Tuple check
        if type == 'DCLR':
            if len(args) == 1:
                if args[0][0].type != 'ID':
                    raise TypeError(f'Expected ID, got {args[0][0].type}')
                
                print('Tuple len 1',args[0][0])
                return str(name + ' = lambda ' + args[0][0].value)   
            
            # Ensure all args are of type 'ID'
            for i in args:
                if i.type != 'ID':
                    raise TypeError(f'Expected ID, got {i.type}')
            
             
            # Ensure all args are unique
            seen = {}
    
            for index, element in enumerate([i.value for i in args]):
                if element in seen:
                    if seen[element] == 1:
                        raise ValueError(f'Argument {element} is already defined')
                    seen[element] += 1
                else:
                    seen[element] = 1
        elif type == 'CALL':
                ...
            
        print(args)
        return str(name + ' = ' + ','.join([i.value for i in args]))
        
    def compile_tuple(self):
        ...
    
    def compile_expr(self):
        ...
    
                

if __name__ == '__main__':
    compiler = Compiler('main.phi')
    compiler.compile()
        