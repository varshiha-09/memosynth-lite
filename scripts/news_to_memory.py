import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import os
import json
import requests
import hashlib
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from transformers import pipeline
from memosynth.memory_schema import Memory
from memosynth.vector_store import write_memory, client
from memosynth.graph_store import create_memory_node
from qdrant_client.models import Filter, FieldCondition, MatchValue
from memosynth.timeline_store import init_timeline_table
# Load environment variables
load_dotenv()
API_KEY = os.getenv("NEWSDATA_API_KEY")
if not API_KEY:
    raise ValueError("Missing NEWSDATA_API_KEY in .env")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
config_dir = Path("config")
config_dir.mkdir(exist_ok=True)
memory_file = config_dir / "news_memories.json"

init_timeline_table()
def fetch_ai_news(api_key, limit=20):
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q=artificial+intelligence+OR+AI&language=en&category=technology,science"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    relevant_articles = []
    keywords = ["AI", "artificial intelligence", "machine learning", "deep learning", "generative AI"]

    for article in data.get("results", []):
        content = f"{article.get('title') or ''} {article.get('description') or ''}".lower()
        if any(kw.lower() in content for kw in keywords):
            relevant_articles.append(article)
        if len(relevant_articles) >= limit:
            break

    return relevant_articles


def summarize_article(description, title):
    text = description or title or ""
    if not text:
        return "No summary available."
    result = summarizer(text, max_length=60, min_length=20, do_sample=False)
    return result[0]["summary_text"]

def generate_unique_id(article):
    base = (article.get("title") or "") + (article.get("pubDate") or "")
    return "m-news-ai-" + hashlib.md5(base.encode()).hexdigest()[:8]

def generate_memory(article):
    summary = summarize_article(article.get("description"), article.get("title"))
    memory_id = generate_unique_id(article)
    return memory_id, {
        "id": memory_id,
        "project": "news_tracker",
        "agent": "news_bot",
        "summary": summary,
        "type": "insight",
        "tags": ["AI"],
        "source": article.get("source_id") or "unknown",
        "author": "news_bot",
        "created_at": article.get("pubDate", str(datetime.now().date()))[:10],
        "version": 1,
        "confidence": 0.9,
        "visibility": "project",
        "sensitivity": "low",
        "topic": "AI"
    }


def save_all_memories(memories, file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            try:
                existing = json.load(f)
            except json.JSONDecodeError:
                existing = []
    else:
        existing = []

    existing_ids = {mem["id"] for mem in existing}
    new_memories = [mem for mem in memories if mem["id"] not in existing_ids]

    if not new_memories:
        print("No new memories to add.")
        return

    existing.extend(new_memories)

    with open(file_path, "w") as f:
        json.dump(existing, f, indent=2)

    print(f" Added {len(new_memories)} new memories to {file_path.name}")


def memory_exists_in_qdrant(memory_id: str) -> bool:
    try:
        result, _ = client.scroll(
            collection_name="memos",
            scroll_filter=Filter(
                must=[FieldCondition(key="id", match=MatchValue(value=memory_id))]
            ),
            limit=1
        )
        return len(result) > 0
    except Exception as e:
        print(f"Qdrant check failed for ID {memory_id}: {e}")
        return False

def import_to_qdrant_and_graph(memory_list):
    added = 0
    for data in memory_list:
        try:
            memory = Memory(**data)
            if memory_exists_in_qdrant(memory.id):
                print(f" Skipping existing memory in Qdrant: {memory.id}")
                continue
            write_memory(memory)
            create_memory_node(memory)
            added += 1
        except Exception as e:
            print(f" Skipped memory ID {data.get('id', 'unknown')}: {e}")
    print(f"Imported {added} memories to Qdrant and Neo4j")


def main():
    print(" Fetching latest AI news...")
    articles = fetch_ai_news(API_KEY, limit=20)
    memory_list = []

    for article in articles:
        memory_id, memory = generate_memory(article)
        memory_list.append(memory)

    save_all_memories(memory_list, memory_file)

    print(" Syncing to Qdrant + Graph DB...")
    with open(memory_file, "r") as f:
        all_memories = json.load(f)

    import_to_qdrant_and_graph(all_memories)

if __name__ == "__main__":
    main()
