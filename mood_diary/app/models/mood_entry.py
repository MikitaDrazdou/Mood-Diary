"""
MoodEntry model for storing user's daily mood and notes
"""
from datetime import datetime
from app import db

class MoodEntry(db.Model):
    """Model for daily mood entries"""
    __tablename__ = 'mood_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow().date, nullable=False)
    mood_score = db.Column(db.Integer, nullable=False)  # 1-10 scale
    emoji = db.Column(db.String(10), nullable=True)  # Emoji representation
    notes = db.Column(db.Text, nullable=True)
    activities = db.Column(db.String(255), nullable=True)  # Comma-separated activities
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, date, mood_score, emoji=None, notes=None, activities=None):
        """Initialize a new mood entry"""
        self.user_id = user_id
        self.date = date
        self.mood_score = mood_score
        self.emoji = emoji
        self.notes = notes
        self.activities = activities
    
    def update(self, mood_score=None, emoji=None, notes=None, activities=None):
        """Update this mood entry"""
        if mood_score is not None:
            self.mood_score = mood_score
        if emoji is not None:
            self.emoji = emoji
        if notes is not None:
            self.notes = notes
        if activities is not None:
            self.activities = activities
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_monthly_entries(cls, user_id, year, month):
        """Get all entries for a specific month"""
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        
        return cls.query.filter(
            cls.user_id == user_id,
            cls.date >= start_date,
            cls.date < end_date
        ).order_by(cls.date.asc()).all()
    
    @classmethod
    def get_entry_by_date(cls, user_id, date):
        """Get a mood entry for a specific date"""
        return cls.query.filter_by(user_id=user_id, date=date).first()
    
    def __repr__(self):
        """String representation of MoodEntry"""
        return f'<MoodEntry {self.date} score:{self.mood_score}>' 