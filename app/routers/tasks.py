from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.security import decode_access_token, is_token_blacklisted
from app.services.task_service import (
    get_user_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)
from app.services.user_service import get_user_by_email

router = APIRouter(prefix="/tasks", tags=["Tasks"])
security = HTTPBearer()


class TaskCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


def get_db():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    if is_token_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked"
        )
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.get("/")
def list_tasks(
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    tasks = get_user_tasks(db, current_user.id)
    return tasks


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_new_task(
    request: TaskCreateRequest,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    task = create_task(db, request.title, request.description, current_user.id)
    return task


@router.get("/{task_id}")
def get_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    task = get_task_by_id(db, task_id, current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.put("/{task_id}")
def update_existing_task(
    task_id: int,
    request: TaskUpdateRequest,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    task = update_task(
        db, task_id, current_user.id,
        request.title, request.description, request.is_completed
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    current_user=Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    success = delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )