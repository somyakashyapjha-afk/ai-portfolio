
import os
from pathlib import Path

from dotenv import load_dotenv
from backend.retriever import retrieve_context

from groq import Groq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# -----------------------------------
# 1. Paths and environment
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# -----------------------------------
# 2. Connect to Groq
# -----------------------------------

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# -----------------------------------
# 3. Create FastAPI application
# -----------------------------------

app = FastAPI()


# -----------------------------------
# 4. CORS
# -----------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
# 5. Request model
# -----------------------------------

class ChatRequest(BaseModel):
    question: str


# -----------------------------------
# 6. Chat endpoint
# -----------------------------------

@app.post("/chat")
def chat(request: ChatRequest):

    # Get user's question
    user_question = request.question


    # Retrieve relevant context
    retrieval = retrieve_context(
        user_question,
        n_results=2
    )

    context = retrieval["context"]


    # Build RAG prompt
    messages = [
        {
            "role": "system",
            "content": f"""
You are the AI assistant for Somya Kashyap's developer portfolio.

Use the retrieved portfolio context below to answer
the user's question.

Retrieved portfolio context:

{context}

Rules:
- Use the retrieved context as your primary source.
- Do not invent skills, projects, experience, academics,
  certifications, or achievements.
- If the requested information is not available in the
  retrieved context, say that you don't have that information.
- Answer clearly and professionally.
"""
        },
        {
            "role": "user",
            "content": user_question
        }
    ]


    # Send context + question to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages
    )


    # Get AI response
    answer = response.choices[0].message.content


    # Return answer
    return {
        "answer": answer
    }