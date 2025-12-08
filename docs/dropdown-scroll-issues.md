# Comprehensive Research: Dropdown/Multiselect Cell Editor Positioning Issues

## Executive Summary

This document provides a thorough investigation of dropdown and multiselect cell editor issues in `@glideapps/glide-data-grid`. The problems stem from both **intentional design decisions** in Glide Data Grid's overlay system AND **missing configuration** in the react-select implementation.

---

## Problem Statement

When clicking on dropdown or multiselect cells:
1. **Dropdown menu extends past viewport** instead of flipping above the cell
2. **Page scrolls unexpectedly** when the editor opens
3. **Editor overlay becomes orphaned** from its cell after scroll

---

## Architecture Deep Dive

### How Glide Data Grid Renders

```
┌─────────────────────────────────────────────────────────────┐
│                    HTML Document                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              <canvas> element                         │  │
│  │   ┌─────┬─────┬─────┬─────┐                           │  │
│  │   │cell │cell │cell │cell │  ← Pixels drawn on canvas │  │
│  │   ├─────┼─────┼─────┼─────┤    NOT DOM elements       │  │
│  │   │cell │cell │cell │cell │                           │  │
│  │   └─────┴─────┴─────┴─────┘                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  <div id="portal">  ← Fixed position, z-index 9999   │  │
│  │    ┌─────────────────┐                                │  │
│  │    │ Editor Overlay  │  ← React component, DOM element│  │
│  │    │ (position:abs)  │                                │  │
│  │    │    ┌─────────┐  │                                │  │
│  │    │    │ Select  │  │  ← react-select component     │  │
│  │    │    │ ┌─────┐ │  │                                │  │
│  │    │    │ │Menu │ │  │  ← Another portal layer       │  │
│  │    │    │ └─────┘ │  │                                │  │
│  │    │    └─────────┘  │                                │  │
│  │    └─────────────────┘                                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Key insight**: Grid cells are **painted pixels**, editor overlays are **DOM elements**. They exist in completely different rendering contexts.

### Overlay Editor Positioning System

**Source**: `@glideapps/glide-data-grid/packages/core/src/internal/data-grid-overlay-editor/`

#### CSS Positioning (data-grid-overlay-editor-style.tsx)
```css
position: absolute;
left: ${targetX}px;
top: ${targetY}px;
min-width: ${targetWidth}px;
min-height: ${targetHeight}px;
```

- Uses `position: absolute` NOT `fixed`
- `targetX`/`targetY` set **once** when editor opens
- Values come from `target: Rectangle` prop passed to editor

#### useStayOnScreen Hook (use-stay-on-screen.ts)
```typescript
export function useStayOnScreen(): StayOnScreen {
  // Uses IntersectionObserver to detect overflow
  // Only handles HORIZONTAL overflow via translateX
  // Does NOT track scroll or reposition on scroll

  const style = { transform: `translateX(${xOffset}px)` };
  return { ref: setRef, style };
}
```

**Limitations**:
- Only adjusts horizontal position
- Does not respond to scroll events
- One-time calculation, not continuous

### Intentional Design Decision (GitHub Issue #583)

**Issue**: "When scroll after entering edit-mode in cells, the popup does not stay with the cell"
**Status**: Closed as COMPLETED (not fixed)

**Maintainer (jassmith) explanation**:
> "Keeping overlays synced creates cropping issues as cells exit the viewport. It also allows users to open an overlay, then scroll a couple pages to reference something else for data entry purposes."

**Community workaround mentioned**:
> "We locked the scroll of the page when editor overlays are open"

**Conclusion**: This is **intentional behavior** - Glide chose NOT to sync overlay position with scroll.

---

## The Cascade Failure (Dropdown-Specific)

When a dropdown cell near the viewport bottom is clicked:

```
1. User clicks dropdown cell
   ↓
2. Overlay editor opens at cell position (targetX=100, targetY=500)
   ↓
3. react-select mounts with menuPlacement="auto"
   ↓
4. Menu tries to render below cell, extends past viewport
   ↓
5. menuShouldScrollIntoView=true (default) triggers browser scroll
   ↓
6. Page scrolls down to show menu
   ↓
7. BUT overlay is still at (100, 500) - original position
   ↓
8. Cell is now visually at (100, 300) due to scroll
   ↓
9. Editor overlay is 200px BELOW where the cell appears
   ↓
10. User sees disconnected input field floating in wrong position
```

---

## react-select Configuration Analysis

### Current Configuration (dropdown-cell.js, multi-select-cell.js)

```javascript
<Select
  menuPlacement="auto"                    // ✓ Correct
  menuPortalTarget={document.getElementById("portal")}  // ✓ Correct
  // MISSING: menuPosition="fixed"
  // MISSING: menuShouldScrollIntoView={false}
