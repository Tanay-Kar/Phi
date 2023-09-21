import inspect

l = lambda x: x**2

def f(x):
    return x**3

def g(x):
    a = 8
    return x**a

def ___get_function___(func):
    if not callable(func):
        return None
    if isinstance(func, type(lambda:0)) and func.__name__ == (lambda:0).__name__:
        return inspect.getsource(func).split('\n')[0].split(':')[1].strip()
    else:
        commands = [i for i in inspect.getsource(func).split('\n') if i.strip()]
        if len(commands) == 2:
            return commands[1].strip().split('return')[1].strip()
        else:
            return None
    

print(___get_function___(l))
print(___get_function___(f))
print(___get_function___(g))