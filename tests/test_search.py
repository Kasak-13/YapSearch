import pytest
import numpy as np
import datetime
from backend.search_core import SearchCore

class TestSearchCoreUnits:
    """Unit tests for SearchCore internal mechanics (masks, context expansion, hybrid blending)."""

    @pytest.fixture
    def mock_core(self):
        core = SearchCore()
        core.messages = [
            {"id": "1", "sender": "Aman", "timestamp": "2026-08-15T10:00:00", "text": "Good morning"},
            {"id": "2", "sender": "Priya", "timestamp": "2026-08-15T10:01:00", "text": "Hey all"},
            {"id": "3", "sender": "Rahul", "timestamp": "2026-08-15T10:02:00", "text": "Plan banate hai"},
            {"id": "4", "sender": "Priya", "timestamp": "2026-08-16T12:00:00", "text": "budget nahi hai mera"},
            {"id": "5", "sender": "Neha", "timestamp": "2026-08-16T12:05:00", "text": "Same here"}
        ]
        return core

    def test_boolean_mask_speaker(self, mock_core):
        mask = mock_core.get_boolean_mask(speaker="Priya", date_range=None)
        assert len(mask) == 5
        assert np.array_equal(mask, [False, True, False, True, False])

    def test_boolean_mask_date_range(self, mock_core):
        start = datetime.datetime(2026, 8, 16, 0, 0, 0)
        end = datetime.datetime(2026, 8, 16, 23, 59, 59)
        mask = mock_core.get_boolean_mask(speaker=None, date_range=(start, end))
        assert np.array_equal(mask, [False, False, False, True, True])

    def test_boolean_mask_combined(self, mock_core):
        start = datetime.datetime(2026, 8, 16, 0, 0, 0)
        end = datetime.datetime(2026, 8, 16, 23, 59, 59)
        mask = mock_core.get_boolean_mask(speaker="Priya", date_range=(start, end))
        assert np.array_equal(mask, [False, False, False, True, False])

    def test_expand_context_window_middle(self, mock_core):
        ctx = mock_core.expand_context(index=2, window=1)
        assert len(ctx) == 2
        assert ctx[0]["id"] == "2"
        assert ctx[1]["id"] == "4"

    def test_expand_context_window_boundary_start(self, mock_core):
        ctx = mock_core.expand_context(index=0, window=2)
        assert len(ctx) == 2
        assert ctx[0]["id"] == "2"
        assert ctx[1]["id"] == "3"

    def test_expand_context_window_boundary_end(self, mock_core):
        ctx = mock_core.expand_context(index=4, window=2)
        assert len(ctx) == 2
        assert ctx[0]["id"] == "3"
        assert ctx[1]["id"] == "4"
