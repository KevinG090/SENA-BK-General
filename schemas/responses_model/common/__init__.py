""""""

from pydantic import BaseModel , Field

class StatusService(BaseModel):
    """Model representing the service status."""
    service: str = Field(..., example="Service ok!", description="Status of the service")