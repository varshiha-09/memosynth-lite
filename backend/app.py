from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sys, os, uuid
from datetime import datetime

from memosynth.memory_schema import Memory
from memosynth.vector_store import query_memory, write_memory, memory_exists_in_qdrant
from memosynth.memory_client import summarize_memories, real_llm_call
from memosynth.graph_store import create_memory_node, driver

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    message: str

@app.post("/chat")
def chat_with_memory(query: ChatQuery):
    results = query_memory(query.message, top_k=5, min_score=0.3)

    if not results:
        return {
            "response": "I couldn't find anything relevant in memory for that. Try asking something else?",
            "relevant_memories": []
        }

    memory_objects = [Memory(**r) for r in results if r.get("summary")]
    all_summaries = "\n".join([m.summary for m in memory_objects])
    prompt = (
        f"You are an assistant that only responds based on the following memory summaries:\n\n"
        f"{all_summaries}\n\n"
        f"Now answer this user question strictly using the summaries above:\n{query.message}"
    )
    response = real_llm_call(prompt)

    return {
        "response": response,
        "relevant_memories": results
    }


@app.post("/add_memories")
async def add_manual_memories(data: dict):
    summaries = data.get("summaries", [])
    created = []
    
    for s in summaries:
        if not s.strip():
            continue
        mem = Memory(
            id=str(uuid.uuid4()),
            project="memosynth",
            agent="user_input",
            summary=s.strip(),
            type="insight",
            tags=[],
            source="manual",
            author="user",
            created_at=str(datetime.now().date()),
            version=1,
            confidence=0.9,
            visibility="project",
            sensitivity="medium",
            topic="manual"
        )
        if not memory_exists_in_qdrant(mem.id):
            write_memory(mem)
            create_memory_node(mem)
            created.append(mem.id)
    
    return {"status": "success", "memories_created": len(created)}
