from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")

collections = client.get_collections()
print("Collections in Qdrant:")
for col in collections.collections:
    print("-", col.name)

collection_name = "memos"  
info = client.get_collection(collection_name=collection_name)

print(f"Collection '{collection_name}' has {info.points_count} points.")
result, _ = client.scroll(collection_name="memos", limit=5)
for r in result:
    print(r.payload.get("summary", ""), getattr(r, "score", "No Score"))
