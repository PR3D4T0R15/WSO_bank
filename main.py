from fastapi import FastAPI, Request, Response
from fun import DataUpdate
import json

app = FastAPI()


@app.get("/ping")
async def pingPong(request: Request):
    bankAuth = request.headers.get("Authorization")

    if bankAuth != "test":
        return Response(json.dumps({"error": "bad machine"}), status_code=401, media_type="application/json")
    else:
        return Response(json.dumps({"ping": "pong"}), status_code=200, media_type="application/json")


@app.post("/login")
async def loginLogin(request: Request):
    pass


@app.delete("/login")
async def loginLogout(request: Request):
    pass


@app.put("/login")
async def loginRegister(request: Request):
    pass


@app.get("/account")
async def accountBalance(request: Request):
    pass

@app.post("/account")
async def accountUpdate(request: Request):
    pass