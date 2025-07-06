from fastapi import FastAPI
from api import import_routes

app = FastAPI()

app.include_router(import_routes, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
