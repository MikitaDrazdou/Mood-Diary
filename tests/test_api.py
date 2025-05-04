import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import app.fastapi_app as fastapi_app

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(autouse=True)
def setup_and_teardown_db(monkeypatch):
    # Create engine and a single connection
    test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    connection = test_engine.connect()
    # Create tables on this connection
    fastapi_app.Base.metadata.create_all(bind=connection)
    # Create sessionmaker bound to this connection
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    # Monkeypatch engine and SessionLocal
    monkeypatch.setattr(fastapi_app, "engine", test_engine)
    monkeypatch.setattr(fastapi_app, "SessionLocal", TestingSessionLocal)
    yield
    fastapi_app.Base.metadata.drop_all(bind=connection)
    connection.close()
    test_engine.dispose()

app = fastapi_app.create_app()
client = TestClient(app)

def test_register_and_login():
    # Register a new user
    resp = client.post("/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert resp.status_code == 201
    data = resp.json()
    assert "user_id" in data
    user_id = data["user_id"]

    # Login with the same user
    resp = client.post("/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "user_id" in data
    assert data["user_id"] == user_id

    # Try to register with the same username again
    resp = client.post("/register", json={
        "username": "testuser",
        "email": "testuser2@example.com",
        "password": "testpassword"
    })
    assert resp.status_code == 400
    assert "Username already in use." in resp.text

    # Try to register with the same email again
    resp = client.post("/register", json={
        "username": "testuser2",
        "email": "testuser@example.com",
        "password": "testpassword"
    })
    assert resp.status_code == 400
    assert "Email already registered." in resp.text

    # Try to login with wrong password
    resp = client.post("/login", json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert resp.status_code == 401
    assert "Invalid username or password" in resp.text

    # Try to register with empty fields
    resp = client.post("/register", json={
        "username": "",
        "email": "",
        "password": ""
    })
    assert resp.status_code == 422

def test_mood_entry_flow():
    # Register and login
    reg = client.post("/register", json={
        "username": "mooduser",
        "email": "mooduser@example.com",
        "password": "moodpass"
    })
    user_id = reg.json()["user_id"]

    # Add mood entry
    resp = client.post("/mood-entry", params={"user_id": user_id}, json={
        "date": "2025-05-05",
        "mood_score": 8,
        "emoji": "😀",
        "notes": "Great day!",
        "activities": "work, gym"
    })
    assert resp.status_code == 200
    entry = resp.json()
    assert entry["mood_score"] == 8

    # Get mood entries
    resp = client.get(f"/mood-entries/{user_id}")
    assert resp.status_code == 200
    entries = resp.json()
    assert any(e["mood_score"] == 8 for e in entries)

    # Get stats
    resp = client.get(f"/stats/{user_id}")
    assert resp.status_code == 200
    stats = resp.json()
    assert stats["total_entries"] >= 1 