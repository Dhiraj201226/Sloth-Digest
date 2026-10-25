"""
Sloth Digest — Nightly CLI Daemon (`sloth run`)
Enables lazy-first operation: user drops files into watched_chats/,
and the overnight job reads them automatically.
"""

import sys
import argparse
import hashlib
import time
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from backend.config import WATCHED_DIR, DEFAULT_MODEL
from backend.parser import parse_chat_text, extract_text_from_file_bytes
from backend.orchestrator import digest_chat
from backend.database import init_db, get_connection
from backend.tidier import scan_tidier_directory, apply_tidy_action


def get_file_hash(path: Path) -> str:
    """Calculates SHA256 of file for change detection."""
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def process_watched_file(file_path: Path, model_name: str = DEFAULT_MODEL) -> bool:
    """Processes a single chat file if new or modified."""
    file_hash = get_file_hash(file_path)

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT file_hash, status FROM watched_files WHERE file_path = ?", (str(file_path),))
        row = cursor.fetchone()
        if row and row["file_hash"] == file_hash and row["status"] == "processed":
            # Already digested
            return False

    print(f"🦥 [Sloth Run] Processing: {file_path.name} ...")
    raw_bytes = file_path.read_bytes()
    raw_text = extract_text_from_file_bytes(raw_bytes, file_path.name)
    messages = parse_chat_text(raw_text)

    if not messages:
        print(f"⚠️ [Sloth Run] No messages found in {file_path.name}")
        return False

    def progress(p):
        print(f"   [{p.percent}%] {p.message} (~{p.estimated_remaining_sec}s remaining)")

    digest = digest_chat(
        messages=messages,
        chat_name=file_path.stem,
        model_name=model_name,
        progress_callback=progress
    )

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO watched_files (file_path, file_hash, last_processed_at, digest_id, status)
            VALUES (?, ?, CURRENT_TIMESTAMP, ?, 'processed')
        """, (str(file_path), file_hash, digest.id))
        conn.commit()

    print(f"✅ [Sloth Run] Digested {digest.chat_name}: {digest.total_messages} messages read, {digest.safe_to_ignore_count} safely ignored.")
    print(f"   Summary:\n   {digest.two_line_summary}")
    return True


def run_sloth_job(watch_dir: Path = WATCHED_DIR, model_name: str = DEFAULT_MODEL):
    """One-shot batch run across watched directory."""
    init_db()
    watch_dir.mkdir(parents=True, exist_ok=True)
    files = [f for f in watch_dir.iterdir() if f.is_file() and f.suffix.lower() in [".txt", ".zip"]]

    if not files:
        print(f"🦥 [Sloth Run] No chat files found in watched folder: {watch_dir}")
        print("   Drop a WhatsApp export (.txt or .zip) into the folder to digest.")
        return

    processed_count = 0
    for f in files:
        if process_watched_file(f, model_name=model_name):
            processed_count += 1

    if processed_count == 0:
        print("🦥 [Sloth Run] All files up to date. Nothing to do. Stay lazy!")
    else:
        print(f"🦥 [Sloth Run] Successfully digested {processed_count} chat(s). Ready for morning glance.")


def main():
    parser = argparse.ArgumentParser(description="Sloth Digest CLI: Automated offline morning reader.")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    run_parser = subparsers.add_parser("run", help="Run overnight batch digestion on watched folder.")
    run_parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model tag override.")
    run_parser.add_argument("--loop", action="store_true", help="Keep running as daemon polling every 60s.")

    tidy_parser = subparsers.add_parser("tidy", help="Scan and tidy chat archive folder.")
    tidy_parser.add_argument("--apply", action="store_true", help="Automatically apply tidy recommendations.")

    args = parser.parse_args()

    if args.command == "run":
        if args.loop:
            print("🦥 Sloth Daemon started. Polling watched folder every 60s (Ctrl+C to stop)...")
            try:
                while True:
                    run_sloth_job(model_name=args.model)
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n🦥 Sloth Daemon stopped.")
        else:
            run_sloth_job(model_name=args.model)
    elif args.command == "tidy":
        suggestions = scan_tidier_directory()
        if not suggestions:
            print("✨ Watched folder is already tidy! No actions needed.")
            return
        print(f"Found {len(suggestions)} tidy suggestions:")
        for idx, s in enumerate(suggestions, 1):
            print(f"  {idx}. [{s.action.upper()}] {s.original_name} -> {s.suggested_name} ({s.reason})")
        if args.apply:
            for s in suggestions:
                apply_tidy_action(s)
            print("✅ Applied all tidy suggestions!")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
