"""
User model for authentication and user management
"""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    """User model with authentication capabilities"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationship with mood entries
    mood_entries = db.relationship('MoodEntry', backref='user', lazy='dynamic',
                                   cascade='all, delete-orphan')
    
    def __init__(self, username, email, password):
        """Initialize a new user"""
        self.username = username
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        """String representation of User"""
        return f'<User {self.username}>'


@login_manager.user_loader
def load_user(user_id):
    """User loader for Flask-Login"""
    return User.query.get(int(user_id)) 