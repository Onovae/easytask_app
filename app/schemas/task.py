# app/schemas/task.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_done: Optional[bool] = False
    reminder_at: Optional[datetime] = None 

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: UUID
    completed: bool
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True
