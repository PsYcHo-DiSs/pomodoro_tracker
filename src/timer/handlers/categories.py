from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends

from src.timer.schemas import Category, CategoryUpdate
from src.timer.services import (CategoryService,
                                CategoryValidationError,
                                CategoryNotFoundError)
from src.fixtures import categories as fixtures_categories
from src.timer.dependencies import get_category_repo, get_category_service

router = APIRouter(prefix="/category", tags=["category"])


@router.get("/all",
            response_model=list[Category])
async def get_categories(
        service: CategoryService = Depends(get_category_service)
):
    """получение всех категорий"""
    categories = await service.get_all_categories()
    return categories


@router.get("/{category_id}",
            response_model=Category)
async def get_category_by_id(
        category_id: int,
        service: CategoryService = Depends(get_category_service)
):
    """получение категории по id"""
    try:
        category = await service.get_category(category_id)
        return category
    except CategoryNotFoundError as e:
        raise HTTPException(404, str(e))


@router.post("/",
             response_model=Category)
async def create_category(
        category: Category,
        service: CategoryService = Depends(get_category_service)
):
    """создание категории"""
    try:
        category_data = category.model_dump()
        category = await service.create_category(category_data)
        return category
    except CategoryValidationError as e:
        raise HTTPException(400, str(e))


@router.patch("/{category_id}",
              response_model=Category)
async def patch_category(
        category_id: int,
        data_to_update: CategoryUpdate,
        service: CategoryService = Depends(get_category_service)
):
    """обновление полей категории"""
    try:
        update_dict = data_to_update.model_dump(exclude_unset=True)
        if not update_dict:
            raise HTTPException(400, detail="No fields to update")

        patched_category = await service.update_category(category_id, update_dict)
        return patched_category
    except CategoryNotFoundError as e:
        raise HTTPException(404, detail=str(e))


@router.delete("/{category_id}",
               response_model=Category)
async def delete_category(
        category_id: int,
        service: CategoryService = Depends(get_category_service)
):
    """удаление категории по id"""
    try:
        category = await service.delete_category(category_id)
        return category
    except CategoryNotFoundError as e:
        raise HTTPException(404, detail=str(e))
