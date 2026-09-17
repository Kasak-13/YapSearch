import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

try:
    from backend.config import FRONTEND_DIR, MODEL_NAME, REFERENCE_DATE
    from backend.schemas import SearchRequest, SearchResponse, HealthResponse
    from backend.search_core import search_core
except ImportError:
    from config import FRONTEND_DIR, MODEL_NAME, REFERENCE_DATE
    from schemas import SearchRequest, SearchResponse, HealthResponse
    from search_core import search_core

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("yapsearch.api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager: initializes in-memory vector index and models on boot."""
    logger.info("Starting YapSearch application...")
    try:
        search_core.load_data()
        logger.info("Search core data loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load search core data: {e}", exc_info=True)
    yield
    logger.info("Shutting down YapSearch application...")

app = FastAPI(
    title="YapSearch API",
    description="Localized, high-performance semantic search engine for transliterated Hinglish group chats.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static frontend assets
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/", response_class=HTMLResponse, tags=["Web Interface"])
async def root():
    """Serves the WhatsApp-style glassmorphic search frontend."""
    index_path = FRONTEND_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Frontend index.html not found."
        )
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """System health check and vector index diagnostic endpoint."""
    return HealthResponse(
        status="healthy" if search_core.is_loaded else "initializing",
        messages_indexed=len(search_core.messages),
        embeddings_loaded=search_core.embeddings_raw is not None,
        model_name=MODEL_NAME,
        reference_date=REFERENCE_DATE.isoformat()
    )

@app.post("/search", response_model=SearchResponse, tags=["Search Engine"])
async def search(req: SearchRequest):
    """
    Executes hybrid semantic search over the indexed chat dataset.
    Features:
      - Automatic participant entity extraction (e.g. 'What did Priya say...')
      - Rule-based temporal bounds pre-filtering (e.g. '...last month?')
      - Z-score normalized dual-embedding ranking (Raw + Contextual)
      - Temporal dialogue context window expansion (+/-3 messages)
    """
    query_str = req.query.strip()
    if not query_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Query cannot be empty."
        )

    try:
        results = search_core.search(query=query_str, top_k=req.top_k or 5)
        return results
    except Exception as e:
        logger.error(f"Search error for query '{req.query}': {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error during semantic search execution."
        )

if __name__ == "__main__":
    import uvicorn
    import sys
    from pathlib import Path
    root_path = str(Path(__file__).resolve().parent.parent)
    if root_path not in sys.path:
        sys.path.insert(0, root_path)
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
