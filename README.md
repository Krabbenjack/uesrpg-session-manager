# UESRPG Session Manager

Python/Tkinter session manager for UESRPG — JSON import/export, spec-driven UI, and character management.

## Features

- **Spec-driven UI**: The entire character sheet UI is generated from `ui/ui_spec.json`
- **Character Management**: Create, open, save character sheets as JSON
- **Import System**: Import character data from external JSON files with merge rules
- **Portrait Support**: Select and display character portraits
- **Tabbed Interface**: Organized tabs for Core stats, Combat & Skills, Gear, and Magic

## Requirements

- Python 3.7+
- tkinter (usually included with Python)
- Pillow (PIL) for JPG/JPEG portrait support (optional - PNG/GIF work without it)

## Installation

1. Install dependencies (optional, for JPG portrait support):
```bash
pip install Pillow
```

## Running the Application

Simply run the main entry point:

```bash
python app.py
```

Or run as a module:

```bash
python -m uesrpg_sm
```

## Testing

Run the core module tests (does not require a display):

```bash
python test_core.py
```

This validates:
- Spec loading from `ui/ui_spec.json`
- Character model data binding with JSONPath
- Import functionality with merge rules
- Validator for ensuring data completeness

## Project Structure

```
uesrpg-session-manager/
├── app.py                          # Main entry point
├── uesrpg_sm/                      # Main package
│   ├── __main__.py                 # Module entry point
│   ├── core/                       # Core logic
│   │   ├── character_model.py      # Character data model with JSONPath binding
│   │   ├── importer.py             # Import logic with merge rules
│   │   ├── spec_loader.py          # UI spec loader
│   │   └── validator.py            # Data validation and filling
│   ├── ui/                         # UI components
│   │   ├── character_window.py     # Main character window
│   │   ├── import_window.py        # Import dialog
│   │   └── spec_renderer.py        # Widget renderer from spec
│   └── images/                     # Assets
│       └── portraits/              # Character portrait images
├── ui/
│   └── ui_spec.json               # UI specification
└── docs/
    └── charsheet_cass.json        # Example character data
```

## Usage

### Character Portraits

To add character portraits:

1. Place PNG, GIF, or JPG images in: `uesrpg_sm/images/portraits/`
2. Click "Select Portrait..." in the character window
3. Choose from available images

**Note:** PNG and GIF images work without any extra dependencies. For JPG/JPEG images, you need to install Pillow (`pip install Pillow`).

If no images are found, you'll see a message. The directory is created automatically.

### File Operations

- **New**: Create a new character (resets to default)
- **Open**: Load a character from JSON file
- **Save**: Save current character (prompts for location if new)
- **Save As**: Save character to a new file

All files are saved as UTF-8 encoded JSON with 2-space indentation.

### Import System

The Import feature allows you to load character data from external JSON files:

1. Go to **Import → Import Base Data...**
2. Click **Choose JSON...** to select a file (e.g., `docs/charsheet_cass.json`)
3. Review the preview showing name, race, birthsign, and skill count
4. Check **Overwrite existing fields** if you want to replace current data
   - **Unchecked** (default): Only fills empty/missing fields
   - **Checked**: Overwrites all fields from the source
5. Click **Import** to merge the data

The import uses a mapping defined in `ui_spec.json` to match source fields to character sheet fields. After import, the validator ensures all expected fields exist with proper structure.

### Supported Field Types

The spec-driven UI supports the following widget types:

- `entry`: Text input field
- `readonly_entry`: Read-only text field
- `textarea`: Multi-line text area
- `spin_int`: Integer spinner (with min/max)
- `check`: Checkbox
- `tags`: Comma-separated list of strings
- `int_list_csv`: Comma-separated list of integers
- `table`: Treeview table with add/delete (for skills, weapons, items, etc.)
- `table_inline`: Inline table (for characteristics, armor slots)

### Theme

The application uses the theme defined in `ui/ui_spec.json`:

- **Background**: `#FFD5AF` (light peach)
- **Foreground**: `#9D6E6B` (brown)
- **Headings**: Bold
- **Skills**: Italic (in Skills tables)

## Data Format

Character data is stored as JSON with a structure defined by `data.default_character` in the UI spec. Key sections include:

- Identity (name, race, size, XP)
- Birthsign and favored characteristics
- Characteristics (Str, End, Ag, Int, Wp, Prc, Prs, Lck)
- Derived stats (HP, MP, SP, etc.)
- Skills, weapons, armor
- Items, equipment, and currency
- Magic (rituals, spells)

## License

See LICENSE file for details.
