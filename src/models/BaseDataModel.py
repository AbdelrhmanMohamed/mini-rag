from helpers.config import get_settings
from motor.motor_asyncio import AsyncIOMotorCollection


class BaseDataModel:
    def __init__(self, db_client=AsyncIOMotorCollection):
        self.db_client = db_client
        self.settings = get_settings()
