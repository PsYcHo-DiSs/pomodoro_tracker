from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends

from src.fixtures import tasks as fixtures_tasks
from src.timer.schemas import (Task,
                               TaskUpdate,
                               DeleteAllTasksResponse)
from src.timer.services import (TaskService,
                                TaskNotFoundError,
                                NoTasksToDeleteError,
                                TaskValidationError)
from src.timer.dependencies import get_task_repo, get_task_service

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all",
            response_model=list[Task])
async def get_tasks(
        service: TaskService = Depends(get_task_service)
):
    return await service.get_all_tasks()


@router.get("/{task_id}",
            response_model=Task)
async def get_task_by_id(
        task_id: int,
        service: TaskService = Depends(get_task_service)
):
    """получение задачи по id"""

    try:
        task = await service.get_task(task_id)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(404, str(e))


@router.post("/",
             response_model=Task)
async def create_task(
        task: Task,
        service: TaskService = Depends(get_task_service)
):
    # TODO поменять Task на TaskCreate в качестве DTO в schemas.py
    """создание задачи"""
    try:
        task = await service.create_task(task.model_dump())
        return task
    except TaskValidationError as e:
        raise HTTPException(400, str(e))


@router.patch("/{task_id}",
              response_model=TaskUpdate)
async def patch_task(
        task_id: int,
        data_to_update: TaskUpdate,
        service: TaskService = Depends(get_task_service)
):
    """обновление полей задачи"""
    try:
        update_dict = data_to_update.model_dump(exclude_unset=True)
        if not update_dict:
            raise HTTPException(400, detail="No fields to update")

        patched_task = await service.update_task(task_id, update_dict)
        return patched_task
    except TaskNotFoundError as e:
        raise HTTPException(404, detail=str(e))


@router.delete("/{task_id}",
               response_model=Task)
async def delete_task(
        task_id: int,
        service: TaskService = Depends(get_task_service)
):
    """удаление задачи по id"""
    try:
        task = await service.delete_task(task_id)
        return task
    except TaskNotFoundError as e:
        raise HTTPException(404, detail=str(e))


@router.delete("/all",
               response_model=DeleteAllTasksResponse)
async def delete_all_tasks(
        service: TaskService = Depends(get_task_service)
):
    """удаление всех задач"""
    try:
        deleted_count = await service.delete_all_tasks()
        return {
            "message": f"Successfully deleted {deleted_count} tasks",
            "deleted_count": deleted_count
        }
    except NoTasksToDeleteError as e:
        raise HTTPException(404, detail=str(e))