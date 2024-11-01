from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLSession

from app import settings

engine = create_engine(settings.database.uri, pool_pre_ping=True)


class Session(SQLSession):
    def commit(self) -> None:
        try:
            super().commit()
        except:
            self.rollback()
            raise


session = Session(engine, autoflush=False)

from .models.__Base import Base
