"""
Sloth Digest — File & Inbox Tidier (Stretch Goal: Rewarding Laziness)
Scans directories for messy chat exports, suggests standardized naming,
and archives stale chats into an archive subfolder with 1-click execution.
"""

import os
import shutil
import re
import time
from pathlib import Path
from typing import List, Optional
from backend.models import TidySuggestion
from backend.config import WATCHED_DIR, ARCHIVE_DIR


def scan_tidier_directory(directory_path: Optional[str] = None) -> List[TidySuggestion]:

    """
    Scans the given folder for chat export files and identifies cleanup opportunities.
    """
    folder = Path(directory_path) if directory_path else WATCHED_DIR
    folder.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    suggestions: List[TidySuggestion] = []
    now = time.time()
    fourteen_days_sec = 14 * 86400

    for item in folder.iterdir():
        if item.is_dir() or item.name.startswith("."):
            continue

        ext = item.suffix.lower()
        if ext not in [".txt", ".zip"]:
            continue

        filename = item.name
        file_mtime = item.stat().st_mtime
        age_days = int((now - file_mtime) / 86400)

        # 1. Archive suggestions for files older than 14 days
        if age_days > 14:
            suggestions.append(
                TidySuggestion(
                    file_path=str(item),
                    original_name=filename,
                    suggested_name=filename,
                    action="archive",
                    reason=f"File is {age_days} days old and has already been processed.",
                )
            )
            continue

        # 2. Rename messy WhatsApp default names, e.g. "WhatsApp Chat with CS301 (1).txt"
        clean_name = filename
        changed = False

        if "WhatsApp Chat with " in clean_name:
            clean_name = clean_name.replace("WhatsApp Chat with ", "")
            changed = True
        elif "WhatsApp Chat - " in clean_name:
            clean_name = clean_name.replace("WhatsApp Chat - ", "")
            changed = True

        # Remove duplicate indicators like " (1)" or "_copy"
        if re.search(r"\s*\(\d+\)", clean_name):
            clean_name = re.sub(r"\s*\(\d+\)", "", clean_name)
            changed = True

        # Standardize spaces to underscores
        clean_stem = Path(clean_name).stem.strip().replace(" ", "_")
        standardized_name = f"{clean_stem}{ext}"

        if changed or standardized_name != filename:
            suggestions.append(
                TidySuggestion(
                    file_path=str(item),
                    original_name=filename,
                    suggested_name=standardized_name,
                    action="rename",
                    reason="Remove redundant WhatsApp prefixes and duplicate markers.",
                )
            )

    return suggestions


def apply_tidy_action(suggestion: TidySuggestion) -> bool:
    """Applies a single rename or archive action."""
    source_path = Path(suggestion.file_path)
    if not source_path.exists():
        return False

    if suggestion.action == "archive":
        target = ARCHIVE_DIR / suggestion.original_name
        shutil.move(str(source_path), str(target))
        return True
    elif suggestion.action == "rename":
        target = source_path.parent / suggestion.suggested_name
        if not target.exists():
            source_path.rename(target)
            return True

    return False
