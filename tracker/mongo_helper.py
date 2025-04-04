import os
import pymongo
from dotenv import load_dotenv

# Load MongoDB credentials from .env file
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")

# Initialize MongoDB connection
client = pymongo.MongoClient(MONGO_URI)
db = client["test"]
collection = db["desk_usage"]

def save_session_to_mongo(session_data):
    """ Save the study session to MongoDB """
    try:
        if collection is None:  # ✅ Fix: Properly check if collection exists
            print("❌ MongoDB Collection is None. Check database connection.")
            return False

        collection.insert_one(session_data)
        print("✅ Session saved to MongoDB")
        return True
    except Exception as e:
        print(f"❌ Failed to save session to MongoDB: {e}")
        return False
