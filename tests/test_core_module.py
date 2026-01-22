#!/usr/bin/env python3
"""
Test the core.import_export module functionality.
"""

import json
import sys
import tempfile
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    deep_merge,
    load_json_file,
    save_json_file,
    generate_preview,
    merge_character_data,
    validate_character_data,
)


def test_deep_merge():
    """Test deep_merge function with various scenarios."""
    print("=" * 60)
    print("Testing core.import_export.deep_merge")
    print("=" * 60)
    
    # Test 1: Simple merge with overwrite=True
    base = {'name': '', 'race': '', 'xp': {'current': 0, 'total': 0}}
    overlay = {'name': 'Cass', 'race': 'Nord'}
    result = deep_merge(base, overlay, overwrite=True)
    assert result['name'] == 'Cass', "Failed to merge name"
    assert result['race'] == 'Nord', "Failed to merge race"
    assert result['xp']['current'] == 0, "Should preserve nested defaults"
    print("✓ Test 1: Simple merge with overwrite=True")
    
    # Test 2: Merge with overwrite=False (only fill empty)
    base = {'name': 'Existing', 'race': '', 'size': ''}
    overlay = {'name': 'NewName', 'race': 'Orc', 'size': 'Medium'}
    result = deep_merge(base, overlay, overwrite=False)
    assert result['name'] == 'Existing', "Should not overwrite existing value"
    assert result['race'] == 'Orc', "Should fill empty value"
    assert result['size'] == 'Medium', "Should fill empty value"
    print("✓ Test 2: Merge with overwrite=False")
    
    # Test 3: Deep nested merge
    base = {
        'stats': {
            'hp': {'current': 50, 'max': 100},
            'mp': {'current': 0, 'max': 0}
        }
    }
    overlay = {
        'stats': {
            'hp': {'current': 75},
            'mp': {'current': 25, 'max': 50}
        }
    }
    result = deep_merge(base, overlay, overwrite=True)
    assert result['stats']['hp']['current'] == 75, "Should merge nested value"
    assert result['stats']['hp']['max'] == 100, "Should preserve unmerged nested"
    assert result['stats']['mp']['current'] == 25, "Should merge new nested"
    assert result['stats']['mp']['max'] == 50, "Should merge new nested"
    print("✓ Test 3: Deep nested merge")
    
    # Test 4: List handling with overwrite=True
    base = {'skills': [], 'languages': ['Common']}
    overlay = {'skills': ['Acrobatics', 'Stealth'], 'languages': ['Orcish', 'Elvish']}
    result = deep_merge(base, overlay, overwrite=True)
    assert result['skills'] == ['Acrobatics', 'Stealth'], "Should overwrite empty list"
    assert result['languages'] == ['Orcish', 'Elvish'], "Should overwrite list"
    print("✓ Test 4: List handling with overwrite=True")
    
    # Test 5: Preserving legitimate falsy values
    base = {'xp': 0, 'is_elite': False, 'name': '', 'level': 5}
    overlay = {'xp': 100, 'is_elite': True, 'name': 'Hero', 'level': 10}
    result = deep_merge(base, overlay, overwrite=False)
    assert result['xp'] == 0, "Should preserve 0"
    assert result['is_elite'] == False, "Should preserve False"
    assert result['name'] == 'Hero', "Should fill empty string"
    assert result['level'] == 5, "Should preserve existing number"
    print("✓ Test 5: Legitimate falsy values preserved")
    
    print("✓ All deep_merge tests passed!\n")


