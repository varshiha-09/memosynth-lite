import sys
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import duckdb
import pandas as pd

# Setup environment
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, query_memory, memory_exists_in_qdrant
from memosynth.graph_store import create_memory_node
from memosynth.memory_client import summarize_memories, diff, resolve
import pandas as pd
import duckdb
from memosynth.memory_client import real_llm_call
con = duckdb.connect("memory_timeline.db")
# Load memory file
memory_file = Path("config/all_memories.json")
if not memory_file.exists():
    raise FileNotFoundError("config/all_memories.json not found")

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
            print(f" Skipping existing memory: {memory.id}")
    except Exception as e:
        print(f"Skipped {mem_data.get('id', 'unknown')}: {e}")

print("\n Query: What are Q2 risks?")
results = query_memory("What are Q2 risks?", top_k=3)

# Print the results
for i, r in enumerate(results, 1):
    print(f"{i}. {r['summary']}")

# Convert to Memory objects
mem_objs = [Memory(**r) for r in results]

# Summarize
summary = summarize_memories(mem_objs)
print("\n Summary:\n", summary)

# Diff + Resolve
if len(mem_objs) >= 2:
    print("\n Diff Between Top 2 Results:")
    print(diff(mem_objs[0], mem_objs[1]))

    print("\n Resolved Contradiction:")
    print(resolve(mem_objs[0], mem_objs[1]))


query = """
SELECT summary, timestamp
FROM memory_log
WHERE summary ILIKE '%Q2%'
ORDER BY timestamp
"""
df = con.execute(query).fetchdf()

df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%B %d, %Y")

timeline_text = ""
for _, row in df.iterrows():
    timeline_text += f"- ({row['timestamp']}) {row['summary']}\n"

prompt = f"Summarize the following Q2-related events over time:\n{timeline_text}"
summary = real_llm_call(prompt)

print("Timeline Summary:")
print(summary)
