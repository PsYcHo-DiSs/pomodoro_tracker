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

    async def patch_task_by_id(self, task_id: int, update_data: dict) -> Task | None:
        """обновление задачи по id"""
        if not update_data:
            return await self.find_by_id(task_id)

        task = await self.find_by_id(task_id)

        if task:
            # TODO allowed_fields = {"name", "description", "is_completed"}
            # TODO if field in allowed_fields and hasattr ->  setattr
            for attr, val in update_data.items():
                if hasattr(task, attr):
                    setattr(task, attr, val)
            await self.db_session.commit()
            await self.db_session.refresh(task)

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

    async def delete_all_tasks(self) -> int:
        """удаление всех задач"""
        stmt = delete(Task)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount

    async def delete_tasks_in_batch(self, task_ids: list[int]) -> int:
        """удаление задач по списку ID"""
        if not task_ids:
            return 0

        stmt = delete(Task).where(Task.id.in_(task_ids))
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount
