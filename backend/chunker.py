"""
Sloth Digest — Chunking Engine
Segments message streams chronologically into map-reduce chunks.
"""

from typing import List
from backend.models import ParsedMessage, MessageChunk
from backend.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_messages(messages: List[ParsedMessage], chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[MessageChunk]:
    """
    Slices a chronological list of parsed messages into overlapping or partitioned chunks.
    Ensures that conversation context isn't lost at boundaries.
    """
    if not messages:
        return []

    chunks: List[MessageChunk] = []
    total_msgs = len(messages)
    step = max(1, chunk_size - overlap)

    raw_slices = []
    for i in range(0, total_msgs, step):
        slice_msgs = messages[i : i + chunk_size]
        if slice_msgs:
            raw_slices.append(slice_msgs)
        if i + chunk_size >= total_msgs:
            break

    total_chunks = len(raw_slices)
    for idx, slice_msgs in enumerate(raw_slices, start=1):
        chunks.append(
            MessageChunk(
                chunk_index=idx,
                total_chunks=total_chunks,
                messages=slice_msgs,
                start_time=slice_msgs[0].timestamp,
                end_time=slice_msgs[-1].timestamp,
            )
        )

    return chunks
