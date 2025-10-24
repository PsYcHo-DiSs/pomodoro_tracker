from src.timer.repositories import TaskRepository
from src.timer.models import Task


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, task_data: dict) -> Task:
        """сервис метод для создания задачи"""
        # Валидация бизнес-правил
        if len(task_data["name"]) < 3:
            raise ValueError("Task name too short")

        # Сохранение
        return await self.repo.persist(task_data)

    async def get_all_tasks(self):
        """сервис метод для возвращения всех задач"""
        return await self.repo.find_all()

    async def get_task(self, task_id: int):
        """сервис метод для возвращения задачи по id"""
        return await self.repo.find_by_id(task_id)
