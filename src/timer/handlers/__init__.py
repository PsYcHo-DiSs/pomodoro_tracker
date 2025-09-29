from .ping import router as ping_router
from .tasks import router as task_router
from .categories import router as category_router

routers = [ping_router, task_router, category_router]