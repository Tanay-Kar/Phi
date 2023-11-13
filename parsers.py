'''
Phi - Programmation Heuristique Interface

parsers.py - Contains the various parsers for Phi
----------------
Author: Tanay Kar
----------------
'''

from constants import *
from exceptions import *


class ExpressionParser:
    def __init__(self, tokens):
        self.master_tokens = tokens
        self.tokens = tokens
        self.current_token: Token = None
        self.index = -1
        self.startindex, self.endindex = 0, 0
        self.advance()

    def advance(self):
        while self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
            if self.current_token.type != 'EOL':
                break

    def peek(self):
        return self.tokens[self.index + 1] if self.index + 1 < len(self.tokens) else None

    def return_slice(self):
        return self.startindex, self.endindex

    def parse(self):
        self.startindex = self.index - 1
        parsed = self.parse_expression()
        self.endindex = self.index - 1

        if getattr(parsed, 'type', None) is not None and parsed.type == "FACTOR":
            if parsed.value.type in ('ID', 'FUNCTION'):
                parsed = parsed.value
                return parsed
            if parsed.value.type == 'NUMBER':
                parsed = parsed.value.value
                return ExpressionNode(parsed, type_hint='NUM')

        elif not parsed:
            return parsed
        return ExpressionNode(parsed)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = BinOpNode(left, op, right)
        return left

    def parse_term(self):
        left = self.parse_radical()
        while self.current_token.type in ('MULT', 'DIV', 'DOT'):
            op = self.current_token.type if self.current_token.type not in (
                'DOT') else 'MULT'
            self.advance()
            right = self.parse_radical()
            left = BinOpNode(left, op, right)

        return left

    def parse_radical(self):
        left = self.parse_factor()
        while self.current_token.type == 'CARET':
            op = self.current_token.type
            self.advance()
            right = self.parse_factor()
            left = BinOpNode(left, op, right)

        return left

    def parse_factor(self):
        if self.current_token.type == 'NUMBER':
            value = self.current_token
            self.advance()
            if self.current_token.type == 'ID' or self.current_token.type == 'FUNCTION':
                var = self.current_token
                self.advance()
                return BinOpNode(FactorNode(value), 'MULT', FactorNode(var))
            elif self.current_token.type == 'EXPRESSION':
                var = self.current_token
                self.advance()
                return BinOpNode(FactorNode(value), 'MULT', var.expression)
            return FactorNode(value)

        elif self.current_token.type == 'ID':
            value = self.current_token
            self.advance()
            return FactorNode(value)

        elif self.current_token.type == 'FUNCTION':
            value = self.current_token
            self.advance()
            return FactorNode(value)

        elif self.current_token.type == 'MINUS':  # Unary negation handling
            self.advance()
            right = self.parse_factor()
            if self.current_token.type == 'ID' or self.current_token.type == 'FUNCTION':
                var = self.current_token
                self.advance()
                return BinOpNode(FactorNode(value, sign='-'), 'MULT', FactorNode(var))
            elif self.current_token.type == 'EXPRESSION':
                var = self.current_token
                self.advance()
                return BinOpNode(FactorNode(value, sign='-'), 'MULT', var.expression)
            return FactorNode(right, sign='-')

        elif self.current_token.type == 'EXPRESSION':
            value = self.current_token.expression
            self.advance()
            if self.current_token.type == 'ID' or self.current_token.type == 'FUNCTION':
                var = self.current_token
                self.advance()
                return BinOpNode(value, 'MULT', FactorNode(var))
            elif self.current_token.type == 'EXPRESSION':
                var = self.current_token
                self.advance()
                return BinOpNode(value, 'MULT', var.expression)
            return value

        # Handle opening parenthesis "("
        elif self.current_token.type == 'TUPLE':
            print('TUPLE DETECTED ___________________________', self.current_token.variables)
            vars = self.current_token.variables
            vars.append(Token('EOL'))
            print(ExpressionParserWrapper(vars).parse()[:-1])
            self.advance()
            return ExpressionParserWrapper(vars).parse()[0]


class ExpressionParserWrapper:
    def __init__(self, tokens):
        self.index = -1
        self.tokens = tokens
        self.current_token: Token = None

        self.advance()

    def advance(self):
        while self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
            if self.current_token.type != "EOL":
                break

    def return_tokens(self):
        return self.tokens

    def parse(self):
        while self.current_token.type != "EOL":
            ep = ExpressionParser(self.tokens[self.index - 1:])
            pr = ep.parse()
            sl1, sl0 = [i + self.index - 1 for i in ep.return_slice()]
            if pr:
                self.tokens[sl1:sl0] = [pr]
                self.index = sl1 + 1
            self.advance()
        return self.return_tokens()


class TupleParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        tokens = self.parse_depth(tokens)
        tokens = self.format_tuples(tokens,_first=True)
        self.tokens = self.parse_function(tokens)
        

    def push(self, obj, l: list, depth):
        while depth:
            l = l[-1]
            depth -= 1

        l.append(obj)

    def parse_depth(self, s):
        groups = []
        depth = 0

        try:
            for char in s:
                if char.type == 'LPAREN':
                    self.push([], groups, depth)
                    depth += 1
                elif char.type == 'RPAREN':
                    depth -= 1
                else:
                    self.push(char, groups, depth)

        except IndexError:
            raise ValueError('Parentheses mismatch')

        if depth > 0:
            raise ValueError('Parentheses mismatch')
        else:
            return groups

    def parse_function(self, tokens):
        for i, e in enumerate(tokens):
            if e.type == 'ID' and i < len(tokens) - 1 and tokens[i + 1].type == 'TUPLE':
                tokens[i] = DeclarationNode(e, tokens[i + 1])
                tokens.pop(i + 1)
        return tokens

    def format_tuples(self, tokens,_first=False):
        for i, item in enumerate(tokens):
            if isinstance(item, list):
                tokens[i] = self.format_tuples(item)
        
        if not _first:
            return TupleToken(tokens)
        return tokens

    def parse(self):
        return self.tokens

class MasterParser:
    def __init__(self, tokens, grammar: dict):
        self.tokens = tokens
        self.prepare()
        self.grammar_raw = grammar
        self.master_lexeme = None
        self.applicable_rules = []
        self.absolute_rule = None
        self.index = -1
        self.current_token: Token = None
        self.enforce_grammar = False
        self.advance()

    def prepare(self):
        tok = TupleParser(self.tokens).parse()
        tok = ExpressionParserWrapper(tok).parse()
        self.tokens = tok

    def reset_index(self):
        self.index = -1
        self.current_token: Token = None
        self.advance()

    def advance(self):
        while self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
            self.index += 1
            if self.current_token.type != "EOL":
                break

    def get_master_rule(self):
        first_token_type = self.current_token.type
        self.primary_keyword = first_token_type
        if first_token_type in self.grammar_raw:
            self.master_lexeme = first_token_type
            self.applicable_rules = [self.grammar_raw[first_token_type]['syntax'][i]['syntax'].split()
                                     for i in self.grammar_raw[first_token_type]['syntax']
                                     ]
            self.rule_ids = [self.grammar_raw[first_token_type]['syntax'][i]['spec_id']
                             for i in self.grammar_raw[first_token_type]['syntax']
                             ]

    def get_item(self, index, list):
        if index < len(list):
            return list[index]
        else:
            return None

    def grammer_match(self):
        for i in range(len(self.tokens)):
            self.enforce_grammar = True if len(
                self.applicable_rules) == 1 else False
            rules, rules_id = [], []

            if self.enforce_grammar:
                if self.get_item(i, self.applicable_rules[0]) != None:
                    if self.get_item(i, self.applicable_rules[0]) == self.tokens[i].type or self.get_item(i, self.applicable_rules[0]) == getattr(self.tokens[i], 'type_hint', None):
                        pass
                    else:
                        if self.get_item(i, self.applicable_rules[0]) == 'EOL':
                            raise ParseError(
                                f'{self.tokens} \nUnexpected {self.tokens[i].type} \'{self.tokens[i].value}\'')
                        raise ParseError(
                            f'{self.tokens} \nExpected {self.get_item(i,self.applicable_rules[0])} but recieved {self.tokens[i].type} \'{self.tokens[i].value}\'')
                else:
                    raise ParseError(
                        f'{self.tokens} \nUnexpected {self.tokens[i].type} \'{self.tokens[i].value}\'')

            else:
                for j in range(len(self.applicable_rules)):
                    rule = self.applicable_rules[j]
                    id = self.rule_ids[j]
                    if self.get_item(i, rule) == self.tokens[i].type or self.get_item(i, rule) == getattr(self.tokens[i], 'type_hint', None):
                        rules.append(rule)
                        rules_id.append(id)
                self.applicable_rules = rules
                self.rule_ids = rules_id
        if len(self.applicable_rules) != 1:
            raise ParseError(f'Syntax Error')
        elif len(self.applicable_rules) == 1:
            self.absolute_rule = self.applicable_rules[0]
            self.absolute_rule_id = self.rule_ids[0]

    def parse(self):
        self.get_master_rule()
        self.grammer_match()
        line = LineNode(self.tokens, self.absolute_rule_id,
                        self.primary_keyword, self.grammar_raw)
        return line


if __name__ == '__main__':
    from lexer import Lexer
    import json

    lexer = Lexer('a = b + f(x)')
    tokens = lexer.get_tokens()
    # tok = [i for i in tokens]
    # print(tokens)
    # tp = TupleParser(tok).parse()
    # print(tp)

    with open('grammar.json', 'r') as f:
        grammar = json.load(f)
    parser = MasterParser(tokens, grammar)
    print(parser.parse())
    '''lexer = Lexer('c-1')
    tokens = lexer.get_tokens()
    print(tokens)
    epw = ExpressionParserWrapper(tokens)
    print(epw.parse())'''
