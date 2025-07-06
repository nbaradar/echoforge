import logging
from fastapi import FastAPI
from api import import_routes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = FastAPI()

app.include_router(import_routes, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
