"""
app.py

Defines the FastAPI application exposing a simple /ask endpoint for GPT-2.
"""
from fastapi import FastAPI
from pydantic import BaseModel

from chatgpt import ask_gpt2


class Query(BaseModel):
    """
    Pydantic model for request payload containing the question.
    """

    question: str


app = FastAPI()


@app.post("/ask")
def ask(q: Query):
    """
    Handle POST requests to /ask: forwards the question to GPT-2 and returns the answer.

    Args:
        q: Query model with the user's question.

    Returns:
        A dict with the generated 'answer' string.
    """
    return {"answer": ask_gpt2(q.question)}
