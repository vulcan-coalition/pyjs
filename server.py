from fastapi import FastAPI, Depends, HTTPException, Form, Request, Body, Response
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import backend
import bridge

app = FastAPI()

bridge.initialize(use_websocket_transport=True, params=app)

pyjs = bridge.build_javascript()


@app.get("/py.js")
async def get_pyjs():
    return Response(content=pyjs, media_type="text/javascript")

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
         <script src="py.js"></script>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var messages = document.getElementById('messages');
            server.register_callbacks("f0", function(p0){
                var message = document.createElement('li');
                message.appendChild(document.createTextNode(p0));
                messages.appendChild(message)
            });
            function sendMessage(event) {
                event.preventDefault()
                var input = document.getElementById("messageText");
                server.backend.foo(input.value);
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get_index():
    # response = RedirectResponse("/index.html")
    # response.status_code = 302
    # return response
    return HTMLResponse(html)

app.mount("/", StaticFiles(directory="frontend"), name="frontend")


@app.on_event("startup")
async def startup_event():
    bridge.start_listener()


@app.on_event("shutdown")
def shutdown_event():
    bridge.stop_listener()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info")
