# Plan: Freeform Cell Selection Mode

## Overview
Add a new selection mode (`rangeSelect="freeform"`) that allows non-rectangular, freeform cell selection. Unlike `multi-rect` which creates multiple overlapping ranges, this maintains a **single unified set of selected cells**.

## Desired Behavior
- Click/drag without Cmd → **starts new selection** (clears previous, selects clicked cells)
- Cmd+click on unselected cell → **add mode** (adds cells to selection)
- Cmd+click on selected cell → **remove mode** (removes cells from selection)
- Cmd+drag → consistently adds or removes based on first cell clicked
- Escape key → **clears** the selection
- Dragging across unselectable cells **excludes** them automatically
- Visual style matches native selection appearance
- Cell ranges only (row/column selection unchanged)

## Props

**Input:**
```python
rangeSelect="freeform"  # New option alongside "none", "cell", "rect", "multi-cell", "multi-rect"
```

**Output:**
```python
selectedCells: List[Dict]   # [{col: int, row: int}, ...] - simple list of all selected cells
selectedRanges: List[Dict]  # Same data as 1x1 ranges for API consistency
selectedCell: Dict          # {col, row} - focus cell (most recently clicked), unchanged
```

## Actual Implementation

### 1. State & Refs (GlideGrid.react.js lines 531-543)

```javascript
// Modifier key tracking
const modifierKeysRef = useRef({ metaKey: false, ctrlKey: false });

// Set of selected cells stored as "col,row" strings for O(1) lookup
const [freeformSelection, setFreeformSelection] = useState(new Set());

// Drag state tracking for Cmd+drag operations
const freeformDragRef = useRef({
    isDragging: false,
    isAddMode: true,      // true = add cells, false = remove cells
    baseSelection: new Set(),  // selection state before drag started
    lastRange: null       // detect new drag operations by range origin
});
```

### 2. Modifier Key Effect (lines 577-605)

- Tracks Cmd/Ctrl key state via document keydown/keyup listeners
- Only active when `rangeSelect === 'freeform'`
- Also handles Escape to clear selection

### 3. DataEditor Compatibility (line 3661)

**Critical**: glide-data-grid doesn't understand 'freeform', so we map it:
```javascript
rangeSelect={rangeSelect === 'freeform' ? 'rect' : rangeSelect}
```

### 4. Selection Handler (lines 2319-2419)

When `rangeSelect === 'freeform'`:

1. **Detect new drag** by checking if range origin changed
2. **Determine add/remove mode** based on whether first clicked cell was selected
3. **Store base selection** snapshot before drag
4. **Apply selection changes**:
   - Non-Cmd: Clear and select new range
   - Cmd + Add mode: Base selection + drag range
   - Cmd + Remove mode: Base selection - drag range

### 5. Visual Rendering (lines 545-627)

**Rectangle Merging Algorithm** (`mergeCellsIntoRectangles`):
1. Sort cells by row, then column
2. For each unprocessed cell, extend horizontally as far as possible
3. Then extend vertically while entire row segments exist
4. Mark all cells in rectangle as used
5. Result: Minimal rectangles covering all selected cells

**Combined Highlight Regions** (`combinedHighlightRegions`):
- Merges user-provided `highlightRegions` with freeform selection
- Uses `rgba(59, 130, 246, 0.15)` with `style: 'no-outline'`

### 6. Files Modified

| File | Changes |
|------|---------|
| `src/lib/fragments/GlideGrid.react.js` | Modifier tracking, drag state, selection logic, rectangle merging, combined highlights |
| `src/lib/components/GlideGrid.react.js` | Added `'freeform'` to rangeSelect, added `selectedCells` prop |
| `dash_glide_grid/GlideGrid.py` | Auto-generated with new props |
| `examples/62_freeform_selection.py` | Example demonstrating the feature |

## Known Issues (WIP)

- [ ] Cmd+drag behavior still not perfect - range calculation may be off
- [ ] Need to verify add/remove mode detection works correctly

## Decisions Made

1. **Prop naming**: `rangeSelect="freeform"` ✓
2. **Clear behavior**: Escape clears; click without Cmd starts new selection ✓
3. **Cmd behavior**: Add/remove mode based on first cell clicked ✓
4. **Selection props**: Both `selectedCells` AND `selectedRanges` (1x1 ranges) ✓
5. **Visual style**: Match native selection with merged rectangles ✓
6. **glide-data-grid compatibility**: Map 'freeform' to 'rect' internally ✓

## Progress

- [x] Create feature branch (`feature/freeform-selection`)
- [x] Add modifier key tracking (Cmd/Ctrl)
- [x] Add freeformSelection state and logic
- [x] Add drag state tracking for consistent add/remove behavior
- [x] Add unselectable cell filtering
- [x] Implement merged rectangle rendering via highlightRegions
- [x] Add selectedCells prop definitions (React + Python)
- [x] Create example (`examples/62_freeform_selection.py`)
- [ ] Fix remaining Cmd+drag range issues
- [ ] Final testing and polish
