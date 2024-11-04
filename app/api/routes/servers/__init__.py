from app import api

from .servers import router

api.include_router(router)
