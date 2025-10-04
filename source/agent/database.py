import os
import logging
import motor.motor_asyncio
from beanie import init_beanie
from models import Task

logger = logging.getLogger(__name__)


async def init_db():
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    logger.info("Connecting to MongoDB at %s", mongodb_uri)
    client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
    await init_beanie(database=client.todo_db, document_models=[Task])