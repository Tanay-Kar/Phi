"""
Phi - Programmation Heuristique Interface

compiler.py - Compiler for Phi
----------------
Author: Tanay Kar
----------------
"""

from pyparsing import alphanums
from analyser import SpecificAnalyser
import header
from read import read_file
import typing

func_comp_type = typing.Literal["DCLR", "CALL", "FORM", "NAME", "ARGS"]


class Compiler:
    """Compiler class which compiles the ast/file to a python equivalent

    It iteratively goes through the ast, (or the file) and goes through each line(blocks)
    and sends them to their respective parsing functions . The resultant sum of python equivalents,
    along with a special header-footer combination is then written to a file, which is then executed.
    The header-footer combination is used to import the necessary libraries and functions, and to
    create a namespace for the variables.

    Parameters
    ----------
    file_name : str, optional
        The name of the file to be compiled, by default None
    ast : list, optional
        The ast to be compiled, by default None (Either the file name or the ast must be provided)
    repr : bool, optional
        Whether to print log or not, by default False
        This is not implemented yet

    Methods
    -------
    compile()
        If the ast is passed , returns a string of the compiled code,
        If the file name is passed, returns the name of the compiled file

    """

    def __init__(self, file_name=None, ast=None, repr=False) -> None:
        """Initialises the compiler class
        Assigns ast from argument or by analysing the file from the file_name
        The self.block variable is used to check whether the ast is provided or not and
        is used in several places. Primarily , it is there to ensure a smooth operation
        in the scenario of a REPR type console input where the output must be spontaneous
        and doesn't require the header-footer combo again and again

        """
        if file_name:
            analyse = SpecificAnalyser(read_file(file_name))
            self.ast = analyse.specicific_ast
            self.block = False
        else:
            if ast:
                self.ast = ast
                self.block = True
            else:
                raise ValueError("Either file_name or ast must be provided")
        # TODO: Add repr support
        self.as_repr = repr
        self.precompiled_code = ""
        if not self.block:
            self.precompiled_code += header.header
            self.precompile_temp = file_name.split(".")[0] + "_cache.py"
        self.line_no = -1
        self.current_line = None
        self.advance()

    def advance(self):
        while self.line_no + 1 < len(self.ast):
            self.line_no += 1
            self.current_line = self.ast[self.line_no]
            break
        else:
            self.current_line = None

    def compile(self):
        """Assigns the current line to the respective parsing function"""
        while self.current_line:
            match self.current_line.type:
                case "ASSIGN":
                    self.compile_assignment()
                case "FUNCDCLR":
                    if self.current_line.mode == "multiline":
                        self.compile_function_multiline()
                    else:
                        self.compile_function_inline()
                case "PRINT":
                    self.compile_print()
                case "RETURN":
                    self.compile_return()
                case "PLOT":
                    self.compile_plot()
                case "SHWTBL":
                    self.compile_showtable()
                case "SOLVE":
                    self.compile_solve()
                case "INTEGRATE":
                    self.compile_integrate()
            self.advance()
        if self.block:
            return self.precompiled_code
        with open(self.precompile_temp, "w") as f:
            self.precompiled_code += header.footer
            f.write(self.precompiled_code)
        return self.precompile_temp

    def compile_integrate(self):
        """Compiles the integrate command"""
        func = self.compile_function(self.current_line.function, "CALL")
        name = self.compile_function(self.current_line.function, "NAME")
        var = self.compile_expr(self.current_line.var)
        arg_def = f"{var} = sp.Symbol('{var}')\n"
        if self.current_line.definite:
            limits = [self.compile_expr(i) for i in self.current_line.limits]
        else:
            limits = None
            
        if self.current_line.to_plot:
            plot_code = f"__plot__({name},'{func}',integration=True,{'integration_limits=[%s,%s]'%(limits[0],limits[1]) if limits else 'integration_limits=calculated'})"
            
        code = f"{plot_code}\n{arg_def}\n__create_namespace__()\n__integrate__({func},'{name}','{func}','{var}',{'indefinite=True' if not limits else 'indefinite=False,integration_limits=[%s,%s]'%(limits[0],limits[1])})\n\nfrom math import *\n"
        
        self.precompiled_code += code

    def compile_solve(self):
        """Compiles the solve command"""

        _ = self.compile_function(self.current_line.function, "DCLR") # Ensures that the function has single variable(s) as arguments
        name = self.compile_function(self.current_line.function, "NAME")
        args = self.compile_function(self.current_line.function, "ARGS")
        if len(args) == 0:
            raise TypeError("Cannot solve function with no arguments")
        elif len(args) == 1:
            args = list(args[0][0].value)
        else:
            args = [i.value for i in args]
        arg_def = ""
        for i in args:
            arg_def += f"{i} = sp.symbols('{i}')\n"

        func_call = f'{name}({",".join(args)})'
        code = f"{arg_def}\n__create_namespace__()\n__solve__({func_call},'{name}','{func_call}')\nfrom math import *\n"
        self.precompiled_code += code

    def compile_showtable(self):
        """Compiles the showtable command"""

        raise NotImplementedError("Show Table not implemented yet")

    def compile_plot(self):
        """Compiles the plot command"""

        name = self.compile_function(self.current_line.function, "NAME")
        call = self.compile_function(self.current_line.function, "CALL")
        code = f"__plot__({name},{call})\n"
        self.precompiled_code += code

    def compile_return(self):
        """Compiles the return command"""

        expr = self.compile_expr(self.current_line.expression)
        code = f"return {expr}\n"
        self.precompiled_code += code

    def compile_print(self):
        """Compiles the print command"""

        expr = self.compile_expr(self.current_line.expression)
        code = f"\nprint({expr})\n"
        self.precompiled_code += code

    def compile_assignment(self):
        """Compiles the assignment command"""

        variable = self.current_line.variable.value
        value = self.compile_expr(self.current_line.value)
        code = f"{variable} = {value}\n"
        self.precompiled_code += code

    def compile_function_multiline(self):
        """Compiles the multiline function"""

        function = self.current_line.function
        command = []
        self.advance()
        for j, i in enumerate(self.ast[self.line_no :]):
            if i.type == "ENDFUNC":
                command_code = Compiler(ast=command).compile()
                command_code = "\t" + command_code.replace("\n", "\n\t")
                code = f"""def {self.compile_function(function,"CALL")}:\n{command_code}\n"""
                self.precompiled_code += code
                return

            else:
                command.append(i)
            self.advance()
        raise SyntaxError("Function not closed")

    def compile_function_inline(self):
        """Compiles the inline function"""

        function = self.current_line.function
        command = self.current_line.commands
        code = (
            f'{self.compile_function(function,"DCLR")}: {self.compile_expr(command)}\n'
        )
        self.precompiled_code += code

    def compile_function(self, func, type: func_comp_type):
        """Actual function compiler, forms root for the other function-compilers"""

        name = func.function_name
        args = func.args.values
        # Tuple check
        if type == "DCLR":
            if len(args) == 1:
                if args[0][0].type != "ID":
                    raise TypeError(f"Expected ID, got {args[0][0].type}")
                return str(name + " = lambda " + args[0][0].value)

            # Ensure all args are of type 'ID'
            for i in args:
                if i.type != "ID":
                    raise TypeError(f"{self.current_line} \nExpected ID, got {i.type}")

            # Ensure all args are unique
            seen = {}

            for element in enumerate([i.value for i in args]):
                if element in seen:
                    if seen[element] == 1:
                        raise ValueError(f"Argument {element} is already defined")
                    seen[element] += 1
                else:
                    seen[element] = 1
            arg_com = ""
            if len(args) == 1:
                arg_com = args[0][0].value
                return f"{name} = lambda {arg_com}"
            else:
                for i in args:
                    com = i.value
                    arg_com += com + ","
                return f"{name} = lambda {arg_com[:-1]}"

        elif type == "CALL":
            arg_com = ""
            if len(args) == 1:
                arg_com = self.compile_expr(args[0][0])
                return f"{name}({arg_com})"
            else:
                for i in args:
                    com = self.compile_expr(i)
                    arg_com += com + ","
                return f"{name}({arg_com[:-1]})"
            
        elif type == "NAME":
            return name
        elif type == "ARGS":
            return args

    def compile_expr(self, expr):
        """Compiles an expression"""

        match expr.type:
            case "ID":
                return expr.value
            case "FUNCTION":
                return self.compile_function(expr, "CALL")
            case "EXPRESSION":
                if expr.type_hint == "NUM":
                    return expr.expression

                return self.compile_binop(
                    expr.expression.left,
                    expr.expression.operator,
                    expr.expression.right,
                )

    def compile_binop(self, l, op, r):
        """Compiles a binary operation"""

        if r == None:
            raise ValueError("Right side of expression cannot be None")

        if l.type == "BINOP":
            l_com = self.compile_binop(l.left, l.operator, l.right)
        else:
            if l.value.type == "FUNCTION":
                l_com = self.compile_function(l.value, "CALL")
            else:
                if l.sign == "-":
                    l_com = f"-{l.value.value}"
                else:
                    l_com = l.value.value

        if r.type == "BINOP":
            r_com = self.compile_binop(r.left, r.operator, r.right)
        else:
            if r.value.type == "FUNCTION":
                r_com = self.compile_function(r.value, "CALL")
            else:
                if r.sign == "-":
                    r_com = f"-{r.value.value}"
                else:
                    r_com = r.value.value

        match op:
            case "PLUS":
                return f"({l_com} + {r_com})"
            case "MINUS":
                return f"({l_com} - {r_com})"
            case "MULT":
                return f"({l_com} * {r_com})"
            case "DIV":
                return f"({l_com} / {r_com})"
            case "CARET":
                return f"({l_com} ** {r_com})"


if __name__ == "__main__":
    import os

    compiler = Compiler(file_name="main.phi")
    cache = compiler.compile()
    os.system(f"python3 {cache}")
