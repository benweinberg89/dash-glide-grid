# Fix Dropdown/Multiselect Cell Editor Scroll Issues

## Problem Summary
Dropdown and multiselect cells have positioning issues:
1. Menu extends past viewport instead of flipping above
2. Page scrolls unexpectedly when editor opens
3. Editor overlay becomes orphaned from cell after scroll

## Root Cause
The library's react-select configuration (lines 68-151 in dropdown-cell.js, lines 290-339 in multi-select-cell.js) is missing:
- `menuPosition: "fixed"` (currently default "absolute")
- `menuShouldScrollIntoView: false` (currently default true, triggers browser scroll)

## Solution
Create custom cell renderers that copy the library's draw/measure/onPaste logic but fix the react-select editor configuration.

---

## Implementation Steps

### Step 1: Create DropdownCellRenderer.js

**File**: `src/lib/cells/DropdownCellRenderer.js`

Copy from `node_modules/@glideapps/glide-data-grid-cells/dist/esm/cells/dropdown-cell.js`:
- `draw()` - lines 156-177 (canvas text rendering)
- `measure()` - lines 178-183 (text width calculation)
- `onPaste()` - lines 196-203 (paste validation)
- `Editor` component - lines 34-151 (but fix the Select props)

**Key change to Editor's Select component** (around line 68):
```javascript
// Add these two props:
menuPosition="fixed"
menuShouldScrollIntoView={false}
// Keep existing:
menuPlacement="auto"
menuPortalTarget={...}
```

### Step 2: Create MultiSelectCellRenderer.js

**File**: `src/lib/cells/MultiSelectCellRenderer.js`

Copy from `node_modules/@glideapps/glide-data-grid-cells/dist/esm/cells/multi-select-cell.js`:
- Helper functions: `prepareOptions()` (lines 26-41), `resolveValues()` (lines 52-72)
- Constants: `VALUE_PREFIX`, `VALUE_PREFIX_REGEX` (lines 8-9)
- `draw()` - lines 344-397 (bubble rendering)
- `measure()` - lines 398-413 (bubble width calculation)
- `onPaste()` - lines 426-453 (multi-value paste)
- `Editor` component - lines 85-339 (but fix the Select/CreatableSelect props)

**Key change to Editor's Select component** (around line 311):
```javascript
// Add these two props:
menuPosition="fixed"
menuShouldScrollIntoView={false}
// Keep existing:
menuPlacement="auto"
menuPortalTarget={...}
```

### Step 3: Update GlideGrid.react.js

**File**: `src/lib/fragments/GlideGrid.react.js`

**Line 5** - Add imports:
```javascript
import { allCells } from '@glideapps/glide-data-grid-cells';
import DropdownCellRenderer from '../cells/DropdownCellRenderer';
import MultiSelectCellRenderer from '../cells/MultiSelectCellRenderer';
```

**Before line 2192** - Create filtered renderers:
```javascript
const customRenderers = useMemo(() => [
  ...allCells.filter(c =>
    c.isMatch?.({data: {kind: 'dropdown-cell'}}) !== true &&
    c.isMatch?.({data: {kind: 'multi-select-cell'}}) !== true
  ),
  DropdownCellRenderer,
  MultiSelectCellRenderer
], []);
```

**Line 2192** - Use filtered renderers:
```javascript
customRenderers={customRenderers}
```

---

## Files to Create/Modify

| File | Action | Lines |
|------|--------|-------|
| `src/lib/cells/DropdownCellRenderer.js` | Create | ~210 |
| `src/lib/cells/MultiSelectCellRenderer.js` | Create | ~460 |
| `src/lib/fragments/GlideGrid.react.js` | Modify | ~10 lines changed |

## Dependencies
No new dependencies needed - uses existing:
- `react-select` (already installed)
- `react-select/creatable` (already installed)
- `@glideapps/glide-data-grid` exports: `getMiddleCenterBias`, `useTheme`, `GridCellKind`, `measureTextCached`, `roundedRect`, `getLuminance`

## Test Scenarios
- [ ] Dropdown cell at top of viewport - menu opens below
- [ ] Dropdown cell at bottom of viewport - menu flips above (no scroll!)
- [ ] Multiselect cell at bottom - menu flips above (no scroll!)
- [ ] Page with existing scroll position - no unexpected scroll
- [ ] Click outside to close editor
- [ ] Keyboard navigation (Enter, Escape, Tab)
- [ ] Readonly cells remain uneditable