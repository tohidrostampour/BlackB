from typing import Any, Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.base import Base
from db.database import get_db
from routers.base import api_router


def start_app():
    app = FastAPI()
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='session', autouse=True)
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each testcase
    """
    Base.metadata.create_all(engine)
    _app = start_app()
    yield _app
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session', autouse=True)
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='session', autouse=True)
def client(app: FastAPI, db_session: SessionTesting) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture
    the `get_db` dependency that is injected into routes
    """

    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client


