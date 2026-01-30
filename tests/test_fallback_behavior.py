#!/usr/bin/env python3
"""
Test fallback behavior when config file is missing.
"""

import sys
import tempfile
import shutil
import time
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_fallback_behavior():
    """Test that engine falls back to legacy file with warning."""
    print("=" * 60)
    print("TEST: Fallback Behavior When Config is Missing")
    print("=" * 60)
    
    # Temporarily rename the config file with unique identifier
    repo_root = Path(__file__).parent.parent
    config_file = repo_root / "config" / "attributes_derived.json"
    # Use timestamp to avoid conflicts with concurrent tests
    backup_file = repo_root / "config" / f"attributes_derived.json.test_backup_{int(time.time() * 1000)}"
    
    if not config_file.exists():
        print("✗ Config file doesn't exist - cannot test fallback")
        return False
    
    try:
        # Rename config file
        shutil.move(str(config_file), str(backup_file))
        print("\n1. Config file temporarily removed")
        
        # Import after removing file to get fresh module
        import logging
        import io
        
        # Capture log output
        log_stream = io.StringIO()
        handler = logging.StreamHandler(log_stream)
        handler.setLevel(logging.WARNING)
        
        # Get logger and add handler
        from core.mechanics import derived_engine
        logger = derived_engine.logger
        logger.addHandler(handler)
        
        # Create engine (should trigger fallback)
        from core.mechanics.derived_engine import DerivedStatsEngine
        engine = DerivedStatsEngine()
        
        print(f"2. Engine created with path: {engine.rules_path}")
        
        # Check path
        if "core/mechanics/derived_stats_v1.json" not in engine.rules_path:
            print("✗ Engine did not fall back to legacy path")
            return False
        
        print("✓ Engine fell back to legacy path")
        
        # Check for warning log
        log_output = log_stream.getvalue()
        if "Using legacy derived ruleset" in log_output:
            print("✓ Warning message logged:")
            print(f"   {log_output.strip()}")
        else:
            print("✗ Warning message not found in logs")
            print(f"   Log output: {log_output}")
            return False
        
        # Verify engine still works
        state = {
            'characteristics': [
                {'abbr': 'Str', 'name': 'Strength', 'score': 45, 'bonus': 0},
            ],
            'base_bonuses': {},
            'derived_stats': {}
        }
        
        result = engine.apply(state)
        if result['characteristics'][0]['bonus'] == 4:
            print("✓ Engine still computes correctly with legacy file")
        else:
            print("✗ Engine computation failed with legacy file")
            return False
        
        print("\n✓ Fallback behavior working correctly")
        return True
        
    finally:
        # Restore config file
        if backup_file.exists():
            shutil.move(str(backup_file), str(config_file))
            print("\n3. Config file restored")


def main():
    """Run fallback test."""
    print("\n" + "=" * 60)
    print("FALLBACK BEHAVIOR TEST")
    print("=" * 60)
    
    try:
        result = test_fallback_behavior()
        
        print("\n" + "=" * 60)
        if result:
            print("✓✓✓ FALLBACK TEST PASSED ✓✓✓")
        else:
            print("✗✗✗ FALLBACK TEST FAILED ✗✗✗")
        print("=" * 60)
        
        return 0 if result else 1
    except Exception as e:
        print(f"\n✗ Test raised exception: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
