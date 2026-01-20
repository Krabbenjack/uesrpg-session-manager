#!/usr/bin/env python3
"""
Test script to validate core functionality without requiring a display.
This runs unit tests on the core modules.
"""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uesrpg_sm.core.spec_loader import SpecLoader
from uesrpg_sm.core.character_model import CharacterModel
from uesrpg_sm.core.importer import Importer


def test_spec_loader():
    """Test spec loader functionality."""
    print("Testing spec_loader...")
    
    loader = SpecLoader('ui/ui_spec.json')
    
    # Test app config
    app_config = loader.get_app_config()
    assert app_config.get('title') == 'UESRPG Session Manager', "App title mismatch"
    
    # Test theme
    theme = loader.get_theme()
    assert theme.get('colors', {}).get('bg') == '#FFD5AF', "Background color mismatch"
    assert theme.get('colors', {}).get('fg') == '#9D6E6B', "Foreground color mismatch"
    
    # Test menus
    menus = loader.get_menus()
    assert len(menus) == 2, "Expected 2 menus"
    assert menus[0].get('label') == 'File', "First menu should be File"
    assert menus[1].get('label') == 'Import', "Second menu should be Import"
    
    # Test window specs
    char_win = loader.get_window('character_window')
    assert char_win is not None, "Character window spec not found"
    assert char_win.get('title') == 'Character', "Character window title mismatch"
    
    import_win = loader.get_window('import_window')
    assert import_win is not None, "Import window spec not found"
    
    # Test default character
    default_char = loader.get_default_character()
    assert 'name' in default_char, "Default character missing name field"
    assert 'characteristics' in default_char, "Default character missing characteristics"
    assert len(default_char['characteristics']) == 8, "Expected 8 characteristics"
    
    print("✓ spec_loader tests passed")


def test_character_model():
    """Test character model functionality."""
    print("Testing character_model...")
    
    # Create model with test data
    model = CharacterModel({
        'name': '',
        'race': '',
        'characteristics': [
            {'abbr': 'Str', 'name': 'Strength', 'score': 50, 'bonus': 5, 'favored': True},
            {'abbr': 'End', 'name': 'Endurance', 'score': 45, 'bonus': 4, 'favored': False}
        ],
        'derived_stats': {
            'HP': {'current': 20, 'max': 30}
        }
    })
    
    # Test simple get/set
    model.set_value('$.name', 'Test Character')
    assert model.get_value('$.name') == 'Test Character', "Name get/set failed"
    
    # Test nested get/set
    model.set_value('$.derived_stats.HP.current', 25)
    assert model.get_value('$.derived_stats.HP.current') == 25, "Nested get/set failed"
    
    # Test array access with [n] notation
    assert model.get_value('$.characteristics[0].abbr') == 'Str', "Array access failed"
    assert model.get_value('$.characteristics[1].score') == 45, "Array access failed"
    
    model.set_value('$.characteristics[0].score', 60)
    assert model.get_value('$.characteristics[0].score') == 60, "Array set failed"
    
    # Test list values (tags)
    model.set_value('$.tags', ['tag1', 'tag2', 'tag3'])
    tags = model.get_value('$.tags')
    assert isinstance(tags, list) and len(tags) == 3, "List get/set failed"
    
    # Test observer
    observer_called = [False]
    def observer():
        observer_called[0] = True
    
    model.add_observer(observer)
    model.set_value('$.name', 'Changed')
    assert observer_called[0], "Observer not called"
    
    # Test to_dict/from_dict
    data = model.to_dict()
    assert data['name'] == 'Changed', "to_dict failed"
    
    new_data = {'name': 'New Character', 'race': 'Nord'}
    model.from_dict(new_data)
    assert model.get_value('$.name') == 'New Character', "from_dict failed"
    
    print("✓ character_model tests passed")


def test_importer():
    """Test importer functionality."""
    print("Testing importer...")
    
    # Create importer with test map
    import_map = {
        'name': '$.name',
        'race': '$.race',
        'characteristics': '$.characteristics',
        'skills': '$.skills'
    }
    
    importer = Importer(import_map)
    
    # Load example character
    try:
        data = importer.load_json('docs/charsheet_cass.json')
        assert data.get('name') == 'Cassius Andromi', "Failed to load example character"
    except FileNotFoundError:
        print("⚠ Warning: docs/charsheet_cass.json not found, skipping file load test")
        data = {
            'name': 'Test Character',
            'race': 'Imperial',
            'skills': [{'name': 'Skill1'}, {'name': 'Skill2'}],
            'birthsign': {'category': 'The Warrior', 'sign': 'The Steed'}
        }
    
    # Test preview generation
    preview = importer.get_preview_info(data)
    assert 'Name:' in preview, "Preview should contain name"
    
    # Test import with overwrite=False
    model = CharacterModel({'name': 'Existing', 'race': '', 'skills': []})
    importer.import_data(data, model, overwrite=False)
    
    # Name should not change (already had value)
    assert model.get_value('$.name') == 'Existing', "Overwrite=False failed"
    # Race should change (was empty)
    assert model.get_value('$.race') == data.get('race'), "Import of empty field failed"
    
    # Test import with overwrite=True
    model2 = CharacterModel({'name': 'Existing', 'race': 'Orc', 'skills': []})
    importer.import_data(data, model2, overwrite=True)
    
    # Name should change with overwrite
    assert model2.get_value('$.name') == data.get('name'), "Overwrite=True failed"
    
    print("✓ importer tests passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("UESRPG Session Manager - Core Module Tests")
    print("=" * 60)
    print()
    
    try:
        test_spec_loader()
        test_character_model()
        test_importer()
        
        print()
        print("=" * 60)
        print("✓ All tests passed!")
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
