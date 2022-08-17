window.server = (function() {

    const STRIP_COMMENTS = /((\/\/.*$)|(\/\*[\s\S]*?\*\/))/mg;
    const ARGUMENT_NAMES = /([^\s,]+)/g;

    function getParamNames(func) {
        const fnStr = func.toString().replace(STRIP_COMMENTS, '');
        let result = fnStr.slice(fnStr.indexOf('(') + 1, fnStr.indexOf(')')).match(ARGUMENT_NAMES);
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
            const params = [];
            for (const n of this.signature) params.push(data[n]);
            this.callback.apply(null, params);
        }
    }

    const on_error_callbacks = [];
    const on_close_callbacks = [];
    const server_callback = {};
    let ws = null;
    let saved_token = "";

    var url = (window.location.protocol == "https:"? "wss:":"ws:") + "//" + window.location.host + "/ws";
    function connect(token=null) {
        if(token != null) saved_token = token;
        ws = new WebSocket(url + "?token=" + saved_token);

        ws.onopen = function() {
            // subscribe to some channels
            // ws.send(JSON.stringify({}));
        };

        ws.onmessage = function(event) {
            const content = JSON.parse(event.data);
            const params = content["d"];
            const callbacks = server_callback[content["f"]];
            if (callbacks == null) {
                throw 'callback for server response "' + content["f"] + '" has not been registered.';
            }
            for (const cb of callbacks) cb.invoke(params);
        };

        ws.onclose = function(e) {
            console.log('Socket is closed.', e.reason);
            for(const on_close of on_close_callbacks) on_close();
        };

        ws.onerror = function(err) {
            console.error('Socket encountered error: ', err.message);
            for(const on_error of on_error_callbacks) on_error();
        };
    }

    function available() {
        return ws != null && ws.readyState === WebSocket.OPEN;
    }

    function send(f, d) {
        if(!available()) {
            throw 'trouble connecting to the server';
        }
        ws.send(JSON.stringify({ "f": f, "d": d }));
    }

    return {
        "initialize_connection": function(token) {
            connect(token);
        },
        "available": available,
        "register_on_close": function(callback) {
            on_close_callbacks.push(callback);
        },
        "register_on_error": function(callback) {
            on_error_callbacks.push(callback);
        },
        "register_callbacks": function(name, callback) {
            if (server_callback[name] == null) server_callback[name] = [];
            server_callback[name].push(new Callback_parser(callback));
        },
        //<%functions>
    };
})()