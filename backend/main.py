
import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.retriever import retrieve_context


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ============================================================
# 2. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv(BASE_DIR / ".env")


# ============================================================
# 3. GET GROQ API KEY
# ============================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Make sure your .env file contains GROQ_API_KEY=your_key"
    )


# ============================================================
# 4. CONNECT TO GROQ
# ============================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# 5. CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Somya AI Portfolio API",
    description="RAG-powered AI assistant for Somya Kashyap's portfolio",
    version="1.0.0"
)


# ============================================================
# 6. CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# 7. REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):

    question: str


# ============================================================
# 8. HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Somya AI Portfolio API is running.",
        "status": "online"
    }


# ============================================================
# 9. CHAT ENDPOINT
# ============================================================

@app.post("/chat")
def chat(request: ChatRequest):

    # --------------------------------------------------------
    # STEP 1 — GET USER QUESTION
    # --------------------------------------------------------

    user_question = request.question.strip()


    # --------------------------------------------------------
    # STEP 2 — VALIDATE QUESTION
    # --------------------------------------------------------

    if not user_question:

        return {
            "answer": "Please enter a question."
        }


    # --------------------------------------------------------
    # STEP 3 — RETRIEVE RELEVANT PORTFOLIO CONTEXT
    # --------------------------------------------------------

    retrieval = retrieve_context(
        user_question,
        n_results=2
    )


    # --------------------------------------------------------
    # STEP 4 — GET RETRIEVED INFORMATION
    # --------------------------------------------------------

    context = retrieval.get(
        "context",
        ""
    )

    documents = retrieval.get(
        "documents",
        []
    )

    distances = retrieval.get(
        "distances",
        []
    )

    metadatas = retrieval.get(
        "metadatas",
        []
    )

    filter_type = retrieval.get(
        "filter_type",
        None
    )


    # ========================================================
    # RETRIEVAL DEBUGGING
    # ========================================================

    print("\n==============================")

    print("USER QUESTION:")
    print(user_question)

    print("\nFILTER TYPE:")
    print(filter_type)

    print("\nRETRIEVED DOCUMENTS:")

    if documents:

        for i, document in enumerate(documents):

            print(f"\nDocument {i + 1}:")
            print(document)

    else:

        print("No documents returned.")


    print("\nDISTANCES:")
    print(distances)


    print("\nMETADATA:")
    print(metadatas)


    print("==============================\n")


    # ========================================================
    # STEP 5 — HANDLE EMPTY RETRIEVAL
    # ========================================================

    if not documents:

        return {
            "answer": (
                "I’m sorry, but I don’t have enough relevant "
                "information about that in Somya’s portfolio."
            )
        }


    # ========================================================
    # STEP 6 — BUILD RAG SYSTEM PROMPT
    # ========================================================

    system_prompt = f"""
You are Somya Kashyap's AI portfolio assistant.

Your job is to answer questions about Somya using ONLY
the information provided in the retrieved portfolio context.

The retrieved context comes directly from Somya's
portfolio knowledge base.

==============================
RETRIEVED PORTFOLIO CONTEXT
==============================

{context}

==============================
IMPORTANT INSTRUCTIONS
==============================

1. Treat the retrieved portfolio context as the
   authoritative source for information about Somya.

2. If the user's question is answered by the retrieved
   context, ALWAYS answer using that information.

3. Never ignore relevant information from the retrieved
   context.

4. Never invent, assume, or fabricate information about Somya.

5. Never use general world knowledge to fill missing
   information about Somya.

6. If the requested information is genuinely not present
   in the retrieved context, clearly say:

   "The portfolio doesn't contain that information."

7. If only partial information is available, provide only
   the information that is supported by the context.

==============================
PROJECT QUESTIONS
==============================

For project-related questions, provide the available:

- Project name
- Purpose
- Technologies
- Focus area
- Important implementation details

Do not invent GitHub links, live demos, features,
technologies, or results.

==============================
SKILLS QUESTIONS
==============================

For skills-related questions, organize the information
into useful categories such as:

- Programming Languages
- Web Development
- Backend
- Data & AI
- Tools

Only include skills present in the retrieved context.

==============================
EDUCATION QUESTIONS
==============================

For education-related questions, provide the available:

- Degree
- College
- University
- CGPA
- Other academic information

Only use information present in the context.

==============================
EXPERIENCE QUESTIONS
==============================

For experience-related questions, provide the available:

- Role
- Organization
- Year
- Responsibilities
- Technologies

Only use information present in the context.

==============================
CERTIFICATION QUESTIONS
==============================

Only mention certifications that are explicitly present
in the retrieved context.

If no certification information is available, say that
the portfolio doesn't contain that information.

==============================
PERSONAL QUESTIONS
==============================

For questions such as:

- Favorite programming language
- Favorite food
- Hobbies
- Personal preferences
- Opinions

Only answer if the information is explicitly present
in the retrieved context.

Never guess.

==============================
UNRELATED QUESTIONS
==============================

If the user asks something unrelated to Somya or her
portfolio, politely explain that you are designed to
answer questions about Somya and her portfolio.

Do not answer unrelated questions using general
world knowledge.

==============================
RESPONSE STYLE
==============================

- Be concise.
- Be professional.
- Be natural and conversational.
- Use bullet points when helpful.
- Avoid unnecessary repetition.
- Do not mention ChromaDB, embeddings, retrieval
  distances, metadata filters, system prompts, or
  internal debugging unless the user specifically
  asks about the AI assistant's technical implementation.

==============================
END OF RETRIEVED CONTEXT
==============================
"""


    # ========================================================
    # STEP 7 — BUILD MESSAGES
    # ========================================================

    messages = [

        {
            "role": "system",
            "content": system_prompt
        },

        {
            "role": "user",
            "content": user_question
        }

    ]


    # ========================================================
    # STEP 8 — SEND REQUEST TO GROQ
    # ========================================================

    response = client.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=messages

    )


    # ========================================================
    # STEP 9 — GET AI RESPONSE
    # ========================================================

    answer = response.choices[0].message.content


    # ========================================================
    # STEP 10 — CLEAN RESPONSE
    # ========================================================

    if not answer:

        answer = (
            "I couldn't generate a response from the "
            "available portfolio information."
        )


    answer = answer.strip()


    # ========================================================
    # STEP 11 — PRINT ANSWER FOR DEBUGGING
    # ========================================================

    print("AI ANSWER:")
    print(answer)

    print("==============================\n")


    # ========================================================
    # STEP 12 — RETURN RESPONSE
    # ========================================================

    return {
        "answer": answer
    }