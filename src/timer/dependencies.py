from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.database import get_session
from src.timer.cache import get_redis_session
from .repositories import TaskRepository, CategoryRepository
from .repositories import TaskCacheRepository
from .services import TaskService, CategoryService

# ----- СТАРЫЕ зависимости (работают как раньше) -----
async def get_task_repo(session: AsyncSession = Depends(get_session)) -> TaskRepository:
    """получение экземпляра класса репозитория для задачи"""
    return TaskRepository(session)


async def get_task_service(repo: TaskRepository = Depends(get_task_repo)) -> TaskService:
    """получение экземпляра класса сервиса для задачи"""
    return TaskService(repo)


# ----- НОВЫЕ зависимости с кешем -----
async def get_task_cache_repo(
    cache: redis.Redis = Depends(get_redis_session)
) -> TaskCacheRepository:
    """получение экземпляра кеш-репозитория"""
    return TaskCacheRepository(cache)


async def get_task_service_with_cache(
    repo: TaskRepository = Depends(get_task_repo),
    cache_repo: TaskCacheRepository = Depends(get_task_cache_repo)
) -> TaskService:
    """НОВЫЙ сервис с кешем"""
    return TaskService(repo=repo, cache_repo=cache_repo)


# ----- Категории (пока без кеша) -----
async def get_category_repo(session: AsyncSession = Depends(get_session)) -> CategoryRepository:
    """получение экземпляра класса репозитория для категории"""
    return CategoryRepository(session)


async def get_category_service(repo: CategoryRepository = Depends(get_category_repo)) -> CategoryService:
    """получение экземпляра класса сервиса для категории"""
    return CategoryService(repo)
