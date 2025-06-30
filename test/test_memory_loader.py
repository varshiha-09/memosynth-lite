# test/test_memory_loader.py

from memosynth.memory_client import load_memory

if __name__ == "__main__":
    memory = load_memory("config/sample_memory.json")
    print("Memory loaded and validated successfully!")
    print(memory.model_dump_json(indent=2))

