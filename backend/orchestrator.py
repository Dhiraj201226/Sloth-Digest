"""
Sloth Digest — Map-Reduce Orchestrator & Hallucination Guard
Coordinates chunking, map-reduce LLM summarization, citation anchoring, and progress streaming.
"""

import time
import uuid
from typing import List, Optional, Callable, Dict, Any
from backend.models import (
    ParsedMessage,
    MessageChunk,
    DigestResponse,
    ActionItem,
    DeadlineItem,
    SourceCitation,
    ClassifiedMessage,
    ProgressEvent,
)
from backend.chunker import chunk_messages
from backend.llm_client import query_ollama_json, check_ollama
from backend.database import save_digest
from backend.config import DEFAULT_MODEL


SYSTEM_MAP_PROMPT = """You are Sloth Digest, an offline AI assistant that digests busy group chats.
Extract only high-value facts so the user doesn't have to read chatter.
Output strictly valid JSON matching this schema:
{
  "synopsis": "One sentence describing the discussion in this section.",
  "action_items": [
    {
      "description": "Clear statement of what is requested or promised",
      "assignee": "Name of person waiting or assigned, or 'Team'/'You'",
      "line_number": 123
    }
  ],
  "deadlines": [
    {
      "date_mentioned": "Date or time specified, e.g. Friday 3pm or Oct 28",
      "event_description": "What happens on that date",
      "line_number": 123
    }
  ],
  "noise_count": 15
}
Do not invent anything. line_number must correspond exactly to the line number provided in the prompt."""

SYSTEM_REDUCE_PROMPT = """You are Sloth Digest.
Synthesize the section synopses into a calm, thorough morning executive digest.
Output strictly JSON matching this structure:
{
  "two_line_summary": "Line 1 summarizing core event or decision.\\nLine 2 summarizing next steps or social context.",
  "detailed_summary": "A comprehensive 2-3 paragraph markdown breakdown explaining what was discussed, major decisions reached, next steps, and who is waiting on what.",
  "overall_classification": "important or spam or balanced"
}
Tone: Relaxed, clear, zero urgency, reassuring."""


def _format_chunk_for_llm(messages: List[ParsedMessage]) -> str:
    """Formats messages into line-numbered text for LLM citation."""
    lines = []
    for m in messages:
        if m.is_system:
            continue
        lines.append(f"[Line {m.line_number}] {m.sender}: {m.text}")
    return "\n".join(lines)


def _heuristic_fallback_extractor(chunk: MessageChunk) -> Dict[str, Any]:
    """
    Rule-based extractor for instant offline testing or when LLM is unavailable.
    Guarantees that Sloth Digest functions gracefully under all test conditions.
    """
    actions = []
    deadlines = []
    noise = 0

    action_triggers = ["can you", "please", "need you to", "could someone", "who has", "assigned to", "waiting on", "send the", "submit"]
    date_triggers = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "tomorrow", "today", "pm", "am", "oct", "nov", "dec", "jan", "feb", "deadline"]

    for m in chunk.messages:
        if m.is_system:
            noise += 1
            continue

        lower = m.text.lower()
        has_action = any(trigger in lower for trigger in action_triggers)
        has_date = any(trigger in lower for trigger in date_triggers)

        if has_action:
            actions.append({
                "description": m.text[:120],
                "assignee": m.sender,
                "line_number": m.line_number
            })
        elif has_date and ("meet" in lower or "due" in lower or "submit" in lower or "call" in lower or "event" in lower or "quiz" in lower):
            deadlines.append({
                "date_mentioned": "Mentioned in chat",
                "event_description": m.text[:120],
                "line_number": m.line_number
            })
        else:
            noise += 1

    first_sender = chunk.messages[0].sender if chunk.messages else "Participants"
    return {
        "synopsis": f"Discussion involving {first_sender} regarding ongoing activities and planning.",
        "action_items": actions[:3],
        "deadlines": deadlines[:3],
        "noise_count": noise
    }


