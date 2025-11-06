# app/crud/task.py
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from uuid import UUID

def create_task(db: Session, user_id: UUID, task_in: TaskCreate) -> Task:
    task = Task(**task_in.model_dump(), user_id=user_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session, user_id: UUID):
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, task_id: UUID, user_id: UUID):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

def update_task(db: Session, task: Task, task_in: TaskUpdate):
    for field, value in task_in.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
