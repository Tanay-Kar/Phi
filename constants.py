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
}

# Formal mode is for functions with 'FUNC' keyword , direct is for direct declaration without 'FUNC' keyword
FuncMode = typing.Literal['formal', 'direct']

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
        self.variables.append(str(token))
        self.values.append(token)

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
        # Used for a special case when the expression is a single number
        self.type_hint = type_hint
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
    def __init__(self, tokens: list, specid: str, primarykeyword: str, grammar: dict):
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


# Instruction Blocks

class AssignmentBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[Assignment Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class FunctionDeclarationBlock:
    def __init__(self, line, mode: FuncMode) -> None:
        self.line = line
        self.mode = mode
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[Assignment Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class PrintBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[Print Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class ReturnBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[Return Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class EndFuncBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[EndFunc Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class ShowTableBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[ShowTable Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()


class PlotBlock:
    def __init__(self, line) -> None:
        self.line = line
        self.extract()

    def extract(self):
        self.specid = self.line[0].mastergrammar

    def __str__(self) -> str:
        return f"[Plot Block {self.specid} \ncontent {self.line}]"

    def __repr__(self) -> str:
        return self.__str__()
