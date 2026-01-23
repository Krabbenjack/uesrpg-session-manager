# UI Changes Visual Guide

## Before and After Comparison

### Navigation Changes

**BEFORE (Toggle Button)**:
```
┌─────────────────────────────────────────┐
│ Menu Bar                                │
├─────────────────────────────────────────┤
│ [Portrait] [Identity Fields]            │
│ Attributes | Derived | Combat            │
│ Skills Table                             │
├─────────────────────────────────────────┤
│ [▶ Show Details] Button                 │
│ (Details hidden by default)              │
└─────────────────────────────────────────┘
```

**AFTER (Tabbed Interface)**:
```
┌─────────────────────────────────────────┐
│ Menu Bar                                │
├─────────────────────────────────────────┤
│ [Sheet] [Details]  ← Top-level tabs     │
├─────────────────────────────────────────┤
│ Sheet tab:                               │
│   [Portrait] [Identity Fields]           │
│   Attributes | Derived | Combat          │
│   Skills Table                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Menu Bar                                │
├─────────────────────────────────────────┤
│ [Sheet] [Details]  ← Top-level tabs     │
├─────────────────────────────────────────┤
│ Details tab:                             │
│   [Core] [Combat] [Gear] [Magic]        │
│   │ Identity Fields (Name, Race, etc.)  │
│   │ Characteristics Table                │
│   │ Base Bonuses (readonly)              │
│   │ Derived Stats (readonly)             │
└─────────────────────────────────────────┘
```

### Read-Only Derived Stats

**BEFORE**:
```
┌─────────────────┐
│ HP (max) [____] │ ← Editable (incorrect)
│ MP (max) [____] │ ← Editable (incorrect)
│ Speed    [____] │ ← Editable (incorrect)
└─────────────────┘
```

**AFTER**:
```
┌─────────────────┐
│ HP (max) [░░50] │ ← Readonly (grayed out)
│ MP (max) [░░40] │ ← Readonly (grayed out)
│ Speed    [░░12] │ ← Readonly (grayed out)
└─────────────────┘
```

### Identity Field Behavior

**BEFORE (Overwrites)**:
```
Header:     Name [John] ─┐
Details:    Name [Jane] ─┤→ Only last widget registered
                         │   (one overwrites the other)
                         └→ Data inconsistency
```

**AFTER (Multi-Widget Binding)**:
```
Header:     Name [John] ─┐
Details:    Name [John] ─┤→ Both widgets bound to $.name
                         │   All update together
Edit Header → Both update instantly
Edit Details → Both update instantly
Save → First non-empty value used
```

### Characteristic Score Auto-Update

**BEFORE**:
```
1. Edit Strength: 50 → 60
2. Derived stats: [Old values remain]
3. User must reload or recalculate manually
```

**AFTER**:
```
1. Edit Strength: 50 → 60
2. Click outside field (FocusOut)
3. [300ms debounce]
4. Derived stats: [Automatically updated!]
   - SB: 5 → 6
   - HP max: 50 → 60
   - ENC max: 100 → 120
```

### Details Page Layout

**Goal**: Vertical flow, no horizontal scrollbars

```
┌─────────────────────────────────────────┐
│ Details Tab                              │
│ ┌──[Core]──[Combat]──[Gear]──[Magic]──┐ │
│ │                                       │ │
│ │ Section 1: Identity                   │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ Name, Race, Size, etc.          │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │                                       │ │
│ │ Section 2: Characteristics            │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ Abbr | Score | Bonus | Fav      │ │ │
│ │ │ Str  |  50   |  5    | [x]      │ │ │
│ │ │ End  |  40   |  4    | [ ]      │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │                                       │ │
│ │ Section 3: Base Bonuses (readonly)    │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ SB=5  EB=4  AB=3  IB=5  ...     │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │                                       │ │
│ │ Section 4: Derived Stats (readonly)   │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ HP=50  MP=40  WT=100  SP=25     │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │                                       │ │
│ │ [Vertical scroll if needed] │       │ │
│ └───────────────────────────────────┘ │ │
└─────────────────────────────────────────┘
   ▲ No horizontal scroll needed
```

## User Workflow Examples

### Example 1: Creating a New Character

```
1. File → New
2. Enter Name in header → Updates in Details/Core automatically
3. Enter Race, Size, etc.
4. Switch to Details tab
5. Edit Characteristic scores (Str, End, etc.)
6. Tab out → Derived stats update automatically
7. View computed HP, MP, Speed, etc. (readonly)
8. File → Save
```

### Example 2: Editing Existing Character

```
1. File → Open
2. Switch to Details tab
3. Edit Strength: 50 → 60
4. Click outside field
5. Watch derived stats update:
   - SB: 5 → 6 (readonly, auto-updated)
   - HP max: 50 → 60 (readonly, auto-updated)
   - ENC max: 100 → 120 (readonly, auto-updated)
6. File → Save
```

### Example 3: Import/Merge Character Data

```
1. Have character loaded
2. File → Import Character Data
3. Select JSON file
4. Review preview
5. Choose merge or overwrite
6. Click Import
7. Derived stats recompute automatically
8. All identity fields update in all locations
```

## Keyboard Shortcuts

- **Ctrl+N**: New character
- **Ctrl+O**: Open character
- **Ctrl+S**: Save character
- **Tab**: Navigate between fields
- **Ctrl+Tab**: Switch between Sheet/Details tabs (system default)

## Visual Indicators

### Read-Only Fields
- Grayed out background
- Cannot click to edit
- Display computed values

### Editable Fields
- White background
- Click to edit
- Accept user input

### Multi-Bound Fields
- No visual difference
- All instances update together
- Edit any instance to update all

## Error Prevention

### What You CAN'T Do (And Why)

❌ **Edit Derived Stats**: Prevents data corruption from manual edits  
❌ **Edit Base Bonuses**: Automatically computed from characteristics  
❌ **Have Drifting Identity Data**: All instances bound to same source  

### What You CAN Do

✅ **Edit Characteristics**: Changes trigger automatic recalculation  
✅ **Edit Name Anywhere**: Updates all locations instantly  
✅ **Import/Export**: Preserves all data correctly  
✅ **Rapid Edits**: Debouncing prevents lag  

## Technical Notes

### For Developers

1. **Multi-Widget Binding**: See `_register_widget()` in `ui.py`
2. **Read-Only Logic**: Check bind path prefix in widget creation
3. **Recomputation**: See `_recompute_derived_stats()` with debouncing
4. **Event Binding**: FocusOut on characteristic score fields
5. **State Management**: `get_state()` and `set_state()` handle lists

### For Users

- Changes are saved when you use File → Save
- Import preserves existing data unless overwrite is checked
- Derived stats update when you tab out of characteristic fields
- All identity fields are synchronized automatically
- You cannot accidentally corrupt derived statistics

## Summary of Benefits

1. ✅ **No Data Loss**: Multi-widget binding prevents overwrites
2. ✅ **Automatic Updates**: Derived stats refresh on edit
3. ✅ **Error Prevention**: Read-only fields protect computed values
4. ✅ **Better Navigation**: Two-tab interface is more intuitive
5. ✅ **Consistent State**: Identity fields work uniformly
6. ✅ **Performance**: Debouncing prevents excessive computation
7. ✅ **Vertical Layout**: Details page scrolls naturally without horizontal bar
