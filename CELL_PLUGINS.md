# Cell Plugins

The `cellPlugins` prop lets you add custom cell types to `GlideGrid` with your own canvas rendering, click handling, and editor overlays — all declaratively from Python.

## How it works

1. Define a **plugin config** dict with a unique `kind`, a `draw` function, and optional `onClick`, `provideEditor`, `cursor`, and `js` fields.
2. Pass the config(s) to `GlideGrid(cellPlugins=[...])`.
3. In your row data, set the column value to a dict with `"kind": "<your-kind>"` plus whatever data your draw/editor functions need.
4. The grid matches each cell's `kind` to the plugin and calls your functions.

## Quick start

A minimal read-only colored pill cell:

**Python:**
```python
from dash_glide_grid import GlideGrid

app.layout = GlideGrid(
    columns=[
        {"title": "Name", "id": "name", "type": "text"},
        {"title": "Priority", "id": "priority", "type": "custom", "width": 120},
    ],
    data=[
        {"name": "Task A", "priority": {"kind": "pill", "label": "High", "color": "#ef4444"}},
        {"name": "Task B", "priority": {"kind": "pill", "label": "Low", "color": "#22c55e"}},
    ],
    cellPlugins=[{
        "kind": "pill",
        "draw": {"function": "drawPill(args, cell)"},
        "js": """
var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};
dggfuncs.drawPill = function(args, cell) {
    var ctx = args.ctx, rect = args.rect, theme = args.theme, data = cell.data;
    if (!data.label) return true;

    var x = rect.x + 8, y = rect.y + (rect.height - 20) / 2;
    var w = ctx.measureText(data.label).width + 12;

    ctx.fillStyle = data.color || theme.bgBubble || "#e0e0e0";
    ctx.beginPath();
    ctx.moveTo(x + 10, y);
    ctx.arcTo(x + w, y, x + w, y + 20, 10);
    ctx.arcTo(x + w, y + 20, x, y + 20, 10);
    ctx.arcTo(x, y + 20, x, y, 10);
    ctx.arcTo(x, y, x + w, y, 10);
    ctx.fill();

    ctx.fillStyle = "#fff";
    ctx.textBaseline = "middle";
    ctx.fillText(data.label, x + 6, y + 10);
    return true;
};
""",
    }],
)
```

The `js` field injects the draw function at runtime — no separate JS file needed.

## Plugin config reference

Each entry in `cellPlugins` is a dict with these fields:

| Field | Required | Description |
|-------|----------|-------------|
| `kind` | Yes | Unique string identifying this cell type. Used in cell data to route to this plugin. |
| `draw` | Yes | `{"function": "fnName(args, cell)"}` — canvas rendering function. |
| `onClick` | No | `{"function": "fnName(args, cell)"}` — click handler. Return truthy to fire `customCellClicked`, falsy to suppress. |
| `provideEditor` | No | `{"function": "fnName(cell)"}` — returns editor config. When present, clicking the cell opens an editor overlay. |
| `cursor` | No | CSS cursor on hover (e.g. `"pointer"`). |
| `js` | No | JS source string to inject. Registers functions on `window.dashGlideGridFunctions`. Runs once per unique string. |

### Reserved kinds

These `kind` strings are used by built-in cell types and must not be used by plugins:

`button-cell`, `date-picker-cell`, `dropdown-cell`, `links-cell`, `multi-select-cell`, `range-cell`, `sparkline-cell`, `spinner-cell`, `star-cell`, `tags-cell`, `tree-view-cell`, `user-profile-cell`

### `draw`

Called every frame to render the cell on the HTML canvas.

```js
dggfuncs.myDraw = function(args, cell) {
    // args properties:
    //   ctx         - CanvasRenderingContext2D
    //   theme       - Glide theme object (colors, spacing, etc.)
    //   rect        - {x, y, width, height} of the cell
    //   col         - column index
    //   row         - row index (visual, post-sort)
    //   hoverX      - mouse X relative to cell (or undefined)
    //   hoverY      - mouse Y relative to cell (or undefined)
    //   hoverAmount - 0 to 1 hover fade
    //   highlighted - whether cell is in selection range

    // cell.data is whatever dict you provided in Python row data
    var data = cell.data;

    // ... draw on ctx ...

    return true; // return true to indicate the cell was drawn
};
```

### `onClick`

Called when a user clicks the cell. Controls whether the click fires a Dash callback.

