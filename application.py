""""""

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app import api_router
from core.config import _app, get_settings


def get_application():
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in get_settings().BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


application = get_application()

application.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("application:application", debug=True)
