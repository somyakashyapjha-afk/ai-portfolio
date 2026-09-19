import os
import json

from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# -----------------------------------
# 1. Load candidate information
# -----------------------------------

with open("../candidate.json", "r") as file:
    candidate = json.load(file)


# -----------------------------------
# 2. Load environment variables
# -----------------------------------

load_dotenv()


# -----------------------------------
# 3. Connect to Groq
# -----------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------------
# 4. Create FastAPI application
# -----------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# 5. Define the data we receive
# -----------------------------------

class ChatRequest(BaseModel):
    question: str


# -----------------------------------
# 6. Create our /chat endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": "system",
            "content": f"""
You are the AI assistant for Somya Kashyap's developer portfolio.

Use the following candidate information to answer questions:

{candidate}

Rules:
- Only use the information provided above.
- Do not invent skills, projects, experience, or achievements.
- If the information is not available, say that you don't have that information.
- Answer clearly and professionally.
"""
        },
        {
            "role": "user",
            "content": request.question
        }
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer
    }