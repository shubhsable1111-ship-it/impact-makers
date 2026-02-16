from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
import os

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "credit_risk_db"

# Global MongoDB client
client = None
database = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL, server_api=ServerApi('1'))
    database = client[DATABASE_NAME]
    print("Connected to MongoDB")


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return database
