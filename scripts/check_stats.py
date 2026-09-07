import json
import os
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.search_core import search_core

def check_stats():
    search_core.load_data()
    
    eval_file = os.path.join(os.path.dirname(__file__), "..", "data", "eval_set.json")
    with open(eval_file, "r", encoding="utf-8") as f:
        queries = json.load(f)
        
    raw_sims = []
    context_sims = []
    
    for q in queries:
        query_text = q["query"]
        semantic_query, speaker, date_range = search_core.parse_query(query_text)
        mask = search_core.get_boolean_mask(speaker, date_range)
        
        if not np.any(mask): continue
        
        q_emb = search_core.model.encode([semantic_query])[0]
        valid_indices = np.where(mask)[0]
        
        valid_raw = search_core.embeddings_raw[valid_indices]
        norms_raw = np.linalg.norm(valid_raw, axis=1) * np.linalg.norm(q_emb)
        norms_raw[norms_raw == 0] = 1e-10
        sim_raw = np.dot(valid_raw, q_emb) / norms_raw
        raw_sims.extend(sim_raw.tolist())
        
        valid_context = search_core.embeddings_context[valid_indices]
        norms_context = np.linalg.norm(valid_context, axis=1) * np.linalg.norm(q_emb)
        norms_context[norms_context == 0] = 1e-10
        sim_context = np.dot(valid_context, q_emb) / norms_context
        context_sims.extend(sim_context.tolist())
        
    print(f"Raw Similarity     - Min: {np.min(raw_sims):.4f}, Max: {np.max(raw_sims):.4f}, Mean: {np.mean(raw_sims):.4f}, Std: {np.std(raw_sims):.4f}")
    print(f"Context Similarity - Min: {np.min(context_sims):.4f}, Max: {np.max(context_sims):.4f}, Mean: {np.mean(context_sims):.4f}, Std: {np.std(context_sims):.4f}")

if __name__ == "__main__":
    check_stats()
