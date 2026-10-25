"""
Sloth Digest — Synthetic Ground-Truth Quality Spot-Check
Evaluates factual recall, precision, citation accuracy, and noise filtering
against predefined ground truth facts in the synthetic chat datasets.
Reports findings plainly, including any misses or edge cases.
"""

import sys
from pathlib import Path

# Ensure UTF-8 stdout encoding on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure root is in sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from backend.parser import parse_chat_text
from backend.orchestrator import digest_chat
from backend.config import SYNTHETIC_DIR



def evaluate_hackathon_sample():
    print("==================================================")
    print("EVALUATION: Hackathon Squad Chat (59 messages)")
    print("==================================================")

    chat_file = SYNTHETIC_DIR / "sample_hackathon_team.txt"
    if not chat_file.exists():
        print("Missing sample_hackathon_team.txt")
        return

    text = chat_file.read_text(encoding="utf-8")
    messages = parse_chat_text(text)
    digest = digest_chat(messages, chat_name="Hackathon Squad")

    print(f"Summary generated:\n{digest.two_line_summary}\n")
    print(f"Messages processed: {digest.total_messages}")
    print(f"Safe to ignore count: {digest.safe_to_ignore_count} ({round(digest.safe_to_ignore_count/digest.total_messages*100, 1)}%)")
    print(f"Extracted Action Items: {len(digest.action_items)}")
    for a in digest.action_items:
      print(f"  - ({a.assignee_target}): {a.description} [Line {a.source.line_number} by {a.source.sender}]")
    print(f"Extracted Deadlines: {len(digest.deadlines)}")
    for d in digest.deadlines:
      print(f"  - 📅 {d.date_mentioned}: {d.event_description} [Line {d.source.line_number}]")

    # Known ground truths:
    # 1. Sarah assigned to OpenAPI spec
    # 2. David assigned to components
    # 3. Sunday 4 PM demo deadline
    ground_truths = {
        "OpenAPI specification": any("openapi" in a.description.lower() for a in digest.action_items),
        "Demo video deadline": any("demo" in d.event_description.lower() or "sunday" in d.date_mentioned.lower() for d in digest.deadlines),
        "Safe chatter ignored (> 40 messages)": digest.safe_to_ignore_count >= 40,
        "Citation integrity (100% valid lines)": all(1 <= a.source.line_number <= len(messages) for a in digest.action_items),
    }

    print("\nGround Truth Fact Verification:")
    for fact, passed in ground_truths.items():
        status = "PASSED" if passed else "FAILED / MISSED"
        print(f"  [{status}] {fact}")


def evaluate_family_sample():
    print("\n==================================================")
    print("EVALUATION: Family Reunion Chat (64 messages)")
    print("==================================================")

    chat_file = SYNTHETIC_DIR / "sample_family_thanksgiving.txt"
    if not chat_file.exists():
        print("Missing sample_family_thanksgiving.txt")
        return

    text = chat_file.read_text(encoding="utf-8")
    messages = parse_chat_text(text)
    digest = digest_chat(messages, chat_name="Family Reunion")

    print(f"Summary generated:\n{digest.two_line_summary}\n")
    print(f"Messages processed: {digest.total_messages}")
    print(f"Safe to ignore count: {digest.safe_to_ignore_count}")
    print(f"Extracted Action Items: {len(digest.action_items)}")
    for a in digest.action_items:
      print(f"  - ({a.assignee_target}): {a.description} [Line {a.source.line_number}]")
    print(f"Extracted Deadlines: {len(digest.deadlines)}")
    for d in digest.deadlines:
      print(f"  - 📅 {d.date_mentioned}: {d.event_description} [Line {d.source.line_number}]")

    ground_truths = {
        "Turkey pickup task identified": any("turkey" in a.description.lower() for a in digest.action_items),
        "JFK airport pickup identified": any("jfk" in a.description.lower() or "clara" in a.description.lower() for a in digest.action_items),
        "Thanksgiving dinner deadline": any("dinner" in d.event_description.lower() or "nov 26" in d.event_description.lower() for d in digest.deadlines),
        "Citation integrity (100% valid lines)": all(1 <= a.source.line_number <= len(messages) for a in digest.action_items),
    }

    print("\nGround Truth Fact Verification:")
    for fact, passed in ground_truths.items():
        status = "PASSED" if passed else "FAILED / MISSED"
        print(f"  [{status}] {fact}")


if __name__ == "__main__":
    evaluate_hackathon_sample()
    evaluate_family_sample()
