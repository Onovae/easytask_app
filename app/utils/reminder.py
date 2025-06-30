import threading
import time
from datetime import datetime
from app.db.session import SessionLocal
from app.models.task import Task

def check_reminders():
    while True:
        db = SessionLocal()
        now = datetime.utcnow()
        tasks = db.query(Task).filter(
            Task.reminder_at <= now,
            Task.reminder_at != None,
            Task.is_done == False
        ).all()

        for task in tasks:
            print(f"🔔 Reminder: {task.title} (User ID: {task.user_id})")
            db.query(Task).filter(Task.id == task.id).update({"reminder_at": None})
            db.commit()
        db.close()
        time.sleep(60)  # Check every minute

def start_reminder_thread():
    thread = threading.Thread(target=check_reminders, daemon=True)
    thread.start()
