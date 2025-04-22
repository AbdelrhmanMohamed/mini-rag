from routes import base
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv(".env")


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(base.base_router)
