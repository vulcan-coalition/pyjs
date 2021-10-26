import bridge


@bridge.WithContext
def abc(context, p0, p1):
    print(context, p0, p1)


@bridge.Expose
def foo(client, p0: int, p1: str = "a", p2=None):
    pass


abc(1, 2)
