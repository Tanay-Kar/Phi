'''
Phi - Programmation Heuristique Interface

exceptions.py - Contains all the exceptions used in the program
----------------
Author: Tanay Kar
----------------
'''

import colorama

class Error(Exception):
    """Base class for exceptions in this module."""
    def __init__(self, msg):
        self.msg = msg
        super().__init__(colorama.Fore.RED+self.msg+colorama.Style.RESET_ALL)


class ParseError(Error):
    """Exception raised for errors in the input.
    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = 'PARSING ERROR : ' + msg
        super().__init__(self.msg)