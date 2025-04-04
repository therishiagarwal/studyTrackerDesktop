import tkinter as tk
from tkinter import messagebox
import threading
import webbrowser
import os

from tracker.app_tracker import AppTracker, CACHE_FILE

tracker = None
tracking_thread = None

def start_tracking(status_label):
    global tracker, tracking_thread
    if tracker is None:
        tracker = AppTracker()

    if not tracking_thread or not tracking_thread.is_alive():
        tracking_thread = threading.Thread(target=tracker.start)
        tracking_thread.daemon = True
        tracking_thread.start()
        status_label.config(text="🟢 Tracking is ON")
    else:
        messagebox.showinfo("Info", "Tracking is already running.")

def stop_tracking(status_label):
    global tracker
    if tracker:
        tracker.stop()
        status_label.config(text="🔴 Tracking is OFF")
        messagebox.showinfo("Stopped", "Tracking has been stopped.")
    else:
        messagebox.showinfo("Info", "Tracking is not running.")

def open_sessions_file():
    if os.path.exists(CACHE_FILE):
        os.startfile(CACHE_FILE)
    else:
        messagebox.showerror("Error", "Session file not found!")

def launch_gui():
    root = tk.Tk()
    root.title("StudyTracker")

    root.geometry("450x350")
    root.resizable(False, False)

    tk.Label(root, text="📚 Study Tracker", font=("Arial", 16, "bold")).pack(pady=10)

    status_label = tk.Label(root, text="🔴 Tracking is OFF", font=("Arial", 12))
    status_label.pack(pady=5)

    tk.Button(root, text="▶ Start Tracking", width=20, command=lambda: start_tracking(status_label)).pack(pady=5)
    tk.Button(root, text="⏹ Stop Tracking", width=20, command=lambda: stop_tracking(status_label)).pack(pady=5)
    # tk.Button(root, text="📁 View Sessions", width=20, command=open_sessions_file).pack(pady=5)

    tk.Label(root, text="Made with ❤️").pack(side="bottom", pady=5)

    root.mainloop()
