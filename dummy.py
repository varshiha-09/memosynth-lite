from qdrant_client import QdrantClient

client = QdrantClient("http://localhost:6333")
client.delete_collection(collection_name="memos")
print(" Qdrant collection cleared.")

results, _ = client.scroll(collection_name="memos", limit=5)
for r in results:
    print(r.payload)

