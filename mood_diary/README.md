# Mood Diary Application

A web application for tracking daily mood and personal reflections.

## Features

- User authentication (register/login)
- Daily mood tracking with emoji/numeric ratings
- Calendar display with mood indicators
- Statistical data visualization (monthly and all-time)
- Personal user cabinet

## Installation

1. Clone the repository
2. Create and activate virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Initialize the database:
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
5. Run the application:
```
flask run
```

## Quality Metrics

- Modularity: Component-based architecture
- Test coverage: 80% code coverage with unit tests
- Code style: PEP8 compliant
- Recovery time: MTTR < 15 minutes
- Error rate: < 1 critical error per week
- Performance: < 2 second response time
- Security: Encrypted data, protection against common web attacks

## Testing

Run the test suite with:
```
pytest --cov=app
``` 