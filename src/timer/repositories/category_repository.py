from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select
from src.timer.models import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.db_session = session

    async def persist(self, category_data: dict) -> Category:
        """создать категорию"""
        category = Category(**category_data)
        self.db_session.add(category)
        await self.db_session.commit()
        await self.db_session.refresh(category)
        return category

    async def find_by_id(self, category_id: int) -> Category | None:
        """получение категории по id"""
        query = select(Category).where(Category.id == category_id)
        result = await self.db_session.execute(query)
        return result.scalar_one_or_none()