```js
dggfuncs.myClick = function(args, cell) {
    // args has: location [col, row], bounds, cell, etc.
    // Return truthy → fires customCellClicked output
    // Return falsy  → suppresses callback
    return true;
};
```

If no `onClick` is defined, clicks always fire `customCellClicked`.

### `provideEditor`

Returns an editor overlay config when the cell is activated (clicked/selected).

```js
dggfuncs.myEditor = function(cell) {
    // cell.data is the cell's data dict
    // Return { editor: ReactComponent, disablePadding: boolean }
    // Return undefined to skip (no editor for this cell)
    return { editor: MyEditorComponent, disablePadding: true };
};
```

When `provideEditor` is defined, cell selection is enabled — clicking opens the editor instead of just firing a click event. When not defined, selection is suppressed (read-only cell).

The editor component receives these props from Glide:
- `value` — the full cell object (`value.data` is your cell data dict)
- `onFinishedEditing(newCell)` — call to commit the edit. Pass the updated cell object.
- `isHighlighted`, `onChange`, etc.

### `cursor`

CSS cursor string shown when hovering over the cell:

```python
{"kind": "status", "draw": ..., "cursor": "pointer"}
```

### `js`

Inline JavaScript source that registers functions on `window.dashGlideGridFunctions`. Injected once per unique string before renderers are built.

```python
cellPlugins=[{
    "kind": "my-cell",
    "draw": {"function": "myDraw(args, cell)"},
    "js": """
var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};
dggfuncs.myDraw = function(args, cell) { ... };
""",
}]
```

This is the recommended approach for distributing plugins as Python packages — the JS is embedded in the Python package and injected automatically, so users don't need to copy JS files into their `assets/` directory.

Alternatively, you can skip `js` and place a JS file directly in your Dash app's `assets/` directory:

```js
// assets/dashGlideGridFunctions.js
var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};
dggfuncs.myDraw = function(args, cell) { ... };
```

## Cell data format

Each cell using a plugin is a Python dict with a `kind` field matching the plugin's `kind`:

```python
# Minimal cell data
{"kind": "pill", "label": "High", "color": "#ef4444"}

# The only required field is "kind" — everything else is up to your draw/editor functions
{"kind": "my-cell", "foo": 42, "bar": "hello"}
```

Internally, the grid wraps your dict as a `GridCellKind.Custom` cell with your dict accessible at `cell.data`.

## Function resolution

All function references (`draw`, `onClick`, `provideEditor`) use the format `{"function": "fnName(args, cell)"}`.

At runtime, `fnName` is looked up in `window.dashGlideGridFunctions`. The string is parsed as a function call expression — the named parameters (`args`, `cell`) are passed as variables available inside the expression.

Functions can be registered in two ways:
1. Via the `js` field in the plugin config (injected at runtime)
2. Via a JS file in your Dash app's `assets/` directory

Both approaches register on the same `window.dashGlideGridFunctions` namespace.

## `customCellClicked` output

When a plugin cell is clicked, the grid fires the `customCellClicked` output prop (unless `onClick` returns falsy):

```python
@callback(
    Output("result", "children"),
    Input("grid", "customCellClicked"),
    prevent_initial_call=True,
)
def on_click(info):
    # info = {
    #     "kind": "pill",          # plugin kind
    #     "col": 1,                # column index
    #     "row": 0,                # row index (original, pre-sort)
    #     "cellData": {...},       # the full cell data dict
    #     "bounds": {"x": ..., "y": ..., "width": ..., "height": ...},
    #     "timestamp": 1234567890  # for deduplication
    # }
    return f"Clicked {info['kind']} at row {info['row']}"
```

## Editor overlays

### Lifecycle

1. User clicks a cell that has a `provideEditor` plugin
2. Glide calls your `provideEditor` function with the cell data
3. Your function returns `{editor: ReactComponent, disablePadding: true}`
4. Glide renders the component in an overlay positioned over the cell
5. The component calls `onFinishedEditing(updatedCell)` to commit changes
6. The grid fires `cellEdited` with the new value

### Stable editor references

Glide compares editor components by reference. If `provideEditor` returns a new function object each time, Glide will unmount and remount the editor on every call — which can cause infinite loops (unmount fires commit, commit triggers re-render, re-render calls `provideEditor` again).

The fix is to define the editor component once and return the same reference:

