from fastapi import FastAPI

from .routers import surveys


app = FastAPI()

app.include_router(surveys.router)

@app.get("/")
async def read_root():
    return {"msg": "hello world!"}