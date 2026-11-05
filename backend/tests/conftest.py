import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.service import ensure_seed_admin
from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture()
def client():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    ensure_seed_admin(db)
    db.close()

    # Not used as a context manager on purpose: that would run the app's
    # startup event, which creates tables against the real MySQL URL from
    # settings. Tables are created above against the in-memory SQLite engine.
    test_client = TestClient(app)
    yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def admin_token(client):
    response = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    return response.json()["access_token"]
