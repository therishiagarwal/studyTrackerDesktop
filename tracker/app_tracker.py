import time
import jsonpickle
import pywinctl as gw
import uuid
import os
from datetime import datetime, timezone, timedelta
from threading import Event

from .mongo_helper import save_session_to_mongo
from .utils import get_or_create_user_id, APPDATA_DIR, CACHE_FILE, ensure_directories

# Define IST timezone
IST = timezone(timedelta(hours=5, minutes=30))

class AppTracker:
    def __init__(self, user_id=None):
        ensure_directories()
        if not user_id:
            self.username, self.user_id = get_or_create_user_id()
            print(f"👤 Tracking sessions for user: {self.username} (ID: {self.user_id})")
        else:
            self.username = None
            self.user_id = user_id

        self.current_app = None
        self.start_time = None
        self.sessions = self.load_sessions()
        self.stop_event = Event()

    def get_active_application(self):
        try:
            active_window = gw.getActiveWindow()
            if active_window:
                return active_window.title
        except Exception as e:
            print("⚠️ Could not get active window:", e)
        return None

    def track_loop(self):
        print("✅ Started tracking...")
        while not self.stop_event.is_set():
            self.log_session()
            self.stop_event.wait(5)

    def start(self):
        self.stop_event.clear()
        self.track_loop()

    def stop(self):
        self.stop_event.set()
        if self.current_app and self.start_time:
            self.save_session(self.current_app)
        print("🛑 Tracking stopped. Data saved.")

    def log_session(self):
        active_app = self.get_active_application()
        if active_app != self.current_app:
            if self.current_app and self.start_time:
                self.save_session(self.current_app)
            self.current_app = active_app
            self.start_time = time.time() if active_app else None

    def save_session(self, app_name):
        end_time = time.time()
        duration = round((end_time - self.start_time) / 60, 2)

        print(f"⏱️ Saving session for '{app_name}' | Duration: {duration} minutes")

        session_data = {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.fromtimestamp(self.start_time, tz=IST).isoformat(),
            "end_time": datetime.fromtimestamp(end_time, tz=IST).isoformat(),
            "duration": duration,
            "source": "desktop_app",
            "activity": app_name
        }

        # Save locally
        self.sessions["study_sessions"].append(session_data)
        self.sessions["total_time_spent"] += duration
        self.save_sessions()

        # Save to MongoDB
        try:
            save_session_to_mongo(self.user_id, session_data)
        except Exception as e:
            print("❌ Failed to save session to MongoDB:", e)

    def save_sessions(self):
        try:
            with open(CACHE_FILE, "w") as f:
                f.write(jsonpickle.encode(self.sessions, indent=4))
        except Exception as e:
            print("❌ Failed to write sessions to file:", e)

    def load_sessions(self):
        if not os.path.exists(CACHE_FILE):
            return {
                "user_id": self.user_id,
                "study_sessions": [],
                "total_time_spent": 0
            }

        try:
            with open(CACHE_FILE, "r") as f:
                return jsonpickle.decode(f.read())
        except Exception as e:
            print("⚠️ Failed to load sessions. Returning empty structure. Error:", e)
            return {
                "user_id": self.user_id,
                "study_sessions": [],
                "total_time_spent": 0
            }
