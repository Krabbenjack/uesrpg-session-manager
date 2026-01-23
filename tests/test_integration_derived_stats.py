#!/usr/bin/env python3
"""
Integration test for derived stats engine.

Tests the full flow:
1. Import character data
2. Verify derived stats are computed
3. Export character data
4. Verify export is slim (no computed values)
5. Re-import exported data
6. Verify derived stats are recomputed correctly
"""

import sys
import json
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    merge_character_data,
    prepare_export_data,
    load_json_file,
    save_json_file,
)


def test_import_and_derived_computation():
    """Test that importing data computes derived stats."""
    print("\n=== Test Import and Derived Computation ===")
    
    # Create minimal character data (no bonuses or derived stats)
    imported_data = {
        'name': 'Test Character',
        'characteristics': [
            {'abbr': 'Str', 'score': 50},
            {'abbr': 'End', 'score': 40},
            {'abbr': 'Ag', 'score': 30},
            {'abbr': 'Int', 'score': 60},
            {'abbr': 'Wp', 'score': 45},
            {'abbr': 'Prc', 'score': 35},
            {'abbr': 'Prs', 'score': 25},
            {'abbr': 'Lck', 'score': 55},
        ],
    }
    
    # Default schema (from ui_spec.json default_character)
    default_schema = {
        'name': '',
        'characteristics': [
            {'abbr': 'Str', 'name': 'Strength', 'score': 0, 'bonus': 0},
            {'abbr': 'End', 'name': 'Endurance', 'score': 0, 'bonus': 0},
            {'abbr': 'Ag', 'name': 'Agility', 'score': 0, 'bonus': 0},
            {'abbr': 'Int', 'name': 'Intelligence', 'score': 0, 'bonus': 0},
            {'abbr': 'Wp', 'name': 'Willpower', 'score': 0, 'bonus': 0},
            {'abbr': 'Prc', 'name': 'Perception', 'score': 0, 'bonus': 0},
            {'abbr': 'Prs', 'name': 'Personality', 'score': 0, 'bonus': 0},
            {'abbr': 'Lck', 'name': 'Luck', 'score': 0, 'bonus': 0},
        ],
        'base_bonuses': {},
        'derived_stats': {},
    }
    
    # Merge and compute
    merged = merge_character_data(default_schema, imported_data, overwrite=True)
    
    # Verify characteristic bonuses were computed
    print("  Characteristic Bonuses:")
    for char in merged['characteristics']:
        abbr = char['abbr']
        bonus = char.get('bonus', 0)
        score = char['score']
        expected = score // 10
        print(f"    {abbr}: score={score}, bonus={bonus} (expected {expected})")
        assert bonus == expected, f"Bonus mismatch for {abbr}"
    
    # Verify base bonuses were computed
    print("  Base Bonuses:")
    base_bonuses = merged.get('base_bonuses', {})
    assert base_bonuses.get('SB') == 5, "SB not computed"
    assert base_bonuses.get('EB') == 4, "EB not computed"
    assert base_bonuses.get('IB') == 6, "IB not computed"
    print(f"    {base_bonuses}")
    
    # Verify derived stats were computed
    print("  Derived Stats:")
    derived = merged.get('derived_stats', {})
    assert derived.get('HP', {}).get('max') == 20, "HP.max not computed"
    assert derived.get('MP', {}).get('max') == 60, "MP.max not computed"
    assert derived.get('Speed_m') == 11, "Speed_m not computed"
    print(f"    HP.max: {derived.get('HP', {}).get('max')}")
    print(f"    MP.max: {derived.get('MP', {}).get('max')}")
    print(f"    Speed: {derived.get('Speed_m')}")
    
    print("✓ Import and derived computation working correctly")
    return merged


