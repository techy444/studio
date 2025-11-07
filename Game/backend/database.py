import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "codeduel_arena")

logger = logging.getLogger(__name__)

# Create MongoDB client
try:
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    
    # Collections
    users_collection = db["users"]
    battles_collection = db["battles"]
    
    # Create indexes (idempotent)
    users_collection.create_index("email", unique=True)
    users_collection.create_index("username", unique=True)
    battles_collection.create_index("battle_id", unique=True)
    
    logger.info("✓ Connected to MongoDB at %s", MONGO_URL)
    logger.info("✓ Using database: %s", MONGO_DB_NAME)
except Exception as e:
    logger.exception("✗ Failed to connect to MongoDB: %s", e)
    raise