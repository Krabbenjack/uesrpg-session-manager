"""
Core module for UESRPG Session Manager.
Contains business logic separated from UI concerns.
"""

from .import_export import (
    deep_merge,
    load_json_file,
    save_json_file,
    generate_preview,
    merge_character_data,
    validate_character_data,
    prepare_export_data,
)

from .mechanics import apply_derived_stats

__all__ = [
    'deep_merge',
    'load_json_file',
    'save_json_file',
    'generate_preview',
    'merge_character_data',
    'validate_character_data',
    'prepare_export_data',
    'apply_derived_stats',
]
