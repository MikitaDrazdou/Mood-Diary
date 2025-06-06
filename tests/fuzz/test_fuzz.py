from fastapi.testclient import TestClient
from hypothesis import given, strategies as st, settings
from datetime import date, timedelta
import string
import os
import tempfile
import atexit

from app.fastapi_app import app, Base, get_engine_and_session, get_db

# Create a temporary database for testing
test_db_file = tempfile.NamedTemporaryFile(delete=False).name
test_engine, TestSessionLocal = get_engine_and_session(f"sqlite:///{test_db_file}")

# Create all tables in the test database
Base.metadata.create_all(bind=test_engine)

# Function to cleanup the temporary database file
def cleanup_test_database():
    if os.path.exists(test_db_file):
        os.unlink(test_db_file)

# Register cleanup function to run when the script exits
atexit.register(cleanup_test_database)

# Override the get_db dependency to use the test database
def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Override the dependency in the app
app.dependency_overrides = {get_db: override_get_db}

client = TestClient(app)


@settings(deadline=None, max_examples=50)
@given(
    username=st.text(min_size=3, max_size=64, alphabet=string.ascii_lowercase),
    email=st.from_regex(r"[a-z0-9]{3,20}@[a-z0-9]{3,15}\.(com|org|net)"),
    password=st.text(min_size=8, max_size=100, alphabet=string.ascii_letters + string.digits)
)
def test_fuzz_register_endpoint(username, email, password):
    """Fuzz test the register endpoint with a variety of inputs."""
    response = client.post(
        "/register",
        json={"username": username, "email": email, "password": password}
    )
    # We only check that the server doesn't crash (no 500 error)
    assert response.status_code != 500


@settings(deadline=None)
@given(
    date_offset=st.integers(min_value=0, max_value=365),
    mood_score=st.integers(min_value=-100, max_value=100),
    emoji=st.one_of(st.none(), st.text(max_size=10)),
    notes=st.one_of(st.none(), st.text(max_size=1000)),
    activities=st.one_of(st.none(), st.text(max_size=500))
)
def test_fuzz_mood_entry_endpoint(date_offset, mood_score, emoji, notes, activities):
    """Fuzz test the mood entry endpoint with a variety of inputs."""
    # Create a test user first
    test_user_data = {
        "username": "fuzzuser",
        "email": "fuzz@example.com",
        "password": "password123"
    }
    
    # Try to register the test user (ignore if already exists)
    client.post("/register", json=test_user_data)
    
    # Login
    login_response = client.post(
        "/login",
        json={"username": "fuzzuser", "password": "password123"}
    )
    
    # Only proceed if login was successful
    if login_response.status_code == 200:
        user_id = login_response.json()["user_id"]
        
        # Generate a date within the last year
        today = date.today()
        entry_date = today - timedelta(days=date_offset)
        
        response = client.post(
            f"/mood-entry?user_id={user_id}",
            json={
                "date": entry_date.isoformat(),
                "mood_score": mood_score,
                "emoji": emoji,
                "notes": notes,
                "activities": activities
            }
        )
        
        # We're checking the server doesn't crash with a 500 error
        assert response.status_code != 500 