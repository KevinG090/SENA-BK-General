""""""

from fastapi import APIRouter

from app.routes import cursos, materias, users

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
