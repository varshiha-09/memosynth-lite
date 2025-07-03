import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from memosynth.memory_schema import Memory

# Load env variables and setup OpenAI client
load_dotenv()
client = OpenAI()

def load_memory(filepath: str) -> Memory:
    with open(filepath, "r") as f:
        data = json.load(f)
    return Memory(**data)

def summarize_memories(memories):
    all_texts = "\n".join([m.summary for m in memories])
    prompt = f"Summarize these insights:\n{all_texts}"
    return real_llm_call(prompt)

def real_llm_call(prompt: str) -> str:
    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Only answer using the memory content provided. Do not invent details."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content


def diff(mem1, mem2):
    if mem1.summary != mem2.summary:
        return f"Difference in summaries:\n1: {mem1.summary}\n2: {mem2.summary}"
    return " No differences"

def resolve(mem1, mem2):
    prompt = f"Resolve contradiction:\n1. {mem1.summary}\n2. {mem2.summary}"
    return real_llm_call(prompt)
