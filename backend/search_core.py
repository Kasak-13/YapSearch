import json
import logging
import os
import re
import datetime
from typing import Dict, List, Optional, Tuple, Any
from dateutil.relativedelta import relativedelta
import numpy as np
from sentence_transformers import SentenceTransformer

try:
    from backend.config import (
        PARTICIPANTS, REFERENCE_DATE, MODEL_NAME,
        MESSAGES_PATH, EMBEDDINGS_RAW_PATH, EMBEDDINGS_CONTEXT_PATH,
        DEFAULT_TOP_K, CONTEXT_EXPANSION_WINDOW, RAW_WEIGHT, CONTEXT_WEIGHT
    )
except ImportError:
    from config import (
        PARTICIPANTS, REFERENCE_DATE, MODEL_NAME,
        MESSAGES_PATH, EMBEDDINGS_RAW_PATH, EMBEDDINGS_CONTEXT_PATH,
        DEFAULT_TOP_K, CONTEXT_EXPANSION_WINDOW, RAW_WEIGHT, CONTEXT_WEIGHT
    )

logger = logging.getLogger("yapsearch.core")

class SearchCore:
    """
    Core semantic retrieval engine.
    Handles:
      - Intent & entity extraction (speakers, temporal windows)
      - Boolean bitmask pre-filtering
      - Bi-encoder dense vector inference
      - Hybrid Z-score rank fusion (Raw + Context)
      - Dialogue context expansion (+/- 3 messages)
    """

    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self.embeddings_raw: Optional[np.ndarray] = None
        self.embeddings_context: Optional[np.ndarray] = None
        self.model: Optional[SentenceTransformer] = None
        self._is_loaded: bool = False

    def load_data(self) -> None:
        """Loads chat corpus, pre-computed embeddings, and initializes the bi-encoder."""
        if self._is_loaded:
            return

        logger.info(f"Loading chat corpus from {MESSAGES_PATH}...")
        with open(MESSAGES_PATH, "r", encoding="utf-8") as f:
            self.messages = json.load(f)

        logger.info(f"Loading dense vector matrices from {EMBEDDINGS_RAW_PATH}...")
        self.embeddings_raw = np.load(str(EMBEDDINGS_RAW_PATH))
        self.embeddings_context = np.load(str(EMBEDDINGS_CONTEXT_PATH))

        logger.info(f"Initializing SentenceTransformer model ({MODEL_NAME})...")
        self.model = SentenceTransformer(MODEL_NAME)
        self._is_loaded = True
        logger.info(f"YapSearch ready: {len(self.messages)} messages indexed.")

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def parse_query(self, query: str) -> Tuple[str, Optional[str], Optional[Tuple[datetime.datetime, datetime.datetime]]]:
        """
        Parses query for participant speaker detection and temporal bounds.
        Returns:
            semantic_query: Query with parsed entities stripped
            speaker: Extracted participant name or None
            date_range: (start_date, end_date) datetime tuple or None
        """
        speaker: Optional[str] = None
        date_range: Optional[Tuple[datetime.datetime, datetime.datetime]] = None
        semantic_query = query

        # 1. Speaker detection
        q_lower = query.lower()
        for p in PARTICIPANTS:
            if re.search(rf"\b{p.lower()}\b", q_lower):
                speaker = p
                # Strip the speaker name from the query (case insensitive)
                semantic_query = re.sub(rf"(?i)\b{p}\b", "", semantic_query)
                break

        # 2. Date parsing (Rule-based temporal triggers)
        start_date: Optional[datetime.datetime] = None
        end_date: Optional[datetime.datetime] = None

        time_triggers = [
            "last month", "this month", "yesterday", "last week",
            "in july", "in june", "in may"
        ]
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

                # Strip time trigger from query
                semantic_query = re.sub(rf"(?i)\b{trigger}\b", "", semantic_query)
                break

        if start_date and end_date:
            date_range = (start_date, end_date)

        # Normalize whitespace
        semantic_query = re.sub(r"\s+", " ", semantic_query).strip()

        return semantic_query, speaker, date_range

    def get_boolean_mask(
        self, 
        speaker: Optional[str], 
        date_range: Optional[Tuple[datetime.datetime, datetime.datetime]]
    ) -> np.ndarray:
        """
        Builds a boolean filter bitmask across all messages in the dataset.
        Enables efficient vector lookup restricted only to eligible items.
        """
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

    def expand_context(self, index: int, window: int = CONTEXT_EXPANSION_WINDOW) -> List[Dict[str, Any]]:
        """
        Retrieves +/- window dialogue turns surrounding the matched message index
        to reconstruct conversational context.
        """
        start_idx = max(0, index - window)
        end_idx = min(len(self.messages), index + window + 1)
        context = []
        for i in range(start_idx, end_idx):
            if i != index:
                context.append(self.messages[i])
        return context

    def search(self, query: str, top_k: int = DEFAULT_TOP_K) -> Dict[str, Any]:
        """
        Performs hybrid contextual semantic search over the corpus.
        """
        if not self._is_loaded:
            self.load_data()

        semantic_query, speaker, date_range = self.parse_query(query)
        mask = self.get_boolean_mask(speaker, date_range)

        date_range_str = [d.isoformat() for d in date_range] if date_range else None
        parsed_dict = {
            "semantic_query": semantic_query,
            "speaker": speaker,
            "date_range": date_range_str
        }

        # If boolean filters eliminate all messages, return early
        if not np.any(mask):
            return {
                "query": query,
                "parsed": parsed_dict,
                "results": []
            }

        # Embed cleaned query text
        q_emb = self.model.encode([semantic_query])[0]
        q_norm = np.linalg.norm(q_emb) or 1e-10

        valid_indices = np.where(mask)[0]

        # 1. Raw embeddings similarity
        valid_raw = self.embeddings_raw[valid_indices]
        norms_raw = np.linalg.norm(valid_raw, axis=1) * q_norm
        norms_raw[norms_raw == 0] = 1e-10
        sim_raw = np.dot(valid_raw, q_emb) / norms_raw

        # Z-score normalize raw
        sim_raw_std = np.std(sim_raw) or 1e-10
        sim_raw_z = (sim_raw - np.mean(sim_raw)) / sim_raw_std

        # 2. Contextual embeddings similarity
        valid_context = self.embeddings_context[valid_indices]
        norms_context = np.linalg.norm(valid_context, axis=1) * q_norm
        norms_context[norms_context == 0] = 1e-10
        sim_context = np.dot(valid_context, q_emb) / norms_context

        # Z-score normalize context
        sim_context_std = np.std(sim_context) or 1e-10
        sim_context_z = (sim_context - np.mean(sim_context)) / sim_context_std

        # 3. Hybrid score for ranking (internal Z-score blend)
        hybrid_z = (RAW_WEIGHT * sim_raw_z) + (CONTEXT_WEIGHT * sim_context_z)

        # 4. Raw blended cosine similarity for user display [0.0, 1.0]
        hybrid_raw = (RAW_WEIGHT * sim_raw) + (CONTEXT_WEIGHT * sim_context)
        display_scores = np.clip(hybrid_raw, 0.0, 1.0)

        # Top-K candidate sorting
        k = min(top_k, len(hybrid_z))
        top_local_indices = np.argsort(hybrid_z)[::-1][:k]

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

        return {
            "query": query,
            "parsed": parsed_dict,
            "results": results
        }

# Global singleton
search_core = SearchCore()
