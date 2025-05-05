import pytest
from datetime import date, datetime, timezone
from app.models.user import User
from app.models.mood_entry import MoodEntry
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.models import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

def test_user_creation(db_session):
    # Test user creation
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Test password verification
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")
    
    # Test user retrieval
    retrieved_user = db_session.query(User).filter_by(username="testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.email == "test@example.com"
    assert retrieved_user.check_password("password123")
    
    # Test string representation
    assert str(user) == "<User testuser>"
    assert repr(user) == "<User testuser>"

def test_mood_entry_creation(db_session):
    # Create a user first
    user = User(username="mooduser", email="mood@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Test default values
    mood_entry = MoodEntry(
        user_id=user.id,
        date=date(2024, 3, 15),
        mood_score=8
    )
    db_session.add(mood_entry)
    db_session.commit()
    assert mood_entry.emoji is None
    assert mood_entry.notes is None
    assert mood_entry.activities is None
    assert mood_entry.created_at is not None
    assert mood_entry.updated_at is not None
    
    # Test with all fields
    mood_entry_full = MoodEntry(
        user_id=user.id,
        date=date(2024, 3, 15),
        mood_score=8,
        emoji="😊",
        notes="Great day!",
        activities="work, gym"
    )
    db_session.add(mood_entry_full)
    db_session.commit()
    
    # Test mood entry retrieval
    retrieved_entry = db_session.query(MoodEntry).filter_by(user_id=user.id, emoji="😊").first()
    assert retrieved_entry is not None
    assert retrieved_entry.mood_score == 8
    assert retrieved_entry.emoji == "😊"
    assert retrieved_entry.notes == "Great day!"
    assert retrieved_entry.activities == "work, gym"
    assert retrieved_entry.date == date(2024, 3, 15)
    
    # Test string representation
    assert str(retrieved_entry) == f'<MoodEntry {retrieved_entry.date} score:8>'
    assert repr(retrieved_entry) == f'<MoodEntry {retrieved_entry.date} score:8>'

def test_mood_entry_validation(db_session):
    # Create a user
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Test valid mood scores
    valid_scores = [1, 5, 10]
    for score in valid_scores:
        mood_entry = MoodEntry(
            user_id=user.id,
            date=date(2024, 3, 15),
            mood_score=score
        )
        db_session.add(mood_entry)
        db_session.commit()
        assert mood_entry.mood_score == score
    
    # Test update method
    mood_entry = MoodEntry(
        user_id=user.id,
        date=date(2024, 3, 15),
        mood_score=5
    )
    db_session.add(mood_entry)
    db_session.commit()
    
    # Test update with valid values
    initial_updated_at = mood_entry.updated_at.replace(tzinfo=timezone.utc)
    mood_entry.update(
        mood_score=7,
        emoji="🎉",
        notes="Updated notes",
        activities="reading, gaming"
    )
    assert mood_entry.mood_score == 7
    assert mood_entry.emoji == "🎉"
    assert mood_entry.notes == "Updated notes"
    assert mood_entry.activities == "reading, gaming"
    assert mood_entry.updated_at.replace(tzinfo=timezone.utc) > initial_updated_at

def test_user_validation(db_session):
    # Test duplicate username
    user1 = User(username="testuser", email="test1@example.com")
    user1.set_password("password123")
    db_session.add(user1)
    db_session.commit()
    
    # Test duplicate username
    user2 = User(username="testuser", email="test2@example.com")
    user2.set_password("password123")
    db_session.add(user2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    
    # Test duplicate email
    user3 = User(username="testuser2", email="test1@example.com")
    user3.set_password("password123")
    db_session.add(user3)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_mood_entry_methods(db_session):
    # Create a user
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Create multiple mood entries for different dates
    entries = [
        MoodEntry(user_id=user.id, date=date(2024, 3, 1), mood_score=8, notes="First entry"),
        MoodEntry(user_id=user.id, date=date(2024, 3, 15), mood_score=6, notes="Second entry"),
        MoodEntry(user_id=user.id, date=date(2024, 4, 1), mood_score=7, notes="April entry"),
        MoodEntry(user_id=user.id, date=date(2024, 2, 28), mood_score=9, notes="February entry")
    ]
    db_session.add_all(entries)
    db_session.commit()
    
    # Test get_monthly_entries for March
    march_entries = db_session.query(MoodEntry).filter(
        MoodEntry.user_id == user.id,
        MoodEntry.date >= date(2024, 3, 1),
        MoodEntry.date < date(2024, 4, 1)
    ).order_by(MoodEntry.date.asc()).all()
    
    assert len(march_entries) == 2
    assert march_entries[0].date == date(2024, 3, 1)
    assert march_entries[1].date == date(2024, 3, 15)
    
    # Test get_monthly_entries for February
    feb_entries = db_session.query(MoodEntry).filter(
        MoodEntry.user_id == user.id,
        MoodEntry.date >= date(2024, 2, 1),
        MoodEntry.date < date(2024, 3, 1)
    ).order_by(MoodEntry.date.asc()).all()
    
    assert len(feb_entries) == 1
    assert feb_entries[0].date == date(2024, 2, 28)
    
    # Test get_entry_by_date
    specific_entry = db_session.query(MoodEntry).filter_by(
        user_id=user.id,
        date=date(2024, 3, 1)
    ).first()
    assert specific_entry is not None
    assert specific_entry.mood_score == 8
    assert specific_entry.notes == "First entry"
    
    # Test entry not found
    no_entry = db_session.query(MoodEntry).filter_by(
        user_id=user.id,
        date=date(2024, 3, 10)
    ).first()
    assert no_entry is None

def test_user_methods(db_session):
    # Create a user
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Test password methods
    assert user.check_password("password123")
    assert not user.check_password("wrongpassword")
    
    # Test password update
    user.set_password("newpassword")
    assert user.check_password("newpassword")
    assert not user.check_password("password123")

def test_mood_entry_date_handling(db_session):
    # Create a user
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    
    # Test date handling
    entry_date = date(2024, 3, 15)
    mood_entry = MoodEntry(
        user_id=user.id,
        date=entry_date,
        mood_score=8
    )
    db_session.add(mood_entry)
    db_session.commit()
    
    # Test date retrieval
    retrieved_entry = db_session.query(MoodEntry).filter_by(user_id=user.id).first()
    assert retrieved_entry.date == entry_date
    
    # Test date comparison
    assert retrieved_entry.date < date(2024, 3, 16)
    assert retrieved_entry.date > date(2024, 3, 14) 