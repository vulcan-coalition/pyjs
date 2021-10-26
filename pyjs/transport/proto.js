window.server = (function() {


    const STRIP_COMMENTS = /((\/\/.*$)|(\/\*[\s\S]*?\*\/))/mg;
    const ARGUMENT_NAMES = /([^\s,]+)/g;

    function getParamNames(func) {
        var fnStr = func.toString().replace(STRIP_COMMENTS, '');
        var result = fnStr.slice(fnStr.indexOf('(') + 1, fnStr.indexOf(')')).match(ARGUMENT_NAMES);
        if (result === null)
            result = [];
        return result;
    }

    class Callback_parser {
        constructor(callback) {
            this.signature = getParamNames(callback);
            this.callback = callback;
        }
        invoke(data) {
            var params = [];
            for(const n of this.signature) params.push(data[n]);
            this.callback.apply(null, params);
        }
    }

    var ws = new WebSocket("ws://localhost:8000/ws");
    var server_callback = {};
    ws.onmessage = function(event) {
        var content = JSON.parse(event.data);
        var params = content["d"];
        var callbacks = server_callback[content["f"]];
        if (callbacks == null) {
            throw 'callback for server response "' + content["f"] + '" has not been registered.';
        }
        for (const cb of callbacks) cb.invoke(params);
    };

    function send(f, d) {
        ws.send(JSON.stringify({ "f": f, "d": d }));
    }

    return {
        "register_callbacks": function(name, callback) {
            if (server_callback[name] == null) server_callback[name] = [];
            server_callback[name].push(new Callback_parser(callback));
        },
        //<%functions>
    };
})()