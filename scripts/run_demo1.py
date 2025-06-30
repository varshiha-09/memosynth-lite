import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Setup environment and path
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

from memosynth.memory_schema import Memory
from memosynth.vector_store import query_memory
from memosynth.memory_client import summarize_memories, diff, resolve

print("\n🔍 Query: How is AI affecting the job market?")

# 🔍 Step 1: Query with topic filter (IMPORTANT)
results = query_memory("Which companies are using AI?", top_k=3, topic="AI")

if not results:
    print(" No relevant results found.")
    sys.exit()

print("\n🔎 Top Matches:")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['summary']}")

mem_objs = [Memory(**r) for r in results]

summary = summarize_memories(mem_objs)
print("\n Summary:")
print(summary)

# ⚖️ Step 4: Diff + Resolve if there are at least two different summaries
if len(mem_objs) >= 2:
    print("\n🔀 Diff Between Top 2 Results:")
    print(diff(mem_objs[0], mem_objs[1]))

    print("\n🤖 Resolved Contradiction:")
    print(resolve(mem_objs[0], mem_objs[1]))
else:
    print("\n Not enough results to compare differences.")
