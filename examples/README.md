# Dash Glide Grid Examples

This directory contains examples demonstrating the features of `dash-glide-grid`.

## Running Examples

```bash
python examples/01_basic_grid.py
```

Then open http://localhost:8050 in your browser.

## Examples

### Getting Started

| # | Example | Description |
|---|---------|-------------|
| 01 | [basic_grid.py](01_basic_grid.py) | Simple read-only grid displaying data |
| 02 | [editable_grid.py](02_editable_grid.py) | Cell editing with event callbacks |
| 03 | [custom_theme.py](03_custom_theme.py) | Dark and light theme customization |
| 04 | [large_dataset.py](04_large_dataset.py) | Performance with 10,000+ rows |

### Cell Types

| # | Example | Description |
|---|---------|-------------|
| 05 | [all_cell_types.py](05_all_cell_types.py) | All supported cell types: text, number, boolean, markdown, uri, image, bubble, drilldown, rowid, protected, loading |
| 06 | [custom_cells.py](06_custom_cells.py) | Custom cell rendering |

### Data Entry Features

| # | Example | Description |
|---|---------|-------------|
| 07 | [fill_handle_example.py](07_fill_handle_example.py) | Excel-like drag-to-fill functionality |
| 13 | [fill_directions.py](13_fill_directions.py) | Control fill handle direction |
| 19 | [trailing_row.py](19_trailing_row.py) | Add new rows via trailing row |
| 22 | [persistent_editable_grid.py](22_persistent_editable_grid.py) | Persist edits with session storage |
| 32 | [edit_on_type.py](32_edit_on_type.py) | Start editing by typing |
| 37 | [undo_redo.py](37_undo_redo.py) | Undo/redo support (Cmd+Z, Cmd+Shift+Z) |
| 39 | [copy_paste.py](39_copy_paste.py) | Copy/paste cells, including from Excel |

### Layout & Structure

| # | Example | Description |
|---|---------|-------------|
| 08 | [merged_cells_example.py](08_merged_cells_example.py) | Horizontal cell merging with span property |
| 09 | [grouped_columns_example.py](09_grouped_columns_example.py) | Organize columns under group headers |
| 10 | [frozen_trailing_rows.py](10_frozen_trailing_rows.py) | Freeze rows at the bottom |
| 11 | [column_constraints.py](11_column_constraints.py) | Min/max column widths and resize behavior |
| 12 | [row_markers.py](12_row_markers.py) | Row markers: numbers, checkboxes, etc. |

### Events & Interaction

| # | Example | Description |
|---|---------|-------------|
| 14 | [header_events.py](14_header_events.py) | Header click and context menu events |
| 15 | [cell_events.py](15_cell_events.py) | Cell click, double-click, and context menu |
| 30 | [row_hover.py](30_row_hover.py) | Row hover highlighting |
| 31 | [cell_activation_behavior.py](31_cell_activation_behavior.py) | Control cell activation modes |
| 34 | [trap_focus.py](34_trap_focus.py) | Keep keyboard focus within grid |
| 35 | [scroll_to_active_cell.py](35_scroll_to_active_cell.py) | Auto-scroll to active cell |

### Selection & Navigation

| # | Example | Description |
|---|---------|-------------|
| 16 | [visible_region.py](16_visible_region.py) | Track visible row/column region |
| 17 | [row_column_reordering.py](17_row_column_reordering.py) | Drag to reorder rows and columns |
| 18 | [highlight_regions.py](18_highlight_regions.py) | Highlight specific cell regions |
| 20 | [scroll_control.py](20_scroll_control.py) | Programmatic scroll control |
| 33 | [range_selection_column_spanning.py](33_range_selection_column_spanning.py) | Range selection across columns |
| 36 | [column_selection_mode.py](36_column_selection_mode.py) | Select entire columns |

### Data Processing

| # | Example | Description |
|---|---------|-------------|
| 23 | [cell_validation.py](23_cell_validation.py) | Client-side cell validation |
| 24 | [value_formatter.py](24_value_formatter.py) | Format display values |
| 25 | [search_example.py](25_search_example.py) | Built-in search functionality |
| 26 | [filter_example.py](26_filter_example.py) | Filter data rows |
| 27 | [sorting_example.py](27_sorting_example.py) | Sort by columns |
| 28 | [column_filter_example.py](28_column_filter_example.py) | Column-specific filters |
| 29 | [text_wrapping_example.py](29_text_wrapping_example.py) | Wrap long text in cells |

### Advanced

| # | Example | Description |
|---|---------|-------------|
| 21 | [advanced_features.py](21_advanced_features.py) | Combined advanced features |