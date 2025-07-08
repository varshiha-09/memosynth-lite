from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from sentence_transformers import SentenceTransformer
from memosynth.memory_schema import Memory
import uuid
from memosynth.timeline_store import log_memory
from qdrant_client.models import Filter, FieldCondition, MatchValue

client = QdrantClient("http://localhost:6333")

model = SentenceTransformer("all-mpnet-base-v2")

existing_collections = [col.name for col in client.get_collections().collections]
if "memos" not in existing_collections:
    client.create_collection(
        collection_name="memos",
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
def write_memory(memory: Memory):
    vector = model.encode(memory.summary).tolist()
    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload=memory.model_dump()
    )
    client.upsert(collection_name="memos", points=[point])
    log_memory(memory)  
    print("Memory written to Qdrant and timeline.")

def query_memory(prompt: str, top_k: int = 5, topic: str = None, min_score: float = 0.2):
    vector = model.encode(prompt).tolist()

    query_filter = None
    if topic:
        query_filter = Filter(
            must=[FieldCondition(key="topic", match=MatchValue(value=topic))]
        )

    results = client.search(
        collection_name="memos",
        query_vector=vector,
        limit=top_k,
        query_filter=query_filter
    )

    for res in results:
        print(f"Score: {res.score:.4f} | Summary: {res.payload.get('summary')}")
    filtered = [r.payload for r in results if r.score and r.score >= min_score]
    if not filtered:
        print("All results were below the min_score threshold.")
    return filtered

def memory_exists_in_qdrant(memory_id: str) -> bool:
    try:
        result, _ = client.scroll(
            collection_name="memos",
            scroll_filter=Filter(
                must=[FieldCondition(key="id", match=MatchValue(value=memory_id))]
            ),
            limit=1
        )
        return len(result) > 0
    except Exception as e:
        print(f"Qdrant check failed for ID {memory_id}: {e}")
        return False
