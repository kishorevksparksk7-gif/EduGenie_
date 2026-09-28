import os
import json
import re
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MODEL_NAME = "gemini-3.8-flash"

app = FastAPI(title="EduGenie")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def _gen(prompt: str) -> str:
    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        return response.text.strip()
    except Exception as e:
        return f"API Error: {str(e)}"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/qa")
async def qa(question: str):
    return {"answer": _gen(question)}


@app.post("/explain")
async def explain(request: Request):
    data = await request.json()
    return {"explanation": _gen(f"Explain {data.get('topic','')} in simple terms for a student.")}


@app.post("/summarize")
async def summarize(request: Request):
    data = await request.json()
    return {"summary": _gen(f"Summarize in simple language:\n\n{data.get('text','')}")}


@app.post("/quiz")
async def quiz(request: Request):
    data = await request.json()
    prompt = f"""Create 3 MCQs from this passage. Return ONLY valid JSON:
[{{"question":"...","options":["A","B","C","D"],"answer":"A"}}]
Passage: {data.get('text','')}"""
    raw = _gen(prompt)
    if raw.startswith("API Error"):
        return {"quiz": [{"error": raw}]}
    try:
        raw = re.sub(r"```json|```", "", raw).strip()
        return {"quiz": json.loads(raw)}
    except Exception as e:
        return {"quiz": [{"error": str(e)}]}


@app.get("/learn/recommendations")
async def learn(topic: str):
    return {"topic": topic, "recommendation": _gen(f"Create a beginner-to-advanced learning path for {topic} with resources.")}