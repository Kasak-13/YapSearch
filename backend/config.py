import os
import datetime
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

# Chat Dataset Configuration
MESSAGES_PATH = DATA_DIR / "messages.json"
EMBEDDINGS_RAW_PATH = DATA_DIR / "embeddings_raw.npy"
EMBEDDINGS_CONTEXT_PATH = DATA_DIR / "embeddings_context.npy"
EVAL_SET_PATH = DATA_DIR / "eval_set.json"

# Participants
PARTICIPANTS = [
    "Aman", "Priya", "Rahul", "Neha", 
    "Rohit", "Ananya", "Karan", "Simran"
]

# Pinned Reference Date ("Today" in the simulated college chat timeline)
REFERENCE_DATE = datetime.datetime(2026, 9, 1, 0, 0, 0)

# Model Settings
MODEL_NAME = os.getenv("MODEL_NAME", "paraphrase-multilingual-MiniLM-L12-v2")

# Search Settings
DEFAULT_TOP_K = 5
CONTEXT_EXPANSION_WINDOW = 3  # +/- 3 messages
RAW_WEIGHT = 0.6
CONTEXT_WEIGHT = 0.4
