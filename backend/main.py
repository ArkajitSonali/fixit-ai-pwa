import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

# This allows your Vercel frontend to talk to this Render backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

class ErrorRequest(BaseModel):
    error_message: str
    code_snippet: str = None

@app.post("/explain")
async def explain_error(request: ErrorRequest):
    prompt = f"Explain this error: {request.error_message}\nCode: {request.code_snippet}"
    response = model.generate_content(prompt)
    return {"explanation": response.text}

@app.get("/")
async def root():
    return {"message": "Backend is running!"}