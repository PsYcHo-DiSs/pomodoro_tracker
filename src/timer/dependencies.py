from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from .repositories import TaskRepository, CategoryRepository
from .services import TaskService, CategoryService


async def get_task_repo(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    """получение экземпляра класса репозитория для задачи"""
    return TaskRepository(session)


async def get_task_service(repo: TaskRepository = Depends(get_task_repo)) -> TaskService:
    """получение экземпляра класса сервиса для задачи"""
    return TaskService(repo)


async def get_category_repo(session: AsyncSession = Depends(get_session)) -> CategoryRepository:
    """получение экземпляра класса репозитория для категории"""
    return CategoryRepository(session)


async def get_category_service(repo: CategoryRepository = Depends(get_category_repo)) -> CategoryService:
    """получение экземпляра класса сервиса для категории"""
    return CategoryService(repo)
