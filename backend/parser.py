"""
Sloth Digest — Chat Log Parser
Robust, multi-format WhatsApp chat log parser with multi-line support,
system message filtering, and zip archive extraction.
"""

import re
import zipfile
import io
import uuid
from typing import List, Tuple, Optional
from backend.models import ParsedMessage

# Regex patterns for WhatsApp timestamps across iOS and Android
# Pattern 1: iOS bracketed format -> [DD/MM/YY, HH:MM:SS] or [DD/MM/YYYY, HH:MM:SS AM/PM]
IOS_PATTERN = re.compile(
    r"^\[(?P<date>\d{1,4}[/\.\-]\d{1,2}[/\.\-]\d{1,4}),?\s+(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\]\s+(?P<rest>.*)$"
)

# Pattern 2: Android hyphen format -> DD/MM/YY, HH:MM - Sender: Message
ANDROID_PATTERN = re.compile(
    r"^(?P<date>\d{1,4}[/\.\-]\d{1,2}[/\.\-]\d{1,4}),?\s+(?P<time>\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AaPp][Mm])?)\s+-\s+(?P<rest>.*)$"
)

# Pattern to split sender and body
SENDER_PATTERN = re.compile(r"^(?P<sender>[^:]+?):\s+(?P<text>.*)$", re.DOTALL)

# Common system message phrases to flag/filter
SYSTEM_PHRASES = [
    "end-to-end encrypted",
    "created group",
    "added",
    "removed",
    "left",
    "changed the subject",
    "changed the group icon",
    "security code changed",
    "this message was deleted",
    "you deleted this message",
    "media omitted",
    "<media omitted>",
]


def is_system_message(text: str, sender: Optional[str] = None) -> bool:
    """Checks if a message is an automated WhatsApp system notification."""
    lower_text = text.lower()
    for phrase in SYSTEM_PHRASES:
        if phrase in lower_text:
            return True
    return False


def parse_chat_text(raw_text: str) -> List[ParsedMessage]:
    """
    Parses raw WhatsApp chat export text into a list of structured ParsedMessage objects.
    Preserves original line numbers for source citation.
    Handles multi-line messages seamlessly.
    """
    lines = raw_text.splitlines()
    messages: List[ParsedMessage] = []
    current_msg: Optional[dict] = None

    for line_idx, line in enumerate(lines, start=1):
        clean_line = line.strip()
        if not clean_line:
            continue

        # Check for iOS or Android timestamp match
        match = IOS_PATTERN.match(clean_line) or ANDROID_PATTERN.match(clean_line)

        if match:
            # Commit the previous message if one was in progress
            if current_msg:
                messages.append(ParsedMessage(**current_msg))
                current_msg = None

            date_str = match.group("date")
            time_str = match.group("time")
            rest = match.group("rest")
            timestamp = f"{date_str} {time_str}"

            # Check if there is an explicit sender
            sender_match = SENDER_PATTERN.match(rest)
            if sender_match:
                sender = sender_match.group("sender").strip()
                text = sender_match.group("text").strip()
                sys_msg = is_system_message(text)
            else:
                sender = "System"
                text = rest.strip()
                sys_msg = True

            current_msg = {
                "message_id": str(uuid.uuid4())[:8],
                "line_number": line_idx,
                "timestamp": timestamp,
                "sender": sender,
                "text": text,
                "is_system": sys_msg,
            }
        else:
            # Continuation of previous multi-line message
            if current_msg:
                current_msg["text"] += f"\n{clean_line}"
            else:
                # Leading lines before any timestamp
                continue

    if current_msg:
        messages.append(ParsedMessage(**current_msg))

    return messages


def extract_text_from_file_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Accepts raw file bytes and filename. Detects .zip either by extension or
    magic bytes (PK\x03\x04), unpacking the primary chat text file.
    Decodes using robust multi-encoding fallbacks.
    """
    is_zip = filename.lower().endswith(".zip") or file_bytes[:4] == b"PK\x03\x04"
    if is_zip:
        try:
            with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                candidates = [
                    f for f in z.namelist()
                    if not f.startswith("__MACOSX") and not f.endswith("/")
                ]
                txt_files = [f for f in candidates if f.lower().endswith((".txt", ".text", ".chat"))]
                if txt_files:
                    preferred = next((f for f in txt_files if "_chat.txt" in f.lower()), txt_files[0])
                    return _decode_bytes(z.read(preferred))

                non_media = [
                    f for f in candidates
                    if not f.lower().endswith((".jpg", ".jpeg", ".png", ".opus", ".mp4", ".mp3", ".webp", ".gif"))
                ]
                if non_media:
                    return _decode_bytes(z.read(non_media[0]))

                raise ValueError("No text chat file found inside the zip archive.")
        except zipfile.BadZipFile:
            return _decode_bytes(file_bytes)

    return _decode_bytes(file_bytes)



def _decode_bytes(b: bytes) -> str:
    """Decodes bytes with robust multi-encoding fallbacks."""
    for enc in ["utf-8-sig", "utf-8", "latin-1", "cp1252"]:
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", errors="replace")
