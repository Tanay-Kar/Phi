'''
Phi - Programmation Heuristique Interface

constants.py - Contains all the constants and datatypes used in the program
----------------
Author: Tanay Kar
----------------
'''

import typing

r_ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
r_Num = r'(\d+)\.?(\d+)*'
r_Assign = r'='
r_Comma = r'\,'
r_Plus = r'\+'
r_Minus = r'-'
r_Mult = r'\*'
r_Div = r'/'
r_Dot = r'\.'
r_Caret = r'\^'
r_lParen = r'\('
r_rParen = r'\)'
r_lBrace = r'\{'
r_rBrace = r'\}'

# Keywords
keywords = {
    'func': 'FUNC',
    'print': 'PRINT',
    'show': 'SHWTBL',
    'return': 'RETURN',
    'plot': 'PLT',
    'solve': 'SOLVE',
    'integrate': 'INTG',
    'wrt': 'WRT',
    'from': 'FROM',
    'to': 'TO',
}

# multiline definitions end with '{' and inline definitions are self-contained
FuncMode = typing.Literal['multiline', 'inline']

# Tokens

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value if value else type
        if self.type == 'ID' or self.type == 'NUMBER':
            self.base_type = 'VARIABLE'
    def __str__(self):
        return f"< Token {self.type} :: '{self.value}' >" if self.value else f"< Token {self.type} >"

    def __repr__(self):
        return self.__str__()


class TupleToken(Token):
    def __init__(self):
        super().__init__(type='TUPLE')
        self.variables = []
        self.values = []

    def add(self, token):
        self.variables.append(str(token))
        self.values.append(token)

    def __str__(self):
        return f"< Tuple :: {' ,'.join(self.variables)} >"

# Nodes

class BinOpNode:
    def __init__(self, left, operator, right):
        self.type = 'BINOP'
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f'({self.left} {self.operator} {self.right})'

    def __repr__(self) -> str:
        return self.__str__()


class FactorNode:
    def __init__(self, value, sign='+'):
        self.type = 'FACTOR'
        if sign == '-':
            self.value = value.value
        else:
            self.value = value
        self.sign = sign

    def __str__(self) -> str:
        return f'<FACTOR {self.value} sign={self.sign}>'

    def __repr__(self) -> str:
        return self.__str__()


class ExpressionNode:
    def __init__(self, expression, type_hint=None):
        self.type = 'EXPRESSION'
        self.base_type = 'VARIABLE'
        self.expression = expression
        # Used for a special case when the expression is a single number
        self.type_hint = type_hint
        self.value = self.expression

    def __str__(self) -> str:
        return f'< Expression {self.expression}>'

    def __repr__(self) -> str:
        return self.__str__()


class DeclarationNode:
    def __init__(self, func: Token, args: TupleToken):
        self.type = 'FUNCTION'
        self.base_type = 'VARIABLE'
        self.function_name = func.value
        self.args = args
        self.value = self.function_name,self.args.values

    def __str__(self):
        return f'< Function {self.function_name} args {self.args.variables}>'

    def __repr__(self):
        return self.__str__()


class LineNode:
    def __init__(self, tokens: list, specid: str, primarykeyword: str, grammar: dict):
        self.type = 'LINE'
        self.tokens = tokens
        self.grammar = grammar
        self.mastergrammar = specid
        self.primarykeyword = primarykeyword
        self.function = self.grammar[self.primarykeyword]['function']

    def __str__(self) -> str:
        return f'[LINE grammar {self.mastergrammar[0]}:{self.mastergrammar[0:]} <Contents{self.tokens}>]'

    def __repr__(self) -> str:
        return self.__str__()


# Instruction Blocks

class AssignmentBlock:
    def __init__(self, variable, value) -> None:
        self.type = 'ASSIGN'
        self.variable = variable
        self.value = value

    def __str__(self) -> str:
        return f'[Assignment Block {self.variable} = {self.value}]'

    def __repr__(self) -> str:
        return self.__str__()
    
class FunctionDeclarationBlock:
    def __init__(self,function,mode:FuncMode,commands=None) -> None:
        self.type = 'FUNCDCLR'
        self.function = function
        self.mode = mode
        self.commands = commands if commands else []
    
    def __str__(self) -> str:
        return f"[Function Declaration Block {self.function}{self.commands if self.commands else ''}]"
    
    def __repr__(self) -> str:
        return self.__str__()
    
class PrintBlock:
    def __init__(self,expression) -> None:
        self.type = 'PRINT'
        self.expression = expression
        
    def __str__(self) -> str:
        return f'[Print Block {self.expression}]'

    def __repr__(self) -> str:
        return self.__str__()
    
class ReturnBlock:
    def __init__(self,expression) -> None:
        self.type = 'RETURN'
        self.expression = expression
    
    def __str__(self) -> str:
        return f'[Return Block {self.expression}]'

    def __repr__(self) -> str:
        return self.__str__()

class EndFuncBlock:
    def __init__(self) -> None:
        self.type = 'ENDFUNC'
        pass

    def __str(self) -> str:
        return f'[EndFunc Block]'
    
    def __repr__(self) -> str:
        return self.__str__()
    
class ShowTableBlock:
    def __init__(self,function,num=None) -> None:
        self.type = 'SHWTBL'
        self.function = function
        self.num = num
        
    def __str__(self) -> str:
        return f"[ShowTable Block {self.function} {self.num if self.num else ''}]"
    
    def __repr__(self) -> str:
        return self.__str__()

class SolveBlock:
    def __init__(self,function) -> None:
        self.type = 'SOLVE'
        self.function = function
        
    def __str__(self) -> str:
        return f'[Solve Block {self.function}]'
    
    def __repr__(self) -> str:
        return self.__str__()

class PlotBlock:
    def __init__(self,function) -> None:
        self.type = 'PLOT'
        self.function = function
    
    def __str__(self) -> str:
        return f'[Plot Block {self.function}]'

    def __repr__(self) -> str:
        return self.__str__()
    
class IntegrateBlock:
    def __init__(self,function,var,limits=None,plot=False) -> None:
        self.type = 'INTEGRATE'
        self.function = function
        self.var = var
        self.to_plot = plot
        self.limits = limits
        if limits:
            self.definite = True
        else:
            self.definite = False
        
    def __str__(self) -> str:
        return f"[Integrate Block {self.function} {self.limits if self.definite else ''}]"
    
    def __repr__(self) -> str:
        return self.__str__()