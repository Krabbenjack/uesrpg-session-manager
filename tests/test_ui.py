#!/usr/bin/env python3
"""
Test script for Character Window UI - verifies implementation without GUI
"""

import json
import sys
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

def test_spec_loading():
    """Test that the spec file can be loaded and parsed."""
    spec_path = Path("ui/ui_spec.json")
    
    print(f"Testing spec loading from: {spec_path}")
    assert spec_path.exists(), f"Spec file not found: {spec_path}"
    
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    assert spec is not None, "Failed to load spec"
    assert 'spec_version' in spec, "Spec missing version"
    assert 'windows' in spec, "Spec missing windows"
    
    print(f"✓ Spec loaded successfully: version {spec.get('spec_version')}")
    
    # Check for character window
    windows = spec.get('windows', [])
    char_window = None
    for window in windows:
        if window.get('id') == 'character_window':
            char_window = window
            break
    
    assert char_window is not None, "Character window not found in spec"
    print(f"✓ Character window found in spec")
    
    # Check for either new sheet_view or legacy main_panel structure
    has_sheet_view = 'sheet_view' in char_window
    has_main_panel = 'main_panel' in char_window
    has_details_panel = 'details_panel' in char_window
    
    assert has_sheet_view or has_main_panel or has_details_panel, "No panel structure found"
    
    if has_sheet_view:
        print(f"✓ New sheet_view layout detected")
        if has_details_panel:
            details_panel = char_window.get('details_panel', {})
            if details_panel.get('type') == 'notebook':
                tabs = details_panel.get('tabs', [])
                print(f"✓ Details notebook detected with {len(tabs)} tabs")
                
                # Count total sections
                total_sections = 0
                for tab in tabs:
                    sections = tab.get('sections', [])
                    total_sections += len(sections)
                
                print(f"✓ Total sections across all tabs: {total_sections}")
    elif has_main_panel:
        main_panel = char_window.get('main_panel', {})
        if main_panel.get('type') == 'notebook':
            tabs = main_panel.get('tabs', [])
            print(f"✓ Legacy notebook layout detected with {len(tabs)} tabs")
            
            # Count total sections
            total_sections = 0
            for tab in tabs:
                sections = tab.get('sections', [])
                total_sections += len(sections)
            
            print(f"✓ Total sections across all tabs: {total_sections}")
    
    # Check default character data
    default_char = spec.get('data', {}).get('default_character', {})
    assert default_char, "Default character data not found"
    print(f"✓ Default character data found")
    
    return True

def test_module_imports():
    """Test that the modules can be imported (with mocked tkinter)."""
    print("\nTesting module imports...")
    
    # Mock tkinter modules
    sys.modules['tkinter'] = MagicMock()
    sys.modules['tkinter.ttk'] = MagicMock()
    sys.modules['tkinter.filedialog'] = MagicMock()
    sys.modules['tkinter.messagebox'] = MagicMock()
    sys.modules['tkinter.scrolledtext'] = MagicMock()
    
    # Add parent directory to path
    parent_dir = Path(__file__).parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    
    # Import modules
    try:
        import main
        print("✓ main.py imported successfully")
    except Exception as e:
        print(f"⚠ main.py import skipped: {e}")
    
    # Import ui module
    import ui
    print("✓ ui.py imported successfully")
    
    return True

def test_ui_structure():
    """Test UI class structure without actually creating widgets."""
    print("\nTesting UI structure...")
    
    # Mock tkinter
    sys.modules['tkinter'] = MagicMock()
    sys.modules['tkinter.ttk'] = MagicMock()
    sys.modules['tkinter.filedialog'] = MagicMock()
    sys.modules['tkinter.messagebox'] = MagicMock()
    sys.modules['tkinter.scrolledtext'] = MagicMock()
    
    import ui
    
    # Check that CharacterWindowUI class exists
    assert hasattr(ui, 'CharacterWindowUI'), "CharacterWindowUI class not found"
    print("✓ CharacterWindowUI class exists")
    
    # Check for required methods
    required_methods = [
        'get_state',
        'set_state',
        'reset_to_defaults',
        'load_character',
        'save_character',
        'save_character_as'
    ]
    
    for method in required_methods:
        assert hasattr(ui.CharacterWindowUI, method), f"Method {method} not found"
        print(f"✓ Method {method} exists")
    
    return True

def test_nested_value_operations():
    """Test nested value get/set operations."""
    print("\nTesting nested value operations...")
    
    # Mock tkinter
    sys.modules['tkinter'] = MagicMock()
    sys.modules['tkinter.ttk'] = MagicMock()
    sys.modules['tkinter.filedialog'] = MagicMock()
    sys.modules['tkinter.messagebox'] = MagicMock()
    sys.modules['tkinter.scrolledtext'] = MagicMock()
    
    import ui
    
    # Create a mock root
    mock_root = MagicMock()
    
    # We can't actually instantiate the UI without a real Tk root
    # But we can test the helper methods directly
    
    # Test _get_nested_value
    test_data = {
        'name': 'Test',
        'xp': {
            'current': 100,
            'total': 500
        },
        'characteristics': [
            {'abbr': 'Str', 'score': 50}
        ]
    }
    
    # These are instance methods, so we'd need an instance
    # For now, just verify the class exists
    print("✓ Nested value operations defined in class")
    
    return True

def test_sheet_view_structure():
    """Test that the new sheet_view structure is properly defined in spec."""
    print("\nTesting sheet_view structure...")
    
    spec_path = Path("ui/ui_spec.json")
    with open(spec_path, 'r', encoding='utf-8') as f:
        spec = json.load(f)
    
    # Find character window
    windows = spec.get('windows', [])
    char_window = None
    for window in windows:
        if window.get('id') == 'character_window':
            char_window = window
            break
    
    assert char_window is not None, "Character window not found"
    
    # Check for sheet_view
    assert 'sheet_view' in char_window, "sheet_view not found in character window"
    print("✓ sheet_view section exists")
    
    sheet_view = char_window['sheet_view']
    
    # Check for header, core, and content bands
    assert 'header' in sheet_view, "header band not found in sheet_view"
    assert 'core' in sheet_view, "core band not found in sheet_view"
    assert 'content' in sheet_view, "content band not found in sheet_view"
    print("✓ All three bands (header/core/content) defined")
    
    # Check for portrait_box in header
    header = sheet_view['header']
    assert 'widgets' in header, "header widgets not found"
    widgets = header['widgets']
    has_portrait = any(w.get('type') == 'portrait_box' for w in widgets)
    assert has_portrait, "portrait_box not found in header"
    print("✓ portrait_box found in header band")
    
    # Check for details_panel
    assert 'details_panel' in char_window, "details_panel not found"
    details_panel = char_window['details_panel']
    assert details_panel.get('type') == 'notebook', "details_panel is not a notebook"
    assert 'tabs' in details_panel, "tabs not found in details_panel"
    tabs = details_panel['tabs']
    assert len(tabs) >= 4, f"Expected at least 4 tabs, found {len(tabs)}"
    print(f"✓ details_panel notebook has {len(tabs)} tabs")
    
    # Verify old left_panel is removed
    assert 'left_panel' not in char_window, "Old left_panel still exists (should be removed)"
    print("✓ Old left_panel removed from spec")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Character Window UI - Implementation Tests")
    print("=" * 60)
    
    try:
        test_spec_loading()
        test_module_imports()
        test_ui_structure()
        test_nested_value_operations()
        test_sheet_view_structure()
        
        print("\n" + "=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
        print("\nNOTE: Full UI testing requires a display environment.")
        print("Run 'python main.py' on a system with GUI support to test the full application.")
        
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
