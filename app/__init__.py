from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/")
def validate_service():
    """Endpoint for validating responses from sevice"""
    return {"Service": "Service ok!"}