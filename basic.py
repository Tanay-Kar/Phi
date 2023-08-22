'''
Phi - Programmation Heuristique Interface

basic.py - Streamlines the process of executing Phi
----------------
Author: Tanay Kar
----------------
'''

from lexer import Lexer
from parsers import MasterParser
import json


class Interpreter:
    def __init__(self,line,grammer_path='grammar.json') -> None:
        self.line = line
        self.grammer_path = grammer_path
        with open(self.grammer_path,'r') as f:
            self.grammer = json.load(f)
        
        self.tokens = Lexer(self.line).get_tokens()
        self.parser = MasterParser(self.tokens,self.grammer)
        self.parsed = self.parser.parse()
        
    def ast(self):
        return self.parsed