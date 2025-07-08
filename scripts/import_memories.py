import sys
import json
from pathlib import Path
from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, client
from memosynth.graph_store import create_memory_node
from qdrant_client.models import Filter, FieldCondition, MatchValue

sys.path.append(str(Path(__file__).resolve().parents[1]))

config_dir = Path("config")
json_files = list(config_dir.glob("*.json"))
print(f"Found {len(json_files)} memory files.")

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

for file in json_files:
    try:
        with open(file) as f:
            data = json.load(f)
        memories = data if isinstance(data, list) else [data]

        for mem_data in memories:
            try:
                memory = Memory(**mem_data)

                if memory_exists_in_qdrant(memory.id):
                    print(f"⏭Skipping duplicate memory ID: {memory.id}")
                    continue

                write_memory(memory)
                create_memory_node(memory)
                print(f"Imported memory: {memory.id}")

            except Exception as e:
                print(f"Failed to load memory in {file.name}: {e}")

    except Exception as e:
        print(f"Skipped {file.name}: {e}")

print(" Done importing all unique memories.")
