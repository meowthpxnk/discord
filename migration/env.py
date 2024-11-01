from MeowthLogger import Logger
from MeowthLogger.logger.config import MainLoggerConfig
from MeowthLogger.logger.config.utils import ConfigLogger


class Logger(Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def __config(self) -> dict:
        config = MainLoggerConfig(self.settings)

        config.loggers.append(
            ConfigLogger(
                name="alembic",
                level=config.settings.logger_level,
                handlers=config.handlers,
                propagate=False,
            )
        )

        config.loggers.append(
            ConfigLogger(
                name="sqlalchemy.engine",
                level=config.settings.logger_level,
                handlers=config.handlers,
                propagate=False,
            )
        )

        return config.json()


logger = Logger(
    use_uvicorn=True,
    logger_level="INFO",
)

from alembic import context
from sqlalchemy import engine_from_config, pool


config = context.config

# if config.config_file_name is not None:
#     fileConfig(config.config_file_name)

from app.database.models.__Base import Base
from app import settings
import app.database.models


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    context.configure(
        url=settings.database.uri,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    cfg = config.get_section(config.config_ini_section, {})
    cfg.update({"sqlalchemy.url": settings.database.uri})

    connectable = engine_from_config(
        cfg,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
