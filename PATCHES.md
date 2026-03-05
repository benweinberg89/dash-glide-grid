# Upstream Patches

This project applies patches to `@glideapps/glide-data-grid` (v6.0.4-alpha24) via [patch-package](https://github.com/ds300/patch-package). Patches are in `patches/` and applied automatically on `npm install` via the `postinstall` script.

## Patch Files

| File | Target |
|------|--------|
| `@glideapps+glide-data-grid+6.0.4-alpha24.patch` | Main grid library |
| `@glideapps+glide-data-grid-cells+6.0.4-alpha24.patch` | Extra cell renderers |

All changes are applied to both CJS (`dist/cjs/`) and ESM (`dist/esm/`) builds.

## Changes by Category

### 1. Transparent/Translucent Grid Backgrounds

**Problem**: Glide Data Grid assumes opaque backgrounds (`alpha: false` on all canvas contexts). Grids with translucent `bgCell` colors render black instead of transparent.

**Changes**:
- **Canvas alpha mode** (`data-grid.js`, `data-editor.js`, `use-column-sizer.js`, `links-cell.js`): Changed all `getContext("2d", { alpha: false })` to `{ alpha: true }` so `clearRect` clears to transparent instead of opaque black.
- **Double-buffer bypass** (`data-grid-render.js`): When `bgCell` has alpha < 1, skip double-buffering to avoid alpha doubling from buffer-to-canvas compositing. Also skip blit optimization (requires opaque source).
- **clearRect before fillRect** (`data-grid-render.js`): Added `clearRect` calls before `fillRect` in both full-redraw and damage-region paths so stale pixels are erased before painting translucent fills.
- **Disable bgCell blending** (`styles.js`): Removed the `mergeAndRealizeTheme` special case that force-blends `bgCell` overlays against the parent theme. With alpha support, themes should pass through as-is.
- **Transparent color blend guard** (`color-parser.js`): `blend()` now returns `rgba(0,0,0,0)` when combined alpha is zero (previously caused NaN division).

### 2. Opaque Editor/UI Overlays via `bgCellEditor`

**Problem**: When `bgCell` is transparent, editor overlays (text input, search bar, drilldown bubbles) inherit the transparent background, making them unreadable.

**Changes**:
- **New CSS variable** (`styles.js`): Added `--gdg-bg-cell-opaque` mapped to `theme.bgCellEditor ?? theme.bgCell`, giving a fallback opaque color.
- **CSS updates** (4 CSS files): Editor overlay, drilldown bubbles, number editor, and search bar all use `var(--gdg-bg-cell-opaque, var(--gdg-bg-cell))` instead of `var(--gdg-bg-cell)`.

### 3. Header Bottom Border Rendering

**Problem**: The header bottom border was drawn with `blend(headerBottomBorderColor, bgHeader)`, which forced the border to be opaque even when set to `"transparent"`. Additionally, the first horizontal grid line coincided with the header border, causing a double-drawn line.

**Changes**:
- **Skip border blending** (`data-grid-render.js`): Header bottom border uses `headerBottomBorderColor` directly without blending against `bgHeader`, so `"transparent"` actually works.
- **Skip first horizontal line** (`data-grid-render.lines.js`): When `totalHeaderHeight > 0`, the first horizontal line (at the header/body boundary) is skipped because the overlay canvas already draws it via `headerBottomBorderColor`.
- **Clear header before redraw** (`data-grid-render.header.js`): Added `clearRect` at the top of `drawGridHeaders()` so transparent header backgrounds don't accumulate.
- **Move overlay clear into drawHeaderTexture** (`data-grid-render.js`): Moved `overlayCtx.clearRect` from the top of `drawGrid()` into the `drawHeaderTexture` closure, so the overlay is only cleared when the header is actually redrawn. Previously, damage-only repaints (via `updateCells`) would clear the overlay without redrawing the header, causing the header to disappear.

### 4. Cell Border Accumulation During Damage Repaints

**Problem**: When using `DataEditor.updateCells()` for imperative cell redraws, borders accumulate on cell edges frame-over-frame. The damage repaint path draws cells but NOT grid lines. If `drawCell` content bleeds past cell bounds (e.g. strokes centered on cell edges), the bleed is never cleaned up.

The original code had a clip-skip optimization: it only clipped cells that were the leftmost column or overlapping the bottom freeze area. All other cells were drawn unclipped for performance. Additionally, the clip region and fill region used a 1px inset, leaving a border zone that couldn't be cleared.

**Changes** (`data-grid-render.cells.js`):
- **Always clip during damage repaints**: Removed the conditional clip-skip. Every cell in the damage list is now clipped to its full bounds, preventing any `drawCell` content from bleeding into adjacent cells.
- **Full-bounds clear and fill**: Changed from 1px-inset clear/fill (`cellX + 1`, `drawY + 1`, `cellWidth - 1`, `rh - 1`) to full cell bounds (`cellX`, `drawY`, `cellWidth`, `rh`). Added `clearRect` before `fillRect` for translucent backgrounds.

### 5. Grid Line Restoration During Damage Repaints

**Problem**: After patch #4 changed cell fills from 1px-inset to full-bounds, `updateCells()` damage repaints erase grid lines. The damage path calls `drawCells()` (which fills full cell bounds including the border zone) but never calls `drawGridLines()`. Grid lines progressively disappear wherever cells are updated — visible in animations like snake games or cellular automata where `updateCells()` runs every frame.

**Changes** (`data-grid-render.js`):
- **Call drawGridLines in doDamage**: Added `drawGridLines()` after `drawCells()` in the damage repaint path (`doDamage` closure). Grid lines are now redrawn on top of the freshly filled cells, matching the normal full-render flow (which already calls `drawGridLines` after `drawCells`). The always-clip fix from patch #4 prevents any accumulation since each cell is cleared before being refilled.

### 6. Opaque Grid Line Colors (Fixes Accumulation with Semi-Transparent Borders)

**Problem**: Patch #5 added `drawGridLines()` to the damage repaint path, but when border colors are semi-transparent (e.g., `rgba(255, 255, 255, 0.1)` in dark themes), each damage repaint draws grid lines on top of existing ones. Anti-aliased line pixels at cell boundaries accumulate opacity, causing visible artifacts: flickering on header hover, thickening borders on the row marker column, and progressive darkening near animated cells (booleans, sparklines). Additionally, the accumulated grid lines could overpower the 1px focus ring / selection border.

**Changes** (`data-grid-render.lines.js`):
- **Blend grid line colors to opaque**: In `drawGridLines()`, all line colors (`hColor`, `vColor`, and per-row theme overrides) are now blended against `theme.bgCell` using `blendCache()` before stroking. This makes grid lines idempotent — drawing an opaque line on top of itself produces an identical result, eliminating accumulation. This matches what `overdrawStickyBoundaries()` already does for sticky column/freeze row borders.

## Updating Patches

After modifying files in `node_modules/@glideapps/glide-data-grid/`:

```bash
npx patch-package @glideapps/glide-data-grid
npx patch-package @glideapps/glide-data-grid-cells  # if cells package changed
npm run build                                        # rebuild the bundle
```

Each patch file must cover both `dist/cjs/` and `dist/esm/` — the same logical change appears twice.
