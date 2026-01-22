# UESRPG Session Manager - Character Window

A dynamic Tkinter-based Character Window that generates its UI from a JSON specification file.

## Features

- **Character Sheet Dashboard**: Primary view with portrait header, core stats, and skills table - no more hidden sidebar!
- **Dynamic UI Generation**: All UI elements are generated from `/ui/ui_spec.json`
- **Details Tabs**: Organized secondary view with Core, Combat & Skills, Gear, and Magic tabs (toggle to show/hide)
- **Portrait Display**: Fixed 320×200 portrait in header, always visible with Pillow image support (fallback without)
- **Field Types Support**:
  - Text entry (single and multi-line)
  - Integer spinboxes with min/max validation
  - Checkboxes
  - Tag lists (comma-separated)
  - Integer lists (comma-separated)
  - Tables with add/edit/delete functionality
  - Inline tables (fixed rows)
  - Stat blocks (large value + small label)
- **Load/Save**: JSON import/export with UTF-8 support
- **Portrait Selection**: Image selection for character portraits with automatic 320×200 display
- **Robust Error Handling**: Graceful degradation for malformed specs or unsupported features

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Pillow (optional, for portrait image display - graceful fallback without it)

## Quick Start

### Running the Application

```bash
python main.py
```

This will open the Character Window with a character sheet dashboard as the primary view.

### File Structure

- `main.py` - Entry point (minimal)
- `ui.py` - Complete UI implementation
- `ui/ui_spec.json` - UI specification (source of truth)
- `docs/charsheet_cass.json` - Example character data

### Using the Application

1. **New Character**: File → New (or reset to defaults)
2. **Load Character**: File → Open… (select a JSON file)
3. **Save Character**: File → Save or Save As…
4. **Select Portrait**: Click "Select Portrait…" in the portrait header box
5. **Edit Fields**: Modify character data directly on the sheet dashboard
6. **View Details**: Click "Show Details" button to access notebook tabs for gear, magic, etc.
7. **Edit Tables**: Use Add/Edit/Delete buttons for skills, weapons, items, etc.

## Architecture

### Entry Point (main.py)

Minimal entry point that:
- Creates Tk root window
- Instantiates CharacterWindowUI from ui.py
- Runs mainloop

### UI Module (ui.py)

Comprehensive UI implementation with:
- **Spec Loading**: Parses ui_spec.json at startup
- **Dynamic Rendering**: Creates widgets based on spec definitions
- **Sheet View**: New dashboard layout with header/core/content bands
- **Container Widgets**: layout_row, layout_col, sheet_grid, stat_block, portrait_box
- **State Management**: 
  - `get_state()` - Extract current UI values to dict
  - `set_state(data)` - Apply dict values to UI
  - `reset_to_defaults()` - Load default character from spec
- **Load/Save**: JSON serialization with proper encoding
- **Validation**: Placeholder for future validation logic
- **Error Handling**: Try/catch blocks with user-friendly error dialogs

### Specification File (ui/ui_spec.json)

The spec defines:
- Application window properties
- Theme colors and typography
- Menu structure
- **Sheet View** (NEW): Dashboard layout with header, core stats, and content bands
- **Details Panel**: Notebook tabs for secondary data (gear, magic, notes)
- Sections and fields with bindings
- Default character data

#### New Spec Structure

```json
{
  "sheet_view": {
    "type": "sheet",
    "header": { "type": "layout_row", "widgets": [...] },
    "core": { "type": "sheet_grid", "columns": 3, "widgets": [...] },
    "content": { "type": "layout_col", "widgets": [...] }
  },
  "details_panel": {
    "type": "notebook",
    "tabs": [ ...existing tabs... ]
  }
}
```

### Binding Paths

Fields use JSONPath-style bindings to character data:
- `$.name` → character['name']
- `$.xp.current` → character['xp']['current']
- `$.derived_stats.HP.max` → character['derived_stats']['HP']['max']

## Testing

Run tests without GUI:

```bash
# Basic structure and import tests
python tests/test_ui.py

# Round-trip and data handling tests
python tests/test_roundtrip.py
```

