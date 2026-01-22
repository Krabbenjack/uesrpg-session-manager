# UI Spec Documentation - sheet_view Structure

This document explains the new `sheet_view` structure in `ui_spec.json` and how to customize the Character Sheet Dashboard layout.

## Overview

The `sheet_view` defines the primary Character Sheet Dashboard layout, which replaced the old two-column sidebar layout. It consists of three horizontal bands:

1. **Header**: Portrait and identity fields
2. **Core**: Core stats in a 3-column layout (always visible)
3. **Content**: Skills table and other primary content

## Basic Structure

```json
{
  "windows": [
    {
      "id": "character_window",
      "sheet_view": {
        "type": "sheet",
        "header": { ... },
        "core": { ... },
        "content": { ... }
      },
      "details_panel": {
        "type": "notebook",
        "tabs": [ ... ]
      }
    }
  ]
}
```

## Header Band

The header band typically contains:
- Portrait box (fixed 320×200)
- Identity fields (name, race, birthsign, etc.)

### Example

```json
"header": {
  "type": "layout_row",
  "widgets": [
    {
      "type": "portrait_box",
      "id": "portrait_display",
      "bind": "$.portrait.file",
      "size": [320, 200],
      "placeholder": "No portrait selected",
      "button_text": "Select Portrait…",
      "command": "select_portrait_from_dir"
    },
    {
      "type": "layout_col",
      "widgets": [
        {
          "type": "group",
          "title": "Identity",
          "layout": { "type": "grid", "columns": 4 },
          "widgets": [
            {
              "type": "field",
              "label": "Name",
              "bind": "$.name",
              "widget": "entry",
              "colspan": 2
            }
          ]
        }
      ]
    }
  ]
}
```

## Core Band

The core band displays critical stats in a multi-column layout. Uses `sheet_grid` for equal-width columns.

### Example

```json
"core": {
  "type": "sheet_grid",
  "columns": 3,
  "widgets": [
    {
      "type": "group",
      "title": "Attributes",
      "layout": { "type": "grid", "columns": 4 },
      "widgets": [ ... ]
    },
    {
      "type": "group",
      "title": "Derived Stats",
      "layout": { "type": "grid", "columns": 2 },
      "widgets": [ ... ]
    },
    {
      "type": "group",
      "title": "Combat Quick Block",
      "layout": { "type": "grid", "columns": 1 },
      "widgets": [ ... ]
    }
  ]
}
```

## Content Band

The content band displays scrollable content like skills tables.

### Example

```json
"content": {
  "type": "layout_col",
  "widgets": [
    {
      "type": "group",
      "title": "Skills",
      "layout": { "type": "grid", "columns": 1 },
      "widgets": [
        {
          "type": "table",
          "id": "skills_table_sheet",
          "bind": "$.skills",
          "columns": [ ... ],
          "row_editor": { ... }
        }
      ]
    }
  ]
}
```

## New Container Widget Types

### portrait_box

Displays a portrait image with fixed dimensions.

**Properties:**
- `bind`: Path to portrait file field (e.g., `"$.portrait.file"`)
- `size`: `[width, height]` array (e.g., `[320, 200]`)
- `placeholder`: Text to show when no portrait selected
- `button_text`: Text for the select button
- `command`: Command to execute on button click

**Example:**
```json
{
  "type": "portrait_box",
  "bind": "$.portrait.file",
  "size": [320, 200],
  "placeholder": "No portrait selected",
  "button_text": "Select Portrait…",
  "command": "select_portrait_from_dir"
}
```

**Rendering:**
- If Pillow is available: Displays actual image, scaled to fit (letterbox)
- Without Pillow: Shows filename as text
- Missing file: Shows placeholder text

### stat_block

Displays a single stat value with a label (for dashboard stat displays).

**Properties:**
- `label`: Label text (displayed above value)
- `bind`: Path to stat value (e.g., `"$.base_bonuses.SB"`)

