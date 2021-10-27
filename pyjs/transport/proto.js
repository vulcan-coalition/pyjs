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
            for (const n of this.signature) params.push(data[n]);
            this.callback.apply(null, params);
        }
    }

    var server_callback = {};
    var ws = null;
    var saved_token = "";

    var url = (window.location.protocol == "https:"? "wss:":"ws:") + "//" + window.location.host + "/ws";
    function connect(token=null) {
        if(token != null) saved_token = token;
        ws = new WebSocket(url + "?token=" + saved_token);

        ws.onopen = function() {
            // subscribe to some channels
            // ws.send(JSON.stringify({}));
        };

        ws.onmessage = function(event) {
            var content = JSON.parse(event.data);
            var params = content["d"];
            var callbacks = server_callback[content["f"]];
            if (callbacks == null) {
                throw 'callback for server response "' + content["f"] + '" has not been registered.';
            }
            for (const cb of callbacks) cb.invoke(params);
        };

        ws.onclose = function(e) {
            console.log('Socket is closed. Reconnect will be attempted in 1 second.', e.reason);
            setTimeout(function() {
                connect();
            }, 1000);
        };

        ws.onerror = function(err) {
            console.error('Socket encountered error: ', err.message, 'Closing socket');
            ws.close();
            ws = null;
        };
    }

    function send(f, d) {
        if(ws == null) throw 'trouble connecting to the server';
        ws.send(JSON.stringify({ "f": f, "d": d }));
    }

    return {
        "initialize_connection": function(token) {
            connect(token);
        },
        "register_callbacks": function(name, callback) {
            if (server_callback[name] == null) server_callback[name] = [];
            server_callback[name].push(new Callback_parser(callback));
        },
        //<%functions>
    };
})()