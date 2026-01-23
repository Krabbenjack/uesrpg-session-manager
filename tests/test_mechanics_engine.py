#!/usr/bin/env python3
"""
Test script for derived stats mechanics engine.

Tests that the engine correctly computes:
- Characteristic bonuses from scores
- Base bonuses from characteristic bonuses
- Derived stats (HP, MP, Speed, IR, etc.)
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.mechanics import apply_derived_stats


def test_characteristic_bonus_computation():
    """Test that characteristic bonuses are computed correctly."""
    print("\n=== Testing Characteristic Bonus Computation ===")
    
    # Create test state with characteristic scores
    state = {
        'characteristics': [
            {'abbr': 'Str', 'name': 'Strength', 'score': 45, 'bonus': 0},
            {'abbr': 'End', 'name': 'Endurance', 'score': 50, 'bonus': 0},
            {'abbr': 'Ag', 'name': 'Agility', 'score': 38, 'bonus': 0},
            {'abbr': 'Int', 'name': 'Intelligence', 'score': 60, 'bonus': 0},
            {'abbr': 'Wp', 'name': 'Willpower', 'score': 42, 'bonus': 0},
            {'abbr': 'Prc', 'name': 'Perception', 'score': 35, 'bonus': 0},
            {'abbr': 'Prs', 'name': 'Personality', 'score': 28, 'bonus': 0},
            {'abbr': 'Lck', 'name': 'Luck', 'score': 55, 'bonus': 0},
        ],
        'base_bonuses': {},
        'derived_stats': {}
    }
    
    # Apply derived stats
    result = apply_derived_stats(state)
    
    # Verify characteristic bonuses
    expected_bonuses = {
        'Str': 4,  # 45 // 10
        'End': 5,  # 50 // 10
        'Ag': 3,   # 38 // 10
        'Int': 6,  # 60 // 10
        'Wp': 4,   # 42 // 10
        'Prc': 3,  # 35 // 10
        'Prs': 2,  # 28 // 10
        'Lck': 5,  # 55 // 10
    }
    
    for char in result['characteristics']:
        abbr = char['abbr']
        expected = expected_bonuses.get(abbr)
        actual = char.get('bonus')
        print(f"  {abbr}: score={char['score']}, bonus={actual} (expected {expected})")
        assert actual == expected, f"Bonus mismatch for {abbr}: {actual} != {expected}"
    
    print("✓ Characteristic bonuses computed correctly")


def test_base_bonuses_mapping():
    """Test that base bonuses are mapped from characteristic bonuses."""
    print("\n=== Testing Base Bonuses Mapping ===")
    
    state = {
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
        'base_bonuses': {},
        'derived_stats': {}
    }
    
    result = apply_derived_stats(state)
    
    # Verify base bonuses
    expected_base = {
        'SB': 5,   # Str
        'EB': 4,   # End
        'AB': 3,   # Ag
        'IB': 6,   # Int
        'WB': 4,   # Wp
        'PcB': 3,  # Prc
        'PsB': 2,  # Prs
        'LB': 5,   # Lck
    }
    
    base_bonuses = result.get('base_bonuses', {})
    for key, expected in expected_base.items():
        actual = base_bonuses.get(key)
        print(f"  {key}: {actual} (expected {expected})")
        assert actual == expected, f"Base bonus mismatch for {key}: {actual} != {expected}"
    
    print("✓ Base bonuses mapped correctly")


def test_derived_stats_computation():
    """Test that derived stats are computed correctly."""
    print("\n=== Testing Derived Stats Computation ===")
    
    state = {
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
        'base_bonuses': {
            'SB': 5, 'EB': 4, 'AB': 3, 'IB': 6, 'WB': 4, 'PcB': 3, 'PsB': 2, 'LB': 5
        },
        'derived_stats': {}
    }
    
    result = apply_derived_stats(state)
    
    derived = result.get('derived_stats', {})
    
    # HP.max = ceil(End / 2) = ceil(40 / 2) = 20
    hp_max = derived.get('HP', {}).get('max')
    print(f"  HP.max: {hp_max} (expected 20)")
    assert hp_max == 20, f"HP.max mismatch: {hp_max} != 20"
    
    # MP.max = Int = 60
    mp_max = derived.get('MP', {}).get('max')
    print(f"  MP.max: {mp_max} (expected 60)")
    assert mp_max == 60, f"MP.max mismatch: {mp_max} != 60"
    
    # SP.max = EB = 4
    sp_max = derived.get('SP', {}).get('max')
    print(f"  SP.max: {sp_max} (expected 4)")
    assert sp_max == 4, f"SP.max mismatch: {sp_max} != 4"
    
    # Linguistics = ceil(IB / 2) = ceil(6 / 2) = 3
    linguistics = derived.get('Linguistics')
    print(f"  Linguistics: {linguistics} (expected 3)")
    assert linguistics == 3, f"Linguistics mismatch: {linguistics} != 3"
    
    # IR = AB + IB + PcB = 3 + 6 + 3 = 12
    ir = derived.get('IR')
    print(f"  IR: {ir} (expected 12)")
    assert ir == 12, f"IR mismatch: {ir} != 12"
    
    # Speed_m = SB + 2*AB = 5 + 2*3 = 11
    speed = derived.get('Speed_m')
    print(f"  Speed_m: {speed} (expected 11)")
    assert speed == 11, f"Speed_m mismatch: {speed} != 11"
    
    # CR = 4*SB + 2*EB = 4*5 + 2*4 = 28
    cr = derived.get('CR')
    print(f"  CR: {cr} (expected 28)")
    assert cr == 28, f"CR mismatch: {cr} != 28"
    
    # AP.max = 3 (constant)
    ap_max = derived.get('AP', {}).get('max')
    print(f"  AP.max: {ap_max} (expected 3)")
    assert ap_max == 3, f"AP.max mismatch: {ap_max} != 3"
    
    # LP.max = LB = 5
    lp_max = derived.get('LP', {}).get('max')
    print(f"  LP.max: {lp_max} (expected 5)")
    assert lp_max == 5, f"LP.max mismatch: {lp_max} != 5"
    
    # ENC.max = CR = 28
    enc_max = derived.get('ENC', {}).get('max')
    print(f"  ENC.max: {enc_max} (expected 28)")
    assert enc_max == 28, f"ENC.max mismatch: {enc_max} != 28"
    
    print("✓ Derived stats computed correctly")


def test_do_not_overwrite_current_pools():
    """Test that current pool values are not overwritten."""
    print("\n=== Testing Do Not Overwrite Current Pools ===")
    
    state = {
        'characteristics': [
            {'abbr': 'End', 'score': 40, 'bonus': 4},
            {'abbr': 'Int', 'score': 60, 'bonus': 6},
            {'abbr': 'Str', 'score': 50, 'bonus': 5},
            {'abbr': 'Ag', 'score': 30, 'bonus': 3},
            {'abbr': 'Wp', 'score': 45, 'bonus': 4},
            {'abbr': 'Prc', 'score': 35, 'bonus': 3},
            {'abbr': 'Prs', 'score': 25, 'bonus': 2},
            {'abbr': 'Lck', 'score': 55, 'bonus': 5},
        ],
        'base_bonuses': {
            'SB': 5, 'EB': 4, 'AB': 3, 'IB': 6, 'WB': 4, 'PcB': 3, 'PsB': 2, 'LB': 5
        },
        'derived_stats': {
            'HP': {'current': 15, 'max': 0},  # Current HP should not be overwritten
            'MP': {'current': 40, 'max': 0},  # Current MP should not be overwritten
        }
    }
    
    result = apply_derived_stats(state)
    
    derived = result.get('derived_stats', {})
    
    # HP.current should be preserved
    hp_current = derived.get('HP', {}).get('current')
    print(f"  HP.current: {hp_current} (expected 15, preserved)")
    assert hp_current == 15, f"HP.current was overwritten: {hp_current} != 15"
    
    # HP.max should be computed
    hp_max = derived.get('HP', {}).get('max')
    print(f"  HP.max: {hp_max} (expected 20, computed)")
    assert hp_max == 20, f"HP.max not computed correctly: {hp_max} != 20"
    
    # MP.current should be preserved
    mp_current = derived.get('MP', {}).get('current')
    print(f"  MP.current: {mp_current} (expected 40, preserved)")
    assert mp_current == 40, f"MP.current was overwritten: {mp_current} != 40"
    
    # MP.max should be computed
    mp_max = derived.get('MP', {}).get('max')
    print(f"  MP.max: {mp_max} (expected 60, computed)")
    assert mp_max == 60, f"MP.max not computed correctly: {mp_max} != 60"
    
    print("✓ Current pools preserved correctly")


def test_full_pipeline():
    """Test the full pipeline from raw scores to all derived values."""
    print("\n=== Testing Full Pipeline ===")
    
    # Start with just scores (no bonuses or derived stats)
    state = {
        'characteristics': [
            {'abbr': 'Str', 'name': 'Strength', 'score': 45, 'bonus': 0},
            {'abbr': 'End', 'name': 'Endurance', 'score': 50, 'bonus': 0},
            {'abbr': 'Ag', 'name': 'Agility', 'score': 38, 'bonus': 0},
            {'abbr': 'Int', 'name': 'Intelligence', 'score': 60, 'bonus': 0},
            {'abbr': 'Wp', 'name': 'Willpower', 'score': 42, 'bonus': 0},
            {'abbr': 'Prc', 'name': 'Perception', 'score': 35, 'bonus': 0},
            {'abbr': 'Prs', 'name': 'Personality', 'score': 28, 'bonus': 0},
            {'abbr': 'Lck', 'name': 'Luck', 'score': 55, 'bonus': 0},
        ],
        'base_bonuses': {},
        'derived_stats': {}
    }
    
    # Apply all rules
    result = apply_derived_stats(state)
    
    # Verify all stages completed
    print("  Checking characteristic bonuses...")
    for char in result['characteristics']:
        assert char.get('bonus') > 0 or char['score'] < 10, f"Bonus not computed for {char['abbr']}"
    
    print("  Checking base bonuses...")
    base_bonuses = result.get('base_bonuses', {})
    assert len(base_bonuses) == 8, f"Not all base bonuses computed: {len(base_bonuses)}"
    
    print("  Checking derived stats...")
    derived = result.get('derived_stats', {})
    assert 'HP' in derived, "HP not computed"
    assert 'MP' in derived, "MP not computed"
    assert 'Speed_m' in derived, "Speed_m not computed"
    assert 'IR' in derived, "IR not computed"
    assert 'CR' in derived, "CR not computed"
    
    print("✓ Full pipeline executed successfully")
    
    # Print summary
    print("\n  Final State Summary:")
    char_bonuses = [f"{c['abbr']}={c['bonus']}" for c in result['characteristics']]
    print(f"    Characteristics bonuses: {char_bonuses}")
    print(f"    Base bonuses: {result['base_bonuses']}")
    print(f"    HP: max={derived.get('HP', {}).get('max')}")
    print(f"    MP: max={derived.get('MP', {}).get('max')}")
    print(f"    Speed: {derived.get('Speed_m')}")
    print(f"    IR: {derived.get('IR')}")
    print(f"    CR: {derived.get('CR')}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("DERIVED STATS ENGINE TEST SUITE")
    print("=" * 60)
    
    try:
        test_characteristic_bonus_computation()
        test_base_bonuses_mapping()
        test_derived_stats_computation()
        test_do_not_overwrite_current_pools()
        test_full_pipeline()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
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
