from pydantic import BaseModel, Field
from typing import List, Optional, Tuple

class SearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query", json_schema_extra={"example": "What did Priya say about the budget?"})
    top_k: Optional[int] = Field(default=5, ge=1, le=50, description="Maximum number of conversation results to retrieve")

class ParsedMetadata(BaseModel):
    semantic_query: str = Field(..., description="Query stripped of parsed entities and temporal triggers")
    speaker: Optional[str] = Field(None, description="Identified participant name for pre-filtering")
    date_range: Optional[List[str]] = Field(None, description="ISO-formatted [start, end] date bounds for temporal pre-filtering")

class ContextMessage(BaseModel):
    id: str
    sender: str
    timestamp: str
    text: str

class SearchResultItem(BaseModel):
    message_id: str
    sender: str
    timestamp: str
    text: str
    similarity: float = Field(..., description="Confidence match percentage as a float between 0.0 and 1.0")
    context: List[ContextMessage] = Field(default_factory=list, description="Surrounding +/-3 dialogue turns")

class SearchResponse(BaseModel):
    query: str
    parsed: ParsedMetadata
    results: List[SearchResultItem]

class HealthResponse(BaseModel):
    status: str
    messages_indexed: int
    embeddings_loaded: bool
    model_name: str
    reference_date: str
