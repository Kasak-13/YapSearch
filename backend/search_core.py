import json
import numpy as np
import datetime
from dateutil.relativedelta import relativedelta
from sentence_transformers import SentenceTransformer
import os
import re

PARTICIPANTS = ["Aman", "Priya", "Rahul", "Neha", "Rohit", "Ananya", "Karan", "Simran"]
REFERENCE_DATE = datetime.datetime(2026, 9, 1, 0, 0, 0)

class SearchCore:
    def __init__(self):
        self.messages = []
        self.embeddings_raw = None
        self.embeddings_context = None
        self.model = None
        
    def load_data(self):
        print("Loading search core data...")
        messages_path = os.path.join(os.path.dirname(__file__), "..", "data", "messages.json")
        raw_path = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_raw.npy")
        context_path = os.path.join(os.path.dirname(__file__), "..", "data", "embeddings_context.npy")
        
        with open(messages_path, "r", encoding="utf-8") as f:
            self.messages = json.load(f)
            
        self.embeddings_raw = np.load(raw_path)
        self.embeddings_context = np.load(context_path)
        self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print(f"Loaded {len(self.messages)} messages and embeddings shapes: raw {self.embeddings_raw.shape}, context {self.embeddings_context.shape}.")

    def parse_query(self, query):
        """
        Parses query for speaker detection and temporal bounds.
        Returns: semantic_query, speaker, date_range (start, end)
        """
        speaker = None
        date_range = None
        
        semantic_query = query
        
        # 1. Speaker detection
        q_lower = query.lower()
        for p in PARTICIPANTS:
            if re.search(rf"\b{p.lower()}\b", q_lower):
                speaker = p
                # Strip the speaker name from the query (case insensitive)
                semantic_query = re.sub(rf"(?i)\b{p}\b", "", semantic_query)
                break
                
        # 2. Date parsing (Rule-based)
        start_date = None
        end_date = None
        
        time_triggers = ["last month", "this month", "yesterday", "last week", "in july", "in june", "in may"]
        for trigger in time_triggers:
            if trigger in q_lower:
                if trigger == "last month":
                    start_date = REFERENCE_DATE.replace(day=1) - relativedelta(months=1)
                    end_date = REFERENCE_DATE.replace(day=1) - relativedelta(seconds=1)
                elif trigger == "this month":
                    start_date = REFERENCE_DATE.replace(day=1)
                    end_date = start_date + relativedelta(months=1) - relativedelta(seconds=1)
                elif trigger == "yesterday":
                    start_date = REFERENCE_DATE - relativedelta(days=1)
                    end_date = start_date + relativedelta(hours=23, minutes=59, seconds=59)
                elif trigger == "last week":
                    start_date = REFERENCE_DATE - relativedelta(days=7)
                    end_date = REFERENCE_DATE
                elif trigger == "in july":
                    start_date = datetime.datetime(2026, 7, 1)
                    end_date = datetime.datetime(2026, 7, 31, 23, 59, 59)
                elif trigger == "in june":
                    start_date = datetime.datetime(2026, 6, 1)
                    end_date = datetime.datetime(2026, 6, 30, 23, 59, 59)
                elif trigger == "in may":
                    start_date = datetime.datetime(2026, 5, 1)
                    end_date = datetime.datetime(2026, 5, 31, 23, 59, 59)
                
                # Strip the time trigger from the query (case insensitive)
                semantic_query = re.sub(rf"(?i)\b{trigger}\b", "", semantic_query)
                break

        if start_date and end_date:
            date_range = (start_date, end_date)
            
        # Clean up extra spaces left behind by stripping
        semantic_query = re.sub(r'\s+', ' ', semantic_query).strip()
            
        return semantic_query, speaker, date_range

    def get_boolean_mask(self, speaker, date_range):
        mask = np.ones(len(self.messages), dtype=bool)
        
        for i, msg in enumerate(self.messages):
            if speaker and msg["sender"] != speaker:
                mask[i] = False
                continue
                
            if date_range:
                msg_time = datetime.datetime.fromisoformat(msg["timestamp"])
                if not (date_range[0] <= msg_time <= date_range[1]):
                    mask[i] = False
                    
        return mask

    def expand_context(self, index, window=3):
        start_idx = max(0, index - window)
        end_idx = min(len(self.messages), index + window + 1)
        context = []
        for i in range(start_idx, end_idx):
            if i != index:
                context.append(self.messages[i])
        return context

    def search(self, query, top_k=5):
        semantic_query, speaker, date_range = self.parse_query(query)
        mask = self.get_boolean_mask(speaker, date_range)
        
        # If mask eliminates everything, return empty
        if not np.any(mask):
            return {"query": query, "parsed": {"semantic_query": semantic_query, "speaker": speaker, "date_range": date_range}, "results": []}
            
        q_emb = self.model.encode([semantic_query])[0]
        
        valid_indices = np.where(mask)[0]
        
        # Raw embeddings similarity
        valid_raw = self.embeddings_raw[valid_indices]
        norms_raw = np.linalg.norm(valid_raw, axis=1) * np.linalg.norm(q_emb)
        norms_raw[norms_raw == 0] = 1e-10
        sim_raw = np.dot(valid_raw, q_emb) / norms_raw
        
        # Z-score normalize raw
        sim_raw_z = (sim_raw - np.mean(sim_raw)) / (np.std(sim_raw) + 1e-10)
        
        # Context embeddings similarity
        valid_context = self.embeddings_context[valid_indices]
        norms_context = np.linalg.norm(valid_context, axis=1) * np.linalg.norm(q_emb)
        norms_context[norms_context == 0] = 1e-10
        sim_context = np.dot(valid_context, q_emb) / norms_context
        
        # Z-score normalize context
        sim_context_z = (sim_context - np.mean(sim_context)) / (np.std(sim_context) + 1e-10)
        
        # Hybrid score for ranking (internal Z-score blend)
        hybrid_z = (0.6 * sim_raw_z) + (0.4 * sim_context_z)
        
        # Raw blended cosine similarity for display (natural spread, e.g. 0.82, 0.75, 0.68)
        hybrid_raw = (0.6 * sim_raw) + (0.4 * sim_context)
        display_scores = np.clip(hybrid_raw, 0.0, 1.0)
        
        top_k = min(top_k, len(hybrid_z))
        top_local_indices = np.argsort(hybrid_z)[::-1][:top_k]
        
        results = []
        for local_idx in top_local_indices:
            global_idx = valid_indices[local_idx]
            msg = self.messages[global_idx]
            sim_score = float(display_scores[local_idx])
            context = self.expand_context(global_idx)
            
            results.append({
                "message_id": msg["id"],
                "sender": msg["sender"],
                "timestamp": msg["timestamp"],
                "text": msg["text"],
                "similarity": sim_score,
                "context": context
            })
            
        date_range_str = [d.isoformat() for d in date_range] if date_range else None
        
        return {
            "query": query,
            "parsed": {
                "semantic_query": semantic_query,
                "speaker": speaker,
                "date_range": date_range_str
            },
            "results": results
        }

# Global singleton
search_core = SearchCore()
