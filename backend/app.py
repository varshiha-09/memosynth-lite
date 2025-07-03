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
from fastapi.responses import JSONResponse
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
    results = query_memory(query.message, top_k=5, min_score=0.3)

    if not results:
        return {
            "response": "🤔 I couldn't find anything relevant in memory for that. Try asking something else?",
            "relevant_memories": []
        }

    memory_objects = [Memory(**r) for r in results if r.get("summary")]

    # Build a safe prompt with instruction
    all_summaries = "\n".join([m.summary for m in memory_objects])
    prompt = (
        f"You are an assistant that only responds based on the following memory summaries:\n\n"
        f"{all_summaries}\n\n"
        f"Now answer this user question strictly using the summaries above:\n{query.message}"
    )

    # Call the model
    from memosynth.memory_client import real_llm_call
    response = real_llm_call(prompt)

    return {
        "response": response,
        "relevant_memories": results
    }


@app.get("/graph")
def get_graph():
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Memory)-[r:RELATED_TO]->(b:Memory)
            RETURN a.id AS source, b.id AS target
        """)
        edges = [{"source": record["source"], "target": record["target"]} for record in result]
        
        # Get node data
        result = session.run("MATCH (m:Memory) RETURN m.id AS id, m.summary AS summary")
        nodes = [{"id": record["id"], "label": record["summary"][:40]} for record in result]

    return JSONResponse(content={"nodes": nodes, "links": edges})