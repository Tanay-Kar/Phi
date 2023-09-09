'''
Phi - Programmation Heuristique Interface

compiler.py - Compiler for Phi
----------------
Author: Tanay Kar
----------------
'''

from analyser import SpecificAnalyser
import header
from read import read_file
import typing

func_comp_type = typing.Literal['DCLR', 'CALL', 'FORM','NAME']


class Compiler:
    def __init__(self, file_name=None, ast=None, repr=False) -> None:
        if file_name:
            analyse = SpecificAnalyser(read_file(file_name))
            self.ast = analyse.specicific_ast
            self.block = False
        else:
            if ast:
                self.ast = ast
                self.block = True
            else:
                raise ValueError('Either file_name or ast must be provided')
        self.as_repr = repr
        self.precompiled_code = ''
        if not self.block:
            self.precompiled_code += header.header
            self.precompile_temp = file_name.split('.')[0] + '.phicache'
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
                case 'RETURN':
                    self.compile_return()
                case 'PLOT':
                    self.compile_plot()
            self.advance()
        if self.block:
            return self.precompiled_code
        with open(self.precompile_temp, 'w') as f:
            self.precompiled_code += header.footer
            f.write(self.precompiled_code)
        return self.precompile_temp

    def compile_plot(self):
        name = self.compile_function(self.current_line.function,'NAME')
        code = f'__plot__({name},\'{name}\')\n'
        self.precompiled_code += code
    
    def compile_return(self):
        expr = self.compile_expr(self.current_line.expression)
        code = f'return {expr}\n'
        self.precompiled_code += code
    
    def compile_print(self):
        expr = self.compile_expr(self.current_line.expression)
        code = f'\nprint({expr})\n'
        self.precompiled_code += code

    def compile_assignment(self):
        variable = self.current_line.variable.value
        value = self.compile_expr(self.current_line.value)
        code = f'{variable} = {value}\n'
        self.precompiled_code += code

    def compile_function_multiline(self):
        print('Multiline')
        function = self.current_line.function
        command = []
        print(function)
        self.advance()
        for j,i in enumerate(self.ast[self.line_no:]):
            if i.type == 'ENDFUNC':
                command_code = Compiler(ast=command).compile()
                command_code = '\t'+command_code.replace('\n','\n\t')
                code = f'''def {self.compile_function(function,"FORM")}:\n{command_code}'''
                print(code)
                self.precompiled_code += code
                return 

            else:
                print(i)
                command.append(i)
            self.advance()
        raise SyntaxError('Function not closed')

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
                arg_com = args[0][0].value
                return f'{name} = lambda {arg_com}'
            else:
                for i in args:
                    com = i.value
                    arg_com += com + ','
                return f'{name} = lambda {arg_com[:-1]}'

        elif type == 'CALL':
            arg_com = ''
            if len(args) == 1:
                arg_com = self.compile_expr(args[0][0])
                return f'{name}({arg_com})'
            else:
                for i in args:
                    com = self.compile_expr(i)
                    arg_com += com + ','
                return f'{name}({arg_com[:-1]})'
        
        elif type == 'FORM':
            arg_com = ''
            if len(args) == 1:
                arg_com = self.compile_expr(args[0][0])
                return f'{name}({arg_com})'
            else:
                for i in args:
                    com = self.compile_expr(i)
                    arg_com += com + ','
                return f'{name}({arg_com[:-1]})'
        elif type == 'NAME':
            return name

    def compile_expr(self, expr):
        match expr.type:
            case 'ID':
                return expr.value
            case 'FUNCTION':
                return self.compile_function(expr, 'CALL')
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
                l_com = self.compile_function(l.value, 'CALL')
            else:
                l_com = l.value.value

        if r.type == 'BINOP':
            r_com = self.compile_binop(r.left, r.operator, r.right)
        else:
            if r.value.type == 'FUNCTION':
                r_com = self.compile_function(r.value, 'CALL')
            else:
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
    import os
    
    compiler = Compiler(file_name='main.phi')
    cache = compiler.compile()
    os.system(f'python3 {cache}')