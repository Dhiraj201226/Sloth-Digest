"""
Sloth Digest — Configuration
Single source of truth for all runtime settings and local parameters.
Strictly offline: Zero external internet URLs.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

WATCHED_DIR = BASE_DIR / "watched_chats"
WATCHED_DIR.mkdir(exist_ok=True)

ARCHIVE_DIR = WATCHED_DIR / "archive"
ARCHIVE_DIR.mkdir(exist_ok=True)

SYNTHETIC_DIR = BASE_DIR / "synthetic_data"
SYNTHETIC_DIR.mkdir(exist_ok=True)

# SQLite Database
DB_PATH = os.environ.get("SLOTH_DB_PATH", str(DATA_DIR / "sloth_digest.db"))

# Ollama Local Configuration (localhost only)
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("SLOTH_MODEL", "qwen2.5:1.5b")

# Processing Settings
CHUNK_SIZE = int(os.environ.get("SLOTH_CHUNK_SIZE", "60"))
CHUNK_OVERLAP = int(os.environ.get("SLOTH_CHUNK_OVERLAP", "5"))
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("SLOTH_TIMEOUT", "120"))

# Copy / UI text single source of truth
APP_NAME = "Sloth Digest"
TAGLINE = "Slow and steady: rewards laziness by reading overnight chats locally."
OFFLINE_STATUS_LABEL = "Offline · nothing leaves this machine"
