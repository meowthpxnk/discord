# >> App initialisation

# >> Event Loop initialisation
from asyncio import new_event_loop

loop = new_event_loop()


# >> Settings initialisation
from .settings import Settings

settings = Settings()


# >> Base config initialisation
from .utils.base_config import BaseConfig

base_config = BaseConfig()


# >> Logger initialisation
from MeowthLogger import Logger
from MeowthLogger.utilities.fastapi.log_stream import StreamManager

logger = Logger(
    use_uvicorn=True,
    logger_level=settings.logger.level.value,
    stream=StreamManager(loop),
)


# >> Database initialisation
from . import database as db


# >> Redis initialisation
from .redis_client import Redis

redis_client = Redis(host=settings.redis.host, port=settings.redis.port)


# >> API initialisation
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Server, Config
from .api import CorsConfig, APIConfig

api = FastAPI(docs_url=None, **APIConfig().dict)
api.add_middleware(CORSMiddleware, **CorsConfig().dict)
config = Config(
    app=api,
    host=settings.api.host,
    port=settings.api.port,
    log_config=None,
)

server = Server(config)


# >> API add logs websocket initialisation
from MeowthLogger.utilities.fastapi.views import get_log_stream_views_router

router = get_log_stream_views_router(logger)
api.include_router(router)


# >> API routes initialisation
from .api.routes import utils
from .api.routes import routes
from .api import handlers
