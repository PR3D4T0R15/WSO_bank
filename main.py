from fastapi import FastAPI

app = FastAPI()


@app.get("/bank")
async def get_info():
    pass


@app.post("/bank")
async def update_bank():
    pass
