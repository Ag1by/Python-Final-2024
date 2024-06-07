from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models import blog


@asynccontextmanager
async def connect_to_mongodb(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://localhost")
    await init_beanie(database=client["SMIC"], document_models=[
        blog.Blogs
    ])
    print("INFO:     Connected to MongoDB")
    yield
    client.close()
    print("INFO:     Disconnected from MongoDB")
