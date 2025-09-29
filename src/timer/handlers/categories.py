from fastapi import APIRouter, status
from src.fixtures import categories as fixtures_categories
from src.timer.schemas import Category

router = APIRouter(prefix="/category", tags=["category"])


# TODO:
# создать категорию
# удалить категорию
# отредактировать категорию

@router.get("/all",
            response_model=list[Category])
async def get_categories():
    return fixtures_categories


@router.post("/",
             response_model=Category)
async def create_category(category: Category):
    fixtures_categories.append(category)
    return category


@router.patch("/{category_id}",
              response_model=Category)
async def patch_category(category_id: int, name: str):
    patched_category = None
    for cat in fixtures_categories:
        if cat.id == category_id:
            cat.name = name
            patched_category = cat
    return patched_category


@router.delete("/{category_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int):
    for index, cat in enumerate(fixtures_categories):
        if cat.id == category_id:
            fixtures_categories.pop(index)
            return {"message": f"category with {category_id} id was deleted"}

    return {"message": "category not found"}
