import inspect


exposed_functions = {}


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


def register_function(func):
    expose_name, signature = read_signature(func.__module__, func.__name__, func)
    print(expose_name, signature)
    exposed_functions[expose_name] = func


Client_class = None


def register_client(client_class):
    global Client_class
    Client_class = client_class


def get_active_client_class():
    return Client_class


def client_in_call(client, function_name, args, kwargs):
    exposed_functions[function_name](client, *args, **kwargs)


def mock_incoming(*args, **kwargs):
    function_name = args[0]
    exposed_functions[function_name](Client_class("mock_id"), *args[1:], **kwargs)
