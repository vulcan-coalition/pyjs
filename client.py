import bridge


@bridge.Client_interface
class Client:
    def f0(self, p0):
        pass

    def f1(self, p0: int, p1: str = "a", p2=None):
        pass


c = Client()

c.f0(1)
c.f1(1)
