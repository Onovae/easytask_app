# app/api/task.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from app.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskPriority, TaskLabel
from app.models.task import Task
from app.core.security import get_current_user
from app.db.session import get_db
from app.crud import task as crud_task
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskRead)
def create(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    # Ensure user_id is a UUID, not a SQLAlchemy Column
    if not isinstance(user_id, UUID):
        try:
            user_id = UUID(str(user_id))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    return crud_task.create_task(db, user_id, task_in)

@router.get("/", response_model=list[TaskRead])
def read_all(
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    label: Optional[TaskLabel] = Query(None, description="Filter by label"),
    is_done: Optional[bool] = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    if not isinstance(user_id, UUID):
        try:
            user_id = UUID(str(user_id))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Get all tasks for the user
    tasks = crud_task.get_tasks(db, user_id)
    
    # Apply filters
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if label is not None:
        tasks = [task for task in tasks if task.label == label]
    if is_done is not None:
        tasks = [task for task in tasks if task.is_done == is_done]
    
    # Sort by priority (high -> medium -> low) and creation date
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks.sort(key=lambda t: (priority_order.get(t.priority.value if t.priority else "medium", 1), t.created_at), reverse=True)
    
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def read(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure user_id is always a UUID, not a SQLAlchemy Column
    user_id = current_user.id
    if not isinstance(user_id, UUID):
        try:
            user_id = UUID(str(user_id))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    task = crud_task.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
@router.patch("/{task_id}", response_model=TaskRead)
def update(
    task_id: UUID,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    if not isinstance(user_id, UUID):
        try:
            user_id = UUID(str(user_id))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    task = crud_task.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud_task.update_task(db, task, task_in)

@router.delete("/{task_id}", status_code=204)
def delete(
    task_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id
    if not isinstance(user_id, UUID):
        try:
            user_id = UUID(str(user_id))
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid user ID")
    task = crud_task.get_task(db, task_id, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud_task.delete_task(db, task)
    return None
