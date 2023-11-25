'''
Phi - Programmation Heuristique Interface

analyser.py - Analyser for Phi
----------------
Author: Tanay Kar
----------------
'''

from pyrsistent import v
import constants as const

class SpecificAnalyser:
    def __init__(self,ast):
        self.ast = ast
        self.specicific_ast = []
        self.analyse()
        
    def analyse(self):
        for i in self.ast:
            match i.mastergrammar[0]:
                case 'A':
                    if i.mastergrammar == 'A01':
                        self.specicific_ast.append(const.AssignmentBlock(
                            variable=i.tokens[0],
                            value=i.tokens[2]
                            ))
                    elif i.mastergrammar == 'A02':
                        self.specicific_ast.append(const.EquationBlock(
                            name=i.tokens[0],
                            lhs=i.tokens[2],
                            rhs=i.tokens[4],
                            ))
                    else:
                        # Incase I add anymore grammer rules to 'A'
                        pass
                case 'B':
                    if i.mastergrammar in ('B01', 'B02','B03'):
                        self.specicific_ast.append(const.FunctionDeclarationBlock(
                            function=i.tokens[1],
                            commands=i.tokens[3],
                            mode='multiline',
                            ))
                    else:
                        self.specicific_ast.append(const.FunctionDeclarationBlock(
                            function=i.tokens[1],
                            mode='multiline',
                            ))
                case 'C':
                    self.specicific_ast.append(const.FunctionDeclarationBlock(
                        function=i.tokens[0],
                        commands=i.tokens[2],
                        mode='inline',
                        ))
                case 'D':
                    self.specicific_ast.append(const.PrintBlock(
                        expression=i.tokens[1],
                    ))
                case 'E':
                    self.specicific_ast.append(const.ReturnBlock(
                        expression=i.tokens[1],
                    ))
                case 'F':
                    self.specicific_ast.append(const.EndFuncBlock())
                case 'G':
                    if i.mastergrammar == 'G01':
                        self.specicific_ast.append(const.ShowTableBlock(
                            function=i.tokens[1],
                        ))
                    elif i.mastergrammar == 'G02':
                        self.specicific_ast.append(const.ShowTableBlock(
                            function=i.tokens[2],
                            num=i.tokens[1],
                        ))
                    else:
                        # Incase I add anymore grammer rules to 'G'
                        pass
                case 'H':
                    self.specicific_ast.append(const.PlotBlock(
                        function=i.tokens[1],
                    ))
                case 'I':
                    if i.mastergrammar == 'I01':
                        self.specicific_ast.append(const.SolveBlock(
                            function=i.tokens[1],
                        ))
                    elif i.mastergrammar == 'I02':
                        self.specicific_ast.append(const.EquationSolveBlock(
                            eq=i.tokens[1],
                            var=i.tokens[3],
                            ))
                    else:
                        # Incase I add anymore grammer rules to 'I'
                        pass
                    
                case 'J':
                    if i.mastergrammar == 'J01':
                        self.specicific_ast.append(const.IntegrateBlock(
                            function=i.tokens[1],
                            var=i.tokens[3],
                        ))
                    elif i.mastergrammar == 'J02':
                        self.specicific_ast.append(const.IntegrateBlock(
                            function=i.tokens[1],
                            var=i.tokens[3],
                            plot=True,
                        ))
                    elif i.mastergrammar == 'J03':
                        self.specicific_ast.append(const.IntegrateBlock(
                            function=i.tokens[1],
                            var=i.tokens[3],
                            limits=[i.tokens[5],i.tokens[7]],
                        ))
                    elif i.mastergrammar == 'J04':
                        self.specicific_ast.append(const.IntegrateBlock(
                            function=i.tokens[1],
                            var=i.tokens[3],
                            limits=[i.tokens[5],i.tokens[7]],
                            plot=True,
                        ))
                    else:
                        # Incase I add anymore grammer rules to 'J'
                        pass  



if __name__ == '__main__':
    from read import read_file
    ast = read_file('main.phi')
    analyser = SpecificAnalyser(ast)
    analyser.analyse()
    for i in analyser.specicific_ast:
        print(i)
        print()