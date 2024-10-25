
from motor.motor_asyncio import AsyncIOMotorClient

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    DB_NAME: str = "school_blog"

settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.DB_NAME]
blog_collection = database.get_collection("blogs")
