import duckdb
from memosynth.memory_schema import Memory

con = duckdb.connect("memory_timeline.db")

def init_timeline_table():
    con.execute("""
        CREATE TABLE IF NOT EXISTS memory_log (
            id TEXT,
            summary TEXT,
            timestamp TEXT,
            version INT
        )
    """)

def log_memory(memory: Memory):
    exists = con.execute(
        "SELECT COUNT(*) FROM memory_log WHERE id = ?",
        (memory.id,)
    ).fetchone()[0]

    if exists:
        print(f"Skipping log for existing memory: {memory.id}")
        return

    con.execute(
        "INSERT INTO memory_log VALUES (?, ?, ?, ?)",
        (memory.id, memory.summary, str(memory.created_at), memory.version)
    )
    print(f" Logged memory: {memory.id}")
