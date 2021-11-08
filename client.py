import pyjs


@pyjs.Client_interface
class Client:
    def incoming_message(self, p0):
        'This is the incoming_message function.'
        pass

    def another(self, p0: int, p1: str = "a", p2=None):
        'This is another function.'
        pass
