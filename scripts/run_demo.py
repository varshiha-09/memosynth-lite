import os
import sys
import json
from pathlib import Path
import warnings
import duckdb
import pandas as pd
from dotenv import load_dotenv

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore")

load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, query_memory, memory_exists_in_qdrant
from memosynth.graph_store import create_memory_node
from memosynth.memory_client import summarize_memories, diff, resolve, real_llm_call

con = duckdb.connect("memory_timeline.db")

memory_file = Path("config/all_memories.json")
if not memory_file.exists():
    raise FileNotFoundError("config/all_memories.json not found")

with open(memory_file) as f:
    all_memories = json.load(f)

for mem_data in all_memories:
    try:
        memory = Memory(**mem_data)
        if memory_exists_in_qdrant(memory.id):
            print(f"Skipping existing memory: {memory.id}")
            continue
        write_memory(memory)
        create_memory_node(memory)
    except Exception as e:
        print(f"Skipped {mem_data.get('id', 'unknown')}: {e}")

query_text = "What are Q2 insights?"
print(f"\nQuery: {query_text}")
results = query_memory(query_text, top_k=3)

combined_text = "\n".join([f"- {r['summary']}" for r in results])
cleaned_summary = real_llm_call(f"Summarize these points into one paragraph:\n{combined_text}")
print("\n Summary:\n", cleaned_summary)

queried_objs = [Memory(**r) for r in results]
if len(queried_objs) >= 2:
    print("\nDiff Between Top 2 Results:")
    print(diff(queried_objs[0], queried_objs[1]))
    print("\nResolved Contradiction:")
    print(resolve(queried_objs[0], queried_objs[1]))

# Timeline summary
timeline_query = """
SELECT summary, timestamp
FROM memory_log
WHERE summary ILIKE '%Q2%'
ORDER BY timestamp
"""
df = con.execute(timeline_query).fetchdf()
df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%B %d, %Y")

timeline_text = "\n".join(f"- ({row['timestamp']}) {row['summary']}" for _, row in df.iterrows())
timeline_prompt = f"Summarize the following Q2-related events over time:\n{timeline_text}"
timeline_summary = real_llm_call(timeline_prompt)

print("\nTimeline Summary:\n")
print(timeline_summary)
