import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_register_user():
    response = client.post("/auth/register", json={
        "username": "spiderman",
        "email": "spiderman@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "spiderman"


def test_register_duplicate_email():
    client.post("/auth/register", json={
        "username": "testuser2",
        "email": "duplicate@example.com",
        "password": "TestPassword123!"
    })
    response = client.post("/auth/register", json={
        "username": "testuser3",
        "email": "duplicate@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success():
    client.post("/auth/register", json={
        "username": "logintest",
        "email": "logintest@example.com",
        "password": "TestPassword123!"
    })
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "TestPassword123!"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "WrongPassword!"
    })
    assert response.status_code == 401


def test_me_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_valid_token():
    client.post("/auth/register", json={
        "username": "metest",
        "email": "metest@example.com",
        "password": "TestPassword123!"
    })
    login_response = client.post("/auth/login", json={
        "email": "metest@example.com",
        "password": "TestPassword123!"
    })
    token = login_response.json()["access_token"]
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "metest@example.com"