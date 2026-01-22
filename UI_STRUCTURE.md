# Character Window UI - Visual Structure

This document shows the visual structure of the dynamically generated UI.

## New Character Sheet Dashboard (Primary View)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ UESRPG Session Manager                                          [_][□][×]│
├─────────────────────────────────────────────────────────────────────────┤
│ File  Import                                                             │
│  ├─ New                                                                  │
│  ├─ Open…                                                               │
│  ├─ Save                                                                 │
│  ├─ Save As…                                                            │
│  ├─────────                                                              │
│  └─ Exit                                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ ╔═══════════════════════ HEADER BAND ══════════════════════════════════╗│
│ ║ ┌──────────────────┐  ╔════════════════════════════════════════════╗ ║│
│ ║ │ Portrait         │  ║ Identity                                   ║ ║│
│ ║ │                  │  ║ ┌────────────┬────────┬────────┬─────────┐ ║ ║│
│ ║ │   320 × 200      │  ║ │ Name:      │ Race:  │ Size:  │         │ ║ ║│
│ ║ │                  │  ║ │ [Entry]    │[Entry] │[Entry] │         │ ║ ║│
│ ║ │   (always        │  ║ ├────────────┴────────┴────────┴─────────┤ ║ ║│
│ ║ │    visible)      │  ║ │ Birthsign (category): [Entry]          │ ║ ║│
│ ║ │                  │  ║ │ Birthsign (sign): [Entry] ☐ Star-Cursed│ ║ ║│
│ ║ └──────────────────┘  ║ │ Elite Adv.: [Entry]                    │ ║ ║│
│ ║ [Select Portrait…]    ║ │ XP (cur): [___]  XP (tot): [___]       │ ║ ║│
│ ║                       ║ └────────────────────────────────────────┘ ║ ║│
│ ║                       ╚════════════════════════════════════════════╝ ║│
│ ╚═══════════════════════════════════════════════════════════════════════╝│
│ ╔═══════════════════════ CORE BAND (3 Columns) ════════════════════════╗│
│ ║ ┌────────────────┐ ┌──────────────────┐ ┌────────────────────────┐ ║│
│ ║ │ Attributes     │ │ Derived Stats    │ │ Combat Quick Block     │ ║│
│ ║ ├────┬───┬───┬──┤ ├────┬─────┬───────┤ ├────────────────────────┤ ║│
│ ║ │Abbr│Sco│Bon│Fv││ │ HP │ MP  │ WT    │ │ Armor (Head/Body/Leg)  │ ║│
│ ║ ├────┼───┼───┼──┤│ │(cur│(cur)│(cur)  │ │ ┌────┬──┬───┐          │ ║│
│ ║ │Str │[_]│[_]│[]││ │max)│(max)│(max)  │ │ │Head│AR│ENC│          │ ║│
│ ║ │End │[_]│[_]│[]││ ├────┼─────┼───────┤ │ │Body│AR│ENC│          │ ║│
│ ║ │Ag  │[_]│[_]│[]││ │ SP │ LP  │ Speed │ │ │Leg │AR│ENC│          │ ║│
│ ║ │Int │[_]│[_]│[]││ │(cur│(cur)│       │ │ └────┴──┴───┘          │ ║│
│ ║ │Wp  │[_]│[_]│[]││ │max)│(max)│       │ │                        │ ║│
│ ║ │Prc │[_]│[_]│[]││ ├────┼─────┼───────┤ │ Combat Style:          │ ║│
│ ║ │Prs │[_]│[_]│[]││ │ IR │ AP  │ Ling. │ │ [Entry]                │ ║│
│ ║ │Lck │[_]│[_]│[]││ │    │(cur)│       │ │                        │ ║│
│ ║ └────┴───┴───┴──┘│ │    │(max)│       │ │                        │ ║│
│ ║                  │ ├────┼─────┼───────┤ │                        │ ║│
│ ║ Base Bonuses     │ │ENC │ENC  │  CR   │ │                        │ ║│
│ ║ SB EB AB IB WB   │ │(cur│(max)│       │ │                        │ ║│
│ ║ [_][_][_][_][_]  │ └────┴─────┴───────┘ │                        │ ║│
│ ║ PcB PsB LB       │                      │                        │ ║│
│ ║ [_] [_] [_]      │                      │                        │ ║│
│ ║                  │                      │                        │ ║│
│ ║                  │                      │                        │ ║│
│ └──────────────────┘ └──────────────────┘ └────────────────────────┘ ║│
│ ╚═══════════════════════════════════════════════════════════════════════╝│
│ ╔═══════════════════════ CONTENT BAND ═════════════════════════════════╗│
│ ║ ┌─────────────────────────────────────────────────────────────────┐ ║│
│ ║ │ Skills                                                          │ ║│
│ ║ ├──────────────────────┬──────┬───────┬────┐                     │ ║│
│ ║ │ Skill                │ Rank │ Bonus │ TN │                     │ ║│
│ ║ ├──────────────────────┼──────┼───────┼────┤                     │ ║│
│ ║ │ Athletics (Ag, End)  │ N    │ +25   │ 50 │                     │ ║│
│ ║ │ Smithing (Str, End)  │ A    │ +35   │ 60 │                     │ ║│
│ ║ │ ...                  │ ...  │ ...   │... │                     │ ║│
│ ║ └──────────────────────┴──────┴───────┴────┘                     │ ║│
│ ║ [Add] [Edit] [Delete]                                            │ ║│
│ ╚═══════════════════════════════════════════════════════════════════════╝│
├─────────────────────────────────────────────────────────────────────────┤
│ ▶ Show Details (Gear, Magic, Notes...)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ Ready                                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

## Details Panel (Secondary View - Toggled)

When "Show Details" is clicked, the notebook tabs expand below:

```
├─────────────────────────────────────────────────────────────────────────┤
│ ▼ Hide Details (Gear, Magic, Notes...)                                 │
├─────────────────────────────────────────────────────────────────────────┤
│ ┌─ Core ──┬─ Combat & Skills ─┬─ Gear ─┬─ Magic ─┐                    │
│ │                                                                        │
│ │ [Tab content with sections...]                                        │
│ │                                                                        │
│ └────────────────────────────────────────────────────────────────────────│
```

## Details Tab Structure

### Tab 1: Core
- Header (Name, Size, XP, Race, Elite Adv, Birthsign, Favored, Lucky Numbers)
- Characteristics (8 rows: Str, End, Ag, Int, Wp, Prc, Prs, Lck)
- Base Bonuses (SB, EB, AB, IB, WB, PcB, PsB, LB)
- Attributes (HP, MP, WT, SP, Speed, LP, IR, AP, Linguistics, ENC, CR)
- Languages & Bonds
- Wounds / Conditions / Size

### Tab 2: Combat & Skills
- Armor (6 slots: Head, Body, Right Leg, Left Leg, Right Arm, Left Arm)
- Shield (BR, Type, ENC)
- Armor Notes
- Skills Table (with Add/Edit/Delete)
- Professions / Custom Skills
- Combat Style
- Specializations
- Melee Weapons Table
- Ranged Weapons Table

### Tab 3: Gear
- Talents, Traits, & Powers (large textarea)
- Items & Equipment Table (with Add/Edit/Delete)
- Total ENC
- Drakes (money)

### Tab 4: Magic
- Rituals (textarea)
- Magic Skills Table (7 default skills: Alteration, Conjuration, Destruction, Illusion, Mysticism, Necromancy, Restoration)
- Spellcasting (textarea)
- Spells Table (with Add/Edit/Delete)
- Specializations (textarea)

## New Container Widgets

### Stat Block
```
  Label
 ┌─────┐
 │ 100 │  ← Large value (bold)
 └─────┘
```

### Portrait Box
```
┌──────────────────┐
│  Portrait        │
│                  │
│    320 × 200     │
│                  │
│  (fixed size)    │
└──────────────────┘
[Select Portrait…]
```

### Layout Row (Horizontal)
```
┌─────────┐ ┌─────────┐ ┌─────────┐
│ Widget1 │ │ Widget2 │ │ Widget3 │
└─────────┘ └─────────┘ └─────────┘
```

### Layout Col (Vertical)
```
┌─────────┐
│ Widget1 │
├─────────┤
│ Widget2 │
├─────────┤
│ Widget3 │
└─────────┘
```

### Sheet Grid (N columns)
```
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Column 1 │ │ Column 2 │ │ Column 3 │
│          │ │          │ │          │
└──────────┘ └──────────┘ └──────────┘
```

## Widget Examples

### Entry Field
```
Label: [Entry widget               ]
```

### Spinbox
```
Label: [▼ 0 ▲]
```

### Checkbox
```
☐ Label
```

### Textarea
```
Label:
┌────────────────────────────────┐
│                                │
│                                │
│                                │
└────────────────────────────────┘
```

### Tags (comma-separated list)
```
Label: [tag1, tag2, tag3          ]
       comma-separated
```

### Table with Controls
```
┌───────────────────────────────────────┐
│ Column1  │ Column2  │ Column3         │
├──────────┼──────────┼─────────────────┤
│ Value1   │ Value2   │ Value3          │
│ Value4   │ Value5   │ Value6          │
└───────────────────────────────────────┘
[Add] [Edit] [Delete]
```

### Inline Table (fixed rows)
```
        AR   ENC   Type
Head(0)  [_]  [_]  [____________]
Body(1-5)[_]  [_]  [____________]
R.Leg(6) [_]  [_]  [____________]
L.Leg(7) [_]  [_]  [____________]
R.Arm(8) [_]  [_]  [____________]
L.Arm(9) [_]  [_]  [____________]
```

## Color Theme

From ui_spec.json:
- Background: #FFD5AF (light peachy tan)
- Foreground: #9D6E6B (muted brown)
- Border: #9D6E6B (muted brown)
- Panel Background: #FFD5AF (light peachy tan)
- Accent: #9D6E6B (muted brown)

## Key Features Visible in UI

1. **Character Sheet Dashboard**: Portrait header + core stats + skills (always visible)
2. **No sidebar**: Portrait moved to header (320×200 fixed size)
3. **Details toggle**: Show/hide button for notebook tabs (Gear, Magic, Notes)
4. **Three-band layout**: Header / Core / Content structure
5. **Stat blocks**: Large values with small labels for quick reading
6. **Sections**: Each band has labeled containers
7. **Mixed widgets**: Entry, spinbox, checkbox, textarea, tags, tables, stat blocks
8. **Scrolling**: Main content area scrolls vertically
9. **Status bar**: Shows current status at bottom
10. **Menu bar**: File and Import menus
11. **Consistent spacing**: 8px horizontal, 6px vertical padding
12. **Resizable window**: Minimum 980x640, default 1100x720
13. **Dynamic generation**: All from ui_spec.json!

## Data Flow

```
User Input → Widget → get_state() → Python Dict → save_character() → JSON File
                                                                          ↓
                                                                       (UTF-8)
                                                                          ↓
JSON File → load_character() → Python Dict → set_state() → Widget → Display
```

## File Operations

- **New**: Loads default_character from spec
- **Open**: File dialog → Load JSON → Apply to widgets
- **Save**: Get state from widgets → Save JSON with indent=2
- **Save As**: Same as Save but with new filename

All file operations use UTF-8 encoding and proper error handling.
