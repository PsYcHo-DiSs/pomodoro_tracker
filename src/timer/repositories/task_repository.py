from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.timer.models import Task

class TaskRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_task(self, task_id: int):
        query = select(Task).where(Task.id == task_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()

    async def get_tasks(self) -> list[Task]:
        stmt = select(Task)
        result = await self.db_session.execute(stmt)
        return result.scalars().all()

    async def create_task(self, task_data: dict) -> Task:
        task = Task(**task_data)
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)
        return task

