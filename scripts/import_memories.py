from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, client  # Qdrant client and write function
from qdrant_client.models import Filter, FieldCondition, MatchValue
from pathlib import Path
import json
from memosynth.graph_store import create_memory_node


config_dir = Path("config")
json_files = list(config_dir.glob("*.json"))

print(f"Found {len(json_files)} memory files.")

def memory_exists_in_qdrant(memory_id: str) -> bool:
    """Check if a memory with this ID already exists in Qdrant."""
    try:
        result, _ = client.scroll(
            collection_name="memos",
            scroll_filter=Filter(
                must=[
                    FieldCondition(key="id", match=MatchValue(value=memory_id))
                ]
            ),
            limit=1
        )
        return len(result) > 0
    except Exception as e:
        print(f"Qdrant check failed for ID {memory_id}: {e}")
        return False

for file in json_files:
    try:
        with open(file) as f:
            data = json.load(f)
        memory = Memory(**data)

        if memory_exists_in_qdrant(memory.id):
            print(f"Skipping duplicate memory ID: {memory.id}")
            continue

        write_memory(memory)
        create_memory_node(memory)


    except Exception as e:
        print(f"Skipped {file.name}: {e}")

print("Done importing all unique memories.")