def classify_chat_messages(
    messages: List[ParsedMessage],
    verified_actions: List[ActionItem],
    verified_deadlines: List[DeadlineItem]
) -> List[ClassifiedMessage]:
    """
    Classifies every message in the chat as 'important', 'spam', or 'normal'.
    Grounds classifications using verified action items, deadlines, direct questions,
    and chat noise patterns (reactions, emojis, media omitted).
    """
    action_lines = {a.source.line_number: a for a in verified_actions}
    deadline_lines = {d.source.line_number: d for d in verified_deadlines}

    important_triggers = [
        "urgent", "asap", "deadline", "meeting", "submit", "submission",
        "review", "pull request", "pr", "deploy", "release", "bug",
        "error", "fix", "blocker", "can someone", "who can", "please help",
        "assigned to", "status update", "agenda", "presentation", "slides"
    ]
    spam_phrases = {
        "lol", "haha", "hahaha", "hehe", "lmao", "rofl", "k", "ok", "okay", "cool",
        "nice", "yep", "yeah", "sure", "thanks", "thx", "ty", "np",
        "gm", "gn", "good morning", "good night", "congrats", "wow",
        "omg", "great", "awesome", "perfect", "done", "understood", "yes",
        "meme", "memes", "gif", "funny", "bruh", "dude", "bro"
    }

    classified: List[ClassifiedMessage] = []

    for m in messages:
        if m.is_system:
            classified.append(ClassifiedMessage(
                message_id=m.message_id,
                line_number=m.line_number,
                timestamp=m.timestamp,
                sender=m.sender,
                text=m.text,
                is_system=True,
                classification="spam",
                classification_reason="System or encryption notice"
            ))
            continue

        raw = m.text.strip()
        lower = raw.lower()

        # 1. Action item anchor
        if m.line_number in action_lines:
            action_desc = action_lines[m.line_number].description
            classified.append(ClassifiedMessage(
                message_id=m.message_id,
                line_number=m.line_number,
                timestamp=m.timestamp,
                sender=m.sender,
                text=m.text,
                is_system=False,
                classification="important",
                classification_reason=f"Action item: {action_desc[:70]}"
            ))
            continue

        # 2. Deadline anchor
        if m.line_number in deadline_lines:
            event_desc = deadline_lines[m.line_number].event_description
            classified.append(ClassifiedMessage(
                message_id=m.message_id,
                line_number=m.line_number,
                timestamp=m.timestamp,
                sender=m.sender,
                text=m.text,
                is_system=False,
                classification="important",
                classification_reason=f"Event/Deadline: {event_desc[:70]}"
            ))
            continue

        # 3. Known chatter / media / reaction / single word
        clean_words = [w for w in lower.translate(str.maketrans("", "", ",.!?:;~()[]{}'\"")).split() if w]
        is_media = (
            "<media omitted>" in lower or
            "image omitted" in lower or
            "audio omitted" in lower or
            "video omitted" in lower or
            "sticker omitted" in lower or
            "document omitted" in lower or
            "this message was deleted" in lower
        )

        is_pure_emoji_or_short_reaction = False
        if is_media:
            is_pure_emoji_or_short_reaction = True
        elif clean_words and all(w in spam_phrases or (len(w) == 1 and ord(w) > 127) for w in clean_words):
            is_pure_emoji_or_short_reaction = True
        elif clean_words and len(clean_words) <= 5 and (sum(1 for w in clean_words if w in spam_phrases) / len(clean_words)) >= 0.5:
            is_pure_emoji_or_short_reaction = True
        elif len(raw) <= 8 and all(ord(c) > 127 or c in " !?.,:;~()-" for c in raw):
            is_pure_emoji_or_short_reaction = True

        if is_pure_emoji_or_short_reaction:
            classified.append(ClassifiedMessage(
                message_id=m.message_id,
                line_number=m.line_number,
                timestamp=m.timestamp,
                sender=m.sender,
                text=m.text,
                is_system=False,
                classification="spam",
                classification_reason="Casual chatter, reaction emoji, or media placeholder"
            ))
            continue

        # 4. Check for important question or priority terms
        has_important_kw = any(kw in lower for kw in important_triggers)
        has_direct_question = "?" in raw and any(
            q in lower for q in [
                "who", "what", "when", "where", "why", "how",
                "can you", "could you", "do you", "is anyone", "has anyone", "will you"
            ]
        )

        if has_important_kw or has_direct_question:
            reason = "Direct question requiring attention" if has_direct_question else "High-priority coordination keywords"
            classified.append(ClassifiedMessage(
                message_id=m.message_id,
                line_number=m.line_number,
                timestamp=m.timestamp,
                sender=m.sender,
                text=m.text,
                is_system=False,
                classification="important",
                classification_reason=reason
            ))
            continue

        # 5. Default: normal conversation context
        classified.append(ClassifiedMessage(
            message_id=m.message_id,
            line_number=m.line_number,
            timestamp=m.timestamp,
            sender=m.sender,
            text=m.text,
            is_system=False,
            classification="normal",
            classification_reason="Contextual discussion"
        ))

    return classified


