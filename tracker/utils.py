import os
import json
import uuid

APPDATA_DIR = os.path.join(os.getenv("APPDATA"), "StudyTracker")
CONFIG_FILE = os.path.join(APPDATA_DIR, "user_config.json")
CACHE_FILE = os.path.join(APPDATA_DIR, "session.json")

def ensure_directories():
    if not os.path.exists(APPDATA_DIR):
        os.makedirs(APPDATA_DIR)

def get_or_create_user_id():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            return config["username"], config["user_id"]

    username = "default_user"
    user_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, username))

    with open(CONFIG_FILE, "w") as f:
        json.dump({"username": username, "user_id": user_id}, f)

    return username, user_id
