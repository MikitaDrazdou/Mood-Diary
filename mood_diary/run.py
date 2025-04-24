"""
Main entry point for the Mood Diary application
"""
from app import create_app, db
from app.models.user import User
from app.models.mood_entry import MoodEntry

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Provides key objects to flask shell"""
    return {'db': db, 'User': User, 'MoodEntry': MoodEntry}

if __name__ == '__main__':
    app.run(debug=True) 