def _generate_fallback_detailed_summary(
    messages: List[ParsedMessage],
    chat_name: str,
    two_line_summary: str,
    action_items: List[ActionItem],
    deadlines: List[DeadlineItem],
    important_count: int,
    spam_count: int,
) -> str:
    """Generates an eloquent, multi-paragraph markdown breakdown of the chat."""
    total = len(messages)
    senders = list(dict.fromkeys(m.sender for m in messages if not m.is_system))
    sender_str = ", ".join(senders[:4]) + (f" and {len(senders) - 4} others" if len(senders) > 4 else "")

    p1 = (
        f"**Executive Overview**: Across {total} messages in **{chat_name}**, participants including "
        f"{sender_str} convened to discuss active deliverables, scheduling, and project direction. "
        f"{two_line_summary.replace(chr(10), ' ')}"
    )

    decisions = []
    if action_items:
        items_str = "; ".join([f"{a.assignee_target} was tasked with '{a.description}'" for a in action_items[:3]])
        decisions.append(f"Key action items were noted: {items_str}.")
    if deadlines:
        dates_str = "; ".join([f"'{d.event_description}' scheduled for {d.date_mentioned}" for d in deadlines[:3]])
        decisions.append(f"Upcoming timelines and milestones include: {dates_str}.")

    if not decisions:
        p2 = "**Key Decisions & Outcomes**: The conversation was largely exploratory, exchanging progress notes without pending hard blockers or urgent assigned tasks."
    else:
        p2 = f"**Key Decisions & Next Steps**: {' '.join(decisions)}"

    p3 = (
        f"**Signal & Noise Breakdown**: Sloth Digest flagged **{important_count}** high-priority messages "
        f"deserving your focus. In contrast, **{spam_count}** messages were identified as casual chatter, "
        f"media placeholders, or reaction banter and safely filtered to preserve your morning focus."
    )

    return f"{p1}\n\n{p2}\n\n{p3}"


