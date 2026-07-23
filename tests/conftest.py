import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.test_settings import test_settings
from app.database.base import Base
from app.database.session import get_db
from app.main import app

from app.models.user import User
from app.models.asset import Asset
from app.core.roles import UserRole

TEST_DATABASE_URL = test_settings.database_url

engine = create_engine(
    TEST_DATABASE_URL,
    echo=False,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def registered_user(client):
    user = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    }

    response = client.post(
        "/users/register",
        json=user,
    )

    assert response.status_code == 200

    return user


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/users/login",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client, db):
    user = {
        "username": "admin",
        "email": "admin@example.com",
        "password": "password123",
    }

    client.post(
        "/users/register",
        json=user,
    )

    db_user = db.query(User).filter(User.email == user["email"]).first()

    db_user.role = UserRole.ADMIN

    db.commit()
    db.refresh(db_user)

    response = client.post(
        "/users/login",
        json={
            "email": user["email"],
            "password": user["password"],
        },
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
