import pyjs
import client


@pyjs.Expose
def foo(client_obj, p0: int, p1: str = "a", p2=None):
    'This is foo function.'
    print("receiving..", p0, p1, p2)
    client_obj.f0("Hey!")


@pyjs.Expose
def bar(client_obj, p0: int, p1: str = "a", p2=None):
    'This is bar function.'
    print("receiving..", p0, p1, p2)
    client_obj.f1(100)


if __name__ == '__main__':
    # foo(1, 1)
    pyjs.mock_incoming("__main__.foo", 1, p1="aa")
    pyjs.mock_incoming("__main__.bar", 2, p1="bb")

    print(pyjs.get_all_exposed_interfaces())
    print(pyjs.get_active_client_info())

    md_doc = pyjs.generate_md_api_doc()
    with open("README.md", "w") as file:
        file.write(md_doc)
