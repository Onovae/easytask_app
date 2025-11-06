# app/schemas/task.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskLabel(str, Enum):
    WORK = "work"
    PERSONAL = "personal"
    URGENT = "urgent"
    OTHER = "other"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_done: Optional[bool] = False
    reminder_at: Optional[datetime] = None
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    label: Optional[TaskLabel] = TaskLabel.OTHER

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_done: Optional[bool] = None
    reminder_at: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    label: Optional[TaskLabel] = None

class TaskRead(TaskBase):
    id: UUID
    created_at: datetime
    user_id: UUID

    class Config:
        from_attributes = True
