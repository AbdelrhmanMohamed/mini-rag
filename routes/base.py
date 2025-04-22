from fastapi import APIRouter
import os
base_router = APIRouter()


@base_router.get("/", tags=["base2"])
def read_root():
    app_name = os.getenv("APP_NAME")
    return {"Hello": app_name}
