from fastapi import APIRouter

from app import routes
from core.config import app
from schemas.responses_model.common import StatusService

router = APIRouter()

router.include_router(
    routes.router,
    prefix="/api",
    # responses=responses_handlers
)

app.include_router(router)


@app.get("/", response_model=StatusService, tags=["Status Service"])
def validate_service():
    """Endpoint for validating responses from service."""
    return StatusService(service="Service ok!")
