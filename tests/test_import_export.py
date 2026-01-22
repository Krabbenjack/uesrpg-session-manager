#!/usr/bin/env python3
"""
Test script for character import/export functionality
"""

import json
import sys
from pathlib import Path

def test_deep_merge_logic():
    """Test the deep_merge logic with manual implementation."""
    print("\n=== Testing deep_merge logic ===")
    
    from copy import deepcopy
    
    def deep_merge(base, overlay, overwrite=True):
        """Manual implementation for testing."""
        result = deepcopy(base)
        
        for key, value in overlay.items():
            if key not in result:
                result[key] = deepcopy(value)
            elif isinstance(value, dict) and isinstance(result[key], dict):
                result[key] = deep_merge(result[key], value, overwrite)
            elif isinstance(value, list) and isinstance(result[key], list):
                if overwrite:
                    result[key] = deepcopy(value)
                elif len(result[key]) == 0:
                    result[key] = deepcopy(value)
            else:
                if overwrite:
                    result[key] = deepcopy(value)
                elif result[key] in ('', None):
                    result[key] = deepcopy(value)
        
        return result
    
    # Test 1: Simple merge with overwrite=True
    base = {
        'name': '',
        'race': '',
        'xp': {'current': 0, 'total': 0}
    }
    overlay = {
        'name': 'Cass',
        'race': 'Nord'
    }
    result = deep_merge(base, overlay, overwrite=True)
    assert result['name'] == 'Cass', "Failed to merge name"
    assert result['race'] == 'Nord', "Failed to merge race"
    assert result['xp']['current'] == 0, "Should preserve nested defaults"
    print("✓ Test 1: Simple merge with overwrite=True passed")
    
    # Test 2: Merge with overwrite=False (only fill empty)
    base = {
        'name': 'Existing',
        'race': '',
        'size': ''
    }
    overlay = {
        'name': 'NewName',
        'race': 'Orc',
        'size': 'Medium'
    }
    result = deep_merge(base, overlay, overwrite=False)
    assert result['name'] == 'Existing', "Should not overwrite existing value"
    assert result['race'] == 'Orc', "Should fill empty value"
    assert result['size'] == 'Medium', "Should fill empty value"
    print("✓ Test 2: Merge with overwrite=False passed")
    
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
    print("✓ Test 3: Deep nested merge passed")
    
    # Test 4: List handling
    base = {
        'skills': [],
        'languages': ['Common']
    }
    overlay = {
        'skills': ['Acrobatics', 'Stealth'],
        'languages': ['Orcish', 'Elvish']
    }
    result = deep_merge(base, overlay, overwrite=True)
    assert result['skills'] == ['Acrobatics', 'Stealth'], "Should overwrite empty list"
    assert result['languages'] == ['Orcish', 'Elvish'], "Should overwrite list with overwrite=True"
    print("✓ Test 4: List handling with overwrite=True passed")
    
    # Test 5: List handling with overwrite=False
    base = {
        'skills': [],
        'languages': ['Common']
    }
    overlay = {
        'skills': ['Acrobatics', 'Stealth'],
        'languages': ['Orcish', 'Elvish']
    }
    result = deep_merge(base, overlay, overwrite=False)
    assert result['skills'] == ['Acrobatics', 'Stealth'], "Should fill empty list"
    assert result['languages'] == ['Common'], "Should not overwrite non-empty list"
    print("✓ Test 5: List handling with overwrite=False passed")
    
    # Test 6: Adding new keys from overlay
    base = {
        'name': 'Test',
        'race': 'Human'
    }
    overlay = {
        'name': 'New',
        'elite_adv': 'Vampire',
        'spells': [{'name': 'Fireball'}]
    }
    result = deep_merge(base, overlay, overwrite=True)
    assert result['name'] == 'New'
    assert result['elite_adv'] == 'Vampire', "Should add new keys"
    assert 'spells' in result, "Should add new keys"
    print("✓ Test 6: Adding new keys from overlay passed")
    
    # Test 7: Legitimate falsy values preserved with overwrite=False
    base = {
        'xp': 0,
        'is_elite': False,
        'name': '',
        'level': 5
    }
    overlay = {
        'xp': 100,
        'is_elite': True,
        'name': 'Hero',
        'level': 10
    }
    result = deep_merge(base, overlay, overwrite=False)
    assert result['xp'] == 0, "Should preserve 0 (legitimate falsy value)"
    assert result['is_elite'] == False, "Should preserve False (legitimate falsy value)"
    assert result['name'] == 'Hero', "Should fill empty string"
    assert result['level'] == 5, "Should preserve existing non-zero number"
    print("✓ Test 7: Legitimate falsy values preserved with overwrite=False passed")
    
    print("\n✓ All deep_merge logic tests passed!")

