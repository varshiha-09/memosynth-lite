from transformers import pipeline
import time

test_inputs = [
    """OpenAI has unveiled new memory features for its flagship ChatGPT model, enabling users to interact with the assistant in a more contextually aware and personalized way across sessions. 
    With this update, ChatGPT can retain facts about users such as their name, preferred tone, and frequently asked questions, leading to more efficient and natural conversations over time. 
    The memory can be turned off or reset at any time, giving users control over their data. The rollout is part of OpenAI’s broader effort to align AI with user needs while being transparent about how information is retained and used. 
    Feedback from early users has been largely positive, with many noting improved continuity in tasks such as writing assistance, brainstorming, and scheduling."""
]

models = {
    "facebook/bart-large-cnn": None,
    "t5-small": None,
    "google/pegasus-xsum": None
}

results = {}

for model_name in models:
    print(f"\nRunning summarization with: {model_name}")
    try:
        summarizer = pipeline("summarization", model=model_name)
        start = time.time()
        summaries = []
        for text in test_inputs:
            summary = summarizer(text, max_length=100, min_length=30, do_sample=False)
            summaries.append(summary[0]["summary_text"])
        end = time.time()

        metrics = []
        for i, s in enumerate(summaries):
            input_len = len(test_inputs[i].split())
            output_len = len(s.split())
            avg_word_len = sum(len(w) for w in s.split()) / output_len
            metrics.append({
                "input_tokens": input_len,
                "summary_tokens": output_len,
                "compression_ratio": round(input_len / output_len, 2),
                "avg_word_length": round(avg_word_len, 2)
            })

        results[model_name] = {
            "summaries": summaries,
            "metrics": metrics,
            "runtime_seconds": round(end - start, 2),
            "time_per_summary": round((end - start) / len(summaries), 2)
        }

    except Exception as e:
        results[model_name] = {
            "error": str(e)
        }

for model, output in results.items():
    print(f"Model: {model}")
    if "error" in output:
        print(f"Error: {output['error']}")
        continue

    print(f"Runtime: {output['runtime_seconds']}s | Time per summary: {output['time_per_summary']}s")

    for i, summary in enumerate(output["summaries"]):
        print(f"\nInput {i+1} Summary:\n{summary}")
        print("Metrics:")
        for k, v in output["metrics"][i].items():
            print(f" - {k.replace('_', ' ').title()}: {v}")
