from typing import Sequence, Optional

from src.timer.repositories import TaskRepository
from src.timer.repositories import TaskCacheRepository

from src.timer.schemas import TaskCacheSchema, TaskResponse

from src.timer.models import Task


class TaskNotFoundError(Exception): pass


class NoTasksToDeleteError(Exception): pass


class TaskValidationError(Exception): pass


class TaskService:
    """Сервис для работы с задачами"""
    def __init__(
            self,
            repo: TaskRepository,
            cache_repo: Optional[TaskCacheRepository] = None
    ):
        self.repo = repo
        self.cache = cache_repo

    async def create_task(self, task_data: dict) -> Task:
        """Создание задачи"""
        # Бизнес-валидация
        if len(task_data["name"]) < 3:
            raise TaskValidationError("Task name too short")

        # Сохраняем в БД
        task = await self.repo.persist(task_data)

        # Если есть кеш - обновляем
        if self.cache:
            # Конвертируем SQLAlchemy модель в кеш-схему
            cache_dto = TaskCacheSchema.model_validate(task)
            await self.cache.set_task(cache_dto)
            await self.cache.invalidate_all()  # Список задач устарел

        return task

    async def get_all_tasks(self) -> Sequence[Task]:
        """Получение всех задач"""
        # Пробуем из кеша
        if self.cache:
            cached = await self.cache.get_all_tasks()
            if cached:
                # Конвертируем список кеш-схем в список SQLAlchemy моделей
                tasks = []
                for task_dto in cached:
                    task_data = task_dto.model_dump()
                    tasks.append(Task(**task_data))
                return tasks

        # Из БД
        tasks = await self.repo.find_all()

        # Сохраняем в кеш
        if self.cache and tasks:
            cache_dtos = [TaskCacheSchema.model_validate(t) for t in tasks]
            await self.cache.set_all_tasks(cache_dtos)

        return tasks

    async def update_task(self, task_id: int, update_data: dict) -> Task | None:
        """сервис метод для обновления задачи по id"""
        if "name" in update_data and len(update_data["name"]) < 3:
            raise TaskValidationError("Task name too short")

        task = await self.repo.patch_task_by_id(task_id, update_data)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} was not updated")
        return task

    async def delete_task(self, task_id) -> Task | None:
        """сервис метод для удаления задачи по id"""
        task = await self.repo.delete_task_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with id {task_id} was not deleted")
        return task

    async def get_task(self, task_id: int) -> Task:
        """сервис метод для возвращения задачи по id"""
        task = await self.repo.find_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task

    async def delete_all_tasks(self) -> int:
        """сервис метод для удаления всех задач"""
        deleted_count = await self.repo.delete_all_tasks()
        if deleted_count == 0:
            raise NoTasksToDeleteError("No tasks found to delete")
        return deleted_count

    async def delete_tasks_in_batch(self, tasks_ids: list[int]) -> dict:
        """сервис метод для удаления нескольких задач из списка id"""
        requested_count = len(tasks_ids)
        deleted_count = await self.repo.delete_tasks_in_batch(tasks_ids)
        return {
            "message": f"Deleted {deleted_count} of {requested_count} requested tasks",
            "deleted_count": deleted_count,
            "requested_count": requested_count
        }
