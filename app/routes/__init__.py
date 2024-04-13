""""""

from fastapi import APIRouter, Depends
from core.config import get_settings
from app.routes import (
    cursos,
    users,
    materias,
)

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