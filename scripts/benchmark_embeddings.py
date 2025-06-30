from sentence_transformers import SentenceTransformer, util
import time

sentence = "Client asked about margin drop in Q2 and potential risks."

models = {
    "MiniLM": SentenceTransformer("all-MiniLM-L6-v2"),
    "MPNet": SentenceTransformer("all-mpnet-base-v2")
}

for name, model in models.items():
    start = time.time()
    embedding = model.encode(sentence, convert_to_tensor=True)
    duration = time.time() - start

    print(f"{name}")
    print(f"Vector size: {embedding.shape[0]}")
    print(f"Time taken: {duration:.4f} sec")
    print(f"Preview: {embedding[:5]}")
