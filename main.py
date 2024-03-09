from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/bank")
async def get_info(request: Request):
    pass


@app.put("/bank")
async def update_bank(request: Request):
    pass
