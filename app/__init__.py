from fastapi import APIRouter

from app import routes
from schemas.responses_model.common import StatusService

api_router = APIRouter()


@api_router.get("/", response_model=StatusService, tags=["Status Service"])
def validate_service():
    """Endpoint for validating responses from service."""
    return StatusService(service="Service ok!")


api_router.include_router(
    routes.router,
    prefix="/api",
    # tags=[""],
    # responses=responses_handlers
)
