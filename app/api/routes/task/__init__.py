from app import api
from .task import tasks_router

api.include_router(tasks_router)
