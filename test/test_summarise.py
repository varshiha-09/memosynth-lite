from memosynth.memory_client import summarize_memories
from memosynth.memory_client import load_memory

if __name__ == "__main__":
    memory = load_memory("config/sample_memory.json")
    results = [memory]  # Simulating a list of one or more memories

    summary = summarize_memories(results)
    print(" Generated Summary:")
    print(summary)
