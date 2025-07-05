from fastapi import FastAPI
from api import import_router  # Assuming you create an __init__.py in api to expose the router

app = FastAPI()

app.include_router(import_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"Hello": "World"}