**Example:**
```json
{
  "type": "stat_block",
  "label": "HP (cur)",
  "bind": "$.derived_stats.HP.current"
}
```

**Rendering:**
- Small label on top
- Large, bold entry field below
- Width: 6 characters
- Packs side-by-side with other stat_blocks

### sheet_grid

Multi-column container with equal-width columns.

**Properties:**
- `columns`: Number of columns (e.g., `3`)
- `widgets`: Array of child widgets (distributed across columns)

**Example:**
```json
{
  "type": "sheet_grid",
  "columns": 3,
  "widgets": [
    { "type": "group", "title": "Column 1", ... },
    { "type": "group", "title": "Column 2", ... },
    { "type": "group", "title": "Column 3", ... }
  ]
}
```

**Rendering:**
- Creates N equal-weight columns
- Distributes widgets row-by-row (first N widgets = row 1, etc.)
- Each column expands/shrinks equally on resize

### layout_row

Horizontal container (widgets side-by-side).

**Properties:**
- `widgets`: Array of child widgets

**Example:**
```json
{
  "type": "layout_row",
  "widgets": [
    { "type": "portrait_box", ... },
    { "type": "layout_col", ... }
  ]
}
```

**Rendering:**
- Each child packed side-by-side (pack side=LEFT)
- Children fill vertically (fill=BOTH)
- Each child expands equally (expand=True)

### layout_col

Vertical container (widgets stacked).

**Properties:**
- `widgets`: Array of child widgets

**Example:**
```json
{
  "type": "layout_col",
  "widgets": [
    { "type": "group", "title": "Group 1", ... },
    { "type": "group", "title": "Group 2", ... }
  ]
}
```

**Rendering:**
- Each child packed vertically (default pack behavior)
- Children fill horizontally (fill=BOTH)
- Children expand (expand=True)

## Details Panel

The `details_panel` replaces the old `main_panel`. It contains notebook tabs for secondary data.

### Structure

```json
"details_panel": {
  "type": "notebook",
  "tabs": [
    {
      "id": "tab_core",
      "title": "Core",
      "sections": [ ... ]
    },
    {
      "id": "tab_combat_skills",
      "title": "Combat & Skills",
      "sections": [ ... ]
    },
    {
      "id": "tab_gear",
      "title": "Gear",
      "sections": [ ... ]
    },
    {
      "id": "tab_magic",
      "title": "Magic",
      "sections": [ ... ]
    }
  ]
}
```

**Behavior:**
- Hidden by default
- Toggled via "Show Details" button
- Uses existing notebook tab rendering
- Contains same data as old tabs

## Customization Examples

### Example 1: Add a Field to Header

```json
"header": {
  "type": "layout_row",
  "widgets": [
    { "type": "portrait_box", ... },
    {
      "type": "layout_col",
      "widgets": [
        {
          "type": "group",
          "title": "Identity",
          "widgets": [
            { "type": "field", "label": "Name", "bind": "$.name", "widget": "entry" },
            { "type": "field", "label": "Level", "bind": "$.level", "widget": "spin_int", "min": 1, "max": 100 }
          ]
        }
      ]
    }
  ]
}
```

### Example 2: Add a Stat Block to Core

```json
"core": {
  "type": "sheet_grid",
  "columns": 3,
  "widgets": [
    {
      "type": "group",
      "title": "Attributes",
      "widgets": [
        { "type": "stat_block", "label": "Strength", "bind": "$.characteristics[0].score" },
        { "type": "stat_block", "label": "Endurance", "bind": "$.characteristics[1].score" }
      ]
    }
  ]
}
```

### Example 3: Add a Table to Content

