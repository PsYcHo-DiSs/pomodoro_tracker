from typing import Sequence

from src.timer.repositories import TaskRepository
from src.timer.models import Task


class TaskNotFoundError(Exception): pass


class TaskValidationError(Exception): pass


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, task_data: dict) -> Task:
        """сервис метод для создания задачи"""
        # Валидация бизнес-правил
        if len(task_data["name"]) < 3:
            raise TaskValidationError("Task name too short")

        # Сохранение
        return await self.repo.persist(task_data)

    async def get_all_tasks(self) -> Sequence[Task]:
        """сервис метод для возвращения всех задач"""
        return await self.repo.find_all()

    async def update_task(self, task_id: int, update_data: dict) -> Task | None:
        """сервис метод для обновления задачи по id"""
        if "name" in update_data and len(update_data["name"]) < 3:
            raise TaskValidationError("Task name too short")

        task = await self.repo.patch_task_by_id(task_id, update_data)
        if not task:
            raise TaskNotFoundError(f"Task {task_id} was not updated")
        return task

    async def delete_task(self, task_id):
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
