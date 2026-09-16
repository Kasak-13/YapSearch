import pytest
import datetime
from backend.search_core import SearchCore
from backend.config import REFERENCE_DATE

@pytest.fixture
def core():
    return SearchCore()

class TestQueryParser:
    """Tests metadata parsing and entity extraction logic."""

    def test_speaker_detection_priya(self, core):
        query = "What did Priya say about the budget?"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker == "Priya"
        assert "Priya" not in clean_query
        assert "budget" in clean_query
        assert date_range is None

    def test_speaker_detection_case_insensitive(self, core):
        query = "why was neha angry yesterday?"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker == "Neha"
        assert "neha" not in clean_query.lower()
        assert date_range is not None

    def test_temporal_trigger_yesterday(self, core):
        query = "kaha the sab yesterday?"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker is None
        assert date_range is not None
        start, end = date_range
        assert start.date() == (REFERENCE_DATE - datetime.timedelta(days=1)).date()

    def test_temporal_trigger_last_month(self, core):
        query = "what did we discuss last month?"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker is None
        assert date_range is not None
        assert "last month" not in clean_query.lower()

    def test_temporal_trigger_in_july(self, core):
        query = "where did we go in july?"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker is None
        assert date_range is not None
        start, end = date_range
        assert start == datetime.datetime(2026, 7, 1)
        assert end == datetime.datetime(2026, 7, 31, 23, 59, 59)

    def test_pure_semantic_query(self, core):
        query = "internet not working"
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker is None
        assert date_range is None
        assert clean_query == "internet not working"

    def test_whitespace_normalization(self, core):
        query = "  What did    Aman   say   yesterday?   "
        clean_query, speaker, date_range = core.parse_query(query)
        assert speaker == "Aman"
        assert date_range is not None
        assert "  " not in clean_query
