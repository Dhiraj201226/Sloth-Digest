"""
Sloth Digest — Chunker Tests
Tests chronological slicing, boundaries, and overlap.
"""

import pytest
from backend.models import ParsedMessage
from backend.chunker import chunk_messages


def test_chunker_empty():
    assert chunk_messages([]) == []


def test_chunker_segmentation():
    messages = [
        ParsedMessage(
            message_id=str(i),
            line_number=i,
            timestamp=f"2026-10-24 10:{i:02d}",
            sender=f"User{i%3}",
            text=f"Message content {i}",
            is_system=False,
        )
        for i in range(1, 101)
    ]

    # Chunk with chunk_size=30, overlap=5
    chunks = chunk_messages(messages, chunk_size=30, overlap=5)
    assert len(chunks) > 1
    assert chunks[0].chunk_index == 1
    assert chunks[0].total_chunks == len(chunks)
    assert len(chunks[0].messages) == 30
    assert chunks[0].start_time == "2026-10-24 10:01"
    assert chunks[0].end_time == "2026-10-24 10:30"
