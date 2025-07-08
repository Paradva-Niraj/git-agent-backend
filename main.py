from fastapi import FastAPI, Request
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class DiffRequest(BaseModel):
    diff: str

@app.post("/generate-commit")
async def generate_commit(data: DiffRequest):
    prompt = f"""You are an assistant that writes helpful Git commit messages not do much process just analys this different and give a normal commit message with just half line not much more in responce.

Here is a git diff of staged changes:

{data.diff}

Write a concise, meaningful commit message:
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return {"message": response.text.strip()}
    except Exception as e:
        return {"error": str(e)}
