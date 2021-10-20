from jsmin import jsmin
import os

file_path = os.path.dirname(os.path.abspath(__file__))


def build_body(body_params):
    if len(body_params) == 1:
        return body_params[0]
    out = "{"
    for p in body_params:
        out = out + "\"" + p + "\":" + p + ","
    out = out + "}"
    out = out.replace(",}", "}")
    return out


def build_javascript(true_scope, gathered):
    function_list = ""
    for n, p, query_args, body_args in gathered:
        args_default = [a for a in (query_args + body_args)]
        queries = [a + "=\"+" + a + "+\"" for a in query_args]
        function_list = function_list + "\"" + n + "\": function(" + ",".join(args_default) + ") {" + "return makeRequest(\"/" + true_scope + p + "?" + "&".join(queries) + "\", \"POST\"," + build_body(body_args) + ")},"
    function_list = function_list + "\"version\": \"0.0.1\""
    with open(os.path.join(file_path, 'proto_vulcan.js')) as js_file:
        content = js_file.read()
        content = content.replace("<%app_prefix>", true_scope)
        content = content.replace("//<%functions>", function_list)
        minified = jsmin(content)
    return minified
