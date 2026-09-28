# EduGenie: Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant built with FastAPI.

## Features
- Q&A — ask academic questions
- Explain — simplified explanations of concepts
- Summarize — condense long passages
- Quiz Generator — create MCQs from any topic
- Learning Paths — structured recommendations

## Tech Stack
- FastAPI, Python
- Google Gemini (gemini-3.8-flash)
- HTML, CSS, Jinja2

## How to Run
1. Clone: `git clone https://github.com/YOUR_USERNAME/EduGenie.git`
2. `cd EduGenie`
3. `python -m venv venv`
4. `venv\Scripts\activate`
5. `python -m pip install -r requirements.txt`
6. Create `.env` with `GOOGLE_API_KEY=AIzaSy...`
7. `python -m uvicorn app.main:app --reload`
8. Open http://127.0.0.1:8000