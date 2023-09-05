'''
Phi - Programmation Heuristique Interface

compiler.py - Compiler for Phi
----------------
Author: Tanay Kar
----------------
'''
from analyser import SpecificAnalyser
from read import read_file

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
        print(self.precompile_temp)
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
        code = f'{function.function_name} = lambda {args}:{command}\n'
        self.precompiled_code += code
        
    def compile_tuple():
        ...
    
    def compile_expr():
        ...
    
                

if __name__ == '__main__':
    compiler = Compiler('main.phi')
    compiler.compile()
        