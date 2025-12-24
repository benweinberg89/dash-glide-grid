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

## Actual Implementation (v2: Additive/Subtractive Layers)

### Core Concept

Instead of tracking individual cells, we track **selection layers**. Each layer has:
- `range`: `{x, y, width, height}` - the rectangular range
- `value`: `+1` (add) or `-1` (subtract)

A cell is selected if the **sum of all layer values** for that cell is **> 0**.

### 1. State & Refs (GlideGrid.react.js lines 531-545)

```javascript
// Modifier key tracking
const modifierKeysRef = useRef({ metaKey: false, ctrlKey: false });

// Selection layers: each layer has a range and a value (+1 or -1)
// Normal drag = REPLACE (clear all, add +1 layer)
// Cmd+drag = ADD layer (+1 if cell unselected, -1 if selected)
// Final selection = cells where sum of layer values > 0
const [selectionLayers, setSelectionLayers] = useState([]);

// Track current drag: which layer we're updating during drag
const currentDragRef = useRef({
    layerIndex: -1,  // index into selectionLayers for the current drag
    rangeOrigin: null  // "x,y" to detect new drag operations
});
```

### 2. Computing Selected Cells (lines 547-582)

`computeSelectedCells(layers, unselectableCols, unselectableRows, colMin)`:
1. For each layer, iterate through cells in the range
2. Add the layer's value (+1 or -1) to a Map keyed by "col,row"
3. Skip unselectable cells
4. Return cells where net value > 0

### 3. Selection Handler Logic (lines 2365-2442)

When `rangeSelect === 'freeform'`:

**New Drag (range origin changed):**
- **Normal drag (no Cmd)**: REPLACE all layers with a single +1 layer
- **Cmd+drag**: Check if first clicked cell is selected
  - If selected: ADD a -1 layer (subtract)
  - If not selected: ADD a +1 layer (add)

**Continuing Drag (same origin):**
- Update the current layer's range (the layer at `currentDragRef.layerIndex`)

### 4. Visual Rendering (lines 654-680)

`combinedHighlightRegions` useMemo:
1. Compute selected cells from all layers
2. Merge adjacent cells into rectangles using `mergeCellsIntoRectangles`
3. Convert to highlightRegions format with selection color

### 5. Modifier Key Effect (lines 719-751)

- Tracks Cmd/Ctrl key state via document keydown/keyup listeners
- Only active when `rangeSelect === 'freeform'`
- Escape clears all layers and resets drag state

### 6. DataEditor Compatibility (line ~3700)

**Critical**: glide-data-grid doesn't understand 'freeform', so we map it:
```javascript
rangeSelect={rangeSelect === 'freeform' ? 'rect' : rangeSelect}
```

### 7. Files Modified

| File | Changes |
|------|---------|
| `src/lib/fragments/GlideGrid.react.js` | Layers state, computeSelectedCells, selection logic, rectangle merging, combined highlights |
| `src/lib/components/GlideGrid.react.js` | Added `'freeform'` to rangeSelect, added `selectedCells` prop |
| `dash_glide_grid/GlideGrid.py` | Auto-generated with new props |
| `examples/62_freeform_selection.py` | Example demonstrating the feature |

## How The Layers Approach Works

**Example 1: Normal selection then subtract**
1. Click/drag cells A,B,C → layers = `[{range: ABC, value: +1}]`
2. Cells A,B,C all have value +1 → selected
3. Cmd+click on B (which is selected) → layers = `[{ABC: +1}, {B: -1}]`
4. A=+1, B=+1-1=0, C=+1 → A and C selected, B not selected

**Example 2: Normal selection then add**
1. Click/drag cells A,B,C → layers = `[{range: ABC, value: +1}]`
2. Cmd+click on D (which is NOT selected) → layers = `[{ABC: +1}, {D: +1}]`
3. A=+1, B=+1, C=+1, D=+1 → all selected

**Example 3: Drag replaces**
1. Click/drag cells A,B,C → layers = `[{ABC: +1}]`
2. Click/drag (no Cmd) cells D,E → layers = `[{DE: +1}]` (ABC cleared!)
3. Only D,E selected

## Decisions Made

1. **Prop naming**: `rangeSelect="freeform"` ✓
2. **Clear behavior**: Escape clears; click without Cmd starts new selection ✓
3. **Cmd behavior**: Add/remove mode based on first cell clicked ✓
4. **Selection props**: Both `selectedCells` AND `selectedRanges` (1x1 ranges) ✓
5. **Visual style**: Match native selection with merged rectangles ✓
6. **glide-data-grid compatibility**: Map 'freeform' to 'rect' internally ✓
7. **Implementation strategy**: Additive/subtractive layers ✓

## Progress

- [x] Create feature branch (`feature/freeform-selection`)
- [x] Add modifier key tracking (Cmd/Ctrl)
- [x] Implement layers-based selection state
- [x] Add computeSelectedCells function
- [x] Add unselectable cell filtering
- [x] Implement merged rectangle rendering via highlightRegions
- [x] Add selectedCells prop definitions (React + Python)
- [x] Create example (`examples/62_freeform_selection.py`)
- [x] Rewrite selection handler for layers approach
- [ ] Manual testing and verification
- [ ] Final polish
