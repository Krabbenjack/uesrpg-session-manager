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
    Merge imported character data with default schema and compute derived stats.
    
    This function:
    1. Merges imported data with default schema using deep_merge
    2. Applies derived stats engine to compute bonuses and derived values
    
    Args:
        default_schema: Default character schema from ui_spec.json
        imported_data: Imported character data
        overwrite: Whether to overwrite existing values
    
    Returns:
        Merged character data with computed derived stats
    """
    # Import here to avoid circular dependency
    from .mechanics import apply_derived_stats
    
    # Merge data with schema
    merged = deep_merge(default_schema, imported_data, overwrite=overwrite)
    
    # Apply derived stats computation
    # This computes characteristic bonuses, base bonuses, and derived stats
    merged = apply_derived_stats(merged)
    
    return merged


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


def prepare_export_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Prepare character data for export by removing computed/derived values.
    
    Export Strategy (Strategy B - Hybrid):
    - Strip characteristic bonuses (computed from scores)
    - Strip base_bonuses entirely (computed from characteristic bonuses)
    - Strip derived_stats computed maximums and values
    - Keep only current pools (HP.current, MP.current, etc.) that users modify
    
    This ensures:
    1. Exported JSON is slim and doesn't contain redundant computed data
    2. Current resource pools (HP, MP, etc.) are preserved for game state
    3. Re-importing exported JSON works correctly (derived values recomputed)
    
    Args:
        data: Full character data from UI
    
    Returns:
        Slimmed data suitable for export
    """
    # Deep copy to avoid modifying original
    export_data = deepcopy(data)
    
    # Strip characteristic bonuses (these are computed from scores)
    if 'characteristics' in export_data:
        for char in export_data['characteristics']:
            if 'bonus' in char:
                del char['bonus']
    
    # Strip base_bonuses entirely (all computed from characteristic bonuses)
    if 'base_bonuses' in export_data:
        export_data['base_bonuses'] = {}
    
    # Strip derived_stats except for current pools
    # Keep only: HP.current, MP.current, WT.current, SP.current, LP.current, AP.current, ENC.current
    if 'derived_stats' in export_data:
        derived = export_data['derived_stats']
        preserved_currents = {}
        
        # Preserve current values from pool stats
        pool_keys = ['HP', 'MP', 'WT', 'SP', 'LP', 'AP', 'ENC']
        for key in pool_keys:
            if key in derived and isinstance(derived[key], dict):
                if 'current' in derived[key]:
                    preserved_currents[key] = {'current': derived[key]['current']}
        
        # Replace derived_stats with only preserved currents
        export_data['derived_stats'] = preserved_currents
    
    logger.info("Prepared export data: stripped computed bonuses and derived maximums")
    return export_data
