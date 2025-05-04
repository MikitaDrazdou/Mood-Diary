from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date, datetime
from pydantic import ConfigDict

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

class MoodEntryCreate(BaseModel):
    date: date
    mood_score: int = Field(..., ge=1, le=10)
    emoji: Optional[str]
    notes: Optional[str]
    activities: Optional[str]

class MoodEntryOut(BaseModel):
    id: int
    date: date
    mood_score: int
    emoji: Optional[str]
    notes: Optional[str]
    activities: Optional[str]
    user_id: int
    created_at: datetime  # Include creation timestamp in API output

    model_config = ConfigDict(from_attributes=True) 