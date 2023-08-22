'''
Phi - Programmation Heuristique Interface

shell.py - Contains the shell for Phi
----------------
Author: Tanay Kar
----------------
'''

from basic import Interpreter
from exceptions import ParseError


run = True

while run:
    line = input('>>> ')
    if line.lower() == 'q':
        if input('Are you sure you want to quit? (y/n) ').strip().lower() == 'y':
            print('Quitting...')
            break
    elif line == 'help':
        print('''
        Phi - Programmation Heuristique Interface

        Shell Commands:
        help - Displays this message
        exit - Exits the shell
        ''')
    else:
        try:
            print(Interpreter(line).ast())
        except ParseError as e:
            print(e)
        except Exception as e:
            print(e)