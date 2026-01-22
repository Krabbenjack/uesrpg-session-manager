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
