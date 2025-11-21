from src.timer.handlers.ping import router as ping_router
from src.timer.handlers.tasks import router as task_router
from src.timer.handlers.categories import router as category_router

routers = [ping_router, task_router, category_router]

__all__ = [
    "ping_router",
    "task_router",
    "category_router",
    "routers"
]
