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
        return self.tokens[self.index+1] if self.index+1 < len(self.tokens) else None

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
            return FactorNode(right, sign='-')

        elif self.current_token.type == 'EXPRESSION':
            value = self.current_token.expression
            self.advance()
            return value
        
        # Handle opening parenthesis "("
        elif self.current_token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            if self.current_token.type == 'COMMA':
                pass  # Ensure closing parenthesis ")"
            elif self.current_token.type == 'RPAREN':  # Ensure closing parenthesis ")"
                self.advance()
                return expr
            else:
                raise SyntaxError("Missing closing parenthesis")


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
            ep = ExpressionParser(self.tokens[self.index-1:])
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
        self.current_token = tokens[0]
        self.tuple = TupleToken
        self.index = -1
        self.item_corpus = []
        self.advance()

    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = Token('EOL')

    def couplet(self, items, stindex):
        return items[stindex], items[stindex+1]

    def assert_type(self, token, type, enforceable=False, alt_type=None):
        if token.type not in (type, alt_type):
            if enforceable:
                raise Exception('Expected token type ' +
                                type + ' but got ' + token.type)
            else:
                return False
        else:
            return True

    def parse_item(self, items_arg):
        tupletok = TupleToken()
        index = 0
        items = ExpressionParserWrapper(items_arg+[Token('EOL','EOL')]).parse()
        #items = items_arg
        items.pop(-1)
        print(items)
        # check if the list is empty
        if len(items) == 0:
            return tupletok
        # check if the list has only one item
        elif len(items) == 1:
            if self.assert_type(items[0], 'ID') or self.assert_type(items[0], 'EXPRESSION'):
                print('Single item')
                tupletok.add(items)
                return tupletok
            

        # check if the list has the format of a tuple
        id, sep = self.couplet(items, 0)
        if (self.assert_type(id, 'ID') or self.assert_type(id, 'NUMBER')) and self.assert_type(sep, 'COMMA'):
            tupletok.add(id)
            index += 1
            while index < len(items):
                sep, id = self.couplet(items, index)
                self.assert_type(sep, 'COMMA', enforceable=True)
                self.assert_type(id, 'ID', enforceable=True, alt_type='NUMBER')
                tupletok.add(id)
                index += 2

            return tupletok
        else:
            pass  # I have no idea what this block does either 🤷‍♂️

            
    def replace(self, st, end, new_item):
        self.tokens[st:end] = [new_item]
        self.index = st

    def parse(self):
        t_items = []
        while self.index < len(self.tokens):
            if self.current_token.type == 'LPAREN':
                st = self.index
                while self.current_token.type != 'RPAREN' and self.current_token.type != 'EOL':
                    t_items.append(self.current_token)
                    self.advance()
                if self.tokens[self.index].type == 'RPAREN':
                    t_items.pop(0)
                    end = self.index + 1
                    self.replace(st, end, self.parse_item(t_items))

                    t_items = []

                elif self.tokens[self.index].type == 'EOL':
                    raise ParseError('Missing closing parenthesis')

            self.advance()

        self.index = -1
        self.parse_declarations()
        self.index = -1
        self.reverse_expr_parse()
        return self.tokens

    def parse_declarations(self):
        while self.index < len(self.tokens):
            if self.current_token and self.current_token.type == 'ID' and self.index + 1 < len(self.tokens) and self.tokens[self.index+1].type == 'TUPLE':
                self.replace(self.index, self.index+2,
                             DeclarationNode(self.current_token, self.tokens[self.index+1]))

            self.advance()
    
    def reverse_expr_parse(self):
        while self.index < len(self.tokens):
            if self.current_token.type == 'TUPLE' and len(self.current_token.variables) == 1:
                self.tokens[self.index] = self.current_token.values[0][0]
            self.advance()
        


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
                                f'Unexpected {self.tokens[i].type} \'{self.tokens[i].value}\'')
                        raise ParseError(
                            f'Expected {self.get_item(i,self.applicable_rules[0])} but recieved {self.tokens[i].type} \'{self.tokens[i].value}\'')
                else:
                    raise ParseError(
                        f'Unexpected {self.tokens[i].type} \'{self.tokens[i].value}\'')

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
    
    lexer = Lexer('f(x,y) = sqrt(x*y)^x + 2*(x+y)')
    tokens = lexer.get_tokens()
    with open('grammar.json', 'r') as f:
        grammar = json.load(f)
    parser = MasterParser(tokens, grammar)
    print(parser.parse())
    '''lexer = Lexer('x+y,x')
    tokens = lexer.get_tokens()
    epw = ExpressionParserWrapper(tokens)
    print(epw.parse())'''