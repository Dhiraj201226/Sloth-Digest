"""
Sloth Digest — Data Models & Schemas
Pydantic v2 schemas for parsing, chunking, attribution, and API responses.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ParsedMessage(BaseModel):
    """Represents a single parsed message line from a chat export."""
    message_id: str
    line_number: int
    timestamp: str
    sender: str
    text: str
    is_system: bool = False


class ClassifiedMessage(BaseModel):
    """Represents a chat message with AI classification and reason."""
    message_id: str
    line_number: int
    timestamp: str
    sender: str
    text: str
    is_system: bool = False
    classification: str = "normal"  # "important" | "spam" | "normal"
    classification_reason: Optional[str] = None


class MessageChunk(BaseModel):
    """A chronological slice of messages for map-reduce processing."""
    chunk_index: int
    total_chunks: int
    messages: List[ParsedMessage]
    start_time: str
    end_time: str


class SourceCitation(BaseModel):
    """Hallucination guard: links extracted facts directly back to source message."""
    message_id: str
    line_number: int
    sender: str
    timestamp: str
    raw_text: str


class ActionItem(BaseModel):
    """An action or request directed at or concerning someone."""
    id: str
    description: str
    assignee_target: str = "You"
    urgency: str = "normal"  # 'normal' | 'low'
    source: SourceCitation


class DeadlineItem(BaseModel):
    """A date, meeting, or deadline mentioned in conversation."""
    id: str
    date_mentioned: str
    event_description: str
    source: SourceCitation


class DigestResponse(BaseModel):
    """Complete morning digest payload."""
    model_config = {"protected_namespaces": ()}

    id: str
    created_at: str
    chat_name: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_messages: int
    safe_to_ignore_count: int
    important_count: int = 0
    spam_count: int = 0
    overall_classification: str = "balanced"  # "important" | "spam" | "balanced"
    two_line_summary: str
    detailed_summary: Optional[str] = None
    action_items: List[ActionItem] = Field(default_factory=list)
    deadlines: List[DeadlineItem] = Field(default_factory=list)
    messages: List[ClassifiedMessage] = Field(default_factory=list)
    model_used: str
    processing_duration_sec: float



class ProgressEvent(BaseModel):
    """Real-time SSE event payload during digestion."""
    task_id: str
    status: str  # 'parsing' | 'mapping' | 'reducing' | 'completed' | 'error'
    current_chunk: int
    total_chunks: int
    percent: int
    elapsed_sec: float
    estimated_remaining_sec: float
    message: str


class SystemHealth(BaseModel):
    """Local offline status and Ollama availability."""
    status: str
    is_offline: bool = True
    ollama_connected: bool
    active_model: str
    available_models: List[str] = Field(default_factory=list)
    host: str
    error_message: Optional[str] = None


class TidySuggestion(BaseModel):
    """File organization and archive suggestion."""
    file_path: str
    original_name: str
    suggested_name: str
    action: str  # 'rename' | 'archive' | 'keep'
    reason: str
