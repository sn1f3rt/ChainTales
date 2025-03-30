from typing import Any, Generator

import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from application.config.config_service import ConfigService


class DatabaseManager:
    Base = declarative_base()

    def __init__(self) -> None:
        self.engine = create_engine(
            f"mysql+pymysql://{ConfigService.get(key='db.user')}:{ConfigService.get(key='db.password')}"
            f"@{ConfigService.get(key='db.host')}:{ConfigService.get(key='db.port')}"
            f"/{ConfigService.get(key='db.name')}",
            pool_size=100,
            pool_recycle=120,
            pool_pre_ping=True,
            max_overflow=0,
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def setup_database(self) -> None:
        self.Base.metadata.create_all(bind=self.engine)

    @contextlib.contextmanager
    def acquire_session(self) -> Generator[Session, Any, None]:
        session = self.SessionLocal()
        try:
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
