def test_register_user(client):
    response = client.post(
        "/users/register",
        json={
            "username": "john",
            "email": "john@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "john"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_duplicate_email(client):
    user = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "password123",
    }

    client.post("/users/register", json=user)

    response = client.post(
        "/users/register",
        json={
            "username": "alice2",
            "email": "alice@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_duplicate_username(client):
    user = {
        "username": "bob",
        "email": "bob@example.com",
        "password": "password123",
    }

    client.post("/users/register", json=user)

    response = client.post(
        "/users/register",
        json={
            "username": "bob",
            "email": "bob2@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"


def test_login_success(client):
    user = {
        "username": "dhanush",
        "email": "dhanush@example.com",
        "password": "password123",
    }

    client.post("/users/register", json=user)

    response = client.post(
        "/users/login",
        json={
            "email": "dhanush@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    user = {
        "username": "tom",
        "email": "tom@example.com",
        "password": "password123",
    }

    client.post("/users/register", json=user)

    response = client.post(
        "/users/login",
        json={
            "email": "tom@example.com",
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_login_wrong_email(client):
    response = client.post(
        "/users/login",
        json={
            "email": "unknown@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


from app.core.enums.roles import UserRole
from app.models.user import User


def test_admin_route(client, db):
    # Register a normal user
    user = {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "password123",
    }

    client.post("/users/register", json=user)

    # Promote the user to ADMIN
    db_user = db.query(User).filter(User.email == "admin@example.com").first()

    db_user.role = UserRole.ADMIN
    db.commit()
    db.refresh(db_user)

    # Login
    login_response = client.post(
        "/users/login",
        json={
            "email": "admin@example.com",
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Access protected admin endpoint
    response = client.get(
        "/users/admin",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "adminuser"
    assert data["role"] == UserRole.ADMIN.value
    assert data["message"] == "Welcome Admin!"
