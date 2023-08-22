'''
Phi - Programmation Heuristique Interface

constants.py - Contains all the constants and datatypes used in the program
----------------
Author: Tanay Kar
----------------
'''

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
}

# Token Class


class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value if value else type

    def __str__(self):
        return f"< Token {self.type} :: '{self.value}' >" if self.value else f'< Token {self.type} >'

    def __repr__(self):
        return self.__str__()


class TupleToken(Token):
    def __init__(self):
        super().__init__(type='TUPLE')
        self.variables = []
        self.values = []

    def add(self, token):
        if isinstance(token, Token):
            self.variables.append(str(token))
            self.values = self.variables

    def __str__(self):
        return f"< Tuple :: {' ,'.join(self.variables)} >"

class BinOpNode:
    def __init__(self, left, operator, right):
        self.type = "BINOP"
        self.left = left
        self.operator = operator
        self.right = right

    def __str__(self) -> str:
        return f"({self.left} {self.operator} {self.right})"

    def __repr__(self) -> str:
        return self.__str__()


class FactorNode:
    def __init__(self, value, sign='+'):
        self.type = "FACTOR"
        self.value = value if sign == '+' else '-' + value

    def __str__(self) -> str:
        return f"{self.value.value}"

    def __repr__(self) -> str:
        return self.__str__()


class ExpressionNode:
    def __init__(self, expression, type_hint=None):
        self.type = "EXPRESSION"
        self.expression = expression
        self.type_hint = type_hint # Used for a special case when the expression is a single number
        self.value = f"Expression {self.expression}"
        
    def __str__(self) -> str:
        return f"< Expression {self.expression}>"

    def __repr__(self) -> str:
        return self.__str__()


class DeclarationNode:
    def __init__(self, func: Token, args: TupleToken):
        self.type = "FUNCTION"
        self.function_name = func.value
        self.args = args
        self.value = f"Function {self.function_name} args {self.args.variables}"

    def __str__(self):
        return f"< Function {self.function_name} args {self.args.variables}>"

    def __repr__(self):
        return self.__str__()

class LineNode:
    def __init__(self, tokens:list, specid:str, primarykeyword:str, grammar:dict):
        self.type = "LINE"
        self.tokens = tokens
        self.grammar = grammar
        self.mastergrammar = specid
        self.primarykeyword = primarykeyword
        self.function = self.grammar[self.primarykeyword]['function']        
        
    
    def __str__(self) -> str:
        return f"[LINE grammar {self.mastergrammar[0]}:{self.mastergrammar[0:]} <Contents{self.tokens}>]"

    def __repr__(self) -> str:
        return self.__str__()