# Debugging Support Tool (Error Explanation System)

A smart, AI-powered mentor application designed to help beginners and students easily understand programming errors, identify root causes, and learn how to fix them!

## Features
- **Beginner-Friendly Explanations**: Converts cryptic terminal errors into easy-to-understand language.
- **Root Cause & Fixes**: Identifies exactly what went wrong and provides a step-by-step resolution.
- **Real-World Analogies**: Employs relatable analogies to teach programming concepts.
- **Automatic Language Detection**: Detects the language structure automatically without user selection.
- **History Tracking**: Keeps track of recent errors in your local session.
- **One-Click Copy**: Corrected code is readily available to be copied.

## Tech Stack
- Frontend: HTML, Vanilla CSS (Modern Interface with Dark Mode), JavaScript (Vanilla)
- Backend: Python 3.10+, FastAPI (with `uvicorn` and `cors` support)
- AI Model: Google Gemini API via `google-genai`

## Setup & Run Instructions

### 1. Prerequisites
- Python 3.10+ installed
- Google Gemini API Key. You can get one from [Google AI Studio](https://aistudio.google.com/).

### 2. Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables:
   - Copy `.env.example` and rename to `.env`.
   - Update the placeholder with your actual API key.
   ```bash
   cp .env.example .env
   ```
4. Start the backend DEV server:
   ```bash
   uvicorn main:app --reload
   ```
   *The server should run at http://127.0.0.1:8000.*

### 3. Frontend Setup
The frontend uses standard web files, so no bundler setup is needed! 
- Simply open `frontend/index.html` directly in any web browser, OR serve it using a lightweight Python HTTP server via:
  ```bash
  cd frontend
  python -m http.server 3000
  ```
  Then visit `http://localhost:3000`

## Developer Notes
- Change the frontend API endpoint inside `frontend/script.js` (look for `const API_URL = "http://127.0.0.1:8000/api/explain";`) if your Python server is running on a different port or in production.
