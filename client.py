import bridge


@bridge.Client_interface
class Client:
    def f0(self, p0):
        pass

    def f1(self, p0: int, p1: str = "a", p2=None):
        pass


ab = Client("ab")

ab.f0(1)
ab.f1(1)


cd = Client("cd")

cd.f0(1)
cd.f1(1)
