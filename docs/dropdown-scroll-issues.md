# Dropdown/Multiselect Cell Editor Issues

## Problem Description

When clicking on cells with dropdown or multiselect editors, two issues occur:

1. **Dropdown doesn't flip** - When editing cells near the bottom of the viewport, the dropdown menu extends below the viewport instead of flipping to appear above the cell
2. **Unexpected page scroll** - The page scrolls unexpectedly when the editor opens, especially when the page already has some scroll position

## Root Cause Analysis

The `@glideapps/glide-data-grid-cells` library uses `react-select` for dropdown/multiselect editors. While react-select has `menuPlacement: "auto"` configured, the overlay's special positioning (CSS variables, transforms) appears to confuse react-select's viewport space calculation.

Additionally, react-select's focus behavior triggers the browser's scroll-into-view mechanism.

### Relevant Code Locations

- **Multi-select cell**: `node_modules/@glideapps/glide-data-grid-cells/dist/esm/cells/multi-select-cell.js`
- **Dropdown cell**: `node_modules/@glideapps/glide-data-grid-cells/dist/esm/cells/dropdown-cell.js`

Both have `menuPlacement: "auto"` set, which should flip the menu but doesn't work correctly with the overlay positioning.

## Attempted Solutions

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

## Potential Future Solutions

### 1. Fork glide-data-grid-cells
Modify react-select props directly in the source:
- Set `menuShouldScrollIntoView: false`
- Set `menuPosition: "fixed"`
- Adjust `menuPlacement` logic

### 2. Custom Cell Renderers
Write custom dropdown/multiselect cell renderers instead of using the library's built-in ones. This gives full control over positioning and scroll behavior.

### 3. CSS-Only Approach
Investigate if CSS properties can help:
- `scroll-padding`
- `overflow-anchor: none`
- `overscroll-behavior: contain`
- `scroll-behavior: instant`

### 4. Report Upstream Issue
File an issue with `@glideapps/glide-data-grid-cells` about `menuPlacement: "auto"` not working correctly with the overlay positioning system.

## Current State

All custom handling code has been removed. The component uses the default Glide Data Grid behavior with just the standard portal setup required by the library.