def test_export_slimming(character_data):
    """Test that export strips computed values."""
    print("\n=== Test Export Slimming ===")
    
    # Prepare export data
    export_data = prepare_export_data(character_data)
    
    # Verify characteristic bonuses are stripped
    print("  Checking characteristic bonuses stripped:")
    for char in export_data.get('characteristics', []):
        assert 'bonus' not in char or char['bonus'] == 0, f"Bonus not stripped for {char.get('abbr')}"
        print(f"    {char.get('abbr')}: bonus stripped ✓")
    
    # Verify base_bonuses are stripped
    print("  Checking base_bonuses stripped:")
    base_bonuses = export_data.get('base_bonuses', {})
    assert len(base_bonuses) == 0, "base_bonuses not stripped"
    print(f"    base_bonuses: {base_bonuses} ✓")
    
    # Verify derived_stats maximums are stripped
    print("  Checking derived_stats maximums stripped:")
    derived = export_data.get('derived_stats', {})
    # Should only have current values (if they exist), not max
    for key in ['HP', 'MP', 'SP']:
        if key in derived:
            assert 'max' not in derived[key], f"{key}.max not stripped"
            print(f"    {key}.max: stripped ✓")
    
    # Verify scalar derived stats are stripped
    assert 'Speed_m' not in derived, "Speed_m not stripped"
    assert 'IR' not in derived, "IR not stripped"
    assert 'CR' not in derived, "CR not stripped"
    print(f"    Speed_m, IR, CR: stripped ✓")
    
    print("✓ Export slimming working correctly")
    return export_data


def test_roundtrip_with_current_pools():
    """Test roundtrip with current HP/MP values preserved."""
    print("\n=== Test Roundtrip with Current Pools ===")
    
    # Create character with current HP/MP
    character_data = {
        'name': 'Test Hero',
        'characteristics': [
            {'abbr': 'Str', 'score': 50, 'bonus': 5},
            {'abbr': 'End', 'score': 40, 'bonus': 4},
            {'abbr': 'Ag', 'score': 30, 'bonus': 3},
            {'abbr': 'Int', 'score': 60, 'bonus': 6},
            {'abbr': 'Wp', 'score': 45, 'bonus': 4},
            {'abbr': 'Prc', 'score': 35, 'bonus': 3},
            {'abbr': 'Prs', 'score': 25, 'bonus': 2},
            {'abbr': 'Lck', 'score': 55, 'bonus': 5},
        ],
        'base_bonuses': {'SB': 5, 'EB': 4, 'AB': 3, 'IB': 6, 'WB': 4, 'PcB': 3, 'PsB': 2, 'LB': 5},
        'derived_stats': {
            'HP': {'current': 15, 'max': 20},
            'MP': {'current': 40, 'max': 60},
        }
    }
    
    # Export (slim)
    export_data = prepare_export_data(character_data)
    
    # Verify current pools are preserved in export
    print("  Export preserves current pools:")
    assert export_data['derived_stats']['HP']['current'] == 15, "HP.current not preserved"
    assert export_data['derived_stats']['MP']['current'] == 40, "MP.current not preserved"
    print(f"    HP.current: {export_data['derived_stats']['HP']['current']} ✓")
    print(f"    MP.current: {export_data['derived_stats']['MP']['current']} ✓")
    
    # Re-import
    default_schema = {
        'name': '',
        'characteristics': [
            {'abbr': 'Str', 'name': 'Strength', 'score': 0, 'bonus': 0},
            {'abbr': 'End', 'name': 'Endurance', 'score': 0, 'bonus': 0},
            {'abbr': 'Ag', 'name': 'Agility', 'score': 0, 'bonus': 0},
            {'abbr': 'Int', 'name': 'Intelligence', 'score': 0, 'bonus': 0},
            {'abbr': 'Wp', 'name': 'Willpower', 'score': 0, 'bonus': 0},
            {'abbr': 'Prc', 'name': 'Perception', 'score': 0, 'bonus': 0},
            {'abbr': 'Prs', 'name': 'Personality', 'score': 0, 'bonus': 0},
            {'abbr': 'Lck', 'name': 'Luck', 'score': 0, 'bonus': 0},
        ],
        'base_bonuses': {},
        'derived_stats': {},
    }
    
    reimported = merge_character_data(default_schema, export_data, overwrite=True)
    
    # Verify current pools are still preserved after re-import
    print("  Re-import preserves current pools:")
    assert reimported['derived_stats']['HP']['current'] == 15, "HP.current lost in re-import"
    assert reimported['derived_stats']['MP']['current'] == 40, "MP.current lost in re-import"
    print(f"    HP.current: {reimported['derived_stats']['HP']['current']} ✓")
    print(f"    MP.current: {reimported['derived_stats']['MP']['current']} ✓")
    
    # Verify derived values are recomputed
    print("  Re-import recomputes derived values:")
    assert reimported['derived_stats']['HP']['max'] == 20, "HP.max not recomputed"
    assert reimported['derived_stats']['MP']['max'] == 60, "MP.max not recomputed"
    print(f"    HP.max: {reimported['derived_stats']['HP']['max']} ✓")
    print(f"    MP.max: {reimported['derived_stats']['MP']['max']} ✓")
    
    print("✓ Roundtrip with current pools working correctly")


