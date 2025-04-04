from tracker.app_tracker import AppTracker
from ui.gui import launch_gui


if __name__ == "__main__":
    tracker = AppTracker()
    launch_gui()
    try:
        tracker.start()
    except KeyboardInterrupt:
        tracker.stop()