def test_json_file_operations():
    """Test load_json_file and save_json_file functions."""
    print("=" * 60)
    print("Testing core.import_export JSON file operations")
    print("=" * 60)
    
    # Create a temporary file
    test_data = {
        'name': 'Test Character',
        'race': 'Human',
        'stats': {
            'hp': 100,
            'mp': 50
        },
        'skills': ['Acrobatics', 'Stealth']
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        temp_file = f.name
    
    try:
        # Test save_json_file
        save_json_file(temp_file, test_data)
        assert os.path.exists(temp_file), "File should be created"
        print("✓ save_json_file creates file")
        
        # Test load_json_file
        loaded_data = load_json_file(temp_file)
        assert loaded_data == test_data, "Loaded data should match saved data"
        print("✓ load_json_file loads correct data")
        
        # Verify JSON formatting
        with open(temp_file, 'r') as f:
            content = f.read()
            assert '  ' in content, "Should be indented"
        print("✓ JSON is properly formatted with indentation")
        
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("✓ All JSON file operation tests passed!\n")


def test_generate_preview():
    """Test generate_preview function."""
    print("=" * 60)
    print("Testing core.import_export.generate_preview")
    print("=" * 60)
    
    # Test 1: Normal preview
    data = {'name': 'Test', 'value': 123}
    preview = generate_preview(data)
    assert 'Test' in preview, "Preview should contain data"
    assert '123' in preview, "Preview should contain numbers"
    print("✓ Test 1: Normal preview generation")
    
    # Test 2: Truncation
    large_data = {'data': 'x' * 3000}
    preview = generate_preview(large_data, max_length=2000)
    assert len(preview) <= 2020, "Preview should be truncated"  # Allow for truncation message
    assert 'truncated' in preview.lower(), "Should indicate truncation"
    print("✓ Test 2: Large data is truncated")
    
    # Test 3: Unicode handling
    unicode_data = {'name': '日本語', 'value': 'Ελληνικά'}
    preview = generate_preview(unicode_data)
    assert '日本語' in preview, "Should handle unicode"
    assert 'Ελληνικά' in preview, "Should handle unicode"
    print("✓ Test 3: Unicode handling")
    
    print("✓ All generate_preview tests passed!\n")


def test_merge_character_data():
    """Test merge_character_data convenience function."""
    print("=" * 60)
    print("Testing core.import_export.merge_character_data")
    print("=" * 60)
    
    default_schema = {
        'name': '',
        'race': '',
        'level': 1,
        'stats': {
            'hp': 10,
            'mp': 5
        }
    }
    
    imported_data = {
        'name': 'Hero',
        'level': 5,
        'stats': {
            'hp': 100
        }
    }
    
    result = merge_character_data(default_schema, imported_data, overwrite=True)
    assert result['name'] == 'Hero', "Should merge name"
    assert result['level'] == 5, "Should merge level"
    assert result['stats']['hp'] == 100, "Should merge hp"
    assert result['stats']['mp'] == 5, "Should preserve mp"
    print("✓ merge_character_data works correctly")
    
    print("✓ All merge_character_data tests passed!\n")


def test_validate_character_data():
    """Test validate_character_data function."""
    print("=" * 60)
    print("Testing core.import_export.validate_character_data")
    print("=" * 60)
    
    # Test 1: Valid data
    valid_data = {'name': 'Test', 'race': 'Human'}
    is_valid, errors = validate_character_data(valid_data)
    assert is_valid, "Valid data should pass"
    assert len(errors) == 0, "Should have no errors"
    print("✓ Test 1: Valid data passes validation")
    
    # Test 2: Invalid data (not a dict)
    invalid_data = "not a dict"
    is_valid, errors = validate_character_data(invalid_data)
    assert not is_valid, "Invalid data should fail"
    assert len(errors) > 0, "Should have errors"
    print("✓ Test 2: Invalid data fails validation")
    
    print("✓ All validate_character_data tests passed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CORE MODULE TESTS")
    print("=" * 60 + "\n")
    
    try:
        test_deep_merge()
        test_json_file_operations()
        test_generate_preview()
        test_merge_character_data()
        test_validate_character_data()
        
        print("=" * 60)
        print("✓✓✓ ALL CORE MODULE TESTS PASSED ✓✓✓")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
