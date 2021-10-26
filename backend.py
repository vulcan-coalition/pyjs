import bridge
import client


@bridge.Expose
def foo(client_obj, p0: int, p1: str = "a", p2=None):
    print("receiving..", p0, p1, p2)
    client_obj.f0("Hey!")


@bridge.Expose
def bar(client_obj, p0: int, p1: str = "a", p2=None):
    print("receiving..", p0, p1, p2)
    client_obj.f1(100)


# foo(1, 1)
# bridge.mock_incoming("__main__.foo", 1, p1="aa")
# bridge.mock_incoming("__main__.bar", 2, p1="bb")
