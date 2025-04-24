"""
Setup script for initializing the Mood Diary application
"""
import os
import secrets
from dotenv import load_dotenv
from app import create_app, db
from app.models.user import User
from app.models.mood_entry import MoodEntry

def setup_app():
    """Setup and initialize the application"""
    # Check if .env file exists, if not create one from example
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            # Create a new .env file from the example
            with open('.env.example', 'r') as example_file:
                example_content = example_file.read()
            
            # Generate a secure secret key
            secret_key = secrets.token_hex(16)
            env_content = example_content.replace('your_secure_secret_key_here', secret_key)
            
            with open('.env', 'w') as env_file:
                env_file.write(env_content)
            
            print("Created .env file with a secure secret key.")
        else:
            print("Warning: No .env or .env.example file found.")
    
    # Load environment variables
    load_dotenv()
    
    # Create the Flask app instance
    app = create_app()
    
    # Create database
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if there's at least one user in the database
        if User.query.count() == 0:
            print("No users found. Creating admin user...")
            admin = User(
                username='admin',
                email='admin@example.com',
                password='password'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created with username 'admin' and password 'password'")
            print("IMPORTANT: Change this password immediately after first login!")
    
    print("\nSetup complete! You can now run the application with:")
    print("flask run")
    
    return app

if __name__ == '__main__':
    setup_app() 