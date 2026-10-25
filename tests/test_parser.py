"""
Sloth Digest — Chat Log Parser Tests
Validates parsing across iOS and Android formats, multi-line continuation,
system messages, and zip packaging.
"""

import zipfile
import io
import pytest
from backend.parser import (
    parse_chat_text,
    extract_text_from_file_bytes,
    is_system_message,
)


def test_parse_ios_format():
    chat = """
[24/10/2026, 14:02:10] Maya Chen: Hey team, slides are ready.
[24/10/2026, 14:03:00] David K.: Awesome work!
"""
    msgs = parse_chat_text(chat)
    assert len(msgs) == 2
    assert msgs[0].sender == "Maya Chen"
    assert msgs[0].text == "Hey team, slides are ready."
    assert msgs[0].line_number == 2
    assert msgs[1].sender == "David K."


def test_parse_android_format():
    chat = """
10/24/26, 2:02 PM - Alice: Can you check the budget?
10/24/26, 2:03 PM - Bob: Checking now.
"""
    msgs = parse_chat_text(chat)
    assert len(msgs) == 2
    assert msgs[0].sender == "Alice"
    assert msgs[0].text == "Can you check the budget?"
    assert msgs[1].sender == "Bob"


def test_multiline_continuation():
    chat = """
[24/10/2026, 14:02:10] Alice: This is line one of message.
This is line two of the same message.
And line three!
[24/10/2026, 14:05:00] Bob: Understood.
"""
    msgs = parse_chat_text(chat)
    assert len(msgs) == 2
    assert "line two" in msgs[0].text
    assert "line three!" in msgs[0].text
    assert msgs[1].sender == "Bob"


def test_system_message_filtering():
    chat = """
[24/10/2026, 14:00:00] Messages and calls are end-to-end encrypted. No one outside of this chat can read them.
[24/10/2026, 14:01:00] Alice: Hello everyone!
[24/10/2026, 14:02:00] Bob: <Media omitted>
"""
    msgs = parse_chat_text(chat)
    assert len(msgs) == 3
    assert msgs[0].is_system is True
    assert msgs[1].is_system is False
    assert msgs[2].is_system is True


def test_zip_extraction():
    chat_content = "[24/10/2026, 10:00:00] Alice: In zip file!"
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        z.writestr("_chat.txt", chat_content.encode("utf-8"))
        z.writestr("photo.jpg", b"fake binary data")

    extracted = extract_text_from_file_bytes(zip_buffer.getvalue(), "export.zip")
    assert "In zip file!" in extracted
    msgs = parse_chat_text(extracted)
    assert len(msgs) == 1
    assert msgs[0].sender == "Alice"
