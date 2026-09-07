import json
import os
import sys

# Add backend directory to sys.path so we can import SearchCore
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from backend.search_core import search_core

def evaluate():
    print("Initializing SearchCore for evaluation...")
    search_core.load_data()
    
    eval_file = os.path.join(os.path.dirname(__file__), "..", "data", "eval_set.json")
    with open(eval_file, "r", encoding="utf-8") as f:
        queries = json.load(f)
        
    print(f"Loaded {len(queries)} evaluation queries.")
    
    recalls = {1: 0, 3: 0, 5: 0, 10: 0}
    total = len(queries)
    zero_overlap_total = 0
    zero_overlap_failures = []
    
    for i, q in enumerate(queries):
        query_text = q["query"]
        expected_id = q["expected_message_id"]
        q_type = q["type"]
        is_zero_overlap = q.get("zero_overlap", False)
        
        if is_zero_overlap:
            zero_overlap_total += 1
            
        result = search_core.search(query_text, top_k=10)
        retrieved_ids = [r["message_id"] for r in result["results"]]
        
        found_at = -1
        for rank, rid in enumerate(retrieved_ids):
            if rid == expected_id:
                found_at = rank + 1
                break
                
        if found_at != -1:
            if found_at <= 1: recalls[1] += 1
            if found_at <= 3: recalls[3] += 1
            if found_at <= 5: recalls[5] += 1
            if found_at <= 10: recalls[10] += 1
            
        if is_zero_overlap and found_at == -1:
            zero_overlap_failures.append({
                "query": query_text,
                "expected": expected_id,
                "retrieved": retrieved_ids[:3] # top 3 for debugging
            })
            
    print("\n--- EVALUATION RESULTS ---")
    print(f"Total Queries: {total}")
    print(f"Recall@1:  {recalls[1]/total*100:.1f}% ({recalls[1]}/{total})")
    print(f"Recall@3:  {recalls[3]/total*100:.1f}% ({recalls[3]}/{total})")
    print(f"Recall@5:  {recalls[5]/total*100:.1f}% ({recalls[5]}/{total})")
    print(f"Recall@10: {recalls[10]/total*100:.1f}% ({recalls[10]}/{total})")
    
    print("\n--- ZERO-OVERLAP ANALYSIS ---")
    print(f"Total Zero-Overlap Queries: {zero_overlap_total}")
    if zero_overlap_failures:
        print(f"Failed to retrieve within top 10 for {len(zero_overlap_failures)} zero-overlap queries:")
        for fail in zero_overlap_failures:
            print(f"  - Query: {fail['query']}")
            print(f"    Expected: {fail['expected']}")
            print(f"    Retrieved top 3: {fail['retrieved']}")
    else:
        print("All zero-overlap queries were successfully retrieved in the top 10!")

if __name__ == "__main__":
    evaluate()
