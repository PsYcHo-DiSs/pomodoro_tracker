from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/tasks")
async def get_all_tasks_analytics():
    return []


@router.post("/task/{task_id}")
async def get_task_analytics(task_id: int):
    return {"message": f"inf about task with id {task_id}"}
