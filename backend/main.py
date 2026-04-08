import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Debugging Support Tool API")

# Enable CORS to allow the frontend to interact with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini SDK
api_key = os.getenv("GEMINI_API_KEY")
client = None
if api_key and api_key != "your_api_key_here":
    client = genai.Client(api_key=api_key)

class ErrorRequest(BaseModel):
    error_message: str
    code_snippet: str = ""

@app.post("/api/explain")
def explain_error(req: ErrorRequest):
    if not req.error_message.strip() and not req.code_snippet.strip():
        raise HTTPException(status_code=400, detail="Please provide an error message or a code snippet.")

    if not client:
        # Mock mode for immediate testing if no API key is provided
        import time
        time.sleep(1.5) # Simulate API latency
        
        detected_language = "Python" if "def " in req.code_snippet or "print(" in req.code_snippet else "Unknown"
        error_msg = req.error_message if req.error_message else "Syntax Error"
        
        return {
            "language": f"{detected_language} (Mock Mode)",
            "error_type": "Simulated Error",
            "severity": "Medium",
            "explanation": "This is a mock AI response because the GEMINI_API_KEY was not found in your .env file. Normally, our AI mentor would explain what this error means simply here.",
            "root_cause": f"In your snippet, the system noticed: '{error_msg}'. But this is just a dummy response.",
            "analogy": "Imagine trying to read a book in a language you don't know - that's how the computer feels without your API key! 🔑",
            "fixes": [
                "Open backend/.env",
                "Add your real GEMINI_API_KEY from Google AI Studio",
                "Restart the server to get actual AI debugging help!"
            ],
            "corrected_code": "# Mock Correction\n# Add your API key to get real code fixes!\n" + req.code_snippet,
            "prevention_tips": [
                "Always configure your environment variables.",
                "Check out the Google AI Studio for a free key."
            ],
            "did_you_mean": "Did you mean to add your API key first?"
        }

    prompt = f"""
You are an expert, beginner-friendly programming mentor. 
A student has encountered an error in their code.

Code Snippet provided:
```
{req.code_snippet}
```

Error Message provided:
```
{req.error_message}
```

Please analyze the error and the code. Determine the programming language automatically.
Return the response in a strict JSON format with exactly the following keys:
- "language": Detected programming language.
- "error_type": "Syntax Error", "Runtime Error", "Logical Error", or "Unknown".
- "severity": "Low", "Medium", or "High".
- "explanation": A very simple, beginner-friendly explanation of what the error means.
- "root_cause": What specifically caused this to happen in the provided code.
- "analogy": A real-world analogy to help the beginner understand the concept.
- "fixes": An array of step-by-step instructions (strings) to fix the error.
- "corrected_code": The full corrected code snippet.
- "prevention_tips": An array of short tips (strings) to avoid this error in the future.
- "did_you_mean": A brief suggestion of what they might have intended to do (optional, can be an empty string).

If the input is extremely unclear, ask a guiding follow-up question in the "explanation" field and leave the rest as N/A or empty.
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # We parse the json returned by Gemini
        parsed_data = json.loads(response.text)
        return parsed_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")

# Mount the frontend directory to serve the static HTML, CSS, JS files
import os as _os
frontend_path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "frontend"))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
