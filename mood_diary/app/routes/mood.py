"""
Routes for mood entries and statistics
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.mood_entry import MoodEntry
from app.forms import MoodEntryForm
from datetime import datetime
import calendar
import logging
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# Configure logger
logger = logging.getLogger(__name__)

# Create blueprint
mood_bp = Blueprint('mood', __name__, url_prefix='/mood')

@mood_bp.route('/entry/<string:date_str>', methods=['GET', 'POST'])
@login_required
def entry(date_str):
    """Route for creating or updating a mood entry"""
    try:
        # Parse the date string
        entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if entry already exists for this date
    existing_entry = MoodEntry.get_entry_by_date(current_user.id, entry_date)
    
    form = MoodEntryForm()
    
    # Set the date field for both GET and POST requests
    form.date.data = entry_date
    
    if request.method == 'GET':
        if existing_entry:
            # Pre-populate form with existing data
            form.mood_score.data = existing_entry.mood_score
            form.emoji.data = existing_entry.emoji
            form.notes.data = existing_entry.notes
            form.activities.data = existing_entry.activities
    
    if form.validate_on_submit():
        if existing_entry:
            # Update existing entry
            existing_entry.update(
                mood_score=form.mood_score.data,
                emoji=form.emoji.data,
                notes=form.notes.data,
                activities=form.activities.data
            )
            db.session.commit()
            logger.info(f"User {current_user.username} updated mood entry for {date_str}")
            flash('Mood entry updated successfully!', 'success')
        else:
            # Create new entry
            new_entry = MoodEntry(
                user_id=current_user.id,
                date=form.date.data,
                mood_score=form.mood_score.data,
                emoji=form.emoji.data,
                notes=form.notes.data,
                activities=form.activities.data
            )
            db.session.add(new_entry)
            db.session.commit()
            logger.info(f"User {current_user.username} created new mood entry for {date_str}")
            flash('Mood entry saved successfully!', 'success')
        
        return redirect(url_for('main.index'))
    
    return render_template('mood/entry.html',
                          title=f'Mood Entry for {date_str}',
                          form=form,
                          date_str=date_str,
                          existing_entry=existing_entry)

@mood_bp.route('/stats')
@login_required
def stats():
    """Statistics and visualization route"""
    # Get all user's mood entries
    entries = MoodEntry.query.filter_by(user_id=current_user.id).order_by(MoodEntry.date).all()
    
    if not entries:
        flash('You need to add some mood entries first!', 'info')
        return redirect(url_for('main.index'))
    
    # Calculate statistics in Python instead of the template
    total_entries = len(entries)
    total_score = sum(entry.mood_score for entry in entries)
    avg_score = total_score / total_entries if total_entries > 0 else 0
    max_score = max(entry.mood_score for entry in entries) if entries else 0
    min_score = min(entry.mood_score for entry in entries) if entries else 0
    
    # Process emoji counts
    emoji_counts = {}
    for entry in entries:
        if entry.emoji in emoji_counts:
            emoji_counts[entry.emoji] += 1
        else:
            emoji_counts[entry.emoji] = 1
    
    # Process activity counts
    activity_counts = {}
    for entry in entries:
        if entry.activities:
            for activity in entry.activities.split(','):
                activity = activity.strip()
                if activity:
                    if activity in activity_counts:
                        activity_counts[activity] += 1
                    else:
                        activity_counts[activity] = 1
    
    # Sort activities by count
    sorted_activities = sorted(activity_counts.items(), key=lambda x: x[1], reverse=True)
    top_activities = sorted_activities[:5] if sorted_activities else []
    
    # Create DataFrame for analysis
    data = {
        'date': [entry.date for entry in entries],
        'mood_score': [entry.mood_score for entry in entries],
        'emoji': [entry.emoji for entry in entries]
    }
    df = pd.DataFrame(data)
    
    # Convert date column to datetime type
    df['date'] = pd.to_datetime(df['date'])
    
    # Monthly average mood
    monthly_avg = df.set_index('date').resample('M')['mood_score'].mean().reset_index()
    monthly_avg['month_year'] = monthly_avg['date'].dt.strftime('%b %Y')
    
    # Create monthly average chart
    plt.figure(figsize=(10, 6))
    plt.plot(monthly_avg['month_year'], monthly_avg['mood_score'], marker='o')
    plt.title('Monthly Average Mood')
    plt.xlabel('Month')
    plt.ylabel('Average Mood Score')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save plot to a buffer
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.getvalue()).decode('utf-8')
    plt.close()
    
    logger.info(f"User {current_user.username} viewed mood statistics")
    
    return render_template('mood/stats.html',
                          title='Mood Statistics',
                          entries=entries,
                          img_data=img_data,
                          total_entries=total_entries,
                          avg_score=avg_score,
                          max_score=max_score,
                          min_score=min_score,
                          emoji_counts=emoji_counts,
                          top_activities=top_activities)

@mood_bp.route('/api/monthly_data/<int:year>/<int:month>')
@login_required
def monthly_data(year, month):
    """API endpoint for getting monthly mood data"""
    entries = MoodEntry.get_monthly_entries(current_user.id, year, month)
    data = [
        {
            'date': entry.date.strftime('%Y-%m-%d'),
            'mood_score': entry.mood_score,
            'emoji': entry.emoji
        }
        for entry in entries
    ]
    return jsonify(data) 