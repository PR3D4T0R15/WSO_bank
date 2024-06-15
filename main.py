from fastapi import FastAPI, Request, Response
from fun import checkAuthString, RaspBank
import json

app = FastAPI()


@app.get("/ping")
async def pingPong(request: Request):
    bankAuth = request.headers.get("Authorization")

    if checkAuthString(bankAuth):
        return Response(json.dumps({"ping": "pong"}), status_code=200, media_type="application/json")
    else:
        return Response(json.dumps({"error": "bad machine"}), status_code=401, media_type="application/json")


@app.post("/login")
async def loginLogin(request: Request):
    requestBody = await request.body()

    bank = RaspBank(requestBody)
    result = bank.loginUser()

    return Response(result, status_code=200, media_type="application/json")

@app.delete("/login")
async def loginLogout(request: Request):
    requestBody = await request.body()

    bank = RaspBank(requestBody)
    result = bank.logoutUser()

    return Response(result, status_code=200, media_type="application/json")


@app.put("/login")
async def loginRegister(request: Request):
    pass


@app.get("/account")
async def accountBalance(request: Request):
    pass

@app.post("/account")
async def accountOperation(request: Request):
    pass

