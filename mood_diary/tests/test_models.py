"""
Tests for the database models
"""
import unittest
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.mood_entry import MoodEntry

class TestUserModel(unittest.TestCase):
    """Test cases for the User model"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_hashing(self):
        """Test password hashing functionality"""
        user = User(username='test_user', email='test@example.com', password='password123')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrong_password'))
    
    def test_user_creation(self):
        """Test user creation and attributes"""
        user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        # Check if user was saved correctly
        saved_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test@example.com')
        self.assertIsNotNone(saved_user.created_at)
        self.assertIsNone(saved_user.last_login)
    
    def test_update_last_login(self):
        """Test updating the last login time"""
        user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        # Update last login
        user.update_last_login()
        
        # Check if last login was updated
        self.assertIsNotNone(user.last_login)
        self.assertLess(user.last_login - datetime.utcnow(), timedelta(seconds=1))

class TestMoodEntryModel(unittest.TestCase):
    """Test cases for the MoodEntry model"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Create a test user
        self.user = User(username='test_user', email='test@example.com', password='password123')
        db.session.add(self.user)
        db.session.commit()
        
        # Set up some test dates
        self.today = datetime.utcnow().date()
        self.yesterday = self.today - timedelta(days=1)
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_mood_entry_creation(self):
        """Test creating a mood entry"""
        entry = MoodEntry(
            user_id=self.user.id,
            date=self.today,
            mood_score=8,
            emoji='😀',
            notes='Having a great day!',
            activities='Working, Exercise'
        )
        db.session.add(entry)
        db.session.commit()
        
        # Check if entry was saved correctly
        saved_entry = MoodEntry.query.filter_by(user_id=self.user.id, date=self.today).first()
        self.assertIsNotNone(saved_entry)
        self.assertEqual(saved_entry.mood_score, 8)
        self.assertEqual(saved_entry.emoji, '😀')
        self.assertEqual(saved_entry.notes, 'Having a great day!')
        self.assertEqual(saved_entry.activities, 'Working, Exercise')
    
    def test_mood_entry_update(self):
        """Test updating a mood entry"""
        entry = MoodEntry(
            user_id=self.user.id,
            date=self.today,
            mood_score=5,
            emoji='😐',
            notes='Average day'
        )
        db.session.add(entry)
        db.session.commit()
        
        # Update the entry
        entry.update(mood_score=7, emoji='🙂', notes='Day got better!')
        db.session.commit()
        
        # Check if entry was updated correctly
        saved_entry = MoodEntry.query.filter_by(user_id=self.user.id, date=self.today).first()
        self.assertEqual(saved_entry.mood_score, 7)
        self.assertEqual(saved_entry.emoji, '🙂')
        self.assertEqual(saved_entry.notes, 'Day got better!')
        self.assertIsNone(saved_entry.activities)
    
    def test_get_entry_by_date(self):
        """Test retrieving an entry by date"""
        # Create two entries on different dates
        entry1 = MoodEntry(user_id=self.user.id, date=self.today, mood_score=8, emoji='😀')
        entry2 = MoodEntry(user_id=self.user.id, date=self.yesterday, mood_score=6, emoji='🙂')
        db.session.add_all([entry1, entry2])
        db.session.commit()
        
        # Test retrieval by date
        today_entry = MoodEntry.get_entry_by_date(self.user.id, self.today)
        yesterday_entry = MoodEntry.get_entry_by_date(self.user.id, self.yesterday)
        
        self.assertEqual(today_entry.mood_score, 8)
        self.assertEqual(yesterday_entry.mood_score, 6)

if __name__ == '__main__':
    unittest.main() 