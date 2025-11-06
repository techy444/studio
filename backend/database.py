from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "codeduel_arena")

# Create MongoDB client
try:
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB_NAME]
    
    # Collections
    users_collection = db["users"]
    battles_collection = db["battles"]
    
    # Create indexes
    users_collection.create_index("email", unique=True)
    users_collection.create_index("username", unique=True)
    battles_collection.create_index("battle_id", unique=True)
    
    print(f"✓ Connected to MongoDB at {MONGO_URL}")
    print(f"✓ Using database: {MONGO_DB_NAME}")
except Exception as e:
    print(f"✗ Failed to connect to MongoDB: {e}")
    raise