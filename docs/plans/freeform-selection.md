# Plan: Freeform Cell Selection Mode

## Overview
Add a new selection mode (`rangeSelect="freeform"`) that allows non-rectangular, freeform cell selection. Unlike `multi-rect` which creates multiple overlapping ranges, this maintains a **single unified set of selected cells**.

## Desired Behavior
- Click/drag without Cmd → **starts new selection** (clears previous, selects clicked cells)
- Cmd+click/drag → **toggles** cells (adds unselected, removes selected)
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

## Implementation

### 1. React Changes (GlideGrid.react.js)

#### A. Track Modifier Keys
Add refs and effects to track Cmd/Ctrl state:
```javascript
const modifierKeysRef = useRef({ metaKey: false, ctrlKey: false });

useEffect(() => {
    const handleKeyDown = (e) => {
        modifierKeysRef.current = { metaKey: e.metaKey, ctrlKey: e.ctrlKey };
    };
    const handleKeyUp = (e) => {
        modifierKeysRef.current = { metaKey: e.metaKey, ctrlKey: e.ctrlKey };
    };
    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
    return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.removeEventListener('keyup', handleKeyUp);
    };
}, []);
```

#### B. New Selection State
```javascript
const [freeformSelection, setFreeformSelection] = useState(new Set()); // "col,row" strings for O(1) lookup
```

#### C. Handle Selection Changes (when rangeSelect="freeform")
In `handleSelectionChanged`:
1. Detect if Cmd/Ctrl is held via `modifierKeysRef`
2. Get cells in the new range (from `newSelection.current.range`)
3. Filter out unselectable cells (`unselectableColumns`, `unselectableRows`, `selectionColumnMin`)
4. If Cmd/Ctrl held: **toggle** cells (add if unselected, remove if selected)
5. Otherwise: **clear** previous selection and add new cells
6. Update `selectedCells` and `selectedRanges` output props

#### D. Visual Rendering
Convert freeform selection to `highlightRegions` with **merged rectangles**:
- Merge adjacent cells into larger rectangles for continuous border appearance
- Algorithm: Greedy rectangle merging (similar to AG Grid)
  1. Sort cells by row, then column
  2. Find maximal horizontal runs of adjacent cells
  3. Merge vertical runs where possible
- Result: Minimal set of rectangles that cover all selected cells with continuous borders

### 2. Key Files to Modify

| File | Changes |
|------|---------|
| `src/lib/fragments/GlideGrid.react.js` | Add modifier tracking, freeform selection logic, highlightRegions generation |
| `src/lib/components/GlideGrid.react.js` | Add `selectedCells` prop definition |
| `dash_glide_grid/GlideGrid.py` | Add `selectedCells` prop to Python component |

### 3. Selection Logic Pseudocode

```javascript
function handleFreeformSelection(newRange, isCmdHeld) {
    const cellsInRange = [];

    // Enumerate cells in the range, filtering unselectable
    for (let col = newRange.x; col < newRange.x + newRange.width; col++) {
        for (let row = newRange.y; row < newRange.y + newRange.height; row++) {
            if (unselectableColumns.includes(col)) continue;
            if (unselectableRows.includes(row)) continue;
            if (selectionColumnMin && col < selectionColumnMin) continue;
            cellsInRange.push({ col, row });
        }
    }

    if (isCmdHeld) {
        // Toggle mode: add unselected cells, remove selected cells
        cellsInRange.forEach(cell => {
            const key = `${cell.col},${cell.row}`;
            if (freeformSelection.has(key)) {
                freeformSelection.delete(key);
            } else {
                freeformSelection.add(key);
            }
        });
    } else {
        // New selection: clear previous, add these cells
        freeformSelection.clear();
        cellsInRange.forEach(cell => {
            freeformSelection.add(`${cell.col},${cell.row}`);
        });
    }

    // Update output props
    const cells = Array.from(freeformSelection).map(key => {
        const [col, row] = key.split(',').map(Number);
        return { col, row };
    });

    // Also generate selectedRanges (1x1 ranges for API consistency)
    const ranges = cells.map(c => ({
        startCol: c.col, startRow: c.row,
        endCol: c.col, endRow: c.row
    }));

    setProps({ selectedCells: cells, selectedRanges: ranges });
}
```

### 4. Edge Cases to Handle

- **Sorted/filtered data**: Map display rows ↔ data rows via `sortedIndices`
- **Click vs drag**: Single click = single cell; drag = range of cells
- **Clear selection**: Click on empty area or press Escape
- **Performance**: Large selections need efficient storage (Set of strings) and rendering (merge adjacent cells)

### 5. Estimated Effort

| Task | Effort |
|------|--------|
| Modifier key tracking | 1 hour |
| Freeform selection state + logic | 2-3 hours |
| Unselectable filtering | 1 hour |
| Visual rendering via highlightRegions | 1-2 hours |
| Prop definitions (React + Python) | 1 hour |
| Testing + edge cases | 2 hours |
| **Total** | **8-10 hours** |

## Decisions Made

1. **Prop naming**: `rangeSelect="freeform"` ✓
2. **Clear behavior**: Escape clears; click without Cmd starts new selection ✓
3. **Cmd behavior**: Toggle (add unselected, remove selected) ✓
4. **Selection props**: Both `selectedCells` AND `selectedRanges` (1x1 ranges for API consistency) ✓
5. **Visual style**: Match native selection appearance ✓
6. **Visual rendering**: Merge adjacent cells into rectangles for continuous borders ✓

## Progress

- [x] Create feature branch
- [x] Add modifier key tracking (Cmd/Ctrl)
- [x] Add freeformSelection state and logic
- [x] Add unselectable cell filtering
- [x] Implement merged rectangle rendering via highlightRegions
- [x] Add selectedCells prop definitions (React + Python)
- [x] Create example and test edge cases