/>
```

### Required Configuration

| Prop | Current | Required | Purpose |
|------|---------|----------|---------|
| `menuPlacement` | `"auto"` | `"auto"` | Flip menu above/below based on space |
| `menuPortalTarget` | `portal` | `portal` | Render in portal for z-index |
| `menuPosition` | (default: `"absolute"`) | `"fixed"` | Position relative to viewport, not parent |
| `menuShouldScrollIntoView` | (default: `true`) | `false` | **Prevent scroll cascade** |

### Why menuShouldScrollIntoView Matters

This prop controls whether react-select calls `scrollIntoView()` on the menu when it opens. When `true` (default):
1. Browser receives scroll request
2. Viewport scrolls to show menu
3. But overlay doesn't know viewport moved
4. Everything becomes misaligned

Setting to `false` prevents the scroll entirely - the menu either fits or it flips.

---

## Available APIs and Data

### Editor Component Props

Every editor receives these props (from ProvideEditorComponent type):

```typescript
{
  onChange: (newValue: T) => void;
  onFinishedEditing: (newValue?: T, movement?: [...]) => void;
  isHighlighted: boolean;
  value: T;                           // The cell data
  initialValue?: string;
  target: Rectangle;                  // Cell position {x, y, width, height}
  forceEditMode: boolean;
  isValid?: boolean;
}
```

The `target: Rectangle` contains the cell's screen position at the moment the editor opened.

### DataEditorRef Methods

```typescript
interface DataEditorRef {
  getBounds: (col?: number, row?: number) => Rectangle | undefined;
  // Returns CURRENT bounding box of a cell
  // Could be used to track position changes during scroll

  scrollTo: (col, row, dir?, paddingX?, paddingY?, options?) => void;
  updateCells: (cells: DamageUpdateList) => void;
  focus: () => void;
}
```

### onVisibleRegionChanged Callback

Fires when grid scrolls internally:
```javascript
onVisibleRegionChanged={(range, tx, ty, extras) => {
  // range: {x, y, width, height} - visible cell range
  // tx, ty: translation offsets
}}
```

Could potentially detect grid scroll and close editor or reposition.

---

## Existing Pattern: HeaderMenu.react.js

The project already has a working solution for a similar problem:

### Scroll Tracking (lines 79-109)
```javascript
// Capture initial scroll when menu opens
initialScrollRef.current = {
  x: window.scrollX || window.pageXOffset,
  y: window.scrollY || window.pageYOffset
};

const handleScroll = () => {
  const currentX = window.scrollX || window.pageXOffset;
  const currentY = window.scrollY || window.pageYOffset;

  // Calculate delta from initial position
  setScrollOffset({
    x: initialScrollRef.current.x - currentX,
    y: initialScrollRef.current.y - currentY
  });
};

