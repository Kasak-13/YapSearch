import math
import re
from collections import Counter
from typing import List, Dict, Optional, Sequence
import numpy as np

class BM25Okapi:
    """
    In-memory BM25Okapi lexical retrieval engine.
    Computes global Inverse Document Frequency (IDF) over the full corpus
    and scores masked/filtered candidate subsets without IDF distortion.
    """

    def __init__(self, corpus_texts: Sequence[str], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus_texts)
        
        # Tokenize full corpus
        self.doc_tokens: List[List[str]] = [self.tokenize(text) for text in corpus_texts]
        self.doc_lens = np.array([len(tokens) for tokens in self.doc_tokens], dtype=np.float32)
        self.avgdl = float(np.mean(self.doc_lens)) if self.corpus_size > 0 else 1.0
        
        # Inverted index: term -> list of (doc_id, term_frequency)
        # Term frequencies per document
        self.term_freqs: List[Dict[str, int]] = [Counter(tokens) for tokens in self.doc_tokens]
        
        # Global Document Frequency (DF) across the entire corpus
        self.df: Dict[str, int] = Counter()
        for doc in self.doc_tokens:
            for term in set(doc):
                self.df[term] += 1
                
        # Global IDF table (Standard Lucene/Okapi BM25 smoothing)
        self.idf: Dict[str, float] = {}
        for term, freq in self.df.items():
            # ln(1 + (N - df + 0.5) / (df + 0.5))
            self.idf[term] = math.log(1.0 + (self.corpus_size - freq + 0.5) / (freq + 0.5))

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """
        Tokenizes text using word boundaries, lowercasing, and alphanumeric filtering.
        Handles Hinglish tokens cleanly.
        """
        if not text:
            return []
        return re.findall(r"\b[a-zA-Z0-9_]+\b", text.lower())

    def score_candidates(self, query: str, candidate_indices: np.ndarray) -> np.ndarray:
        """
        Scores a specific subset of documents (given by candidate_indices) against the query.
        Uses global corpus IDF values to prevent rare-word score instability on filtered sets.
        
        Returns:
            np.ndarray of BM25 scores with shape matching candidate_indices.
        """
        query_tokens = self.tokenize(query)
        num_candidates = len(candidate_indices)
        scores = np.zeros(num_candidates, dtype=np.float32)
        
        if not query_tokens or num_candidates == 0:
            return scores

        # Filter query tokens to those that appear in global IDF table
        relevant_tokens = [q for q in query_tokens if q in self.idf]
        if not relevant_tokens:
            return scores

        cand_lens = self.doc_lens[candidate_indices]
        # Length normalization factor: (1 - b + b * (doc_len / avgdl))
        denom_len = (1.0 - self.b + self.b * (cand_lens / self.avgdl))

        for token in relevant_tokens:
            idf = self.idf[token]
            # Vectorized extraction of term frequency for candidates
            tfs = np.array([self.term_freqs[idx].get(token, 0) for idx in candidate_indices], dtype=np.float32)
            
            # BM25 term score: idf * (tf * (k1 + 1)) / (tf + k1 * denom_len)
            numerator = tfs * (self.k1 + 1.0)
            denominator = tfs + self.k1 * denom_len
            scores += idf * (numerator / (denominator + 1e-10))

        return scores
