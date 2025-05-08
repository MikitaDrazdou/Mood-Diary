# Mood Diary

[![CI](https://github.com/MikitaDrazdou/Mood-Diary/actions/workflows/main.yml/badge.svg)](https://github.com/MikitaDrazdou/Mood-Diary/actions/workflows/main.yml)

A modern Mood Diary application for tracking and analyzing your mood, built with FastAPI (backend), Streamlit (frontend), and SQLite. All dependencies are managed with Poetry. The project is modular, fully tested, and includes automated quality gates.

## Environment Variables

Create a `.env` file in the project root to store environment variables.  
The backend will automatically load variables from `.env` on startup.

## Features
- User registration and login
- Mood entry with emoji, notes, and activities
- Calendar view with mood chart
- Mood statistics and analytics
- Modern, user-friendly UI (Streamlit)
- FastAPI backend with SQLite and SQLAlchemy
- Automated tests, linting, and security checks

## Project Structure
```
app/
  fastapi_app.py           # FastAPI backend entry point
  fastapi_schemas.py       # Pydantic schemas for API
  models/                  # SQLAlchemy models
  streamlit_frontend/
    main.py                # Streamlit frontend entry point
    pages/                 # Streamlit pages (dashboard, auth, calendar, stats)
    components/            # UI components (sidebar, forms, etc.)
    utils.py               # Shared utilities
tests/
  unit/                    # Unit tests (pytest, all dependencies mocked)
  integration/             # Integration tests (TestClient, real DB, etc.)
  fuzz/                    # Fuzz tests (Hypothesis)
  load/                    # Load tests (Locust)
pyproject.toml             # Poetry dependencies
README.md
```

## Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/MikitaDrazdou/Mood-Diary.git
   cd Mood-Diary
   ```
2. **Install Poetry (if not installed):**
   ```bash
   pip install poetry
   ```
3. **Install dependencies:**
   ```bash
   poetry install
   ```

## Running the Backend (FastAPI)
1. **Start the FastAPI server:**
   ```bash
   poetry run uvicorn app.fastapi_app:app --reload
   ```
   - The backend will be available at [http://localhost:8000](http://localhost:8000)
   - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running the Frontend (Streamlit)
**Always run from the project root!**
1. **In a new terminal:**
   ```bash
   poetry run streamlit run app/streamlit_frontend/main.py
   ```
   - The frontend will be available at [http://localhost:8501](http://localhost:8501)

## Quality Gates & Development
- **Unit tests:**
  ```bash
  poetry run pytest tests/unit
  ```
- **Integration tests:**
  ```bash
  poetry run pytest tests/integration
  ```
- **Fuzz tests:**
  ```bash
  poetry run pytest tests/fuzz
  ```
- **Linting:**
  ```bash
  poetry run ruff check .
  ```
- **Security checks:**
  ```bash
  poetry run bandit -r app/ --severity-level high
  ```
- **Type checking:**
  ```bash
  poetry run mypy app/
  ```
- **Load testing:**
  ```bash
  poetry run locust -f tests/load/locustfile.py --headless --users 10 --spawn-rate 1 --run-time 1m --host http://localhost:8000
  ```

## Troubleshooting
- Make sure both backend (FastAPI) and frontend (Streamlit) are running.
- If you change backend endpoints, restart both servers.
- For database issues, delete `mood_diary.db` to reset (will lose all data).
- If you see import errors, check that you are running from the project root and using Poetry shell.

## License
MIT 