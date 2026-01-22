"""
Import/Export functionality for UESRPG Session Manager.

This module handles all JSON import/export operations, including:
- Loading and saving character JSON files
- Deep merging character data with default schema
- Generating JSON previews
- Schema coercion and validation

NO Tkinter or UI code should be in this module.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from copy import deepcopy

logger = logging.getLogger(__name__)


def deep_merge(base: Dict, overlay: Dict, overwrite: bool = True) -> Dict:
    """
    Deep merge two dictionaries.
    
    This function merges an overlay dictionary into a base dictionary,
    handling nested dictionaries and lists appropriately.
    
    Args:
        base: Base dictionary (e.g., default_character schema)
        overlay: Overlay dictionary (e.g., imported data)
        overwrite: If True, overlay values replace base values.
                  If False, only fill missing/empty fields in base.
    
    Returns:
        Merged dictionary
    
    Examples:
        >>> base = {'name': '', 'stats': {'hp': 10}}
        >>> overlay = {'name': 'Hero', 'stats': {'mp': 20}}
        >>> deep_merge(base, overlay)
        {'name': 'Hero', 'stats': {'hp': 10, 'mp': 20}}
    """
    result = deepcopy(base)
    
    for key, value in overlay.items():
        if key not in result:
            # Key doesn't exist in base, add it
            result[key] = deepcopy(value)
        elif isinstance(value, dict) and isinstance(result[key], dict):
            # Both are dicts, merge recursively
            result[key] = deep_merge(result[key], value, overwrite)
        elif isinstance(value, list) and isinstance(result[key], list):
            # Both are lists
            if overwrite:
                result[key] = deepcopy(value)
            elif len(result[key]) == 0:
                # Only overwrite if base list is empty
                result[key] = deepcopy(value)
        else:
            # Scalar values
            if overwrite:
                result[key] = deepcopy(value)
            elif result[key] in ('', None):
                # Only overwrite if base value is empty string or None
                # Preserves legitimate falsy values like 0, False, []
                result[key] = deepcopy(value)
    
    return result


def load_json_file(filepath: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file.
    
    Args:
        filepath: Path to the JSON file to load
    
    Returns:
        Parsed JSON data as a dictionary
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
        Exception: For other file reading errors
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded JSON from {filepath}")
        return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filepath}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error loading JSON from {filepath}: {e}")
        raise


def save_json_file(filepath: str, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Save data to a JSON file.
    
    Args:
        filepath: Path to save the JSON file
        data: Dictionary to save as JSON
        indent: Number of spaces for indentation (default: 2)
    
    Raises:
        Exception: If there's an error writing the file
    """
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        logger.info(f"Successfully saved JSON to {filepath}")
    except Exception as e:
        logger.error(f"Error saving JSON to {filepath}: {e}")
        raise


def generate_preview(data: Dict[str, Any], max_length: int = 2000) -> str:
    """
    Generate a formatted JSON preview string.
    
    Args:
        data: Dictionary to preview
        max_length: Maximum length of preview (default: 2000)
    
    Returns:
        Formatted JSON string, truncated if necessary
    """
    try:
        preview_text = json.dumps(data, indent=2, ensure_ascii=False)
        
        # Truncate if too large
        if len(preview_text) > max_length:
            preview_text = preview_text[:max_length] + "\n... (truncated)"
        
        return preview_text
    except Exception as e:
        logger.error(f"Error generating preview: {e}")
        return f"Error generating preview: {e}"


def merge_character_data(
    default_schema: Dict[str, Any],
    imported_data: Dict[str, Any],
    overwrite: bool = True
) -> Dict[str, Any]:
    """
    Merge imported character data with default schema.
    
    This is a convenience wrapper around deep_merge specifically for
    character data, ensuring the result conforms to the expected schema.
    
    Args:
        default_schema: Default character schema from ui_spec.json
        imported_data: Imported character data
        overwrite: Whether to overwrite existing values
    
    Returns:
        Merged character data
    """
    return deep_merge(default_schema, imported_data, overwrite=overwrite)


def validate_character_data(data: Dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate character data structure.
    
    Performs basic validation to ensure the data has expected structure.
    This is a placeholder for future more comprehensive validation.
    
    Args:
        data: Character data to validate
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Basic validation - check if it's a dictionary
    if not isinstance(data, dict):
        errors.append("Data must be a dictionary")
        return False, errors
    
    # Could add more validation rules here in the future
    # For example:
    # - Check for required fields
    # - Validate data types
    # - Check value ranges
    
    return len(errors) == 0, errors
