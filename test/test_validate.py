import json
from pathlib import Path
from memosynth.memory_schema import Memory
from pydantic import ValidationError

def validate_all_memories(folder="config"):
    folder_path = Path(folder)
    json_files = list(folder_path.glob("*.json"))

    print(f"Validating {len(json_files)} memory files\n")

    valid_count = 0
    for file in json_files:
        try:
            with open(file) as f:
                data = json.load(f)
            memory = Memory(**data)
            valid_count += 1
        except ValidationError as ve:
            print(f"Validation failed: {file.name}")
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    print(f"Valid files: {valid_count}/{len(json_files)}")

if __name__ == "__main__":
    validate_all_memories()
