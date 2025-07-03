from neo4j import GraphDatabase
from memosynth.memory_schema import Memory

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

#create a node in neo4j
def create_memory_node(memory: Memory):
    with driver.session() as session:
        session.run(
    """
    MERGE (m:Memory {id: $id})
    SET m.summary = $summary
    """,
    {
        "id": memory.id,
        "summary": memory.summary
    }
)
    print(f"Memory node '{memory.id}' created in graph.")

def create_relationships():
    with driver.session() as session:
        session.run("""
            MATCH (a:Memory), (b:Memory)
            WHERE a.id <> b.id AND a.topic = b.topic
            MERGE (a)-[:RELATED_TO]->(b)
        """)
    print("Relationships created for shared topics.")


