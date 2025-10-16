from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .repositories import TaskRepository

async def get_task_repo(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)