def test_file_roundtrip():
    """Test full file-based roundtrip."""
    print("\n=== Test File-Based Roundtrip ===")
    
    # Create test character
    character_data = {
        'name': 'Cassandra',
        'race': 'Nord',
        'characteristics': [
            {'abbr': 'Str', 'score': 45, 'bonus': 4},
            {'abbr': 'End', 'score': 50, 'bonus': 5},
            {'abbr': 'Ag', 'score': 38, 'bonus': 3},
            {'abbr': 'Int', 'score': 60, 'bonus': 6},
            {'abbr': 'Wp', 'score': 42, 'bonus': 4},
            {'abbr': 'Prc', 'score': 35, 'bonus': 3},
            {'abbr': 'Prs', 'score': 28, 'bonus': 2},
            {'abbr': 'Lck', 'score': 55, 'bonus': 5},
        ],
        'base_bonuses': {'SB': 4, 'EB': 5, 'AB': 3, 'IB': 6, 'WB': 4, 'PcB': 3, 'PsB': 2, 'LB': 5},
        'derived_stats': {
            'HP': {'current': 18, 'max': 25},
            'MP': {'current': 50, 'max': 60},
            'Speed_m': 10,
            'IR': 12,
        }
    }
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        export_file = f.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        reimport_file = f.name
    
    try:
        # Export to file
        export_data = prepare_export_data(character_data)
        save_json_file(export_file, export_data)
        print(f"  Exported to {export_file}")
        
        # Verify export file is slim
        with open(export_file, 'r') as f:
            export_content = json.load(f)
        
        # Check sizes
        original_size = len(json.dumps(character_data))
        export_size = len(json.dumps(export_content))
        print(f"  Original size: {original_size} bytes")
        print(f"  Export size: {export_size} bytes")
        print(f"  Reduction: {original_size - export_size} bytes ({100*(original_size-export_size)//original_size}%)")
        
        # Re-import
        loaded_data = load_json_file(export_file)
        default_schema = {
            'name': '',
            'race': '',
            'characteristics': [
                {'abbr': 'Str', 'name': 'Strength', 'score': 0, 'bonus': 0},
                {'abbr': 'End', 'name': 'Endurance', 'score': 0, 'bonus': 0},
                {'abbr': 'Ag', 'name': 'Agility', 'score': 0, 'bonus': 0},
                {'abbr': 'Int', 'name': 'Intelligence', 'score': 0, 'bonus': 0},
                {'abbr': 'Wp', 'name': 'Willpower', 'score': 0, 'bonus': 0},
                {'abbr': 'Prc', 'name': 'Perception', 'score': 0, 'bonus': 0},
                {'abbr': 'Prs', 'name': 'Personality', 'score': 0, 'bonus': 0},
                {'abbr': 'Lck', 'name': 'Luck', 'score': 0, 'bonus': 0},
            ],
            'base_bonuses': {},
            'derived_stats': {},
        }
        
        reimported = merge_character_data(default_schema, loaded_data, overwrite=True)
        
        # Verify data integrity
        assert reimported['name'] == 'Cassandra', "Name lost"
        assert reimported['race'] == 'Nord', "Race lost"
        assert reimported['derived_stats']['HP']['current'] == 18, "HP.current lost"
        assert reimported['derived_stats']['MP']['current'] == 50, "MP.current lost"
        assert reimported['derived_stats']['HP']['max'] == 25, "HP.max not recomputed"
        assert reimported['derived_stats']['MP']['max'] == 60, "MP.max not recomputed"
        
        print("  Data integrity verified ✓")
        print("✓ File-based roundtrip working correctly")
        
    finally:
        # Cleanup
        Path(export_file).unlink(missing_ok=True)
        Path(reimport_file).unlink(missing_ok=True)


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("DERIVED STATS INTEGRATION TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Import and computation
        character_data = test_import_and_derived_computation()
        
        # Test 2: Export slimming
        export_data = test_export_slimming(character_data)
        
        # Test 3: Roundtrip with current pools
        test_roundtrip_with_current_pools()
        
        # Test 4: File-based roundtrip
        test_file_roundtrip()
        
        print("\n" + "=" * 60)
        print("✓ ALL INTEGRATION TESTS PASSED")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
