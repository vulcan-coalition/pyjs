import pyjs
import client


all_clients = set()


@pyjs.Expose
def broadcast(client_obj, message: str, p1: int = 0, p2=None):
    'This is the broadcast function.'
    print("receiving..", message, p1, p2)
    all_clients.add(client_obj)
    for c in all_clients:
        res = c.incoming_message(str(client_obj.client_id) + " : " + message)
        print(res)


@pyjs.Expose
def another(client_obj, p0: int, p1: str = "a", p2=None):
    'This is another function.'
    print("receiving..", p0, p1, p2)
    client_obj.another(100)


if __name__ == '__main__':
    # foo(1, 1)
    pyjs.mock_incoming("__main__.broadcast", "aa")
    pyjs.mock_incoming("__main__.another", 2, p1="bb")

    print(pyjs.get_all_exposed_interfaces())
    print(pyjs.get_active_client_info())

    md_doc = pyjs.generate_md_api_doc()
    with open("README.md", "w") as file:
        file.write(md_doc)
