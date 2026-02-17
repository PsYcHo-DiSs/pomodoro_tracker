from typing import Optional, List
import redis.asyncio as redis
import json
from src.timer.schemas import TaskCacheSchema


class TaskCacheRepository:
    """Репозиторий для работы с Redis"""

    def __init__(self, cache_session: redis.Redis):
        self.cache = cache_session
        self.prefix = "tasks:"  # Префикс для ключей

    def _key(self, suffix: str) -> str:
        """Формирование ключа с префиксом"""
        return f"{self.prefix}{suffix}"

    async def get_task(self, task_id: int) -> Optional[TaskCacheSchema]:
        """Получить задачу из кеша"""
        data = await self.cache.get(self._key(str(task_id)))
        if not data:
            return None

        return TaskCacheSchema.from_redis(data)

    async def set_task(self, task: TaskCacheSchema, expire: int = 3600):
        """Сохранить задачу в кеш"""
        await self.cache.setex(
            self._key(str(task.id)),
            expire,
            task.model_dump_json()
        )

    async def get_all_tasks(self) -> Optional[List[TaskCacheSchema]]:
        """Получить все задачи из кеша"""
        data = await self.cache.get(self._key("all"))
        if not data:
            return None

        tasks_data = json.loads(data)
        return [TaskCacheSchema.model_validate(t) for t in tasks_data]

    async def set_all_tasks(self, tasks: List[TaskCacheSchema], expire: int = 60):
        """Сохранить все задачи в кеш"""
        tasks_data = [t.model_dump() for t in tasks]
        await self.cache.setex(
            self._key("all"),
            expire,
            json.dumps(tasks_data, default=str)
        )

    async def delete_task(self, task_id: int):
        """Удалить задачу из кеша"""
        await self.cache.delete(self._key(str(task_id)))

    async def invalidate_all(self):
        """Инвалидировать кеш списка"""
        await self.cache.delete(self._key("all"))

    async def invalidate_task(self, task_id: int):
        """Инвалидировать кеш задачи и списка"""
        await self.cache.delete(self._key(str(task_id)))
        await self.cache.delete(self._key("all"))