from fastapi import FastAPI, Request, Response
from fun import DataUpdate
import json

app = FastAPI()


@app.get("/bank")
async def get_info(request: Request):
    bankAuth = request.headers.get("Authorization")

    if bankAuth != "test":
        return Response(json.dumps({"error": "bad machine"}), status_code=401, media_type="application/json")

    body = await request.json()
    cardId = body["auth"]["cardId"]
    pin = body["auth"]["pin"]

    database = DataUpdate()

    if not database.checkId(cardId, pin):
        del database
        return Response(json.dumps({"error": "bad pin or card"}), status_code=401, media_type="application/json")

    response_body = database.getAccountInfo(cardId)

    del database
    return Response(response_body, status_code=200, media_type="application/json")


@app.put("/bank")
async def update_bank(request: Request):
    bankAuth = request.headers.get("Authorization")

    if bankAuth != "test":
        return Response(json.dumps({"error": "bad machine"}), status_code=401, media_type="application/json")

    body = await request.json()
    opType = body["type"]
    cardId = body["auth"]["cardId"]
    value = body["value"]

    database = DataUpdate()

    database.updateBalance(cardId, value, opType)

    return {"status": 200}
