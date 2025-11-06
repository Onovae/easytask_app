# app/models/__init__.py
from app.models.user import User
from app.models.task import Task
from app.models.otp_entry import OtpEntry

__all__ = ["User", "Task", "OtpEntry"]
