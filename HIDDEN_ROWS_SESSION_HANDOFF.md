# Hidden Rows Edge Cases - Session Handoff

## Branch
`feature/hidden-rows-edge-cases` (based on `feature/hidden-rows`)

## What Was Completed

### Edge Case Fixes in `src/lib/fragments/GlideGrid.react.js`:
1. **Tab navigation** - Skip hidden rows in `getNextCellWithWrapping()` (~line 4403)
2. **Arrow key navigation** - Capture phase listener to skip hidden rows (~line 4635)
3. **Fill handle** - Skip hidden rows + `event.preventDefault()` to stop Glide's default (~line 2914)
4. **Delete** - Skip hidden rows in `handleDelete()` (~line 3832)
5. **Copy** - `getCellsForSelectionFiltered()` excludes hidden rows (~line 4660)
6. **Focus guard** - Move focus to nearest visible row in `filteredGridSelection` (~line 4647)
7. **Context menu** - Ignore right-click on hidden rows (~line 3634)

### Example Updates in `examples/65_hidden_rows.py`:
- Added `update_tree_cells_only()` to preserve edits on tree toggle
- Made Name column readonly to prevent fill corrupting tree-view-cells
- Added simple "Hide Rows 3-5" / "Show All" buttons for testing

## Fixed Bug

**Tree toggle gets stuck after fill operation:** ✅ FIXED

**Root cause:** The data sync guard in `useEffect` was blocking legitimate Python callback updates. After a fill operation set `lastSentData.current`, subsequent Python callback returns that happened to match this data would be incorrectly skipped.

**Fix:** Clear `lastSentData.current` after matching it in the sync guard, so stale data doesn't block future updates. (Line ~609 in GlideGrid.react.js)

## Future Enhancement Discussed

User suggested a `hiddenRowsConfig` prop to control behavior:
```python
GlideGrid(
    hiddenRows=[3, 4, 5],
    hiddenRowsConfig={
        "skipOnNavigation": True,      # default True
        "excludeFromCopy": True,       # default True
        "excludeFromFill": True,       # default True
        "excludeFromDelete": True,     # default True
    }
)
```

## How to Test

```bash
cd /Users/ben/GitHub/dash-glide-grid
python examples/65_hidden_rows.py
# Open http://127.0.0.1:8065
```

## Files Modified
- `src/lib/fragments/GlideGrid.react.js` - Main edge case fixes
- `examples/65_hidden_rows.py` - Test example with edit preservation
- `dash_glide_grid/dash_glide_grid.min.js` - Built output
