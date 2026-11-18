import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401
from app.config import settings
from app.database import Base, get_db
from app.main import app

assert settings.test_database_url, "TEST_DATABASE_URL nije postavljen u .env"
assert settings.test_database_url != settings.database_url, "Testna baza mora biti različita!"

test_engine = create_engine(settings.test_database_url)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session():
    with TestSessionLocal() as session:
        yield session
    # čišćenje: obriši sve retke, od zavisnih prema nezavisnim tablicama
    with test_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture
def client(db_session):

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(client):
    """Registrira korisnika, prijavi ga i vrati header s tokenom."""
    client.post("/auth/register", json={"email": "ana@example.com", "password": "lozinka123"})
    response = client.post(
        "/auth/login",
        data={"username": "ana@example.com", "password": "lozinka123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}