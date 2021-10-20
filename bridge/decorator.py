import functools
import inspect
from .pillar import *


def read_signature(scope, func_name, func):
    fullargspec = inspect.getfullargspec(func)
    formatted_args = []

    defaults = [] if fullargspec.defaults is None else list(fullargspec.defaults)
    hints = {} if fullargspec.annotations is None else fullargspec.annotations

    for i in range(len(fullargspec.args) - len(defaults)):
        arg = fullargspec.args[i]
        formatted_args.append((arg, None if arg not in hints else hints[arg], None))
    for j, d in enumerate(defaults):
        arg = fullargspec.args[i + j + 1]
        formatted_args.append((arg, None if arg not in hints else hints[arg], d))

    return scope + "." + func_name, formatted_args


class Expose:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        expose_name, signature = read_signature(func.__module__, func.__name__, func)
        print(expose_name, signature)
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Interface:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        expose_name, signature = read_signature(func.__module__, func.__name__, func)
        print(expose_name, signature)
        self.name = expose_name
        self.func = func

    def __call__(self, *args, **kwargs):
        print("sending data..", self.name)


class Client_interface:
    def __init__(self, the_class):
        functools.update_wrapper(self, the_class)
        functions = inspect.getmembers(the_class, predicate=inspect.isfunction)
        for n, f in functions:
            setattr(the_class, n, Interface(f))
        self.the_class = the_class

    def __call__(self):
        return self.the_class
