from helpers.config import get_settings, Settings
from fastapi import APIRouter, Depends
base_router = APIRouter()


@base_router.get("/", tags=["base2"])
async def read_root(app_settings: Settings = Depends(get_settings)):
    return {
        "app_name": app_settings.APP_NAME,
        "app_version": app_settings.APP_VERSION
    }
