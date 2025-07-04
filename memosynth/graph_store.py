from neo4j import GraphDatabase
from memosynth.memory_schema import Memory

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "test1234"))

def create_memory_node(memory: Memory):
    with driver.session() as session:
        session.run(
            """
            MERGE (m:Memory {id: $id})
            SET m.summary = $summary,
                m.topic = $topic
            """,
            {
                "id": memory.id,
                "summary": memory.summary,
                "topic": memory.topic
            }
        )
    print(f"Memory node '{memory.id}' with topic '{memory.topic}' created in graph.")

def create_relationships():
    with driver.session() as session:
        session.run("""
            MATCH (a:Memory), (b:Memory)
            WHERE a.id <> b.id AND a.topic = b.topic
            MERGE (a)-[:RELATED_TO]->(b)
        """)
    print("Relationships created for shared topics.")

def get_memory_links(memory_ids: list[str]):
    with driver.session() as session:
        result = session.run("""
            MATCH (a:Memory)-[r]->(b:Memory)
            WHERE a.id IN $ids
            RETURN a.id AS source, b.id AS target, type(r) AS relation
        """, {"ids": memory_ids})
        return [dict(record) for record in result]
