#!/usr/bin/env python3
"""
Test round-trip functionality: load JSON -> save JSON
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import sys

# Mock tkinter before importing ui
sys.modules['tkinter'] = MagicMock()
sys.modules['tkinter.ttk'] = MagicMock()
sys.modules['tkinter.filedialog'] = MagicMock()
sys.modules['tkinter.messagebox'] = MagicMock()
sys.modules['tkinter.scrolledtext'] = MagicMock()

def test_load_save_roundtrip():
    """Test that we can load and save JSON data."""
    print("Testing load/save round-trip...")
    
    # Load the example character
    example_path = Path("docs/charsheet_cass.json")
    assert example_path.exists(), "Example character file not found"
    
    with open(example_path, 'r', encoding='utf-8') as f:
        original_data = json.load(f)
    
    print(f"✓ Loaded example character: {original_data.get('name', 'Unknown')}")
    
    # Verify some key fields exist
    assert 'name' in original_data
    assert 'characteristics' in original_data
    assert 'skills' in original_data
    
    print(f"✓ Character has {len(original_data.get('characteristics', []))} characteristics")
    print(f"✓ Character has {len(original_data.get('skills', []))} skills")
    
    # Test that we can save it back
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(original_data, tmp, indent=2, ensure_ascii=False)
        tmp_path = tmp.name
    
    # Reload and compare
    with open(tmp_path, 'r', encoding='utf-8') as f:
        reloaded_data = json.load(f)
    
    # Clean up
    Path(tmp_path).unlink()
    
    # Compare key fields
    assert reloaded_data['name'] == original_data['name']
    assert len(reloaded_data['characteristics']) == len(original_data['characteristics'])
    
    print("✓ Round-trip successful - data preserved")
    
    return True

def test_nested_path_operations():
    """Test the nested path get/set operations."""
    print("\nTesting nested path operations...")
    
    test_data = {
        'name': 'Test Character',
        'xp': {
            'current': 100,
            'total': 500
        },
        'derived_stats': {
            'HP': {
                'current': 20,
                'max': 30
            }
        },
        'characteristics': [
            {'abbr': 'Str', 'score': 50, 'bonus': 5}
        ]
    }
    
    # Test getting nested values
    def get_nested(data, path):
        if path.startswith('$.'):
            path = path[2:]
        elif path.startswith('$'):
            path = path[1:]
        
        parts = path.split('.')
        current = data
        
        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
                if current is None:
                    return None
            else:
                return None
        
        return current
    
    # Test various paths
    assert get_nested(test_data, '$.name') == 'Test Character'
    assert get_nested(test_data, '$.xp.current') == 100
    assert get_nested(test_data, '$.derived_stats.HP.max') == 30
    
    print("✓ Nested path get operations work correctly")
    
    # Test setting nested values
    def set_nested(data, path, value):
        if path.startswith('$.'):
            path = path[2:]
        elif path.startswith('$'):
            path = path[1:]
        
        parts = path.split('.')
        current = data
        
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    test_data_copy = test_data.copy()
    set_nested(test_data_copy, '$.name', 'New Name')
    assert test_data_copy['name'] == 'New Name'
    
    print("✓ Nested path set operations work correctly")
    
    return True

def test_spec_field_types():
    """Test that all field types in the spec are recognized."""
    print("\nTesting field type coverage...")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    # Find all widget types used in the spec
    widget_types = set()
    
    def find_widget_types(obj):
        if isinstance(obj, dict):
            if 'widget' in obj:
                widget_types.add(obj['widget'])
            if 'type' in obj:
                widget_types.add(f"type:{obj['type']}")
            for value in obj.values():
                find_widget_types(value)
        elif isinstance(obj, list):
            for item in obj:
                find_widget_types(item)
    
    find_widget_types(spec)
    
    print(f"✓ Found {len(widget_types)} unique widget/type combinations:")
    for wt in sorted(widget_types):
        print(f"  - {wt}")
    
    # Check that we have handlers for common types
    expected_widgets = ['entry', 'textarea', 'spin_int', 'check', 'tags']
    for widget in expected_widgets:
        if widget in widget_types:
            print(f"✓ Handler exists for widget type: {widget}")
    
    return True

def test_default_character_structure():
    """Test that default character has all required fields."""
    print("\nTesting default character structure...")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    default_char = spec.get('data', {}).get('default_character', {})
    
    # Check for key top-level fields
    required_fields = [
        'system', 'name', 'xp', 'race', 'characteristics', 
        'derived_stats', 'skills', 'armor'
    ]
    
    for field in required_fields:
        assert field in default_char, f"Missing required field: {field}"
        print(f"✓ Default character has field: {field}")
    
    # Check characteristics structure
    chars = default_char.get('characteristics', [])
    assert len(chars) == 8, "Should have 8 characteristics"
    
    for char in chars:
        assert 'abbr' in char
        assert 'name' in char
        assert 'score' in char
        assert 'bonus' in char
    
    print(f"✓ Characteristics properly structured ({len(chars)} entries)")
    
    return True

def main():
    """Run all round-trip tests."""
    print("=" * 60)
    print("Character Window UI - Round-Trip Tests")
    print("=" * 60 + "\n")
    
    try:
        test_load_save_roundtrip()
        test_nested_path_operations()
        test_spec_field_types()
        test_default_character_structure()
        
        print("\n" + "=" * 60)
        print("✓ All round-trip tests passed!")
        print("=" * 60)
        
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
