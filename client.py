import pyjs


@pyjs.Client_interface
class Client:
    def f0(self, p0):
        'This is f0 function.'
        pass

    def f1(self, p0: int, p1: str = "a", p2=None):
        'This is f1 function.'
        pass
