import json
import numpy as np
from sentence_transformers import SentenceTransformer

def main():
    print("Loading messages from data/messages.json...")
    with open("data/messages.json", "r", encoding="utf-8") as f:
        messages = json.load(f)
    
    print(f"Loaded {len(messages)} messages.")
    
    # We will use paraphrase-multilingual-MiniLM-L12-v2 which supports Hindi/Hinglish better
    model_name = 'paraphrase-multilingual-MiniLM-L12-v2'
    print(f"Loading SentenceTransformer model: {model_name}...")
    model = SentenceTransformer(model_name)
    
    # Extract raw texts
    raw_texts = [msg["text"] for msg in messages]

    # Extract contextual texts
    context_texts = []
    for i, msg in enumerate(messages):
        context_msgs = []
        start_idx = max(0, i - 2)
        for j in range(start_idx, i):
            context_msgs.append(f"{messages[j]['sender']}: {messages[j]['text']}")
        context_msgs.append(f"{msg['sender']}: {msg['text']}")
        context_texts.append(" | ".join(context_msgs))
    
    print("Computing raw embeddings... This might take a minute.")
    raw_embeddings = model.encode(raw_texts, show_progress_bar=True)
    np.save("data/embeddings_raw.npy", raw_embeddings)
    print(f"Saved raw embeddings to data/embeddings_raw.npy with shape {raw_embeddings.shape}")

    print("Computing context embeddings... This might take a minute.")
    context_embeddings = model.encode(context_texts, show_progress_bar=True)
    np.save("data/embeddings_context.npy", context_embeddings)
    print(f"Saved context embeddings to data/embeddings_context.npy with shape {context_embeddings.shape}")
    
    # Sanity check: two known-similar messages
    # We will compute similarity for two test strings just to show it works
    test_1 = model.encode(["kab aana hai college?"])
    test_2 = model.encode(["college kis time aana hai?"])
    test_3 = model.encode(["the weather is very nice today"])
    
    from numpy.linalg import norm
    sim_1_2 = np.dot(test_1[0], test_2[0]) / (norm(test_1[0]) * norm(test_2[0]))
    sim_1_3 = np.dot(test_1[0], test_3[0]) / (norm(test_1[0]) * norm(test_3[0]))
    
    print(f"Sanity Check: Similarity between similar Hindi/Hinglish questions: {sim_1_2:.4f}")
    print(f"Sanity Check: Similarity between unrelated questions: {sim_1_3:.4f}")

if __name__ == "__main__":
    main()
