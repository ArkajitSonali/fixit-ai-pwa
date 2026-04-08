import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
app = FastAPI()

# Enable CORS so Vercel can talk to Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

class ErrorRequest(BaseModel):
    error_message: str
    code_snippet: str = None

@app.post("/explain")
async def explain_error(request: ErrorRequest):
    try:
        prompt = f"Explain this error briefly and suggest a fix:\nError: {request.error_message}\nCode: {request.code_snippet}"
        response = model.generate_content(prompt)
        return {"explanation": response.text}
    except Exception as e:
        return {"explanation": f"AI Error: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "DebugAI Backend is Live!"}