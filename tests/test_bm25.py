import pytest
import numpy as np
from backend.bm25 import BM25Okapi
from backend.search_core import SearchCore

class TestBM25Okapi:
    """Unit tests for in-memory BM25Okapi retrieval and global IDF stability."""

    @pytest.fixture
    def sample_corpus(self):
        return [
            "yaar project deadline kab hai?",
            "bhai Manali chalte hai weekend pe",
            "Priya bol rahi thi budget nahi hai mera",
            "wifi band hai hostel ka",
            "assignment submit kar diya sabne?"
        ]

    def test_tokenization_hinglish(self):
        text = "Bhai, Manali chalte hai!! 100% plan final."
        tokens = BM25Okapi.tokenize(text)
        assert "bhai" in tokens
        assert "manali" in tokens
        assert "chalte" in tokens
        assert "100" in tokens
        assert "!" not in tokens

    def test_global_idf_calculation(self, sample_corpus):
        bm25 = BM25Okapi(sample_corpus)
        # 'hai' appears in multiple documents, 'manali' appears in only 1 document
        assert "hai" in bm25.idf
        assert "manali" in bm25.idf
        # Rare word 'manali' must have strictly higher IDF than frequent word 'hai'
        assert bm25.idf["manali"] > bm25.idf["hai"]

    def test_scoring_on_filtered_candidates_uses_global_idf(self, sample_corpus):
        bm25 = BM25Okapi(sample_corpus)
        # Even if we only score candidate [2, 3], global IDF for 'budget' should be used
        cand_indices = np.array([2, 3])
        scores = bm25.score_candidates("budget", cand_indices)
        assert len(scores) == 2
        assert scores[0] > 0.0  # Document 2 mentions 'budget'
        assert scores[1] == 0.0  # Document 3 does not mention 'budget'

    def test_exact_keyword_ranking_dominance(self, sample_corpus):
        bm25 = BM25Okapi(sample_corpus)
        all_indices = np.arange(len(sample_corpus))
        scores = bm25.score_candidates("Manali", all_indices)
        best_idx = np.argmax(scores)
        assert best_idx == 1
        assert "Manali" in sample_corpus[best_idx]

class TestRRFIntegration:
    """Integration test verifying RRF fusion with Top-100 candidate pooling."""

    def test_search_core_hybrid_rrf(self):
        core = SearchCore()
        core.load_data()
        assert core.bm25 is not None
        assert core.bm25.corpus_size == len(core.messages)

        # Test search with exact keyword that should benefit from BM25
        result = core.search("wifi", top_k=5)
        assert len(result["results"]) > 0
        # Top hits must contain wifi
        assert any("wifi" in r["text"].lower() for r in result["results"][:3])
