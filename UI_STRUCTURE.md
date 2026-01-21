# Character Window UI - Visual Structure

This document shows the visual structure of the dynamically generated UI.

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
├─────────┬───────────────────────────────────────────────────────────────┤
│         │ ┌─ Core ──┬─ Combat & Skills ─┬─ Gear ─┬─ Magic ─┐           │
│ ┌───────┴─┴─────────┴───────────────────┴────────┴─────────┘           │
│ │ Portrait      │                                                        │
│ │               │ ╔═══════════════════════════════════════════════════╗ │
│ │  ┌─────────┐  │ ║ Header                                            ║ │
│ │  │ No      │  │ ║ ┌─────────────┬───────┬────────────┬────────────┐ ║ │
│ │  │ portrait│  │ ║ │ Name:       │ Size: │ XP (cur):  │ XP (tot):  │ ║ │
│ │  │ selected│  │ ║ │ [Entry]     │[Entry]│ [Spinbox]  │ [Spinbox]  │ ║ │
│ │  │         │  │ ║ ├─────────────┴───────┴────────────┴────────────┤ ║ │
│ │  └─────────┘  │ ║ │ Race: [Entry]  Elite Adv: [Entry]             │ ║ │
│ │               │ ║ │ Birthsign (category): [Entry]                  │ ║ │
│ │ [Select       │ ║ │ Birthsign (sign): [Entry]  ☐ Star-Cursed      │ ║ │
│ │  Portrait…]   │ ║ │ Favored: [Tags] Lucky #s: [CSV] Unlucky: [CSV]│ ║ │
│ │               │ ║ └────────────────────────────────────────────────┘ ║ │
│ │ Put images    │ ╠═══════════════════════════════════════════════════╣ │
│ │ into assets/  │ ║ Characteristics                                   ║ │
│ │ portraits     │ ║ ┌────┬───────┬───────┬─────┐                      ║ │
│ │ (png/jpg/gif) │ ║ │Abbr│ Score │ Bonus │ Fav │                      ║ │
│ │               │ ║ ├────┼───────┼───────┼─────┤                      ║ │
│ └───────────────┘ ║ │Str │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │End │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Ag  │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Int │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Wp  │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Prc │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Prs │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ │Lck │ [___] │ [___] │ [ ] │                      ║ │
│                   ║ └────┴───────┴───────┴─────┘                      ║ │
│                   ║                                                    ║ │
│                   ║ SB EB AB IB WB PcB PsB LB                         ║ │
│                   ║ [0][0][0][0][0][0] [0] [0]                        ║ │
│                   ╠═══════════════════════════════════════════════════╣ │
│                   ║ Attributes                                        ║ │
│                   ║ HP(cur)[__] HP(max)[__] MP(cur)[__] MP(max)[__]  ║ │
│                   ║ WT(cur)[__] WT(max)[__] SP(cur)[__] SP(max)[__]  ║ │
│                   ║ Speed[__]  LP(cur)[__]  LP(max)[__]  IR[__]      ║ │
│                   ║ AP(cur)[__] AP(max)[__] Linguistics[__] ENC[__]  ║ │
│                   ║ ENC(max)[__]  CR[__]                              ║ │
│                   ╠═══════════════════════════════════════════════════╣ │
│                   ║ Languages & Bonds                                 ║ │
│                   ║ Languages: [Tags - comma-separated]               ║ │
│                   ║ Bonds: [Tags - comma-separated]                   ║ │
│                   ╠═══════════════════════════════════════════════════╣ │
│                   ║ Wounds / Conditions / Size                        ║ │
│                   ║ ┌──────────────┬──────────────┬──────────────┐    ║ │
│                   ║ │ Wounds       │ Conditions   │ Size         │    ║ │
│                   ║ │ [          ] │ [          ] │ [Entry]      │    ║ │
│                   ║ │ [Textarea  ] │ [Textarea  ] │              │    ║ │
│                   ║ │ [          ] │ [          ] │              │    ║ │
│                   ║ └──────────────┴──────────────┴──────────────┘    ║ │
│                   ╚═══════════════════════════════════════════════════╝ │
│                   ▲                                                      │
│                   ║  [Scrollable Content]                               │
│                   ▼                                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ Ready                                                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

## Tab Structure

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

1. **Two-column layout**: Portrait panel (left) + Main content (right)
2. **Tabbed interface**: 4 tabs for organized content
3. **Sections**: Each tab has multiple labeled sections
4. **Mixed widgets**: Entry, spinbox, checkbox, textarea, tags, tables
5. **Scrolling**: Main content area scrolls vertically
6. **Status bar**: Shows current status at bottom
7. **Menu bar**: File and Import menus
8. **Consistent spacing**: 8px horizontal, 6px vertical padding
9. **Resizable window**: Minimum 980x640, default 1100x720
10. **Dynamic generation**: All from ui_spec.json!

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