```json
"content": {
  "type": "layout_col",
  "widgets": [
    {
      "type": "group",
      "title": "Custom Table",
      "widgets": [
        {
          "type": "table",
          "bind": "$.custom_data",
          "columns": [
            { "key": "name", "label": "Name", "width": 20 },
            { "key": "value", "label": "Value", "width": 10 }
          ],
          "row_editor": {
            "fields": [
              { "label": "Name", "key": "name", "widget": "entry" },
              { "label": "Value", "key": "value", "widget": "spin_int" }
            ],
            "buttons": ["add", "update", "delete"]
          }
        }
      ]
    }
  ]
}
```

### Example 4: Change Portrait Size

```json
{
  "type": "portrait_box",
  "bind": "$.portrait.file",
  "size": [400, 300],
  "placeholder": "No portrait",
  "button_text": "Choose Image",
  "command": "select_portrait_from_dir"
}
```

### Example 5: Four-Column Core Layout

```json
"core": {
  "type": "sheet_grid",
  "columns": 4,
  "widgets": [
    { "type": "group", "title": "Col 1", ... },
    { "type": "group", "title": "Col 2", ... },
    { "type": "group", "title": "Col 3", ... },
    { "type": "group", "title": "Col 4", ... }
  ]
}
```

## Best Practices

### Header Band
- Keep portrait on left for visual consistency
- Use `layout_col` for identity fields to stack them vertically
- Limit fields to most essential identity data

### Core Band
- Use 3-4 columns maximum (more becomes cramped)
- Group related stats together
- Use `stat_block` for numeric values that need quick reading
- Use `table_inline` for fixed-row data (like characteristics)

### Content Band
- Place most frequently accessed tables here (skills, inventory)
- Use `layout_col` to stack multiple sections vertically
- Keep tables with row editors here (Add/Edit/Delete buttons)

### Details Panel
- Move less frequently accessed data to tabs
- Group related data in sections within each tab
- Keep tab count to 4-6 for usability

## Migration from Old Spec

If you have a custom spec using the old `left_panel` + `main_panel` structure:

1. **Extract portrait from left_panel**
   - Move portrait widget to `sheet_view.header`
   - Change type from `image` to `portrait_box`

2. **Identify core stats from tabs**
   - Move characteristics, base bonuses, derived stats to `sheet_view.core`
   - Use `stat_block` for individual stats
   - Use `table_inline` for characteristics table

3. **Move primary tables to content**
   - Skills table → `sheet_view.content`
   - Keep full skills table with row editor

4. **Rename main_panel**
   - Rename `main_panel` to `details_panel`
   - Keep all existing tabs intact

5. **Update bindings**
   - Ensure all bind paths remain the same
   - Verify default_character structure unchanged

## Troubleshooting

### Portrait not displaying image
- Check Pillow is installed: `pip show Pillow`
- Verify image file exists at path
- Check file format is supported (PNG, JPG, GIF)

### Layout looks cramped
- Reduce number of columns in `sheet_grid`
- Reduce number of stat_blocks per row
- Increase window size or min_size

### Fields not saving
- Verify bind paths are correct
- Check default_character has corresponding fields
- Use `get_state()` to debug data extraction

### Tabs not showing
- Ensure `details_panel` is defined
- Click "Show Details" button
- Check browser console for errors

## Reference

### Full Character Window Structure

```json
{
  "id": "character_window",
  "type": "main",
  "title": "Character",
  "sheet_view": {
    "type": "sheet",
    "header": { "type": "layout_row", "widgets": [...] },
    "core": { "type": "sheet_grid", "columns": 3, "widgets": [...] },
    "content": { "type": "layout_col", "widgets": [...] }
  },
  "details_panel": {
    "type": "notebook",
    "tabs": [...]
  }
}
```

### Supported Field Types in sheet_view

All existing field types work within sheet_view containers:
- `field` with widgets: entry, textarea, spin_int, check, tags, int_list_csv
- `table` with row_editor
- `table_inline` for fixed rows
- `group` for nested containers
- `portrait_box`, `stat_block` (new)
- `layout_row`, `layout_col`, `sheet_grid` (new containers)
