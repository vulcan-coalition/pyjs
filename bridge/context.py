import functools
from .pillar import *


class WithContext:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(7, *args, **kwargs)
