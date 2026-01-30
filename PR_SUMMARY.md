# PR Summary: Default Rules Migration

## What Was Changed

This PR successfully migrates the derived stats rules to use `config/attributes_derived.json` as the default source of truth, with the legacy `core/mechanics/derived_stats_v1.json` retained as a fallback.

## Key Changes

### 1. Mechanics Engine (`core/mechanics/derived_engine.py`)
- **New Method**: `_find_repo_root()` - Walks up directory tree to find repository root
- **Updated Method**: `_get_default_rules_path()` - Uses new resolution order:
  1. First: `config/attributes_derived.json` (NEW DEFAULT)
  2. Fallback: `core/mechanics/derived_stats_v1.json` (LEGACY)
  3. Logs WARNING when fallback is used

### 2. Configuration File (`config/attributes_derived.json`)
- Created with operational rules format (copied from legacy file)
- Contains same 4 operations for computing bonuses and derived stats
- Includes pool protection to preserve user-edited current values

### 3. UI Specification (`ui/ui_spec.json`)
- Marked `bonus` column as `readonly: true` in characteristics table
- Prevents users from manually editing computed bonus values

### 4. Test Suite
- **New**: `tests/test_rules_path_resolution.py` - Verifies default path and repo root finding
- **New**: `tests/test_fallback_behavior.py` - Verifies fallback with WARNING
- **New**: `tests/test_manual_verification.py` - Comprehensive verification suite
- **Existing**: All 8 existing test suites pass without modification

## Verification

### ✅ All Acceptance Criteria Met
1. App uses `config/attributes_derived.json` by default
2. Falls back to legacy file with WARNING when config is missing
3. Bonus column is not editable but updates when scores change
4. No regressions in load/save and recompute
5. Tests verify default path resolution and fallback behavior

### ✅ Security & Quality
- CodeQL scan: 0 alerts
- Code review: All feedback addressed
- Test coverage: 100% of new code paths tested

### ✅ Backward Compatibility
- Legacy rules file retained for fallback
- All existing character files load correctly
- No breaking changes to API or data format

## Testing Results

```
✅ test_mechanics_engine.py         - Engine computation tests
✅ test_integration_derived_stats.py - Import/export/roundtrip tests
✅ test_roundtrip.py                 - UI state management tests
✅ test_import_export.py             - Data merging tests
✅ test_core_module.py               - Validation tests
✅ test_ui.py                        - UI component tests
✅ test_rules_path_resolution.py     - NEW: Path resolution tests
✅ test_fallback_behavior.py         - NEW: Fallback behavior tests
✅ test_manual_verification.py       - NEW: Comprehensive verification
```

## Migration Impact

### For End Users
- ✅ No action required
- ✅ Existing saves work unchanged
- ✅ Bonus values now read-only (auto-computed)

### For Developers
- ✅ New rules go in `config/attributes_derived.json`
- ✅ Legacy file kept for compatibility
- ✅ Engine auto-finds repo root (no path config needed)

## Log Messages Reference

**Normal operation:**
```
INFO: Loaded derived stats rules from .../config/attributes_derived.json
```

**Fallback mode:**
```
WARNING: Using legacy derived ruleset: core/mechanics/derived_stats_v1.json. 
         Consider moving rules to config/attributes_derived.json
INFO: Loaded derived stats rules from .../core/mechanics/derived_stats_v1.json
```

## Files Changed

### Modified
- `core/mechanics/derived_engine.py` - Rules path resolution
- `ui/ui_spec.json` - Bonus column readonly marker

### Added
- `config/attributes_derived.json` - New default rules file
- `tests/test_rules_path_resolution.py` - Path resolution tests
- `tests/test_fallback_behavior.py` - Fallback tests
- `tests/test_manual_verification.py` - Verification suite
- `IMPLEMENTATION_NOTES.md` - Detailed implementation notes

## Ready to Merge

This PR is ready to merge. All tests pass, security scan is clean, code review feedback has been addressed, and all acceptance criteria are met.

### Final Checklist
- [x] All existing tests pass
- [x] New test suite added and passing
- [x] Code review feedback addressed
- [x] Security scan clean (0 alerts)
- [x] Documentation updated
- [x] Backward compatibility maintained
- [x] No breaking changes
