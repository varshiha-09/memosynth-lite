from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys, os
import sys, os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from memosynth.memory_schema import Memory
from memosynth.vector_store import query_memory
from memosynth.memory_client import summarize_memories

# So it can find your memosynth module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from memosynth.vector_store import query_memory  # you already have write_memory if needed

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    message: str

@app.post("/chat")
def chat_with_memory(query: ChatQuery):
    results = query_memory(query.message, top_k=3)

    if not results:
        return {"response": "I couldn't find anything relevant in memory."}

    memory_objects = [Memory(**r) for r in results if r.get("summary")]
    response = summarize_memories(memory_objects)

    return {
        "response": response,
        "relevant_memories": results
    }
