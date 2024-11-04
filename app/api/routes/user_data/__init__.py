from app import api

from .user_data import router

api.include_router(router)
