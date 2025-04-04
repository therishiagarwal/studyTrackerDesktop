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

def save_session_to_mongo(user_id, session_data):
    """ Save the study session to MongoDB under the respective user_id """
    try:
        if collection is None:
            print("❌ MongoDB Collection is None. Check database connection.")
            return False

        # Push session to the study_sessions array of the corresponding user_id
        result = collection.update_one(
            {"user_id": user_id},
            {
                "$push": {"study_sessions": session_data}
            },
            upsert=True
        )

        print("✅ Session saved to MongoDB")
        return True
    except Exception as e:
        print(f"❌ Failed to save session to MongoDB: {e}")
        return False
