import json
import logging
from typing import Any, Dict, List, Tuple, Union
from pydantic import ValidationError
from schemas.requests import ImportRequest, MemoryRequest
import re

logger = logging.getLogger(__name__)

def normalize_content(text: str) -> str:
    """Normalizes memory content by stripping whitespace, lowercasing, and flattening newlines."""
    return re.sub(r'\s+', ' ', text.strip().lower())

"""
Parses raw memory import data into a structured ImportRequest and collects any malformed items.

Args:
    raw_data (str | dict): JSON string or Python dict representing exported memory data.

Returns:
    Tuple[ImportRequest, List[Dict[str, Any]]]: A tuple containing:
        - ImportRequest: A validated object containing well-formed memory entries.
        - List of failed memory items that could not be parsed due to structure or validation errors.

Raises:
    ValueError: If the JSON is invalid or no valid memory entries are found.

Supports:
    - JSON string or dict input
    - Dict with top-level 'memories' or 'memory' keys
    - Raw list of memory-like objects (dictionaries with 'title' and 'content')
"""
def parse_raw_import_data(raw_data: Union[str, Dict[str, Any]]) -> Tuple[ImportRequest, List[Dict[str, Any]]]:
    """
    Parses raw import data into an ImportRequest, handling common variations.
    Attempts to extract a list of memories from various possible structures.
    Returns the parsed ImportRequest and a list of any malformed memory items.
    """
    failed_memories: List[Dict[str, Any]] = []

    if isinstance(raw_data, str):
        try:
            data = json.loads(raw_data)
            logger.info("Successfully parsed raw data string as JSON.")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format detected: {e}. Raw data: {raw_data[:200]}...")
            raise ValueError(f"Invalid JSON format: {e}")
    else:
        data = raw_data
        logger.info("Received raw data as a dictionary.")

    memories_list: List[MemoryRequest] = []
    potential_memory_keys = ["memories", "memory"]
    found_key = None

    for key in potential_memory_keys:
        if key in data and isinstance(data[key], list):
            found_key = key
            logger.info(f"Attempting to parse memories from top-level key: '{key}'")
            break

    if found_key:
        for item in data[found_key]:
            if isinstance(item, dict):
                try:
                    memories_list.append(MemoryRequest(
                        title=item.get("title", ""),
                        content=normalize_content(item.get("content", ""))
                    ))
                except ValidationError as e:
                    logger.warning(f"Skipping malformed memory item due to validation error: {e}. Item: {item}")
                    failed_memories.append(item)
                    continue
            else:
                logger.warning(f"Skipping non-dictionary item in memory list: {item}")
                failed_memories.append(item)
    elif isinstance(data, list):
        logger.info("Attempting to parse memories from raw list of objects.")
        for item in data:
            if isinstance(item, dict):
                try:
                    memories_list.append(MemoryRequest(
                        title=item.get("title", ""),
                        content=normalize_content(item.get("content", ""))
                    ))
                except ValidationError as e:
                    logger.warning(f"Skipping malformed memory item due to validation error: {e}. Item: {item}")
                    failed_memories.append(item)
                    continue
            else:
                logger.warning(f"Skipping non-dictionary item in raw list: {item}")
                failed_memories.append(item)
    else:
        logger.error(f"Unsupported raw data format. Expected a dictionary with 'memories'/'memory' key or a list of memory objects. Data type: {type(data)}")
        raise ValueError("Unsupported raw data format. Expected a dictionary with 'memories'/'memory' key or a list of memory objects.")

    if not memories_list:
        logger.warning("No valid memories found in the provided data after parsing.")
        raise ValueError("No valid memories found in the provided data.")

    logger.info(f"Successfully parsed {len(memories_list)} memories. {len(failed_memories)} memories failed to parse.")
    return ImportRequest(memories=memories_list), failed_memories
