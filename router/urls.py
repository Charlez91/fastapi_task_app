from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from .v1.task_router import router as task_routes
from .v1.user_router import router as user_routes

router = APIRouter(prefix="/api/v1")

@router.get("/")
async def home():
    return HTMLResponse("<h1>Welcome to the Task Management app V1 api</h1>")

router.include_router(task_routes)
router.include_router(user_routes)