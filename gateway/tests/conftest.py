import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from main import app
from core.database import get_session

DATABASE_URL = os.getenv("DATABASE_URL") + '_test'


@pytest.fixture(name="session")
def session_fixture():

    engine = create_engine(
        DATABASE_URL, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def check_db_connection() -> bool:
    try:
        engine = create_engine(DATABASE_URL)
        with Session(engine) as session:
            session.exec(select(1))
        return True
    except Exception:
        return False
