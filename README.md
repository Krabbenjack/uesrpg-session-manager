# UESRPG Session Manager - Character Window

A dynamic Tkinter-based Character Window that generates its UI from a JSON specification file.

## Features

- **Dynamic UI Generation**: All UI elements are generated from `/ui/ui_spec.json`
- **Multiple Tabs**: Organized layout with Core, Combat & Skills, Gear, and Magic tabs
- **Field Types Support**:
  - Text entry (single and multi-line)
  - Integer spinboxes with min/max validation
  - Checkboxes
  - Tag lists (comma-separated)
  - Integer lists (comma-separated)
  - Tables with add/edit/delete functionality
  - Inline tables (fixed rows)
- **Load/Save**: JSON import/export with UTF-8 support
- **Portrait Selection**: Image selection for character portraits
- **Robust Error Handling**: Graceful degradation for malformed specs or unsupported features

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- No external dependencies (stdlib only)

## Quick Start

### Running the Application

```bash
python main.py
```

This will open the Character Window with a default character template.

### File Structure

- `main.py` - Entry point (minimal)
- `ui.py` - Complete UI implementation
- `ui/ui_spec.json` - UI specification (source of truth)
- `docs/charsheet_cass.json` - Example character data

### Using the Application

1. **New Character**: File → New (or reset to defaults)
2. **Load Character**: File → Open… (select a JSON file)
3. **Save Character**: File → Save or Save As…
4. **Select Portrait**: Click "Select Portrait…" in the left panel
5. **Edit Fields**: Navigate tabs and modify character data
6. **Edit Tables**: Use Add/Edit/Delete buttons for skills, weapons, items, etc.

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
- Window layout (columns, panels)
- Tab structure
- Sections and fields with bindings
- Default character data

### Binding Paths

Fields use JSONPath-style bindings to character data:
- `$.name` → character['name']
- `$.xp.current` → character['xp']['current']
- `$.derived_stats.HP.max` → character['derived_stats']['HP']['max']

## Testing

Run tests without GUI:

```bash
# Basic structure and import tests
python test_ui.py

# Round-trip and data handling tests
python test_roundtrip.py
```

## Extending the UI

To add new fields or sections:

1. Edit `ui/ui_spec.json`
2. Add field definition with:
   - `type`: "field", "table", "group", etc.
   - `label`: Display label
   - `bind`: Path to data (e.g., "$.new_field")
   - `widget`: Widget type (entry, textarea, spin_int, etc.)
3. Update `default_character` in spec if needed
4. Restart application - changes are automatic!

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

## Error Handling

The application handles errors gracefully:
- Missing/malformed spec files: Error dialog + log
- Unknown widget types: Placeholder + warning log
- Failed widget creation: Skip + error log
- Load/Save errors: User-friendly error dialogs

## Logging

Application logs to stdout:
- INFO: Spec loading, tab detection, user actions
- WARNING: Unsupported features, missing config
- ERROR: Failures with full tracebacks

## Known Limitations

1. No validation implementation yet (placeholder exists)
2. Portrait images not rendered (path stored only)
3. Some complex spec features not yet implemented
4. No undo/redo functionality

## Future Enhancements

- [ ] Field validation (required, min/max, patterns)
- [ ] Visual validation feedback
- [ ] Portrait image rendering
- [ ] Import functionality for base data
- [ ] Undo/redo support
- [ ] Auto-save functionality
- [ ] Character templates

## License

See LICENSE file in repository root.

## Contributing

This is a spec-driven UI. To contribute:
1. Propose changes to ui_spec.json format
2. Implement support in ui.py
3. Add tests to verify functionality
4. Submit PR with examples