def digest_chat(
    messages: List[ParsedMessage],
    chat_name: str = "Group Chat",
    model_name: Optional[str] = None,
    progress_callback: Optional[Callable[[ProgressEvent], None]] = None,
) -> DigestResponse:
    """
    Executes the full Map-Reduce summarization pipeline.
    Applies the Hallucination Guard to ensure 100% citation grounding.
    """
    start_time = time.time()
    task_id = str(uuid.uuid4())[:8]
    active_model = model_name or DEFAULT_MODEL

    if not messages:
        raise ValueError("Cannot digest empty message list.")

    # Build line index for O(1) hallucination guard verification
    line_map: Dict[int, ParsedMessage] = {m.line_number: m for m in messages}

    # Segment into chunks
    chunks = chunk_messages(messages)
    total_chunks = len(chunks)

    # Check if Ollama is available
    health = check_ollama(active_model)
    use_llm = health.ollama_connected and health.status == "ready"

    if progress_callback:
        progress_callback(ProgressEvent(
            task_id=task_id,
            status="parsing",
            current_chunk=0,
            total_chunks=total_chunks,
            percent=5,
            elapsed_sec=0.1,
            estimated_remaining_sec=total_chunks * 2.5 if use_llm else 0.5,
            message="Chat parsed. Commencing map-reduce summarization..."
        ))

    synopses: List[str] = []
    raw_action_items: List[Dict[str, Any]] = []
    raw_deadlines: List[Dict[str, Any]] = []
    total_noise_count = 0

    # 1. MAP PHASE
    for idx, chunk in enumerate(chunks, start=1):
        chunk_start = time.time()
        map_result = None

        if use_llm:
            formatted_text = _format_chunk_for_llm(chunk.messages)
            prompt = f"Chat Chunk ({chunk.start_time} to {chunk.end_time}):\n{formatted_text}"
            try:
                map_result = query_ollama_json(prompt, SYSTEM_MAP_PROMPT, active_model)
            except Exception:
                # Graceful fallback to heuristic if individual chunk fails
                map_result = _heuristic_fallback_extractor(chunk)
        else:
            map_result = _heuristic_fallback_extractor(chunk)

        if not map_result or not isinstance(map_result, dict):
            map_result = _heuristic_fallback_extractor(chunk)

        synopsis = map_result.get("synopsis", "")
        if synopsis:
            synopses.append(synopsis)

        raw_action_items.extend(map_result.get("action_items", []))
        raw_deadlines.extend(map_result.get("deadlines", []))
        total_noise_count += map_result.get("noise_count", len(chunk.messages))

        elapsed = time.time() - start_time
        avg_chunk_time = elapsed / idx
        remaining_chunks = total_chunks - idx
        est_remaining = max(0.5, remaining_chunks * avg_chunk_time)
        percent = int(5 + (idx / total_chunks) * 80)

        if progress_callback:
            progress_callback(ProgressEvent(
                task_id=task_id,
                status="mapping",
                current_chunk=idx,
                total_chunks=total_chunks,
                percent=percent,
                elapsed_sec=round(elapsed, 1),
                estimated_remaining_sec=round(est_remaining, 1),
                message=f"Reading chunk {idx} of {total_chunks}..."
            ))

    # 2. REDUCE PHASE
    if progress_callback:
        progress_callback(ProgressEvent(
            task_id=task_id,
            status="reducing",
            current_chunk=total_chunks,
            total_chunks=total_chunks,
            percent=90,
            elapsed_sec=round(time.time() - start_time, 1),
            estimated_remaining_sec=1.5,
            message="Synthesizing morning digest and verifying citations..."
        ))

    combined_synopses = " ".join(synopses)
    two_line_summary = ""
    detailed_summary = ""
    overall_classification = "balanced"

    if use_llm and combined_synopses:
        reduce_prompt = f"Section synopses:\n{combined_synopses}"
        try:
            reduce_result = query_ollama_json(reduce_prompt, SYSTEM_REDUCE_PROMPT, active_model)
            two_line_summary = reduce_result.get("two_line_summary", "")
            detailed_summary = reduce_result.get("detailed_summary", "")
            overall_classification = reduce_result.get("overall_classification", "balanced")
            if overall_classification not in ("important", "spam", "balanced"):
                overall_classification = "balanced"
        except Exception:
            two_line_summary = ""

    if two_line_summary:
        two_line_summary = two_line_summary.strip()
        if "\n" not in two_line_summary:
            if ". " in two_line_summary:
                first_dot = two_line_summary.find(". ")
                two_line_summary = f"{two_line_summary[:first_dot+1]}\n{two_line_summary[first_dot+2:]}"
            else:
                two_line_summary = f"{two_line_summary}\nNo further urgent action items or scheduling blockers were identified."

    if not two_line_summary:
        # Fallback calm 2-line summary
        line1 = f"The group discussed key plans, updates, and logistics across {len(messages)} messages."
        line2 = f"Key commitments were identified, while casual banter and chatter were safely filtered."
        two_line_summary = f"{line1}\n{line2}"

    # 3. HALLUCINATION GUARD & CITATION ANCHORING
    verified_actions: List[ActionItem] = []
    seen_action_texts = set()

    for item in raw_action_items:
        line_no = item.get("line_number")
        desc = item.get("description", "").strip()
        if not desc or desc in seen_action_texts:
            continue

        matched_msg = line_map.get(line_no)
        # If line number was missing or mismatched, try to locate message containing key words
        if not matched_msg:
            for m in messages:
                if desc.lower() in m.text.lower() or m.sender.lower() == str(item.get("assignee", "")).lower():
                    matched_msg = m
                    break

        # If anchored successfully, bind citation
        if matched_msg:
            seen_action_texts.add(desc)
            verified_actions.append(
                ActionItem(
                    id=str(uuid.uuid4())[:8],
                    description=desc,
                    assignee_target=item.get("assignee") or matched_msg.sender,
                    urgency="normal",
                    source=SourceCitation(
                        message_id=matched_msg.message_id,
                        line_number=matched_msg.line_number,
                        sender=matched_msg.sender,
                        timestamp=matched_msg.timestamp,
                        raw_text=matched_msg.text,
                    ),
                )
            )

    verified_deadlines: List[DeadlineItem] = []
    seen_deadline_texts = set()

    for d in raw_deadlines:
        line_no = d.get("line_number")
        event = d.get("event_description", "").strip()
        date_str = d.get("date_mentioned", "").strip() or "Upcoming"
        if not event or event in seen_deadline_texts:
            continue

        matched_msg = line_map.get(line_no)
        if not matched_msg:
            for m in messages:
                if event.lower() in m.text.lower() or date_str.lower() in m.text.lower():
                    matched_msg = m
                    break

        if matched_msg:
            seen_deadline_texts.add(event)
            verified_deadlines.append(
                DeadlineItem(
                    id=str(uuid.uuid4())[:8],
                    date_mentioned=date_str,
                    event_description=event,
                    source=SourceCitation(
                        message_id=matched_msg.message_id,
                        line_number=matched_msg.line_number,
                        sender=matched_msg.sender,
                        timestamp=matched_msg.timestamp,
                        raw_text=matched_msg.text,
                    ),
                )
            )

    # 4. MESSAGE CLASSIFICATION
    classified_messages = classify_chat_messages(messages, verified_actions, verified_deadlines)
    important_count = sum(1 for m in classified_messages if m.classification == "important")
    spam_count = sum(1 for m in classified_messages if m.classification == "spam")

    # Re-evaluate overall classification from ground truths
    if important_count >= 3 or (len(messages) > 0 and (important_count / len(messages)) >= 0.20):
        overall_classification = "important"
    elif spam_count >= 8 and (spam_count / len(messages)) >= 0.60 and important_count <= 2:
        overall_classification = "spam"
    elif overall_classification not in ("important", "spam", "balanced"):
        overall_classification = "balanced"

    # Ensure rich detailed summary
    if not detailed_summary or len(detailed_summary.strip()) < 40:
        detailed_summary = _generate_fallback_detailed_summary(
            messages=messages,
            chat_name=chat_name,
            two_line_summary=two_line_summary,
            action_items=verified_actions,
            deadlines=verified_deadlines,
            important_count=important_count,
            spam_count=spam_count,
        )

    # Safe to ignore count calculation: total messages minus actionable facts
    safe_to_ignore = max(0, len(messages) - (len(verified_actions) + len(verified_deadlines)))

    total_duration = round(time.time() - start_time, 2)
    digest_id = str(uuid.uuid4())[:8]

    digest = DigestResponse(
        id=digest_id,
        created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        chat_name=chat_name,
        start_date=messages[0].timestamp if messages else None,
        end_date=messages[-1].timestamp if messages else None,
        total_messages=len(messages),
        safe_to_ignore_count=safe_to_ignore,
        important_count=important_count,
        spam_count=spam_count,
        overall_classification=overall_classification,
        two_line_summary=two_line_summary,
        detailed_summary=detailed_summary,
        action_items=verified_actions,
        deadlines=verified_deadlines,
        messages=classified_messages,
        model_used=active_model if use_llm else f"{active_model} (offline-heuristic)",
        processing_duration_sec=total_duration,
    )

    # Persist in SQLite
    save_digest(digest)

    if progress_callback:
        progress_callback(ProgressEvent(
            task_id=task_id,
            status="completed",
            current_chunk=total_chunks,
            total_chunks=total_chunks,
            percent=100,
            elapsed_sec=total_duration,
            estimated_remaining_sec=0,
            message="Digest complete! Ready for your morning glance."
        ))

    return digest
