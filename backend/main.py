"""
Sloth Digest — FastAPI Backend Service
Serves REST endpoints, SSE progress streaming, and health checks on localhost.
Strictly local-first.
"""

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import (
    APP_NAME,
    TAGLINE,
    DEFAULT_MODEL,
    SYNTHETIC_DIR,
    WATCHED_DIR,
)
from backend.models import (
    DigestResponse,
    SystemHealth,
    ProgressEvent,
    TidySuggestion,
)
from backend.database import (
    init_db,
    get_latest_digest,
    get_digest_by_id,
    list_all_digests,
)
from backend.parser import parse_chat_text, extract_text_from_file_bytes
from backend.orchestrator import digest_chat
from backend.llm_client import check_ollama
from backend.tidier import scan_tidier_directory, apply_tidy_action

# Initialize DB on start
init_db()

app = FastAPI(
    title=APP_NAME,
    description=TAGLINE,
    version="1.0.0",
)

# CORS restricted to localhost development and production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# In-memory progress tracking for active tasks
TASK_PROGRESS: Dict[str, ProgressEvent] = {}


@app.get("/api/health", response_model=SystemHealth)
def get_health(model: Optional[str] = None):
    """Checks localhost offline status and Ollama model readiness."""
    return check_ollama(model or DEFAULT_MODEL)


@app.get("/api/digest/latest")
def get_latest():
    """Returns the most recent morning digest for instant 0-click glance."""
    digest = get_latest_digest()
    if not digest:
        return JSONResponse(status_code=200, content=None)
    return digest


@app.get("/api/digest/list")
def list_digests():
    """Lists historical digests."""
    return list_all_digests()


@app.get("/api/digest/{digest_id}")
def get_digest(digest_id: str):
    """Retrieves a specific digest by ID."""
    digest = get_digest_by_id(digest_id)
    if not digest:
        raise HTTPException(status_code=404, detail="Digest not found.")
    return digest


@app.get("/api/digest/progress/{task_id}")
async def stream_progress(task_id: str):
    """Server-Sent Events endpoint for real-time progress and honest ETA."""
    async def event_generator():
        last_percent = -1
        while True:
            if task_id in TASK_PROGRESS:
                event = TASK_PROGRESS[task_id]
                if event.percent != last_percent:
                    last_percent = event.percent
                    yield f"data: {json.dumps(event.model_dump())}\n\n"
                if event.status in ["completed", "error"]:
                    break
            await asyncio.sleep(0.3)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/digest/upload", response_model=DigestResponse)
async def upload_and_digest(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None),
):
    """Uploads a WhatsApp chat (.txt or .zip) and generates the morning digest."""
    filename = file.filename or "uploaded_chat.txt"
    ext = Path(filename).suffix.lower()
    if ext not in [".txt", ".zip"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format. Please upload a WhatsApp export in .txt or .zip format."
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        raw_text = extract_text_from_file_bytes(file_bytes, filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract chat text: {e}")

    messages = parse_chat_text(raw_text)
    if not messages:
        raise HTTPException(
            status_code=422,
            detail="No recognizable WhatsApp messages found in the file. Ensure it contains standard timestamps."
        )

    task_id = str(uuid.uuid4())[:8]

    def update_progress(p: ProgressEvent):
        TASK_PROGRESS[task_id] = p

    try:
        digest = digest_chat(
            messages=messages,
            chat_name=Path(filename).stem,
            model_name=model or DEFAULT_MODEL,
            progress_callback=update_progress,
        )
        return digest
    except Exception as e:
        TASK_PROGRESS[task_id] = ProgressEvent(
            task_id=task_id,
            status="error",
            current_chunk=0,
            total_chunks=0,
            percent=0,
            elapsed_sec=0,
            estimated_remaining_sec=0,
            message=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


@app.get("/api/synthetic/samples")
def list_synthetic_samples():
    """Lists pre-bundled synthetic sample chats for 1-click test runs."""
    SYNTHETIC_DIR.mkdir(parents=True, exist_ok=True)
    samples = []
    for f in SYNTHETIC_DIR.iterdir():
        if f.suffix.lower() == ".txt":
            samples.append({
                "id": f.stem,
                "filename": f.name,
                "size_bytes": f.stat().st_size,
            })
    return samples


@app.post("/api/synthetic/digest/{sample_id}", response_model=DigestResponse)
def digest_synthetic_sample(sample_id: str, model: Optional[str] = None):
    """Runs summarization on a pre-bundled synthetic chat."""
    target_file = SYNTHETIC_DIR / f"{sample_id}.txt"
    if not target_file.exists():
        raise HTTPException(status_code=404, detail=f"Synthetic chat '{sample_id}' not found.")

    raw_text = target_file.read_text(encoding="utf-8")
    messages = parse_chat_text(raw_text)
    if not messages:
        raise HTTPException(status_code=422, detail="No messages in synthetic sample.")

    digest = digest_chat(
        messages=messages,
        chat_name=target_file.stem,
        model_name=model or DEFAULT_MODEL,
    )
    return digest


@app.get("/api/tidier/scan", response_model=List[TidySuggestion])
def get_tidier_suggestions():
    """Scans watched directory for messy chat filenames and archive candidates."""
    return scan_tidier_directory(str(WATCHED_DIR))


@app.post("/api/tidier/apply")
def apply_tidier_suggestions(suggestions: List[TidySuggestion]):
    """Applies selected tidy suggestions (renaming, archiving)."""
    success_count = 0
    for s in suggestions:
        if apply_tidy_action(s):
            success_count += 1
    return {"applied_count": success_count, "total": len(suggestions)}


# Serve frontend production build if available
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIST), html=True), name="static")
