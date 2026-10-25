"""
Sloth Digest — SQLite Persistence Layer
Local-first embedded database for storing historical digests, citations, and watched files.
"""

import sqlite3
import json
from typing import Optional, List, Dict, Any
from pathlib import Path
from backend.config import DB_PATH
from backend.models import DigestResponse, ActionItem, DeadlineItem, SourceCitation, ClassifiedMessage


def get_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes schema if not already present."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS digests (
                id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chat_name TEXT NOT NULL,
                start_date TEXT,
                end_date TEXT,
                total_messages INTEGER NOT NULL,
                safe_to_ignore_count INTEGER NOT NULL,
                two_line_summary TEXT NOT NULL,
                model_used TEXT NOT NULL,
                processing_duration_sec REAL NOT NULL,
                detailed_summary TEXT,
                overall_classification TEXT DEFAULT 'balanced',
                important_count INTEGER DEFAULT 0,
                spam_count INTEGER DEFAULT 0,
                messages_json TEXT
            );
        """)

        # Safe migrations for existing SQLite databases
        for col_name, col_type in [
            ("detailed_summary", "TEXT"),
            ("overall_classification", "TEXT DEFAULT 'balanced'"),
            ("important_count", "INTEGER DEFAULT 0"),
            ("spam_count", "INTEGER DEFAULT 0"),
            ("messages_json", "TEXT"),
        ]:
            try:
                cursor.execute(f"ALTER TABLE digests ADD COLUMN {col_name} {col_type}")
            except sqlite3.OperationalError:
                pass

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS action_items (
                id TEXT PRIMARY KEY,
                digest_id TEXT NOT NULL,
                description TEXT NOT NULL,
                assignee_target TEXT NOT NULL,
                urgency TEXT NOT NULL,
                source_message_id TEXT NOT NULL,
                source_sender TEXT NOT NULL,
                source_timestamp TEXT NOT NULL,
                source_text TEXT NOT NULL,
                source_line_number INTEGER NOT NULL,
                FOREIGN KEY(digest_id) REFERENCES digests(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deadlines (
                id TEXT PRIMARY KEY,
                digest_id TEXT NOT NULL,
                date_mentioned TEXT NOT NULL,
                event_description TEXT NOT NULL,
                source_message_id TEXT NOT NULL,
                source_sender TEXT NOT NULL,
                source_timestamp TEXT NOT NULL,
                source_text TEXT NOT NULL,
                source_line_number INTEGER NOT NULL,
                FOREIGN KEY(digest_id) REFERENCES digests(id) ON DELETE CASCADE
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS watched_files (
                file_path TEXT PRIMARY KEY,
                file_hash TEXT NOT NULL,
                last_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                digest_id TEXT,
                status TEXT NOT NULL
            );
        """)
        conn.commit()