def test_schema_completeness():
    """Test that default schema has all required keys."""
    print("\n=== Testing schema completeness ===")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    default_character = spec.get('data', {}).get('default_character', {})
    
    # Check for magic-related keys
    required_magic_keys = ['spells', 'magic_skills', 'rituals', 'spellcasting']
    for key in required_magic_keys:
        assert key in default_character, f"Missing required key: {key}"
        print(f"✓ Found key: {key}")
    
    # Check structure
    assert isinstance(default_character.get('spells', []), list), "spells should be a list"
    print("✓ spells is a list")
    
    assert isinstance(default_character.get('magic_skills', []), list), "magic_skills should be a list"
    print("✓ magic_skills is a list")
    
    print("\n✓ Schema completeness test passed!")

def test_import_window_spec():
    """Test that import window spec exists and is properly configured."""
    print("\n=== Testing import window spec ===")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    # Find import window
    import_window = None
    for window in spec.get('windows', []):
        if window.get('id') == 'import_window':
            import_window = window
            break
    
    assert import_window is not None, "import_window not found"
    print("✓ import_window found")
    
    assert import_window.get('title') == 'Import Character Data', f"Wrong title: {import_window.get('title')}"
    print(f"✓ Title is correct: {import_window.get('title')}")
    
    # Check widgets
    widgets = import_window.get('widgets', [])
    widget_types = [w.get('type') for w in widgets]
    
    assert 'button' in widget_types, "No button widgets found"
    assert 'preview' in widget_types, "No preview widget found"
    print("✓ Required widgets present")
    
    # Check for preview widget with bind path
    preview_widget = next((w for w in widgets if w.get('type') == 'preview'), None)
    assert preview_widget is not None, "Preview widget not found"
    assert preview_widget.get('bind') == '$dialog.preview', f"Wrong bind path: {preview_widget.get('bind')}"
    print("✓ Preview widget properly configured")
    
    # Check for overwrite checkbox
    overwrite_widget = next((w for w in widgets if w.get('bind') == '$dialog.overwrite'), None)
    assert overwrite_widget is not None, "Overwrite checkbox not found"
    assert overwrite_widget.get('widget') == 'check', "Overwrite should be a checkbox"
    print("✓ Overwrite checkbox properly configured")
    
    print("\n✓ Import window spec test passed!")

def test_menu_structure():
    """Test that menu structure is properly updated."""
    print("\n=== Testing menu structure ===")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    menus = spec.get('menus', [])
    
    # Find Import menu
    import_menu = None
    for menu in menus:
        if menu.get('label') == 'Import':
            import_menu = menu
            break
    
    assert import_menu is not None, "Import menu not found"
    print("✓ Import menu found")
    
    items = import_menu.get('items', [])
    item_labels = [item.get('label') for item in items]
    
    assert 'Import Character Data…' in item_labels, "Import Character Data menu item not found"
    print("✓ 'Import Character Data…' menu item found")
    
    assert 'Export Character Data…' in item_labels, "Export Character Data menu item not found"
    print("✓ 'Export Character Data…' menu item found")
    
    # Check commands
    import_item = next((item for item in items if item.get('label') == 'Import Character Data…'), None)
    assert import_item.get('command') == 'import_character_data', f"Wrong command: {import_item.get('command')}"
    print(f"✓ Import command correct: {import_item.get('command')}")
    
    export_item = next((item for item in items if item.get('label') == 'Export Character Data…'), None)
    assert export_item.get('command') == 'export_character_data', f"Wrong command: {export_item.get('command')}"
    print(f"✓ Export command correct: {export_item.get('command')}")
    
    print("\n✓ Menu structure test passed!")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Character Import/Export Tests")
    print("=" * 60)
    
    try:
        test_schema_completeness()
        test_import_window_spec()
        test_menu_structure()
        test_deep_merge_logic()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
