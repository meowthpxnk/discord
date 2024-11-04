from app import api

from .auth import router

api.include_router(router)
