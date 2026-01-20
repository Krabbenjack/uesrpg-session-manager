#!/usr/bin/env python3
"""
Test script to validate UI functionality.
Requires a display (or xvfb) to run.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uesrpg_sm.core.spec_loader import SpecLoader
from uesrpg_sm.core.character_model import CharacterModel
from uesrpg_sm.core.importer import Importer
from uesrpg_sm.ui.spec_renderer import SpecRenderer
from uesrpg_sm.ui.character_window import CharacterWindow


def test_spec_renderer():
    """Test the SpecRenderer component."""
    print("Testing spec_renderer...")
    
    # Load spec
    loader = SpecLoader('ui/ui_spec.json')
    spec = loader.spec
    
    # Create character model
    default_char = loader.get_default_character()
    model = CharacterModel(default_char)
    
    # Create root window
    root = tk.Tk()
    root.withdraw()  # Hide window
    
    # Create renderer
    renderer = SpecRenderer(spec, model)
    
    # Test theme application
    renderer.apply_theme(root)
    
    # Test rendering various field types
    test_frame = ttk.Frame(root)
    
    # Test entry field
    entry_spec = {'widget': 'entry', 'label': 'Test', 'bind': '$.name', 'colspan': 2}
    widget = renderer.render_field(test_frame, entry_spec, row=0, column=0)
    assert widget is not None, "Entry widget not created"
    
    # Test spin_int field
    spin_spec = {'widget': 'spin_int', 'label': 'Number', 'bind': '$.xp.current', 'min': 0, 'max': 100, 'colspan': 2}
    widget = renderer.render_field(test_frame, spin_spec, row=1, column=0)
    assert widget is not None, "Spinbox widget not created"
    
    # Test check field
    check_spec = {'widget': 'check', 'label': 'Enabled', 'bind': '$.birthsign.star_cursed', 'colspan': 1}
    widget = renderer.render_field(test_frame, check_spec, row=2, column=0)
    assert widget is not None, "Checkbox widget not created"
    
    # Test tags field  
    tags_spec = {'widget': 'tags', 'label': 'Tags', 'bind': '$.languages', 'colspan': 2}
    widget = renderer.render_field(test_frame, tags_spec, row=3, column=0)
    assert widget is not None, "Tags widget not created"
    
    # Test textarea field
    textarea_spec = {'widget': 'textarea', 'label': 'Notes', 'bind': '$.wounds', 'height': 3, 'colspan': 2}
    widget = renderer.render_field(test_frame, textarea_spec, row=4, column=0)
    assert widget is not None, "Textarea widget not created"
    
    # Test int_list_csv field
    intlist_spec = {'widget': 'int_list_csv', 'label': 'Lucky', 'bind': '$.luck_numbers.lucky', 'colspan': 2}
    widget = renderer.render_field(test_frame, intlist_spec, row=5, column=0)
    assert widget is not None, "Int list widget not created"
    
    # Clean up
    root.destroy()
    
    print("✓ spec_renderer tests passed")


def test_character_window():
    """Test the CharacterWindow component."""
    print("Testing character_window...")
    
    # Load spec
    loader = SpecLoader('ui/ui_spec.json')
    spec = loader.spec
    
    # Create character model
    default_char = loader.get_default_character()
    model = CharacterModel(default_char)
    
    # Create root window
    root = tk.Tk()
    
    # Create renderer
    renderer = SpecRenderer(spec, model)
    renderer.apply_theme(root)
    
    # Create importer
    import_window_spec = loader.get_window('import_window')
    import_map = import_window_spec.get('import_map', {}) if import_window_spec else {}
    importer = Importer(import_map)
    
    # Get character window spec
    char_window_spec = loader.get_window('character_window')
    assert char_window_spec is not None, "Character window spec not found"
    
    # Create character window
    char_window = CharacterWindow(root, char_window_spec, loader, renderer, model, importer)
    
    # Verify window was created
    assert char_window.root is not None, "Window root not set"
    assert char_window.spec == char_window_spec, "Window spec mismatch"
    
    # Update window to ensure no render errors
    root.update()
    
    # Test that all tabs exist
    main_panel = char_window_spec.get('main_panel', {})
    tabs = main_panel.get('tabs', [])
    assert len(tabs) >= 4, "Expected at least 4 tabs (Core, Combat & Skills, Gear, Magic)"
    
    # Clean up
    root.destroy()
    
    print("✓ character_window tests passed")


def test_ui_spec_compliance():
    """Test that the UI matches the spec."""
    print("Testing UI spec compliance...")
    
    loader = SpecLoader('ui/ui_spec.json')
    
    # Test window configuration
    app_config = loader.get_app_config()
    window_config = app_config.get('window', {})
    
    assert window_config.get('size') == [1100, 720], "Window size mismatch"
    assert window_config.get('min_size') == [980, 640], "Minimum size mismatch"
    assert window_config.get('resizable') == True, "Resizable mismatch"
    
    # Test character window spec
    char_win = loader.get_window('character_window')
    assert char_win.get('type') == 'main', "Character window should be main type"
    
    # Test left panel (portrait)
    left_panel = char_win.get('left_panel', {})
    assert left_panel.get('id') == 'portrait_panel', "Left panel should be portrait"
    
    # Test main panel (notebook with tabs)
    main_panel = char_win.get('main_panel', {})
    assert main_panel.get('type') == 'notebook', "Main panel should be notebook"
    
    tabs = main_panel.get('tabs', [])
    tab_ids = [t.get('id') for t in tabs]
    
    assert 'tab_core' in tab_ids, "Missing Core tab"
    assert 'tab_combat_skills' in tab_ids, "Missing Combat & Skills tab"
    assert 'tab_gear' in tab_ids, "Missing Gear tab"
    assert 'tab_magic' in tab_ids, "Missing Magic tab"
    
    # Test import window spec
    import_win = loader.get_window('import_window')
    assert import_win.get('type') == 'dialog', "Import window should be dialog type"
    assert 'import_map' in import_win, "Import window should have import_map"
    
    print("✓ UI spec compliance tests passed")


def test_data_binding():
    """Test two-way data binding."""
    print("Testing data binding...")
    
    loader = SpecLoader('ui/ui_spec.json')
    spec = loader.spec
    
    default_char = loader.get_default_character()
    model = CharacterModel(default_char)
    
    root = tk.Tk()
    root.withdraw()
    
    renderer = SpecRenderer(spec, model)
    test_frame = ttk.Frame(root)
    
    # Set initial value in model
    model.set_value('$.name', 'Test Character')
    
    # Create entry widget bound to name
    entry_spec = {'widget': 'entry', 'label': 'Name', 'bind': '$.name', 'colspan': 2}
    widget = renderer.render_field(test_frame, entry_spec, row=0, column=0)
    
    # Widget should show model value
    assert widget.get() == 'Test Character', "Widget not initialized with model value"
    
    # Change widget value
    widget.delete(0, tk.END)
    widget.insert(0, 'New Name')
    
    # Trigger focus out to update model
    widget.event_generate('<FocusOut>')
    
    # Model should have new value
    assert model.get_value('$.name') == 'New Name', "Model not updated from widget"
    
    # Test checkbox binding
    model.set_value('$.birthsign.star_cursed', False)
    check_spec = {'widget': 'check', 'label': 'Star-Cursed', 'bind': '$.birthsign.star_cursed', 'colspan': 1}
    check_widget = renderer.render_field(test_frame, check_spec, row=1, column=0)
    
    assert check_widget.var.get() == False, "Checkbox not initialized correctly"
    
    # Toggle checkbox
    check_widget.var.set(True)
    
    # Give time for trace to fire
    root.update()
    
    assert model.get_value('$.birthsign.star_cursed') == True, "Model not updated from checkbox"
    
    root.destroy()
    
    print("✓ data binding tests passed")


def main():
    """Run all UI tests."""
    print("=" * 60)
    print("UESRPG Session Manager - UI Tests")
    print("=" * 60)
    print()
    
    try:
        test_spec_renderer()
        test_character_window()
        test_ui_spec_compliance()
        test_data_binding()
        
        print()
        print("=" * 60)
        print("✓ All UI tests passed!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"✗ Test failed: {e}")
        print("=" * 60)
        return 1
    except Exception as e:
        print()
        print("=" * 60)
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
