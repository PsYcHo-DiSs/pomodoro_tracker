from typing import Sequence

from src.timer.repositories import CategoryRepository
from src.timer.models import Category


class CategoryNotFoundError(Exception): pass


class CategoryValidationError(Exception): pass


class CategoryService:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    async def create_category(self, category_data: dict) -> Category | None:
        """сервис метод для создания категории"""
        name = category_data.get("name")

        if not name or not name.strip():
            raise CategoryValidationError("Category name is required")

        if len(name.strip()) < 2:
            raise CategoryValidationError("Category name must be at least 2 characters")

        return await self.repo.persist(category_data)

    async def get_category(self, category_id: int) -> Category:
        """сервис метод для возвращения категории по id"""
        category = await self.repo.find_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} not found")
        return category

    async def get_all_categories(self) -> Sequence[Category]:
        """сервис метод для возвращения всех категорий"""
        categories = await self.repo.find_all()
        return categories

    async def update_category(self, category_id: int, update_data: dict) -> Category | None:
        """сервис метод для обновления категории по id"""
        if "name" in update_data and len(update_data["name"]) < 3:
            raise CategoryValidationError("Category name too short")

        category = await self.repo.patch_category_by_id(category_id, update_data)
        if not category:
            raise CategoryNotFoundError(f"Category {category_id} was not updated")
        return category

    async def delete_category(self, category_id: int) -> Category | None:
        """сервис метод для удаления категории по id"""
        category = await self.repo.delete_category_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category with id {category_id} was not deleted")

        return category

    async def delete_all_categories(self) -> int:
        """сервис метод для удаления всех категорий"""
        deleted_count = await self.repo.delete_all_categories()
        return deleted_count

    async def delete_categories_in_batch(self, category_ids: list[int]) -> dict:
        """сервис метод для удаления нескольких категорий из списка id"""
        deleted_count = await self.repo.delete_categories_in_batch(category_ids)
        return {
            "message": f"Deleted {deleted_count} of {len(category_ids)} requested categories",
            "deleted_count": deleted_count,
            "requested_count": len(category_ids)
        }
