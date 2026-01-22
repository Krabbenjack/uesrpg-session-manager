# Character Import/Export Feature Implementation Summary

## Overview
This PR implements character JSON import/export functionality and fixes the "Unsupported widget type: stat_block" warnings.

## Branch
`copilot/character-import-export`

## Changes Made

### 1. ui_spec.json (5 lines changed)
- **Line 117**: Renamed menu item from "Import Base Data…" to "Import Character Data…"
- **Line 117**: Changed command from `import_base_data` to `import_character_data`
- **Line 118**: Added new menu item "Export Character Data…" with command `export_character_data`
- **Line 699**: Updated import window title from "Import Base Data" to "Import Character Data"

### 2. ui.py (244 lines added)

#### Widget Rendering Fixes (3 new methods)
- **`_create_stat_block_widget()`**: New method to handle stat_block widgets in grid layout (lines ~885-909)
  - Creates stat blocks with label on top and entry below
  - Registers widget for data binding
  - Eliminates "Unsupported widget type: stat_block" warnings

- **`_create_preview_widget()`**: New method to handle preview widgets in grid layout (lines ~840-852)
  - Creates disabled ScrolledText widget for read-only previews
  - Used by import dialog to show JSON content

- **Updated `_build_widgets_with_layout()`**: Added handling for `stat_block` and `preview` widget types (lines ~618-621)
  - Delegates to new methods instead of logging warnings

#### Import/Export Functionality (6 new methods)

- **`deep_merge()`**: Core merge logic (lines ~1220-1264)
  - Merges imported data with default schema
  - Supports `overwrite=True/False` modes
  - Handles nested dicts, lists, and scalars recursively
  - Ensures schema completeness (magic keys always present)

- **`show_import_dialog()`**: Opens import dialog (lines ~1320-1369)
  - Finds import_window spec
  - Creates Toplevel dialog
  - Manages dialog state and widgets
  - Properly scopes widget registry to avoid conflicts

- **`import_choose_json()`**: File picker for import (lines ~1371-1401)
  - Opens file dialog
  - Loads and validates JSON
  - Generates preview (truncated if >2000 chars)
  - Updates dialog state

- **`import_apply()`**: Applies import with merge logic (lines ~1403-1437)
  - Gets overwrite setting from dialog
  - Merges with default schema using `deep_merge()`
  - Updates UI with merged data
  - Closes dialog and shows success message

- **`export_character_data()`**: Exports character to JSON (lines ~1318-1320)
  - Reuses existing `save_character_as()` functionality
  - Maintains menu distinction for clarity

- **`close_dialog()`**: Closes import dialog (lines ~1439-1447)
  - Restores original widget registry
  - Destroys dialog window

#### Supporting Updates
- **`_set_dialog_state()`**: Sets dialog widget values from state dict (lines ~1449-1456)
- **Updated `_set_widget_value()`**: Handles disabled ScrolledText widgets (lines ~1045-1053)
  - Temporarily enables, sets value, then re-disables
- **Updated `_handle_command()`**: Added command handlers (lines ~942-950)
  - `import_character_data` → `show_import_dialog()`
  - `export_character_data` → `export_character_data()`
  - `import_choose_json` → `import_choose_json()`
  - `import_apply` → `import_apply()`
  - `dialog_close` → `close_dialog()`

### 3. tests/test_import_export.py (268 lines added)
Comprehensive automated tests for:
- Deep merge logic (6 test cases)
- Schema completeness verification
- Import window spec validation
- Menu structure validation

### 4. MANUAL_TEST_CHECKLIST.md (249 lines added)
17 new manual test cases (Tests 22-38) covering:
- Menu structure verification
- Import dialog functionality
- Import with overwrite on/off
- Export functionality
- JSON validation and error handling
- Round-trip import/export
- stat_block warning elimination
- Edge cases (invalid JSON, special characters, large files)

## Technical Implementation Details

### Deep Merge Algorithm
The `deep_merge()` function implements a recursive merge strategy:

1. **Base preservation**: Always starts with the complete default schema
2. **Recursive merging**: For nested dicts, merges recursively
3. **List handling**: 
   - With `overwrite=True`: Replaces list entirely
   - With `overwrite=False`: Only replaces if base list is empty
4. **Scalar handling**:
   - With `overwrite=True`: Replaces value
   - With `overwrite=False`: Only replaces if base value is falsy
5. **New keys**: Always adds keys from overlay that don't exist in base

This ensures that imported data always has complete schema (e.g., `spells`, `magic_skills` always present).

### Dialog Management
The import dialog uses a separate widget registry to avoid conflicts:
1. Store original `self.widgets` → `self.original_widgets`
2. Create new `self.dialog_widgets` dict
3. Temporarily set `self.widgets = self.dialog_widgets`
4. Build dialog widgets (they register to dialog_widgets)
5. Restore `self.widgets = self.original_widgets` after dialog closes

This allows dialog widgets to use bind paths like `$dialog.preview` without conflicting with main window widgets.

### Widget Type Support
The implementation adds two new widget types to the system:

1. **stat_block**: For grid layouts (already existed for pack layouts)
   - Label on top (small font)
   - Entry below (bold, centered)
   - Used in derived stats sections

2. **preview**: For displaying read-only text
   - ScrolledText widget in disabled state
   - Temporarily enabled when setting value
   - Used in import dialog to show JSON preview

## Testing

### Automated Tests (4 test suites)
✅ Schema completeness - verifies magic keys exist
✅ Import window spec - validates dialog configuration
✅ Menu structure - confirms menu changes
✅ Deep merge logic - 6 test cases covering all merge scenarios

### Manual Tests (17 new test cases)
See MANUAL_TEST_CHECKLIST.md tests 22-38

All automated tests pass. Manual tests require GUI environment.

## Verification

### No Breaking Changes
- All existing tests pass (test_ui.py)
- No modifications to existing file operations (Open/Save/Save As)
- No changes to UI layout or bindings
- No folder renames or file moves

### Requirements Met
✅ Menu renamed: "Import Base Data…" → "Import Character Data…"
✅ New menu: "Export Character Data…" added
✅ Import dialog shows preview and overwrite option
✅ Deep merge implemented with no external dependencies
✅ Schema completeness ensured (magic keys always present)
✅ stat_block warnings eliminated
✅ Comprehensive tests provided

## Files Changed
- `ui/ui_spec.json` (5 lines)
- `ui.py` (244 lines added)
- `tests/test_import_export.py` (268 lines added - new file)
- `MANUAL_TEST_CHECKLIST.md` (249 lines added)

**Total**: 766 lines changed, 4 files modified

## Security Considerations
- No external dependencies added
- Uses standard library only (json, pathlib, tkinter)
- File dialogs use tkinter's built-in secure dialogs
- JSON parsing uses standard json module with error handling
- No code execution from imported files (data-only import)

## Performance
- Deep merge is O(n) where n is number of keys in overlay
- Preview truncation prevents memory issues with large files
- No performance impact on existing operations

## Known Limitations
- Import dialog does not support mapping/transformation of data
- Preview limited to 2000 characters
- No validation of imported data structure (schema-free)

## Next Steps for Users
1. Review this PR and code changes
2. Merge to main branch
3. Run manual tests (Tests 22-38) in GUI environment
4. Verify no stat_block warnings appear in console
5. Test import/export with real character files
6. Verify exported files contain all magic keys

## Notes
- This is a feature addition, NOT a refactor
- No files moved or folders renamed
- No changes to UI architecture or bindings
- All changes are additive (no deletions except outdated menu items)
- Backward compatible with existing character JSON files
