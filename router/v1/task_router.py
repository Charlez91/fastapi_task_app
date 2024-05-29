from typing import Type

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from pydantic import UUID4

from config.database import get_db
from models.task_model import Task


router = APIRouter(
    prefix="/task",
    tags= ['tasks'],
)

@router.get("/{id}", summary="Retrieve a Task", status_code=200)
async def get_task(id:UUID4, session: Session = Depends(get_db)):
    task:Type[Task] = await session.query(Task).get(id)
    return task