# FitBuddy – AI Fitness Plan Generator

FastAPI + Jinja2 + SQLite educational project with Google Gemini integration.

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Run:
```bash
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000

## Features
- User input form
- AI-generated 7-day general wellness/workout plan
- Nutrition/recovery tip
- Feedback-based plan update
- SQLite database
- User/admin view
- GitHub-ready structure

Never upload your real API key to GitHub.