## Extending the UI

### Adding Fields to the Sheet Dashboard

To add fields to the character sheet:

1. Edit `ui/ui_spec.json`
2. Add field definition within `sheet_view.header`, `sheet_view.core`, or `sheet_view.content`:
   ```json
   {
     "type": "field",
     "label": "New Field",
     "bind": "$.new_field",
     "widget": "entry"
   }
   ```
3. Update `default_character` in spec if needed
4. Restart application - changes are automatic!

### Using Container Widgets

New container widgets available for layout:

- **layout_row**: Horizontal container (widgets side-by-side)
- **layout_col**: Vertical container (widgets stacked)
- **sheet_grid**: Grid layout with N columns and weight distribution
- **stat_block**: Individual stat display (large value, small label above)
- **portrait_box**: Fixed-size portrait area (320×200) with image display

### Adding to Details Tabs

Secondary data (gear, magic, long notes) should go in `details_panel.tabs`:

1. Edit `ui/ui_spec.json` → `details_panel` → `tabs`
2. Add sections and fields as before
3. Users toggle details panel with "Show Details" button

## Supported Widget Types

- **entry**: Single-line text input
- **textarea**: Multi-line text input
- **spin_int**: Integer spinner with min/max
- **check**: Checkbox (boolean)
- **tags**: Comma-separated list
- **int_list_csv**: Comma-separated integer list
- **table**: Editable table with add/edit/delete
- **table_inline**: Fixed-row table
- **readonly_entry**: Read-only text display
- **stat_block**: Large value with small label (for dashboard)
- **portrait_box**: Fixed 320×200 portrait display with image loading

## Error Handling

The application handles errors gracefully:
- Missing/malformed spec files: Error dialog + log
- Unknown widget types: Placeholder + warning log
- Failed widget creation: Skip + error log
- Load/Save errors: User-friendly error dialogs
- Missing Pillow: Fallback portrait display (path/filename only)

## Logging

Application logs to stdout:
- INFO: Spec loading, tab detection, user actions
- WARNING: Unsupported features, missing config
- ERROR: Failures with full tracebacks

## Visual Layout Changes

### Before (Old Layout)
```
┌─────────────────────────────────┐
│ Menu Bar                        │
├──────────┬──────────────────────┤
│ Portrait │ [Tab 1] [Tab 2] ... │
│ Sidebar  │                      │
│ (always  │ Content requires     │
│ visible) │ switching tabs       │
└──────────┴──────────────────────┘
```

### After (New Layout)
```
┌─────────────────────────────────┐
│ Menu Bar                        │
├─────────────────────────────────┤
│ ┌─────────┐ Identity Fields    │ ← Header Band
│ │Portrait │ Name, Race, etc.   │
│ └─────────┘                     │
├─────────────────────────────────┤
│ Attributes  Derived  Combat     │ ← Core Band (3 columns)
│ • Chars     • HP/MP  • Armor    │   Always visible!
│ • Bonuses   • WT/SP  • Style    │
├─────────────────────────────────┤
│ Skills Table (scrollable)       │ ← Content Band
│ [Add] [Edit] [Delete]           │
├─────────────────────────────────┤
│ ▶ Show Details (Gear, Magic...) │ ← Toggle button
└─────────────────────────────────┘
```

## Known Limitations

1. No validation implementation yet (placeholder exists)
2. Portrait images require Pillow library (graceful fallback without it)
3. Some complex spec features not yet implemented
4. No undo/redo functionality

## Future Enhancements

- [ ] Field validation (required, min/max, patterns)
- [ ] Visual validation feedback
- [ ] Import functionality for base data
- [ ] Undo/redo support
- [ ] Auto-save functionality
- [ ] Character templates
- [ ] Responsive layout for different screen sizes

## License

See LICENSE file in repository root.

## Contributing

This is a spec-driven UI. To contribute:
1. Propose changes to ui_spec.json format
2. Implement support in ui.py
3. Add tests to verify functionality
4. Submit PR with examples
