from sqlalchemy.orm import Session
from app.models.task import Task


def get_user_tasks(db: Session, owner_id: int) -> list[Task]:
    return db.query(Task).filter(Task.owner_id == owner_id).all()


def get_task_by_id(db: Session, task_id: int, owner_id: int) -> Task | None:
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == owner_id
    ).first()


def create_task(db: Session, title: str, description: str | None, owner_id: int) -> Task:
    new_task = Task(
        title=title,
        description=description,
        owner_id=owner_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task_id: int, owner_id: int, title: str | None, description: str | None, is_completed: bool | None) -> Task | None:
    task = get_task_by_id(db, task_id, owner_id)
    if task is None:
        return None
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if is_completed is not None:
        task.is_completed = is_completed
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    task = get_task_by_id(db, task_id, owner_id)
    if task is None:
        return False
    db.delete(task)
    db.commit()
    return True