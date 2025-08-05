from fastapi import FastAPI
from pydantic import BaseModel
from chatgpt import ask_gpt2

class Query(BaseModel):
    question: str

app = FastAPI()

@app.post("/ask")
def ask(q: Query):
    return {"answer": ask_gpt2(q.question)}
