from fastapi import FastAPI, Depends, HTTPException, Form, Request, Body, Response
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import bridge

app = FastAPI()

pyjs = bridge.compile()


@app.get("/py.js")
async def get_pyjs():
    return Response(content=pyjs, media_type="text/javascript")


@app.get("/")
async def get_index():
    response = RedirectResponse("/index.html")
    response.status_code = 302
    return response


app.mount("/", StaticFiles(directory="frontend"), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info")