def save_digest(digest: DigestResponse) -> None:
    """Stores a complete digest and associated action items/deadlines."""
    with get_connection() as conn:
        cursor = conn.cursor()
        messages_serialized = json.dumps([m.model_dump() for m in digest.messages]) if digest.messages else "[]"
        cursor.execute("""
            INSERT OR REPLACE INTO digests (
                id, created_at, chat_name, start_date, end_date,
                total_messages, safe_to_ignore_count, two_line_summary,
                model_used, processing_duration_sec,
                detailed_summary, overall_classification,
                important_count, spam_count, messages_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            digest.id, digest.created_at, digest.chat_name, digest.start_date,
            digest.end_date, digest.total_messages, digest.safe_to_ignore_count,
            digest.two_line_summary, digest.model_used, digest.processing_duration_sec,
            digest.detailed_summary, digest.overall_classification,
            digest.important_count, digest.spam_count, messages_serialized
        ))

        # Clear existing items if replacing
        cursor.execute("DELETE FROM action_items WHERE digest_id = ?", (digest.id,))
        cursor.execute("DELETE FROM deadlines WHERE digest_id = ?", (digest.id,))

        for item in digest.action_items:
            cursor.execute("""
                INSERT INTO action_items (
                    id, digest_id, description, assignee_target, urgency,
                    source_message_id, source_sender, source_timestamp,
                    source_text, source_line_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id, digest.id, item.description, item.assignee_target, item.urgency,
                item.source.message_id, item.source.sender, item.source.timestamp,
                item.source.raw_text, item.source.line_number
            ))

        for item in digest.deadlines:
            cursor.execute("""
                INSERT INTO deadlines (
                    id, digest_id, date_mentioned, event_description,
                    source_message_id, source_sender, source_timestamp,
                    source_text, source_line_number
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item.id, digest.id, item.date_mentioned, item.event_description,
                item.source.message_id, item.source.sender, item.source.timestamp,
                item.source.raw_text, item.source.line_number
            ))

        conn.commit()


def _hydrate_digest(row: sqlite3.Row, conn: sqlite3.Connection) -> DigestResponse:
    """Hydrates a full DigestResponse with its related action items and deadlines."""
    digest_id = row["id"]
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM action_items WHERE digest_id = ? ORDER BY source_line_number ASC
    """, (digest_id,))
    action_rows = cursor.fetchall()
    actions = [
        ActionItem(
            id=a["id"],
            description=a["description"],
            assignee_target=a["assignee_target"],
            urgency=a["urgency"],
            source=SourceCitation(
                message_id=a["source_message_id"],
                line_number=a["source_line_number"],
                sender=a["source_sender"],
                timestamp=a["source_timestamp"],
                raw_text=a["source_text"]
            )
        )
        for a in action_rows
    ]

    cursor.execute("""
        SELECT * FROM deadlines WHERE digest_id = ? ORDER BY source_line_number ASC
    """, (digest_id,))
    deadline_rows = cursor.fetchall()
    deadlines = [
        DeadlineItem(
            id=d["id"],
            date_mentioned=d["date_mentioned"],
            event_description=d["event_description"],
            source=SourceCitation(
                message_id=d["source_message_id"],
                line_number=d["source_line_number"],
                sender=d["source_sender"],
                timestamp=d["source_timestamp"],
                raw_text=d["source_text"]
            )
        )
        for d in deadline_rows
    ]

    raw_messages_json = row["messages_json"] if "messages_json" in row.keys() and row["messages_json"] else "[]"
    try:
        parsed_msgs_data = json.loads(raw_messages_json)
        classified_messages = [ClassifiedMessage(**m) for m in parsed_msgs_data]
    except Exception:
        classified_messages = []

    return DigestResponse(
        id=row["id"],
        created_at=row["created_at"],
        chat_name=row["chat_name"],
        start_date=row["start_date"],
        end_date=row["end_date"],
        total_messages=row["total_messages"],
        safe_to_ignore_count=row["safe_to_ignore_count"],
        important_count=row["important_count"] if "important_count" in row.keys() else 0,
        spam_count=row["spam_count"] if "spam_count" in row.keys() else 0,
        overall_classification=row["overall_classification"] if "overall_classification" in row.keys() and row["overall_classification"] else "balanced",
        two_line_summary=row["two_line_summary"],
        detailed_summary=row["detailed_summary"] if "detailed_summary" in row.keys() else None,
        action_items=actions,
        deadlines=deadlines,
        messages=classified_messages,
        model_used=row["model_used"],
        processing_duration_sec=row["processing_duration_sec"]
    )



def get_latest_digest() -> Optional[DigestResponse]:
    """Retrieves the most recent digest for the morning glance screen."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM digests ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        return _hydrate_digest(row, conn)


def get_digest_by_id(digest_id: str) -> Optional[DigestResponse]:
    """Retrieves a specific digest by ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM digests WHERE id = ?", (digest_id,))
        row = cursor.fetchone()
        if not row:
            return None
        return _hydrate_digest(row, conn)


def list_all_digests() -> List[Dict[str, Any]]:
    """Returns summaries of all processed digests."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, chat_name, total_messages, safe_to_ignore_count
            FROM digests ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
