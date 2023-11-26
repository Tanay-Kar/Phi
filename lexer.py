'''
Phi - Programmation Heuristique Interface

lexer.py - Contains the lexer for Phi 
----------------
Author: Tanay Kar
----------------
'''
import re
from constants import *

# Lexer Class
class Lexer:
    def __init__(self, line) -> None:
        self.line = line
        self.pos = -1
        self.char = None
        self.token_corpus = []
        self.advance()

    def advance(self):
        # Advance the position pointer and set the current character
        if self.pos < len(self.line) - 1:
            self.pos += 1
            self.char = self.line[self.pos]

        else:
            self.char = None
            self.token_corpus.append(Token('EOL'))

    def peek(self):
        # Return the next character in the line
        return self.line[self.pos + 1] if self.pos < len(self.line) - 1 else 'EOL'

    def assert_char(self, char, tokentype):
        # Asserts if the character matches the token type
        if re.fullmatch(tokentype, char):
            return True
        else:
            return False

    def make_number(self):
        # Constructs a number token by matching it against the Number regex
        num = self.char
        next_char = self.peek()
        while self.assert_char(num+next_char, r_Num) and next_char != 'EOL':
            num += next_char
            self.advance()
            next_char = self.peek()

        return Token('NUMBER', num)

    def make_id(self):
        # Constructs an ID token by matching it against the ID regex
        if not self.assert_char(self.char, r_ID):
            return
        id = self.char
        next_char = self.peek()
        while self.assert_char(id+next_char, r_ID) and next_char != 'EOL':
            id += next_char
            self.advance()
            next_char = self.peek()

        if id in keywords:
            return Token(keywords[id])
        else:
            return Token('ID', id)

    def get_tokens(self):
        # Iterates through the line and constructs tokens corpus
        while self.char != None:
            if self.assert_char(self.char, r_Num):
                self.token_corpus.append(self.make_number())
            elif self.assert_char(self.char, r_ID):
                self.token_corpus.append(self.make_id())
            elif self.assert_char(self.char, r_lParen):
                self.token_corpus.append(Token('LPAREN'))
            elif self.assert_char(self.char, r_rParen):
                self.token_corpus.append(Token('RPAREN'))
            elif self.assert_char(self.char, r_Comma):
                self.token_corpus.append(Token('COMMA'))
            elif self.assert_char(self.char, r_Plus):
                self.token_corpus.append(Token('PLUS'))
            elif self.assert_char(self.char, r_Minus):
                self.token_corpus.append(Token('MINUS'))
            elif self.assert_char(self.char, r_Mult):
                self.token_corpus.append(Token('MULT'))
            elif self.assert_char(self.char, r_Div):
                self.token_corpus.append(Token('DIV'))
            elif self.assert_char(self.char, r_Dot):
                self.token_corpus.append(Token('DOT'))
            elif self.assert_char(self.char, r_Assign):
                self.token_corpus.append(Token('ASSIGN'))
            elif self.assert_char(self.char, r_Caret):
                self.token_corpus.append(Token('CARET'))
            elif self.assert_char(self.char, r_lBrace):
                self.token_corpus.append(Token('LBRACE'))
            elif self.assert_char(self.char, r_rBrace):
                self.token_corpus.append(Token('RBRACE'))
            elif self.assert_char(self.char, r_Colon):
                self.token_corpus.append(Token('COLON'))

            elif self.char == ' ':
                pass
            elif self.char == '\n':
                # EOL is for End of Line Token
                self.token_corpus.append(Token('EOL'))
            else:
                raise Exception(f'Invalid Character: {self.char}')
            self.advance()
        return self.token_corpus
    
if __name__ == '__main__':
    lexer = Lexer('a = 1+b')
    print(lexer.get_tokens())