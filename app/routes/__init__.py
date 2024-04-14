""""""

from fastapi import APIRouter, Depends

from app.routes import cursos, materias, users
from core.config import get_settings

router = APIRouter()

router.include_router(
    cursos.router,
    prefix="/cursos",
    tags=["Cursos"],
    # responses=responses_handlers
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Usuarios"],
    # responses=responses_handlers
)

router.include_router(
    materias.router,
    prefix="/materias",
    tags=["Materias"],
    # responses=responses_handlers
)
