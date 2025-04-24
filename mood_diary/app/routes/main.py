"""
Main routes for the application
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.mood_entry import MoodEntry
from datetime import datetime, timedelta
import calendar
import logging

# Configure logger
logger = logging.getLogger(__name__)

# Create blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Homepage route"""
    if current_user.is_authenticated:
        # Get today's date
        today = datetime.utcnow().date()
        
        # Get current month for calendar
        year = today.year
        month = today.month
        
        # Get today's mood entry if it exists
        today_entry = MoodEntry.get_entry_by_date(current_user.id, today)
        
        # Get monthly entries for calendar
        monthly_entries = MoodEntry.get_monthly_entries(current_user.id, year, month)
        
        # Create a calendar display
        cal = calendar.monthcalendar(year, month)
        
        # Convert monthly entries to a dictionary for easy lookup
        entry_dict = {entry.date: entry for entry in monthly_entries}
        
        # Calculate average mood directly in Python
        total_score = sum(entry.mood_score for entry in monthly_entries)
        avg_mood = total_score / len(monthly_entries) if monthly_entries else 0
        
        month_name = calendar.month_name[month]
        
        return render_template('index.html', 
                              title='Home',
                              today=today,
                              today_entry=today_entry,
                              calendar=cal,
                              month=month,
                              year=year,
                              month_name=month_name,
                              entries=entry_dict,
                              entry_count=len(monthly_entries),
                              avg_mood=avg_mood)
    
    # If user is not logged in, show landing page
    return render_template('landing.html', title='Welcome to Mood Diary')

@main_bp.route('/calendar')
@login_required
def view_calendar():
    """Calendar view route - full calendar display"""
    # Get current month by default
    today = datetime.utcnow().date()
    year = today.year
    month = today.month
    
    # Get monthly entries for calendar
    monthly_entries = MoodEntry.get_monthly_entries(current_user.id, year, month)
    
    # Create a calendar display
    cal = calendar.monthcalendar(year, month)
    
    # Convert monthly entries to a dictionary for easy lookup
    entry_dict = {entry.date: entry for entry in monthly_entries}
    
    month_name = calendar.month_name[month]
    
    logger.info(f"User {current_user.username} viewed calendar for {month_name} {year}")
    
    return render_template('calendar.html', 
                          title='Calendar',
                          calendar=cal,
                          month=month,
                          year=year,
                          month_name=month_name,
                          entries=entry_dict)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile route"""
    # Get user statistics
    entry_count = MoodEntry.query.filter_by(user_id=current_user.id).count()
    
    # Get average mood score
    entries = MoodEntry.query.filter_by(user_id=current_user.id).all()
    avg_mood = sum(entry.mood_score for entry in entries) / entry_count if entry_count > 0 else 0
    
    # Get streak information (consecutive days with entries)
    streak = 0
    current_date = datetime.utcnow().date()
    
    # Check consecutive days
    while True:
        entry = MoodEntry.get_entry_by_date(current_user.id, current_date)
        if not entry:
            break
        streak += 1
        current_date -= timedelta(days=1)
    
    logger.info(f"User {current_user.username} viewed profile")
    
    return render_template('profile.html', 
                          title='Profile',
                          entry_count=entry_count,
                          avg_mood=round(avg_mood, 1),
                          streak=streak) 