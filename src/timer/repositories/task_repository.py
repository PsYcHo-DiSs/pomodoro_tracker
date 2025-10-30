from typing import Any, Coroutine, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.timer.models import Task


class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def persist(self, task_data: dict) -> Task:
        """создать задачу"""
        task = Task(**task_data)
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

    async def find_by_id(self, task_id: int) -> Task | None:
        """получение задачи по id"""
        query = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def patch_name_by_id(self, task_id: int, name: str) -> Task | None:
        """обновление названия задачи по id"""
        task = await self.find_by_id(task_id)

        if task:
            task.name = name
            await self.db_session.commit()

        return task

    async def delete_task_by_id(self, task_id: int) -> Task | None:
        """удаление записи по id"""
        task = await self.find_by_id(task_id)

        if task:
            await self.db_session.delete(task)
            await self.db_session.commit()

        return task

    # TODO async def delete_and_return(self, task_id: int) -> Task | None:

    async def find_all(self) -> Sequence[Task]:
        """получение всех задач"""
        stmt = select(Task)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()
