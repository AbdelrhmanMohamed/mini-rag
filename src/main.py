from routes import base, data
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from helpers.config import get_settings
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Setup: Create a MongoDB connection
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGO_URI)
    app.db_client = app.mongo_conn[settings.MONGO_DB]

    yield  # FastAPI will handle the app lifecycle during this point

    # Cleanup: Close the MongoDB connection when the app shuts down
    app.mongo_conn.close()


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