```js
// GOOD: Editor defined once via IIFE, stable reference
dggfuncs.myEditor = (function() {
    var _Editor = function(props) {
        var value = props.value;
        var onFinishedEditing = props.onFinishedEditing;
        // ... render editor ...
    };

    return function(cell) {
        return { editor: _Editor, disablePadding: true };
    };
})();

// BAD: Creates a new Editor function every call → infinite loop
dggfuncs.myEditor = function(cell) {
    var Editor = function(props) { ... }; // new reference every time!
    return { editor: Editor, disablePadding: true };
};
```

### Commit strategies

- **Immediate commit** (single-select): Call `onFinishedEditing` as soon as the user picks a value. The overlay closes immediately.
- **Commit on unmount** (multi-select): Store the current value in a ref, commit in a `useEffect` cleanup function. The overlay stays open until the user clicks away.

### Portal click handling

Dropdown menus rendered by editor components often portal outside the editor overlay. Glide sees these clicks as "outside" and closes the editor.

Add the CSS class `click-outside-ignore` to portalled elements to prevent this:

```js
// For DMC components with comboboxProps:
React.createElement(CompClass, {
    comboboxProps: { classNames: { dropdown: "click-outside-ignore" } },
    // ...
});
```

## Theme properties

Draw functions receive the theme object at `args.theme`. Useful properties:

| Property | Description |
|----------|-------------|
| `bgCell` | Cell background color |
| `bgBubble` | Default pill/badge background |
| `bgBubbleSelected` | Pill background when cell is selected |
| `textDark` | Primary text color |
| `textLight` | Secondary text color |
| `textBubble` | Text color inside pills |
| `borderColor` | Cell border color |
| `accentColor` | Accent/highlight color |
| `accentLight` | Light accent for selected ranges |
| `cellHorizontalPadding` | Horizontal padding inside cells (default: 8) |
| `cellVerticalPadding` | Vertical padding inside cells |
| `bubbleHeight` | Default pill height (default: 20) |
| `bubblePadding` | Padding inside pills (default: 6) |
| `bubbleMargin` | Space between pills (default: 4) |
| `roundingRadius` | Border radius for pills |

## Writing a plugin package

The recommended pattern for distributable plugins is a Python class that subclasses `dict`:

1. **Plugin config** — the class instance serializes naturally as a dict for `cellPlugins`
2. **Cell data factory** — `__call__` creates cell data dicts
3. **Embedded JS** — reads the JS file once at import time and sets `js` field

### Example: `dgg-dmc-cells`

[dgg-dmc-cells](https://github.com/bencivjan/dgg-dmc-cells) uses this pattern for DMC editor cells:

```python
import dash_mantine_components as dmc
from dgg_dmc_cells import DmcPlugin

# Create plugins — auto-detects single vs multi-select from component type
status = DmcPlugin("status", dmc.Select(data=["To Do", "In Progress", "Done"]),
                   color_map={"To Do": "#94a3b8", "In Progress": "#3b82f6", "Done": "#22c55e"})
tags = DmcPlugin("tags", dmc.MultiSelect(data=["Frontend", "Backend", "Bug"]))

GlideGrid(
    columns=[
        {"title": "Status", "id": "status", "type": "custom", "width": 150},
        {"title": "Tags", "id": "tags", "type": "custom", "width": 280},
    ],
    data=[{
        "status": status("In Progress"),
        "tags": tags([{"label": "Frontend", "color": "#8b5cf6"}]),
    }],
    cellPlugins=[status, tags],  # DmcPlugin is a dict subclass
)
```

No JS file copying, no extra imports — just create the plugin and use it.

### Plugin package structure

```
my-plugin-package/
├── my_plugin/
│   ├── __init__.py       # re-export plugin class
│   ├── plugin.py         # dict subclass with draw/editor/js config
│   └── assets/
│       └── myPlugin.js   # canvas draw + editor functions
└── pyproject.toml
```

### Key pitfalls

- **Kind name collisions**: Don't use reserved built-in kinds (listed above). Choose a unique prefix for your package.
- **Unstable editor references**: Always define editor components once via IIFE. Never create new function references inside `provideEditor`.
- **Portal click handling**: Add `click-outside-ignore` class to dropdown portals so Glide doesn't close the editor when users interact with them.
- **React access**: In injected JS, use `window.React` (available in Dash apps). Don't assume `React` is in scope — assign it locally: `var _React = window.React;`
