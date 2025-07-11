import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, query_memory, memory_exists_in_qdrant
from memosynth.graph_store import create_memory_node,get_memory_links
from memosynth.memory_client import summarize_memories, diff, resolve,real_llm_call

memory_file = Path("config/news_memories.json")
if not memory_file.exists():
    raise FileNotFoundError("config/ai_news_memories.json not found")

with open(memory_file) as f:
    all_memories = json.load(f)

mem_objs = []
for mem_data in all_memories:
    try:
        memory = Memory(**mem_data)
        mem_objs.append(memory)

        if not memory_exists_in_qdrant(memory.id):
            write_memory(memory)
            create_memory_node(memory)
        else:
            print(f"Skipping existing memory: {memory.id}")
            
    except Exception as e:
        print(f" Skipped {mem_data.get('id', 'unknown')}: {e}")

print("\n Query: What's trending in AI?")
results = query_memory("What's trending in AI?", top_k=5, topic="AI")
queried_mems = [Memory(**r) for r in results]

memory_ids = [r["id"] for r in results]
combined_text = "\n".join([f"- {r['summary']}" for r in results])
cleaned_summary = real_llm_call(f"Summarize these points into one paragraph:\n{combined_text}")
print("\n Summary:\n", cleaned_summary)
if len(queried_mems) >= 2:
    print("\n Diff Between Top 2 Results:")
    print(diff(queried_mems[0], queried_mems[1]))

    print("\n Resolved Contradiction:")
    print(resolve(queried_mems[0], queried_mems[1]))
