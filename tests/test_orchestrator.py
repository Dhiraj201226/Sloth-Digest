"""
Sloth Digest — Orchestrator & Hallucination Guard Tests
Validates map-reduce flow, citation preservation, and noise filtering.
"""

import pytest
from backend.models import ParsedMessage
from backend.orchestrator import digest_chat
from backend.database import init_db, get_latest_digest


def test_digest_chat_and_hallucination_guard():
    init_db()
    messages = [
        ParsedMessage(
            message_id="m1",
            line_number=1,
            timestamp="24/10/2026, 10:00",
            sender="Alice",
            text="Hey team, can you please submit the design file by Friday at 5 PM?",
            is_system=False,
        ),
        ParsedMessage(
            message_id="m2",
            line_number=2,
            timestamp="24/10/2026, 10:05",
            sender="Bob",
            text="I will do it! Don't worry.",
            is_system=False,
        ),
        ParsedMessage(
            message_id="m3",
            line_number=3,
            timestamp="24/10/2026, 10:10",
            sender="Charlie",
            text="Lol nice meme haha 🍕",
            is_system=False,
        ),
        ParsedMessage(
            message_id="m4",
            line_number=4,
            timestamp="24/10/2026, 10:12",
            sender="David",
            text="Yeah really funny.",
            is_system=False,
        ),
    ]

    events = []
    def on_progress(p):
        events.append(p)

    digest = digest_chat(
        messages=messages,
        chat_name="TestSquad",
        progress_callback=on_progress
    )

    assert digest.chat_name == "TestSquad"
    assert digest.total_messages == 4
    assert digest.safe_to_ignore_count >= 1
    assert len(digest.two_line_summary.splitlines()) >= 2
    assert len(events) >= 2

    # Verify hallucination guard citation integrity
    for action in digest.action_items:
        assert action.source.line_number in [1, 2, 3, 4]
        assert action.source.raw_text != ""
        assert action.source.sender in ["Alice", "Bob", "Charlie", "David"]

    for deadline in digest.deadlines:
        assert deadline.source.line_number in [1, 2, 3, 4]
        assert deadline.source.raw_text != ""

    # Verify DB persistence
    latest = get_latest_digest()
    assert latest is not None
    assert latest.id == digest.id
