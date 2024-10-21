from fastapi.testclient import TestClient
from main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./tests.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_user():
    response = client.post("/Create_User/", json={"id": 1, "name": "Test User", "username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_create_url():
    response = client.post("/Create_User/", json={"id": 2, "name": "User2", "username": "user2", "password": "password2"})
    assert response.status_code == 200
    response = client.post("/Create_URL/", json={"id": 1, "long_url": "https://example.com", "short_url": "", "user_id": 2},
                           auth=("user2", "password2"))
    assert response.status_code == 200
    assert "short_url" in response.json()

def test_redirect_to_long_url():
    short_url = "Team3example"
    response = client.get(f"/{short_url}")
    assert response.status_code == 200
