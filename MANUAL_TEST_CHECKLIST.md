# Manual Test Checklist - Character Sheet Dashboard

This checklist should be used to manually verify the new Character Sheet Dashboard layout in a GUI environment.

## Prerequisites
- Python 3.7+
- tkinter installed (`python3-tk` on Linux, included with Python on Windows/Mac)
- Optional: Pillow for portrait image display (`pip install Pillow`)

## Test Environment Setup

1. **Clone and navigate to repository**
   ```bash
   cd uesrpg-session-manager
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

## Visual Layout Tests

### ✅ Test 1: Primary View - Character Sheet Dashboard
**Expected:** Application opens directly to Character Sheet dashboard (not tabs)

- [ ] Window opens without errors
- [ ] No left sidebar visible (old portrait column removed)
- [ ] Portrait box visible in top-left of header (320×200 placeholder)
- [ ] Identity fields visible in header (Name, Race, Birthsign, etc.)
- [ ] Three horizontal bands clearly separated:
  - Header (portrait + identity)
  - Core (3 columns: Attributes / Derived Stats / Combat)
  - Content (Skills table)

### ✅ Test 2: Portrait Display
**Expected:** Portrait box is fixed 320×200, always visible

- [ ] Portrait box shows "No portrait selected" placeholder
- [ ] "Select Portrait…" button present below portrait
- [ ] Portrait box maintains 320×200 size when window resizes
- [ ] Portrait remains visible (never hidden or scrolled away)

### ✅ Test 3: Core Stats Visibility
**Expected:** All core stats visible without switching tabs

- [ ] Characteristics table visible (Str, End, Ag, Int, Wp, Prc, Prs, Lck)
- [ ] Base Bonuses visible (SB, EB, AB, IB, WB, PcB, PsB, LB)
- [ ] Derived Stats visible (HP, MP, WT, SP, Speed, LP, IR, AP, Ling, ENC, CR)
- [ ] Combat Quick Block visible (partial armor slots, combat style)
- [ ] All three columns have equal width distribution

### ✅ Test 4: Skills Table
**Expected:** Skills table visible and functional

- [ ] Skills table visible in content band
- [ ] Table shows columns: Skill, Rank, Bonus, TN
- [ ] Add/Edit/Delete buttons present below table
- [ ] Table is scrollable if many skills present

### ✅ Test 5: Details Panel Toggle
**Expected:** Details panel hidden by default, toggles on button click

- [ ] "▶ Show Details (Gear, Magic, Notes...)" button visible
- [ ] Clicking button expands Details panel below
- [ ] Button text changes to "▼ Hide Details..."
- [ ] Details panel shows notebook tabs: Core, Combat & Skills, Gear, Magic
- [ ] Clicking button again collapses Details panel

## Functionality Tests

### ✅ Test 6: Portrait Selection (Without Pillow)
**Expected:** Portrait selection works, shows filename

- [ ] Click "Select Portrait…" button
- [ ] File dialog opens
- [ ] Navigate to `uesrpg_sm/assets/portraits` (or any directory)
- [ ] Select an image file (PNG, JPG, or GIF)
- [ ] Portrait box shows filename (not full path)
- [ ] Status bar shows "Portrait selected: [filename]"

### ✅ Test 7: Portrait Selection (With Pillow)
**Expected:** Portrait loads and displays as image

*Prerequisites: `pip install Pillow`*

- [ ] Restart application
- [ ] Click "Select Portrait…" button
- [ ] Select an image file
- [ ] Portrait box displays actual image (scaled to fit 320×200)
- [ ] Image maintains aspect ratio (letterbox fit)
- [ ] No distortion or stretching

### ✅ Test 8: Field Editing
**Expected:** All fields remain editable and functional

**Header Fields:**
- [ ] Edit Name field
- [ ] Edit Race field
- [ ] Edit Birthsign fields
- [ ] Toggle Star-Cursed checkbox
- [ ] Change XP values (spinboxes)

**Core Stats:**
- [ ] Edit Characteristics scores
- [ ] Edit Characteristics bonuses
- [ ] Toggle Favored checkboxes
- [ ] Edit Base Bonuses (SB, EB, etc.)
- [ ] Edit Derived Stats (HP, MP, etc.)

**Skills:**
- [ ] Click "Add" button in skills table
- [ ] Enter skill data in dialog
- [ ] Click "Update" to save
- [ ] Select a skill and click "Edit"
- [ ] Modify skill data
- [ ] Click "Update" to save
- [ ] Select a skill and click "Delete"

### ✅ Test 9: Save/Load Character
**Expected:** Data persists correctly with new layout

- [ ] Enter test data in various fields
- [ ] Select a portrait
- [ ] Add some skills
- [ ] File → Save As… → Save as `test_character.json`
- [ ] File → New (clears data)
- [ ] File → Open… → Select `test_character.json`
- [ ] All data loaded correctly
- [ ] Portrait displays correctly
- [ ] All fields populated with saved values

### ✅ Test 10: Window Resize Behavior
**Expected:** Layout remains stable when resizing

- [ ] Resize window wider → Layout expands properly
- [ ] Resize window narrower → Layout shrinks without breaking
- [ ] Resize window taller → Content band scrolls appropriately
- [ ] Resize window shorter → Scrollbar appears, content accessible
- [ ] Portrait box remains 320×200 (does not resize)
- [ ] Core stats remain visible (do not collapse)

### ✅ Test 11: Details Panel Content
**Expected:** All notebook tabs still work in Details panel

**Show Details, then navigate tabs:**
- [ ] Core tab: Shows full character data (same as old Tab 1)
- [ ] Combat & Skills tab: Shows armor, weapons, skills (same as old Tab 2)
- [ ] Gear tab: Shows items, equipment (same as old Tab 3)
- [ ] Magic tab: Shows rituals, spells (same as old Tab 4)
- [ ] All sections within tabs visible
- [ ] All fields editable

### ✅ Test 12: Example Character Load
**Expected:** Existing character JSON files load correctly

- [ ] File → Open… → Select `docs/charsheet_cass.json`
- [ ] Character loads: Cassius Andromi
- [ ] Name, race, XP values correct
- [ ] Characteristics populated
- [ ] Skills table populated
- [ ] Open Details panel
- [ ] Navigate all tabs to verify data

### ✅ Test 13: Scrolling Behavior
**Expected:** Scroll operates correctly

- [ ] Use mouse wheel to scroll main content
- [ ] Content scrolls smoothly
- [ ] Portrait and header remain visible at top
- [ ] Skills table scrolls into/out of view
- [ ] Details panel (if open) scrolls with content

## Edge Cases & Error Handling

### ✅ Test 14: Missing Portrait File
**Expected:** Graceful handling of missing file

- [ ] Manually edit a saved JSON file
- [ ] Set `portrait.file` to a non-existent path
- [ ] Load the character
- [ ] Portrait box shows placeholder (not error)
- [ ] Application does not crash

### ✅ Test 15: Invalid Data in JSON
**Expected:** Application handles gracefully

- [ ] Manually edit a saved JSON file
- [ ] Change a numeric field to a string
- [ ] Load the character
- [ ] Application loads (may show default values)
- [ ] No crash or error dialog

### ✅ Test 16: Minimum Window Size
**Expected:** Window respects minimum size constraints

- [ ] Try to resize window smaller than 980×640
- [ ] Window stops at minimum size
- [ ] Layout remains usable at minimum size
- [ ] Scrollbars appear as needed

## Cross-Platform Tests (if applicable)

### ✅ Test 17: Windows
- [ ] All tests above on Windows

### ✅ Test 18: macOS
- [ ] All tests above on macOS

### ✅ Test 19: Linux
- [ ] All tests above on Linux

## Performance

### ✅ Test 20: Large Character File
**Expected:** Application remains responsive

- [ ] Load or create character with many skills (50+)
- [ ] Add many items to gear table
- [ ] Add many spells
- [ ] Application remains responsive
- [ ] Scrolling is smooth
- [ ] Switching Details tabs is instant

## Final Verification

### ✅ Test 21: Complete Workflow
**Expected:** Full workflow from blank to saved character

1. [ ] Start application
2. [ ] File → New
3. [ ] Fill in identity fields (name, race, etc.)
4. [ ] Select portrait
5. [ ] Edit characteristics and stats
6. [ ] Add 5 skills
7. [ ] Show Details
8. [ ] Add gear in Gear tab
9. [ ] Add spell in Magic tab
10. [ ] File → Save As → `complete_test.json`
11. [ ] Close application
12. [ ] Restart application
13. [ ] File → Open → `complete_test.json`
14. [ ] All data preserved correctly

---

## Notes for Testers

- **Portrait images:** Test with various sizes and aspect ratios (square, portrait, landscape)
- **Data integrity:** Verify old character JSON files still load correctly
- **UI consistency:** Check that colors, fonts, spacing match the theme
- **Accessibility:** Tab order should flow logically through fields
- **Error messages:** Any errors should be user-friendly, not technical tracebacks

## Reporting Issues

When reporting issues, please include:
1. Operating system and version
2. Python version (`python --version`)
3. tkinter version (if known)
4. Pillow version (`pip show Pillow`) if applicable
5. Steps to reproduce
6. Expected vs actual behavior
7. Screenshots if visual issue

---

# Character Import/Export Feature Tests

## Prerequisites
- All previous tests completed
- At least one saved character JSON file available (e.g., `docs/charsheet_cass.json`)

## Import/Export Menu Tests

### ✅ Test 22: Menu Structure
**Expected:** Import menu updated with new options

- [ ] Menu bar has "Import" menu
- [ ] "Import" menu contains "Import Character Data…" (renamed from "Import Base Data…")
- [ ] "Import" menu contains "Export Character Data…" (new)

### ✅ Test 23: Import Character Data Dialog
**Expected:** Import dialog opens and displays correctly

1. [ ] Click **Import → Import Character Data…**
2. [ ] Dialog opens with title "Import Character Data"
3. [ ] Dialog has "Choose JSON…" button
4. [ ] Dialog has "Selected file" field (read-only, empty initially)
5. [ ] Dialog has preview area (large text box, empty initially)
6. [ ] Dialog has "Overwrite existing fields" checkbox (checked by default)
7. [ ] Dialog has "Import" button
8. [ ] Dialog has "Cancel" button

### ✅ Test 24: Choose JSON File
**Expected:** File picker and preview work correctly

1. [ ] In import dialog, click **Choose JSON…**
2. [ ] File picker opens
3. [ ] Navigate to `docs/charsheet_cass.json` and select it
4. [ ] Selected file path appears in "Selected file" field
5. [ ] Preview area shows JSON content (pretty-printed)
6. [ ] Preview is read-only (cannot edit)
7. [ ] If JSON is large (>2000 chars), preview is truncated with "... (truncated)" message

### ✅ Test 25: Import with Overwrite = True
**Expected:** All fields are replaced with imported values

1. [ ] Start with empty character (File → New)
2. [ ] Manually enter: Name = "Test", Race = "Orc", XP Current = 100
3. [ ] Click **Import → Import Character Data…**
4. [ ] "Overwrite existing fields" checkbox is **checked**
5. [ ] Choose `docs/charsheet_cass.json`
6. [ ] Click **Import**
7. [ ] Dialog closes
8. [ ] Name is replaced with value from JSON (e.g., "Cassandra Silvershadow")
9. [ ] Race is replaced with value from JSON (e.g., "Nord, vampire")
10. [ ] XP Current is replaced with value from JSON
11. [ ] All other fields populated from JSON
12. [ ] Status bar shows "Imported: charsheet_cass.json"
13. [ ] Success message appears: "Character data imported successfully"

### ✅ Test 26: Import with Overwrite = False
**Expected:** Only empty fields are filled, existing values preserved

1. [ ] Start with empty character (File → New)
2. [ ] Manually enter: Name = "Existing Name", Race = "Existing Race"
3. [ ] Leave other fields empty
4. [ ] Click **Import → Import Character Data…**
5. [ ] **Uncheck** "Overwrite existing fields" checkbox
6. [ ] Choose `docs/charsheet_cass.json`
7. [ ] Click **Import**
8. [ ] Dialog closes
9. [ ] Name remains "Existing Name" (NOT overwritten)
10. [ ] Race remains "Existing Race" (NOT overwritten)
11. [ ] Empty fields are filled from JSON (skills, characteristics, etc.)
12. [ ] Status bar shows "Imported: charsheet_cass.json"
13. [ ] Success message appears

### ✅ Test 27: Import Cancel
**Expected:** Cancel closes dialog without changes

1. [ ] Enter some data in character sheet
2. [ ] Click **Import → Import Character Data…**
3. [ ] Choose a JSON file
4. [ ] Click **Cancel**
5. [ ] Dialog closes
6. [ ] No changes made to character sheet
7. [ ] Original data still present

### ✅ Test 28: Import Without Selecting File
**Expected:** Warning shown if no file selected

1. [ ] Click **Import → Import Character Data…**
2. [ ] Do NOT click "Choose JSON…"
3. [ ] Click **Import**
4. [ ] Warning message appears: "No file selected"
5. [ ] Dialog remains open

### ✅ Test 29: Export Character Data
**Expected:** Current character exported to JSON file

1. [ ] Load a character (e.g., `docs/charsheet_cass.json`)
2. [ ] Click **Import → Export Character Data…**
3. [ ] Save file dialog opens
4. [ ] Default extension is `.json`
5. [ ] Enter filename (e.g., `test_export.json`)
6. [ ] Click Save
7. [ ] File is saved
8. [ ] Status bar shows "Saved: test_export.json"
9. [ ] Success message appears: "Character saved successfully"

### ✅ Test 30: Verify Exported JSON Structure
**Expected:** Exported JSON has all required keys including magic fields

1. [ ] Export a character to `test_export.json`
2. [ ] Open `test_export.json` in a text editor
3. [ ] JSON is well-formatted with proper indentation
4. [ ] **CRITICAL**: All magic-related keys exist even if empty:
   - [ ] `"spells"` key exists (array)
   - [ ] `"magic_skills"` key exists (array)
   - [ ] `"rituals"` key exists (object or array)
   - [ ] `"spellcasting"` key exists (object)
5. [ ] Other expected keys present: `name`, `race`, `characteristics`, `skills`, etc.
6. [ ] Values match what was displayed in the UI

### ✅ Test 31: Round-Trip Import/Export
**Expected:** Data survives export → import cycle without loss

1. [ ] Load `docs/charsheet_cass.json`
2. [ ] Export to `roundtrip_1.json`
3. [ ] File → New (clear character)
4. [ ] Import `roundtrip_1.json` with Overwrite = True
5. [ ] All data restored exactly as before
6. [ ] Export to `roundtrip_2.json`
7. [ ] Compare `roundtrip_1.json` and `roundtrip_2.json`:
   - [ ] Files are identical (or functionally equivalent)
   - [ ] No data loss or corruption

### ✅ Test 32: Import Incomplete JSON
**Expected:** Missing keys filled with defaults

1. [ ] Create a minimal JSON file `minimal.json`:
   ```json
   {
     "name": "Minimal Character",
     "race": "Human"
   }
   ```
2. [ ] Click **Import → Import Character Data…**
3. [ ] Choose `minimal.json`
4. [ ] Overwrite = True, click Import
5. [ ] Name and race imported correctly
6. [ ] All missing keys filled with defaults from schema
7. [ ] Export the character to verify:
   - [ ] `spells`, `magic_skills`, `rituals`, `spellcasting` keys exist
   - [ ] All default schema keys present

### ✅ Test 33: Import Invalid JSON
**Expected:** Error handled gracefully

1. [ ] Create invalid JSON file `invalid.json`:
   ```
   { "name": "Test", invalid syntax here }
   ```
2. [ ] Click **Import → Import Character Data…**
3. [ ] Choose `invalid.json`
4. [ ] Error message appears: "Failed to load JSON: ..."
5. [ ] Application does not crash
6. [ ] Dialog remains open

### ✅ Test 34: stat_block Warning Elimination
**Expected:** No "Unsupported widget type: stat_block" warnings

1. [ ] Close application if running
2. [ ] Start application from terminal: `python main.py`
3. [ ] Monitor terminal output during:
   - [ ] Application startup
   - [ ] Loading the character sheet
   - [ ] Opening Details panel
   - [ ] Switching between tabs
4. [ ] **Verify NO warnings**: "Unsupported widget type: stat_block"
5. [ ] All stat blocks (HP, MP, Speed, LP, IR, AP, etc.) display correctly
6. [ ] Layout looks correct with no missing stat displays

### ✅ Test 35: Multiple Imports in Sequence
**Expected:** Can import multiple times without issues

1. [ ] Import `docs/charsheet_cass.json`
2. [ ] Verify data loaded
3. [ ] Import a different character JSON (or same file again)
4. [ ] Verify data replaced/merged correctly
5. [ ] Import a third time
6. [ ] No memory leaks or slowdowns
7. [ ] Dialog continues to work correctly

### ✅ Test 36: Import/Export with Special Characters
**Expected:** Unicode and special characters handled correctly

1. [ ] Enter character name with special characters: "Ñörmân Drågøñ"
2. [ ] Export to `unicode_test.json`
3. [ ] Open file, verify special characters saved correctly
4. [ ] File → New
5. [ ] Import `unicode_test.json`
6. [ ] Special characters restored correctly: "Ñörmân Drågøñ"

### ✅ Test 37: Import/Export Large Character
**Expected:** Performance remains acceptable

1. [ ] Create/load character with extensive data:
   - [ ] 50+ skills
   - [ ] 20+ spells
   - [ ] 30+ items
   - [ ] Long text in notes fields
2. [ ] Export to `large_character.json`
3. [ ] Export completes in reasonable time (< 5 seconds)
4. [ ] File size is reasonable (< 1 MB)
5. [ ] Import `large_character.json`
6. [ ] Import completes in reasonable time (< 5 seconds)
7. [ ] All data imported correctly
8. [ ] Application remains responsive

## Final Import/Export Verification

### ✅ Test 38: Complete Import/Export Workflow
**Expected:** Full workflow succeeds without errors

1. [ ] File → New
2. [ ] Create new character:
   - [ ] Enter name, race, size
   - [ ] Edit characteristics
   - [ ] Add 5 skills
   - [ ] Show Details, add gear item
   - [ ] Add spell in Magic tab
3. [ ] Export to `workflow_test.json`
4. [ ] Close application
5. [ ] Restart application
6. [ ] Import `workflow_test.json` with Overwrite = True
7. [ ] All data restored correctly
8. [ ] No errors or warnings in console

---

## Success Criteria for Import/Export

✅ All import/export tests (22-38) passed
✅ No "Unsupported widget type: stat_block" warnings
✅ Exported JSON contains all magic-related keys
✅ Data integrity maintained through import/export cycles
✅ Error handling works correctly for invalid inputs
✅ UI remains stable and responsive
✅ Console output is clean (no unexpected warnings/errors)

