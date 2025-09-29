from fastapi import APIRouter, status
from src.fixtures import tasks as fixtures_tasks
from src.timer.schemas import Task

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all",
            response_model=list[Task])
async def get_tasks():
    return fixtures_tasks


@router.post("/",
             response_model=Task)
async def create_task(task: Task):
    fixtures_tasks.append(task)
    return task


@router.patch("/{task_id}",
              response_model=Task)
async def patch_task(task_id: int, name: str):
    patched_task = None
    for task in fixtures_tasks:
        if task.id == task_id:
            task.name = name
            patched_task = task
            break
    return patched_task


@router.delete("/{task_id}",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int):
    for index, task in enumerate(fixtures_tasks):
        if task.id == task_id:
            fixtures_tasks.pop(index)
            return {"message": f"task with {task_id} id was deleted"}
    return {"message": "task not found"}
