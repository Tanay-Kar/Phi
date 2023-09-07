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

func_comp_type = typing.Literal['DCLR', 'CALL']


class Compiler:
    def __init__(self, file, repr=False) -> None:
        analyse = SpecificAnalyser(read_file(file))
        self.ast = analyse.specicific_ast   
            
        self.precompiled_code = "from math import *\n"
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
                    if self.current_line.mode == 'multiline':
                        self.compile_function_multiline()
                    else:
                        self.compile_function_inline()
                case 'PRINT':
                    self.compile_print()
            self.advance()

        with open(self.precompile_temp, 'w') as f:
            f.write(self.precompiled_code)
    
    def compile_print(self):
        expr = self.compile_expr(self.current_line.expression)
        code = f'print({expr})'
        self.precompiled_code += code
        

    def compile_assignment(self):
        variable = self.current_line.variable.value
        value = self.compile_expr(self.current_line.value)
        code = f'{variable} = {value}\n'
        self.precompiled_code += code

    def compile_function_multiline(self):
        ...
    
    def compile_function_inline(self):
        function = self.current_line.function
        command = self.current_line.commands
        code = f'{self.compile_function(function,"DCLR")}: {self.compile_expr(command)}\n'
        self.precompiled_code += code

    def compile_function(self, func, type: func_comp_type):
        name = func.function_name
        args = func.args.values
        # Tuple check
        if type == 'DCLR':
            if len(args) == 1:
                if args[0][0].type != 'ID':
                    raise TypeError(f'Expected ID, got {args[0][0].type}')
                print(name)
                return str(name + ' = lambda ' + args[0][0].value)

            # Ensure all args are of type 'ID'
            for i in args:
                if i.type != 'ID':
                    raise TypeError(f'Expected ID, got {i.type}')

            # Ensure all args are unique
            seen = {}

            for element in enumerate([i.value for i in args]):
                if element in seen:
                    if seen[element] == 1:
                        raise ValueError(
                            f'Argument {element} is already defined')
                    seen[element] += 1
                else:
                    seen[element] = 1
            arg_com = ''
            if len(args) == 1:
                print(args[0])
                arg_com = args[0][0].value
                return f'{name} = lambda {arg_com}'
            else:
                for i in args:
                    com = i.value
                    arg_com += com + ','       
                return f'{name} = lambda {arg_com[:-1]}'
                    
        elif type == 'CALL':
            print(func)
            arg_com = ''
            if len(args) == 1:
                print('ARG : ',self.compile_expr(args[0][0]))
                arg_com = self.compile_expr(args[0][0])
                return f'{name}({arg_com})'
            else:
                for i in args:
                    com = self.compile_expr(i)
                    arg_com += com + ','
                return f'{name}({arg_com[:-1]})'


    def compile_expr(self, expr):
        print(expr)
        match expr.type:
            case 'ID':
                return expr.value
            case 'FUNCTION':
                print('Function')
                return self.compile_function(expr,'CALL')
            case 'EXPRESSION':
                if expr.type_hint == 'NUM':
                    return expr.expression

                return self.compile_binop(expr.expression.left, expr.expression.operator, expr.expression.right)

    def compile_binop(self, l, op, r):
        if r == None:
            raise ValueError('Right side of expression cannot be None')
        
        if l.type == 'BINOP':
            l_com = self.compile_binop(l.left, l.operator, l.right)
        else:
            if l.value.type == 'FUNCTION':
                l_com = self.compile_function(l.value,'CALL')
            else:
                print('Else',l.value.type,l.value.value)
                l_com = l.value.value
    
            
        if r.type == 'BINOP':
            r_com = self.compile_binop(r.left, r.operator, r.right)
        else:
            if r.value.type == 'FUNCTION':
                r_com = self.compile_function(r.value,'CALL')
            else:
                print('Else',r.value.type,r.value.value)
                r_com = r.value.value

        match op:
            case 'PLUS':
                return f'({l_com} + {r_com})'
            case 'MINUS':
                return f'({l_com} - {r_com})'
            case 'MULT':
                return f'({l_com} * {r_com})'
            case 'DIV':
                return f'({l_com} / {r_com})'
            case 'CARET':
                return f'({l_com} ** {r_com})'


if __name__ == '__main__':
    compiler = Compiler('main.phi')
    compiler.compile()
