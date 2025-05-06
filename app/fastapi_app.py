from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from .models.user import User
from .models.mood_entry import MoodEntry
from .models import Base
from .fastapi_schemas import UserCreate, UserLogin, MoodEntryCreate, MoodEntryOut
from typing import List
from datetime import datetime
from collections import Counter
from contextlib import asynccontextmanager

load_dotenv()


def get_engine_and_session(database_url=None):
    url = database_url or os.getenv("DATABASE_URL", "sqlite:///./mood_diary.db")
    engine = create_engine(url, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


engine, SessionLocal = get_engine_and_session()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def register_routes(app):
    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/register", status_code=201)
    def register(user: UserCreate, db: Session = Depends(get_db)):
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already in use.")
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered.")
        db_user = User(username=user.username, email=user.email)
        db_user.set_password(user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"msg": "Registration successful!", "user_id": db_user.id}

    @app.post("/login")
    def login(user: UserLogin, db: Session = Depends(get_db)):
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or not db_user.check_password(user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password.")
        db_user.last_login = None
        db.commit()
        return {"msg": "Login successful!", "user_id": db_user.id}

    @app.post("/mood-entry", response_model=MoodEntryOut)
    def create_mood_entry(entry: MoodEntryCreate, user_id: int, db: Session = Depends(get_db)):
        db_entry = MoodEntry(
            user_id=user_id,
            date=entry.date,
            mood_score=entry.mood_score,
            emoji=entry.emoji,
            notes=entry.notes,
            activities=entry.activities
        )
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry

    @app.get("/mood-entries/{user_id}", response_model=List[MoodEntryOut])
    def get_mood_entries(user_id: int, db: Session = Depends(get_db)):
        entries = db.query(MoodEntry).filter(MoodEntry.user_id == user_id).order_by(MoodEntry.date.asc()).all()
        return entries

    @app.get("/mood-entries/{user_id}/{year}/{month}", response_model=List[MoodEntryOut])
    def get_monthly_entries(user_id: int, year: int, month: int, db: Session = Depends(get_db)):
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        entries = db.query(MoodEntry).filter(
            MoodEntry.user_id == user_id,
            MoodEntry.date >= start_date,
            MoodEntry.date < end_date
        ).order_by(MoodEntry.date.asc()).all()
        return entries

    @app.get("/stats/{user_id}")
    def get_stats(user_id: int, db: Session = Depends(get_db)):
        entries = db.query(MoodEntry).filter(MoodEntry.user_id == user_id).all()
        if not entries:
            return {"total_entries": 0, "avg_score": 0, "max_score": 0, "min_score": 0, "emoji_counts": {},
                    "top_activities": []}
        total_entries = len(entries)
        scores = [e.mood_score for e in entries]
        avg_score = sum(scores) / total_entries
        max_score = max(scores)
        min_score = min(scores)
        emoji_counts = Counter(e.emoji for e in entries if e.emoji)
        activity_counts = Counter()
        for e in entries:
            if e.activities:
                for act in e.activities.split(","):
                    act = act.strip()
                    if act:
                        activity_counts[act] += 1
        top_activities = activity_counts.most_common(5)
        return {
            "total_entries": total_entries,
            "avg_score": avg_score,
            "max_score": max_score,
            "min_score": min_score,
            "emoji_counts": emoji_counts,
            "top_activities": top_activities
        }


def create_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=engine)
        yield

    app = FastAPI(title="Mood Diary API", lifespan=lifespan)
    register_routes(app)
    return app


app = create_app()
