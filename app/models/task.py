import uuid
from sqlalchemy import Column, String, Text, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship
import enum


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskLabel(str, enum.Enum):
    WORK = "work"
    PERSONAL = "personal"
    URGENT = "urgent"
    OTHER = "other"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    reminder_at = Column(DateTime, nullable=True)
    priority = Column(Enum(TaskPriority), nullable=True, default=TaskPriority.MEDIUM)
    label = Column(Enum(TaskLabel), nullable=True, default=TaskLabel.OTHER)
    
    # Foreign key to users table
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="tasks")