window.addEventListener('scroll', handleScroll, true);
```

### Position Adjustment (lines 237-265)
```javascript
// Apply scroll offset to keep menu anchored
let left = position.x + scrollOffset.x;
let top = position.y + scrollOffset.y;
```

### Invisible Backdrop (lines 339-353)
```javascript
const backdropStyle = {
  position: 'fixed',
  top: 0, left: 0, right: 0, bottom: 0,
  zIndex: 9999
};
<div style={backdropStyle} onClick={onClose} />
```

**Note**: HeaderMenu tracks **page scroll** only. Cell editors would also need to handle **internal grid scroll**.

---

## All Custom Cell Types in glide-data-grid-cells

| Cell Type | Has Dropdown/Menu | Affected |
|-----------|-------------------|----------|
| StarCell | No | No |
| SparklineCell | No | No |
| TagsCell | No | No |
| UserProfileCell | No | No |
| **DropdownCell** | **Yes (react-select)** | **Yes** |
| ArticleCell | No | No |
| RangeCell | No (slider) | No |
| SpinnerCell | No | No |
| DatePickerCell | No (native input) | No |
| LinksCell | No | No |
| ButtonCell | No | No |
| TreeViewCell | No | No |
| **MultiSelectCell** | **Yes (react-select)** | **Yes** |

Only DropdownCell and MultiSelectCell are affected because they use react-select.

---

## Solution Approaches

### Approach 1: Custom Cell Renderers with Fixed react-select

Create custom renderers that:
1. Copy drawing logic from original library
2. Configure react-select properly:
   - `menuPosition: "fixed"`
   - `menuShouldScrollIntoView: false`
3. Optionally add backdrop to prevent scroll during editing

**Pros**: Full control, no upstream dependency
**Cons**: Must maintain custom code, sync with library updates

### Approach 2: Scroll Lock During Editing

Add invisible backdrop when dropdown/multiselect editor opens:
1. Backdrop covers entire viewport
2. Prevents scroll events from reaching page
3. Click outside backdrop closes editor
4. User can then scroll

**Pros**: Simple, matches HeaderMenu pattern
**Cons**: Users can't scroll while editing (usually acceptable)

### Approach 3: Dynamic Repositioning

Track scroll and reposition overlay:
1. Use `onVisibleRegionChanged` for grid scroll
2. Use window scroll listener for page scroll
3. Call `getBounds(col, row)` to get current cell position
4. Update overlay position accordingly

**Pros**: Overlay stays with cell
**Cons**: Complex, may cause performance issues, visual jitter

### Approach 4: Fork glide-data-grid-cells

Fork the library and modify source directly:
- Add `menuShouldScrollIntoView: false`
- Add `menuPosition: "fixed"`

**Pros**: Clean fix at source
**Cons**: Must maintain fork

### Approach 5: patch-package

Use patch-package to auto-patch node_modules:
```bash
npx patch-package @glideapps/glide-data-grid-cells
```

**Pros**: No fork to maintain, patches apply on install
**Cons**: Patches may break on library updates

---

## Recommended Solution

**Approach 1 + 2 Combined**: Custom cell renderers with scroll lock backdrop

1. Create `src/lib/cells/DropdownCellRenderer.js`:
   - Copy draw/measure logic from library
   - Custom editor with proper react-select config
   - Wrap in backdrop component

2. Create `src/lib/cells/MultiSelectCellRenderer.js`:
   - Same approach

3. Update `GlideGrid.react.js`:
   - Import custom renderers
   - Filter out library's dropdown/multiselect from `allCells`
   - Add custom renderers to `customRenderers` prop

---

## Files Reference

### Library Source (node_modules)
- `@glideapps/glide-data-grid-cells/dist/esm/cells/dropdown-cell.js`
- `@glideapps/glide-data-grid-cells/dist/esm/cells/multi-select-cell.js`
- `@glideapps/glide-data-grid-cells/dist/esm/index.js`

### Project Files
- `src/lib/fragments/GlideGrid.react.js` - Main grid component
- `src/lib/fragments/HeaderMenu.react.js` - Working scroll-lock pattern
- `docs/dropdown-scroll-issues.md` - This document

### Glide Core (for reference)
- `data-grid-overlay-editor.tsx` - Overlay positioning
- `data-grid-overlay-editor-style.tsx` - CSS positioning
- `use-stay-on-screen.ts` - Horizontal overflow handling

---

## GitHub Issues Reference

- **#583**: "When scroll after entering edit-mode in cells, the popup does not stay with the cell" - Closed, intentional design
- **#298**: "Fix scroll issue with overlay editor" - CSS overflow fix, unrelated
- **#1159**: "How to keep the cell editor input/dropdown box fixed in place?" - Open, no response

---

## Attempted Solutions (Historical)

### 1. Dropdown Repositioning with MutationObserver
**Approach**: Watch for dropdown menus using MutationObserver and manually reposition using `targetx`/`targety` attributes from the overlay.

**Result**: Never worked properly - the positioning calculations were incorrect.

### 2. Scroll Lock on Overlay Open
**Approach**: Detect when overlay opens and lock/restore scroll position.

**Result**: Caused jarring scroll-then-correct behavior - user sees scroll happen then snap back.

### 3. Scroll Lock on Mousedown
**Approach**: Capture scroll position on mousedown and lock immediately before overlay opens.

**Result**: Made things worse - scroll happened and didn't restore to correct position.

### 4. Body Fixed Positioning (Modal-style)
**Approach**: Use `position: fixed` on body with negative top offset (standard modal scroll lock technique).

**Result**: Still had visual jitter during the transition.

### 5. Menu Flip with MutationObserver
**Approach**: Detect menu elements when added and reposition with `position: fixed; bottom: X`.

**Result**: The flip partially worked but scroll issues persisted.

---

## Current State

All custom handling code has been removed. The component uses the default Glide Data Grid behavior with just the standard portal setup required by the library.

---

## Implementation Checklist

For the implementation session:

- [ ] Create `DropdownCellRenderer.js` with:
  - [ ] Same `draw()` function as library
  - [ ] Same `measure()` function as library
  - [ ] Custom `provideEditor()` with:
    - [ ] `menuPosition: "fixed"`
    - [ ] `menuShouldScrollIntoView: false`
    - [ ] `menuPlacement: "auto"`
    - [ ] Backdrop wrapper component
  - [ ] Same `onPaste()` function as library

- [ ] Create `MultiSelectCellRenderer.js` with same approach

- [ ] Update `GlideGrid.react.js`:
  - [ ] Import custom renderers
  - [ ] Create filtered `customRenderers` array excluding library dropdown/multiselect
  - [ ] Add custom renderers

- [ ] Test scenarios:
  - [ ] Dropdown cell at top of viewport
  - [ ] Dropdown cell at bottom of viewport
  - [ ] Page with existing scroll position
  - [ ] Grid scroll (internal)
  - [ ] Click outside to close
