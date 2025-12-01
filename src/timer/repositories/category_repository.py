from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, delete
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

    async def find_all(self) -> Sequence[Category]:
        """получение всех категорий"""
        query = select(Category)
        result = await self.db_session.execute(query)
        return result.scalars().all()

    async def patch_category_by_id(self, category_id: int, update_data: dict) -> Category | None:
        """обновление категории по id"""
        if not update_data:
            return await self.find_by_id(category_id)

        category = await self.find_by_id(category_id)

        if category:
            # TODO allowed_fields = {"name"}
            # TODO if field in allowed_fields and hasattr ->  setattr
            for attr, val in update_data.items():
                if hasattr(category, attr):
                    setattr(category, attr, val)
            await self.db_session.commit()
            await self.db_session.refresh(category)

        return category

    async def delete_category_by_id(self, category_id: int) -> Category | None:

        """удаление категории по id"""
        category = await self.find_by_id(category_id)

        if category:
            await self.db_session.delete(category)
            await self.db_session.commit()

        return category


    async def delete_all_categories(self) -> int:
        """удаление всех категорий"""
        stmt = delete(Category)
        result = await self.db_session.execute(stmt)
        await self.db_session.commit()
        return result.rowcount

