# UI Behavior Documentation: Read-Only Bonus Column

## Overview
The bonus column in the characteristics table is now read-only, automatically computed from the score column using the formula: `bonus = floor(score / 10)` (tens digit).

## Visual Representation

### Before (Editable Bonus)
```
┌────────────────────────────────────────┐
│ Attributes                              │
├──────┬───────┬───────┬─────────────────┤
│ Abbr │ Score │ Bonus │ Fav             │
├──────┼───────┼───────┼─────────────────┤
│ Str  │  45   │  [4]  │ ☐               │  ← Bonus was editable
│ End  │  52   │  [5]  │ ☐               │  ← User could change it
│ Ag   │  38   │  [3]  │ ☐               │  ← Causing inconsistency
│ Int  │  60   │  [6]  │ ☑               │
│ Wp   │  42   │  [4]  │ ☐               │
│ Prc  │  35   │  [3]  │ ☐               │
│ Prs  │  28   │  [2]  │ ☐               │
│ Lck  │  55   │  [5]  │ ☐               │
└──────┴───────┴───────┴─────────────────┘
```

### After (Read-Only Bonus)
```
┌────────────────────────────────────────┐
│ Attributes                              │
├──────┬───────┬───────┬─────────────────┤
│ Abbr │ Score │ Bonus │ Fav             │
├──────┼───────┼───────┼─────────────────┤
│ Str  │  45   │   4   │ ☐               │  ← Bonus is read-only
│ End  │  52   │   5   │ ☐               │  ← Automatically computed
│ Ag   │  38   │   3   │ ☐               │  ← Always consistent
│ Int  │  60   │   6   │ ☑               │
│ Wp   │  42   │   4   │ ☐               │
│ Prs  │  28   │   2   │ ☐               │
│ Prc  │  35   │   3   │ ☐               │
│ Lck  │  55   │   5   │ ☐               │
└──────┴───────┴───────┴─────────────────┘
```

## User Interaction Flow

### Step 1: User Enters Score
```
User types in Score field: 45 → Str score = 45
```

### Step 2: On Focus Out (or Tab/Enter)
```
1. UI calls _recompute_derived_stats (with 300ms debounce)
2. Gets current state from all widgets
3. Calls apply_derived_stats(state)
4. Engine computes: bonus = floor(45/10) = 4
5. UI calls set_state with updated state
6. Bonus field automatically updates to 4
```

### Step 3: Bonus Field is Read-Only
```
┌────────────────────┐
│ Str │  45  │   4   │  ← Try to click bonus field
└─────┴──────┴───────┘
                  ↑
                  No cursor appears
                  Field is greyed out (readonly state)
                  Value cannot be changed by user
```

## Technical Implementation

### UI Spec Configuration
```json
{
  "columns": [
    { "key": "abbr", "label": "Abbr", "width": 6, "readonly": true },
    { "key": "score", "label": "Score", "width": 6 },
    { "key": "bonus", "label": "Bonus", "width": 6, "readonly": true },
    { "key": "favored", "label": "Fav", "width": 4, "widget": "check" }
  ]
}
```

### UI Rendering (ui.py)
```python
# When creating entry widget
widget = ttk.Entry(frame, width=width)
widget.insert(0, str(row_data.get(col_key, '')))

if readonly:
    widget.config(state='readonly')  # ← Makes field read-only
```

### Recompute Flow
```python
def _recompute_derived_stats(self, event=None):
    # Called when score is edited
    current_state = self.get_state()
    self.set_state(current_state)  # ← Triggers apply_derived_stats

def set_state(self, state):
    state = apply_derived_stats(state)  # ← Computes bonuses
    # Update all widgets, including readonly ones
```

## Benefits

### 1. Data Consistency
- Bonus is always correct: `bonus = floor(score / 10)`
- No manual errors or typos
- System-computed values are reliable

### 2. User Experience
- Clear visual indication (readonly styling)
- Automatic updates on score change
- No need to calculate manually

### 3. Data Integrity
- Prevents corruption of computed values
- Export/import maintains consistency
- Load/save preserves correct relationships

## Test Verification

### Automated Tests
```
✅ Bonus column marked readonly in UI spec
✅ UI code renders readonly fields correctly
✅ Recompute automatically updates bonus values
✅ Current pools protected (HP, MP, etc.)
✅ All roundtrip tests pass
```

### Manual Test Steps
1. Start app: `python3 main.py`
2. Create new character
3. Enter Str score: 45
4. Verify bonus shows: 4
5. Try to edit bonus: Field should be disabled
6. Change score to 52
7. Verify bonus updates to: 5
8. Save and reload character
9. Verify bonus is still correct: 5

## Logging

### Normal Operation (Default Config)
```
INFO: Loaded derived stats rules from .../config/attributes_derived.json
```

### Fallback Mode (Config Missing)
```
WARNING: Using legacy derived ruleset: core/mechanics/derived_stats_v1.json. 
         Consider moving rules to config/attributes_derived.json
INFO: Loaded derived stats rules from .../core/mechanics/derived_stats_v1.json
```

## Summary

The implementation ensures:
- ✅ Bonus values are always computed correctly
- ✅ Users cannot accidentally edit computed values
- ✅ UI clearly indicates read-only fields
- ✅ Automatic updates on score changes
- ✅ No breaking changes to existing saves
- ✅ Full backward compatibility maintained
