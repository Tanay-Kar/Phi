'''
Phi - Programmation Heuristique Interface

analyser.py - Analyser for Phi
----------------
Author: Tanay Kar
----------------
'''

from constants import *

class SpecificAnalyser:
    def __init__(self,ast):
        self.ast = ast

    def analyse(self):
        for i in self.ast:
            print(i)
            
if __name__ == '__main__':
    from read import read_file
    read_file('main.phi')