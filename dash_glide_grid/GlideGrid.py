# AUTO GENERATED FILE - DO NOT EDIT

import typing  # noqa: F401
from typing_extensions import TypedDict, NotRequired, Literal # noqa: F401
from dash.development.base_component import Component, _explicitize_args

ComponentType = typing.Union[
    str,
    int,
    float,
    Component,
    None,
    typing.Sequence[typing.Union[str, int, float, Component, None]],
]

NumberType = typing.Union[
    typing.SupportsFloat, typing.SupportsInt, typing.SupportsComplex
]


class GlideGrid(Component):
    """A GlideGrid component.
GlideGrid is a high-performance data grid component for Dash.
It wraps the Glide Data Grid library to provide an Excel-like grid experience
with support for millions of rows, multiple cell types, and rich interactions.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- allowDelete (boolean; default True):
    Controls whether the Delete key clears cell contents. When True
    (default), pressing Delete clears selected cells. When False,
    Delete key is disabled and deletePressed still fires for custom
    handling. Default: True.

- allowedFillDirections (a value equal to: 'horizontal', 'vertical', 'orthogonal', 'any'; default 'orthogonal'):
    Allowed directions for fill handle. Default: 'orthogonal' -
    'horizontal': Only fill left/right - 'vertical': Only fill up/down
    - 'orthogonal': Fill horizontally or vertically (not diagonal) -
    'any': Fill in any direction including diagonal.

- buttonClicked (dict; optional):
    Information about the last clicked button cell. Format: {\"col\":
    0, \"row\": 1, \"title\": \"Button Text\", \"timestamp\":
    1234567890}.

    `buttonClicked` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - title (string; optional)

    - timestamp (number; optional)

- canRedo (boolean; default False):
    Whether redo is available (read-only output prop). True when there
    are undone edits that can be redone.

- canUndo (boolean; default False):
    Whether undo is available (read-only output prop). True when there
    are edits that can be undone.

- cellActivated (dict; optional):
    Information about the last activated cell (Enter, Space, or
    double-click). Useful for implementing drill-down or detail views.
    Format: {\"col\": 0, \"row\": 1, \"timestamp\": 1234567890}.

    `cellActivated` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- cellActivationBehavior (a value equal to: 'double-click', 'second-click', 'single-click'; default 'second-click'):
    Controls when a cell is considered \"activated\" and will open for
    editing. - \"double-click\": Activate on double-click only -
    \"second-click\": Activate on second click (click selected cell
    again) - DEFAULT - \"single-click\": Activate immediately on
    single click  When activated, the cell fires onCellActivated and
    opens in edit mode. Default: \"second-click\".

- cellClicked (dict; optional):
    Information about the last clicked cell. Format: {\"col\": 0,
    \"row\": 1, \"timestamp\": 1234567890}.

    `cellClicked` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- cellContextMenu (dict; optional):
    Information about the last right-clicked cell. Useful for
    implementing cell context menus. Format: {\"col\": 0, \"row\": 1,
    \"timestamp\": 1234567890}.

    `cellContextMenu` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- cellEdited (dict; optional):
    Information about the last edited cell. Format: {\"col\": 0,
    \"row\": 1, \"value\": \"new value\", \"timestamp\": 1234567890}.

    `cellEdited` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - value (boolean | number | string | dict | list; optional)

    - timestamp (number; optional)

- cellsEdited (dict; optional):
    Information about batch cell edits (paste or fill operations).
    Fires when multiple cells are edited at once, such as when pasting
    data or using the fill handle. Format: {\"edits\": [{\"col\": 0,
    \"row\": 0, \"value\": \"x\"}, ...], \"count\": 5, \"timestamp\":
    1234567890}.

    `cellsEdited` is a dict with keys:

    - edits (list of dicts; optional)

        `edits` is a list of dicts with keys:

        - col (number; optional)

        - row (number; optional)

        - value (boolean | number | string | dict | list; optional)

    - count (number; optional)

    - timestamp (number; optional)

- className (string; optional):
    CSS class name to apply to the grid container.

- coercePasteValue (dict; optional):
    Client-side paste value coercion using JavaScript functions.
    Transforms pasted strings into proper cell types.  **Setup**:
    Create `assets/dashGlideGridFunctions.js` in your app folder:
    ```javascript var dggfuncs = window.dashGlideGridFunctions =
    window.dashGlideGridFunctions || {};  dggfuncs.parsePaste =
    function(val, cell) {     if (cell.kind === 'boolean') {
    return {             kind: 'boolean',             data:
    val.toLowerCase() === 'True' || val === '1'         };     }
    return undefined;  // Use default parsing }; ```  **Usage**:
    `coercePasteValue={\"function\": \"parsePaste(val, cell)\"}`
    **Return values**: - `GridCell object`: Use this transformed value
    - `undefined`: Use default paste behavior  **Available
    parameters**: `val` (pasted string), `cell` (target GridCell),
    `value` (alias for val).

    `coercePasteValue` is a dict with keys:

    - function (string; required)

- columnFilters (dict with strings as keys and values of type list of boolean | number | string | dict | lists; optional):
    Column filter state. Maps column index to array of selected
    values. Set to {} to clear all filters.  Example: {\"0\":
    [\"Active\", \"Pending\"], \"2\": [\"Sales\", \"Marketing\"]}
    This prop is bidirectional - you can read the current filter state
    and also set it from Dash to programmatically filter columns.

- columnMovable (boolean; optional):
    Allow column reordering by dragging column headers. Default: True.

- columnMoved (dict; optional):
    Information about the last column move (drag reorder). Fired when
    user drags a column header to a new position. Note: You must
    update the columns prop in your callback to effect the move.
    Format: {\"startIndex\": 0, \"endIndex\": 2, \"timestamp\":
    1234567890}.

    `columnMoved` is a dict with keys:

    - startIndex (number; optional)

    - endIndex (number; optional)

    - timestamp (number; optional)

- columnResize (boolean; default True):
    Allow column resizing by dragging column edges. Default: True.

- columnSelect (a value equal to: 'none', 'single', 'multi'; default 'none'):
    Column selection mode. Options: 'none', 'single', 'multi'.

- columnSelectionBlending (a value equal to: 'exclusive', 'mixed'; optional):
    How column selection blends with other selections. 'exclusive'
    clears other selections, 'mixed' allows combining. Default:
    'exclusive'.

- columnSelectionMode (a value equal to: 'auto', 'multi'; default 'auto'):
    Column selection modifier key behavior. - \"auto\": Requires
    Ctrl/Cmd for multi-column selection (default) - \"multi\": Allows
    multi-column selection without modifier keys Default: \"auto\".

- columnWidths (list of numbers; optional):
    Array of column widths (updated when columns are resized).
    Example: [200, 150, 300].

- columns (list of dicts; required):
    Array of column definitions. Each column must have at least a
    title and width. Example: [{\"title\": \"Name\", \"width\": 200,
    \"id\": \"name_col\"}].

    `columns` is a list of dicts with keys:

    - title (string; required):
        Column header text.

    - id (string; optional):
        Column identifier (defaults to title if not provided).

    - width (number; optional):
        Column width in pixels.

    - icon (string; optional):
        Icon name to display in header.

    - overlayIcon (string; optional):
        Overlay icon name.

    - hasMenu (boolean; optional):
        Whether column has a menu dropdown arrow.

    - filterable (boolean; optional):
        Whether this column is filterable. Shows filter menu with
        unique values.

    - sortable (boolean; optional):
        Whether this column is sortable (when grid-level
        sortable=True). Default: True.

    - group (string; optional):
        Group name for column grouping.

    - themeOverride (dict; optional):
        Column-specific theme overrides.

    - valueFormatter (dict; optional):
        Custom value formatter for display. Formats the cell value for
        display without changing the underlying data.  **Usage**:
        `valueFormatter={\"function\": \"formatCurrency(value)\"}`
        **Setup**: Create `assets/dashGlideGridFunctions.js`:
        ```javascript var dggfuncs = window.dashGlideGridFunctions =
        window.dashGlideGridFunctions || {};  dggfuncs.formatCurrency
        = function(value) {     return new Intl.NumberFormat('en-US',
        {         style: 'currency',         currency: 'USD'
        }).format(value); }; ```  **Parameters passed to function**: -
        `value`: The cell's raw data value - `cell`: The full cell
        object - `row`: Row index - `col`: Column index  **Return**:
        String to display (or undefined to use default).

        `valueFormatter` is a dict with keys:

        - function (string; required)

- copyHeaders (boolean; default False):
    Include column headers when copying to clipboard. Default: False.

- data (list of dicts; required):
    Array of row data objects (records format). Each row is a dict
    where keys match column `id` values. Compatible with
    `df.to_dict('records')`.  **Example**: ```python columns = [
    {'title': 'Name', 'id': 'name'},     {'title': 'Price', 'id':
    'price'}, ] data = [     {'name': 'Laptop', 'price': 1299.99},
    {'name': 'Mouse', 'price': 29.99}, ] # Or from pandas: data =
    df.to_dict('records') ```  **Simple values** (auto-detected
    types): - String → Text cell - Number → Number cell - Boolean →
    Checkbox cell - None/undefined → Empty cell  **Cell object
    properties** (for explicit control): - `kind`: Cell type -
    \"text\", \"number\", \"boolean\", \"markdown\", \"uri\",
    \"image\", \"bubble\", \"dropdown-cell\", \"multi-select-cell\" -
    `data`: The cell's value (type depends on kind) - `allowOverlay`:
    (boolean) If True, double-click opens editor popup. Required for
    editing. Default: True - `copyData`: (string) Text copied to
    clipboard on Ctrl+C. Required for copy to work on custom cells -
    `displayData`: (string) Text shown in cell (for text/number).
    Defaults to data value - `readonly`: (boolean) If True, cell
    cannot be edited even with allowOverlay - `themeOverride`:
    (object) Custom colors for this cell, e.g. {\"bgCell\": \"#fff\"}
    - `span`: ([start, end]) For merged cells - column indices this
    cell spans - `contentAlign`: (\"left\"|\"right\"|\"center\") Text
    alignment hint for the cell - `cursor`: (string) CSS cursor
    override when hovering, e.g. \"pointer\"  **Number cell props**
    (kind: \"number\"): - `fixedDecimals`: (number) Fixed number of
    decimal places in editor - `allowNegative`: (boolean) Allow
    negative numbers. Default: True - `thousandSeparator`:
    (boolean|string) Add thousand separators. True for default, or
    custom string - `decimalSeparator`: (string) Custom decimal
    separator, e.g. \",\" for European format  **Boolean cell props**
    (kind: \"boolean\"): - `maxSize`: (number) Maximum size of the
    checkbox in pixels  **Uri cell props** (kind: \"uri\"): -
    `hoverEffect`: (boolean) If True, underline on hover with pointer
    cursor  **Image cell props** (kind: \"image\"): - `rounding`:
    (number) Corner radius for rounded images in pixels -
    `displayData`: (string[]) Reduced-size image URLs for display
    (full URLs in data for overlay)  **Dropdown cell example**: ``` {
    \"kind\": \"dropdown-cell\",   \"data\": {     \"value\":
    \"active\",     \"options\": [{\"value\": \"active\", \"label\":
    \"Active\", \"color\": \"#10b981\"}],     \"allowedValues\":
    [\"active\", \"pending\"]   },   \"allowOverlay\": True,
    \"copyData\": \"active\" } ```  **Multi-select cell example**: ```
    {   \"kind\": \"multi-select-cell\",   \"data\": {     \"values\":
    [\"python\", \"react\"],     \"options\": [{\"value\": \"python\",
    \"label\": \"Python\", \"color\": \"#3776ab\"}],
    \"allowedValues\": [\"python\", \"react\", \"sql\"]   },
    \"allowOverlay\": True,   \"copyData\": \"python, react\" } ```.

- deletePressed (dict; optional):
    Information about delete key press events. Fires when user presses
    Delete/Backspace on selected cells. Use with allowDelete prop to
    control whether deletion is allowed. Format: {\"cells\":
    [{\"col\": 0, \"row\": 0}, ...], \"rows\": [0, 1], \"columns\":
    [2], \"timestamp\": 1234567890}.

    `deletePressed` is a dict with keys:

    - cells (list of dicts; optional)

        `cells` is a list of dicts with keys:

        - col (number; optional)

        - row (number; optional)

    - rows (list of numbers; optional)

    - columns (list of numbers; optional)

    - timestamp (number; optional)

- dragOverCell (dict; optional):
    Information about external drag-over events on cells. Fires when
    something is dragged over a cell from outside the grid. Format:
    {\"col\": 0, \"row\": 1, \"timestamp\": 1234567890}.

    `dragOverCell` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- dragStarted (dict; optional):
    Information about drag start events (when isDraggable is enabled).
    Format: {\"col\": 0, \"row\": 1, \"timestamp\": 1234567890}.

    `dragStarted` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- drawCell (dict; optional):
    Custom cell rendering using JavaScript Canvas API. Allows complete
    control over how cells are drawn.  **Usage**:
    `drawCell={\"function\": \"drawCircularWell(ctx, cell, theme,
    rect, col, row, hoverAmount, highlighted, cellData, rowData,
    drawContent)\"}`  **Return values**: - `True`: Custom drawing
    complete, skip default rendering - `False` or `undefined`: Draw
    default content after custom drawing  **Available parameters**: -
    `ctx`: CanvasRenderingContext2D for drawing - `cell`: The GridCell
    object - `theme`: Theme object with colors - `rect`: {x, y, width,
    height} of the cell - `col`: Column index - `row`: Row index -
    `hoverAmount`: 0-1 hover state - `highlighted`: Whether cell is
    selected - `cellData`: The cell data from your data array -
    `rowData`: The full row data array - `drawContent`: Function to
    draw default cell content.

    `drawCell` is a dict with keys:

    - function (string; required)

- drawFocusRing (boolean; default True):
    Show focus ring around selected cell. Default: True.

- drawHeader (dict; optional):
    Custom header rendering using JavaScript Canvas API. Allows
    complete control over how column headers are drawn.  **Usage**:
    `drawHeader={\"function\": \"drawCenteredHeader(ctx, column,
    theme, rect, columnIndex, isSelected, hoverAmount,
    drawContent)\"}`  **Available parameters**: - `ctx`:
    CanvasRenderingContext2D for drawing - `column`: The column
    definition object - `theme`: Theme object with colors - `rect`:
    {x, y, width, height} of the header cell - `columnIndex`: Column
    index - `isSelected`: Whether column is selected - `hoverAmount`:
    0-1 hover state - `drawContent`: Function to draw default header
    content.

    `drawHeader` is a dict with keys:

    - function (string; required)

- droppedOnCell (dict; optional):
    Information about external drop events on cells. Fires when
    something is dropped onto a cell from outside the grid. Format:
    {\"col\": 0, \"row\": 1, \"timestamp\": 1234567890}.

    `droppedOnCell` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - timestamp (number; optional)

- editOnType (boolean; default True):
    When True, typing on a selected cell will immediately start
    editing. When False, users must explicitly activate the cell
    (double-click, Enter, etc.) before typing will enter edit mode.
    Default: True.

- editorScrollBehavior (a value equal to: 'default', 'close-overlay-on-scroll', 'lock-scroll'; default 'default'):
    Controls how the grid behaves when the user scrolls while an
    editor is open. - \"default\": Editor stays at original position
    (standard Glide behavior) - \"close-overlay-on-scroll\": Entire
    editor overlay closes on scroll - \"lock-scroll\": Scrolling is
    prevented while editor is open Default: \"default\".

- enableCopyPaste (boolean; default True):
    Enable copy/paste functionality. Default: True.

- enableUndoRedo (boolean; default False):
    Enable undo/redo functionality. When enabled, cell edits can be
    undone/redone using Cmd+Z/Cmd+Shift+Z (Mac) or Ctrl+Z/Ctrl+Y
    (Windows/Linux), or programmatically via undoRedoAction. Default:
    False.

- experimental (dict; optional):
    Experimental options. These are not considered stable API. Use
    with caution as they may change or be removed.  Options: -
    disableAccessibilityTree: Disable the accessibility tree for
    performance - disableMinimumCellWidth: Allow cells narrower than
    the default minimum - enableFirefoxRescaling: Enable rescaling
    fixes for Firefox - hyperWrapping: Enable hyper text wrapping mode
    - isSubGrid: Mark this grid as a sub-grid - kineticScrollPerfHack:
    Performance hack for kinetic scrolling - paddingBottom: Extra
    padding at the bottom - paddingRight: Extra padding on the right -
    renderStrategy: \"single-buffer\", \"double-buffer\", or
    \"direct\" - scrollbarWidthOverride: Override the detected
    scrollbar width - strict: Enable strict mode for debugging.

    `experimental` is a dict with keys:

    - disableAccessibilityTree (boolean; optional)

    - disableMinimumCellWidth (boolean; optional)

    - enableFirefoxRescaling (boolean; optional)

    - hyperWrapping (boolean; optional)

    - isSubGrid (boolean; optional)

    - kineticScrollPerfHack (boolean; optional)

    - paddingBottom (number; optional)

    - paddingRight (number; optional)

    - renderStrategy (a value equal to: 'single-buffer', 'double-buffer', 'direct'; optional)

    - scrollbarWidthOverride (number; optional)

    - strict (boolean; optional)

- fillHandle (boolean; default False):
    Enable fill handle for dragging to fill cells (Excel-like).
    Default: False When enabled, users can drag a small square at the
    bottom-right of a selection to fill adjacent cells with the
    selected pattern.

- fixedShadowX (boolean; default True):
    Show shadow behind frozen columns. Default: True.

- fixedShadowY (boolean; default True):
    Show shadow behind header row(s). Default: True.

- freezeColumns (number; default 0):
    Number of columns to freeze on the left side. Default: 0.

- freezeTrailingRows (number; default 0):
    Number of rows to freeze at the bottom of the grid. Default: 0
    Useful for totals or summary rows.

- getRowThemeOverride (dict; optional):
    Client-side row theme override using JavaScript functions. Allows
    dynamic row styling based on row data (conditional formatting).
    **Setup**: Create `assets/dashGlideGridFunctions.js` in your app
    folder: ```javascript var dggfuncs = window.dashGlideGridFunctions
    =     window.dashGlideGridFunctions || {};
    dggfuncs.rowThemeByStatus = function(row, rowData) {     if
    (!rowData) return undefined;     // rowData is a dict with keys
    matching column ids     const status = rowData.status;  // e.g.,
    column with id='status'     if (status === 'error') {
    return { bgCell: 'rgba(255, 0, 0, 0.1)' };  // Light red     }
    if (status === 'success') {         return { bgCell: 'rgba(0, 255,
    0, 0.1)' };  // Light green     }     return undefined;  //
    Default theme }; ```  **Usage**:
    `getRowThemeOverride={\"function\": \"rowThemeByStatus(row,
    rowData)\"}`  **Return values**: - `Theme object`: Override theme
    properties for this row (e.g., bgCell, textDark) - `undefined`:
    Use default theme  **Available parameters**: `row` (row index),
    `rowData` (dict of cell values keyed by column id), `data` (full
    grid data).

    `getRowThemeOverride` is a dict with keys:

    - function (string; required)

- groupHeaderClicked (dict; optional):
    Information about the last clicked group header. Format: {\"col\":
    0, \"group\": \"Group Name\", \"timestamp\": 1234567890}.

    `groupHeaderClicked` is a dict with keys:

    - col (number; optional)

    - group (string; optional)

    - timestamp (number; optional)

- groupHeaderHeight (number; optional):
    Height of column group headers in pixels. Defaults to
    headerHeight.

- headerClicked (dict; optional):
    Information about the last clicked column header. Useful for
    implementing column sorting. Format: {\"col\": 0, \"timestamp\":
    1234567890}.

    `headerClicked` is a dict with keys:

    - col (number; optional)

    - timestamp (number; optional)

- headerContextMenu (dict; optional):
    Information about the last right-clicked column header. Useful for
    implementing column context menus. Format: {\"col\": 0,
    \"timestamp\": 1234567890}.

    `headerContextMenu` is a dict with keys:

    - col (number; optional)

    - timestamp (number; optional)

- headerHeight (number; default 36):
    Height of the header row in pixels. Default: 36.

- headerMenuClicked (dict; optional):
    Information about the last clicked header menu icon. Fired when
    user clicks the dropdown arrow on columns with hasMenu=True.
    Format: {\"col\": 0, \"screenX\": 100, \"screenY\": 50,
    \"timestamp\": 1234567890}.

    `headerMenuClicked` is a dict with keys:

    - col (number; optional)

    - screenX (number; optional)

    - screenY (number; optional)

    - timestamp (number; optional)

- headerMenuConfig (dict; optional):
    Configuration for the header filter menu.  - customItems: Array of
    custom menu items with onClick handlers - filterActiveColor: Color
    for header when filter is active (default: theme accentColor)
    Example: ``` headerMenuConfig={     \"filterActiveColor\":
    \"#2563eb\",     \"customItems\": [         {             \"id\":
    \"export\",             \"label\": \"Export Column\",
    \"onClick\": {\"function\": \"exportColumn(col, columns, data)\"}
    }     ] } ```.

    `headerMenuConfig` is a dict with keys:

    - menuIcon (a value equal to: 'chevron', 'hamburger', 'dots'; optional)

    - filterActiveColor (string; optional)

    - customItems (list of dicts; optional)

        `customItems` is a list of dicts with keys:

        - id (string; required)

        - label (string; required)

        - icon (string; optional)

        - onClick (dict; optional)

            `onClick` is a dict with keys:

            - function (string; required)

        - dividerAfter (boolean; optional)

- headerMenuItemClicked (dict; optional):
    Information about the last clicked custom menu item. Format:
    {\"col\": 0, \"itemId\": \"export\", \"timestamp\": 1234567890}.

    `headerMenuItemClicked` is a dict with keys:

    - col (number; optional)

    - itemId (string; optional)

    - timestamp (number; optional)

- height (number | string; default 400):
    Container height (REQUIRED). Can be a number (pixels) or string
    (\"600px\", \"100vh\"). The grid requires an explicit height to
    render properly.

- highlightRegions (list of dicts; optional):
    Array of highlight regions to display on the grid. Each region is
    drawn with a background color and dashed border. Useful for
    conditional formatting, search highlights, or validation errors.
    Format: [{\"color\": \"rgba(255,0,0,0.2)\", \"range\": {\"x\": 0,
    \"y\": 0, \"width\": 2, \"height\": 3}}]  - color: CSS color
    string (use rgba for transparency to allow overlapping regions to
    blend) - range: Rectangle defining the region (x=start column,
    y=start row, width=columns, height=rows) - style: Border style -
    \"dashed\" (default), \"solid\", \"solid-outline\", or
    \"no-outline\".

    `highlightRegions` is a list of dicts with keys:

    - color (string; required)

    - range (dict; required)

        `range` is a dict with keys:

        - x (number; required)

        - y (number; required)

        - width (number; required)

        - height (number; required)

    - style (a value equal to: "dashed", "solid", "solid-outline", "no-outline"; optional)

- hoverRow (boolean; default False):
    Enable row hover effect. When True, the entire row is visually
    highlighted when the mouse hovers over any cell in that row.
    Customize the color via theme.bgRowHovered (default: 'rgba(0, 0,
    0, 0.04)'). Default: False.

- isDraggable (boolean | a value equal to: 'header', 'cell'; optional):
    Makes the grid draggable for external drag-and-drop operations. -
    True: Entire grid is draggable - \"header\": Only headers are
    draggable - \"cell\": Only cells are draggable  When enabled, the
    dragStarted output will fire with drag information.

- itemHovered (dict; optional):
    Information about the currently hovered item. Kind can be:
    \"cell\", \"header\", \"group-header\", \"out-of-bounds\" Format:
    {\"col\": 0, \"row\": 1, \"kind\": \"cell\", \"timestamp\":
    1234567890}.

    `itemHovered` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - kind (string; optional)

    - timestamp (number; optional)

- keybindings (dict; optional):
    Customize keyboard shortcuts. Each key can be set to: - True:
    Enable the default keybinding - False: Disable the keybinding -
    string: Custom key combination (e.g., \"ctrl+shift+c\")  Available
    keybindings: - Navigation: goToFirstColumn, goToLastColumn,
    goToFirstCell, goToLastCell,   goToFirstRow, goToLastRow,
    goToNextPage, goToPreviousPage,   goUpCell, goDownCell,
    goLeftCell, goRightCell - Selection: selectAll, selectRow,
    selectColumn, selectToFirstColumn,   selectToLastColumn,
    selectToFirstCell, selectToLastCell,   selectGrowUp,
    selectGrowDown, selectGrowLeft, selectGrowRight - Actions: copy,
    cut, paste, delete, clear, search, activateCell,   downFill,
    rightFill, scrollToSelectedCell - Overlay: closeOverlay,
    acceptOverlayDown, acceptOverlayUp,   acceptOverlayLeft,
    acceptOverlayRight.

- linkClicked (dict; optional):
    Information about the last clicked link in a links cell. Format:
    {\"col\": 0, \"row\": 1, \"href\": \"https://example.com\",
    \"title\": \"Link\", \"linkIndex\": 0, \"timestamp\": 1234567890}.

    `linkClicked` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - href (string; optional)

    - title (string; optional)

    - linkIndex (number; optional)

    - timestamp (number; optional)

- maxColumnAutoWidth (number; optional):
    Maximum width for auto-sized columns. Defaults to maxColumnWidth.

- maxColumnWidth (number; default 500):
    Maximum width users can resize columns to. Default: 500.

- maxUndoSteps (number; default 50):
    Maximum number of undo steps to track. Older edits beyond this
    limit will be discarded. Default: 50.

- minColumnWidth (number; default 50):
    Minimum width users can resize columns to. Default: 50.

- mouseMove (dict; optional):
    Information about mouse movement over the grid. Fires on every
    mouse move, providing raw position data. More granular than
    itemHovered - useful for custom tooltips or highlighting. Format:
    {\"col\": 0, \"row\": 1, \"kind\": \"cell\", \"localEventX\": 150,
    \"localEventY\": 75, \"timestamp\": 1234567890}.

    `mouseMove` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - kind (string; optional)

    - localEventX (number; optional)

    - localEventY (number; optional)

    - timestamp (number; optional)

- nClicks (number; default 0):
    Total number of cell clicks (increments with each click).

- overscrollX (number; default 0):
    Extra horizontal scroll space beyond content. Default: 0.

- overscrollY (number; default 0):
    Extra vertical scroll space beyond content. Default: 0.

- preventDiagonalScrolling (boolean; default False):
    Only allow horizontal or vertical scrolling, not diagonal.
    Default: False.

- rangeSelect (a value equal to: 'none', 'cell', 'rect', 'multi-cell', 'multi-rect'; default 'rect'):
    Range selection mode. Options: 'none', 'cell', 'rect',
    'multi-cell', 'multi-rect'.

- rangeSelectionBlending (a value equal to: 'exclusive', 'mixed'; optional):
    How range selection blends with other selections. 'exclusive'
    clears other selections, 'mixed' allows combining. Default:
    'exclusive'.

- rangeSelectionColumnSpanning (boolean; default True):
    When True, range selections can span across multiple columns. When
    False, range selections are restricted to a single column only.
    Useful for spreadsheet-like interfaces where column-based
    selection is preferred. Default: True.

- readonly (boolean; default False):
    Make the entire grid read-only. Default: False.

- redrawTrigger (number | string; optional):
    Trigger a grid redraw. Change this value (e.g., increment a
    counter or use timestamp) to force the grid to re-render. Useful
    for custom drawCell functions that need periodic updates
    (animations, hover effects, etc.).

- rowAppended (dict; optional):
    Information about the last row append event. Fired when user
    clicks on the trailing row to add a new row. Note: You must handle
    adding the new row to your data in your callback. Format:
    {\"timestamp\": 1234567890}.

    `rowAppended` is a dict with keys:

    - timestamp (number; optional)

- rowHeight (dict; default 34):
    Height of each data row in pixels, or a function for variable row
    heights. Can be a number (e.g., 34) or an object with a function
    string. Function format: {\"function\":
    \"getRowHeight(rowIndex)\"} where the function receives rowIndex
    and should return a number. Default: 34.

    `rowHeight` is a number | dict with keys:

    - function (string; required)

- rowMarkerStartIndex (number; default 1):
    Starting index for row numbers. Default: 1.

- rowMarkerTheme (dict; optional):
    Theme overrides for the row marker column.

- rowMarkerWidth (number; optional):
    Width of the row marker column in pixels. Auto-calculated if not
    set.

- rowMarkers (a value equal to: 'none', 'number', 'checkbox', 'both', 'checkbox-visible', 'clickable-number'; default 'none'):
    Row marker style. Options: - 'none': No row markers - 'number':
    Show row numbers - 'checkbox': Show selection checkboxes (on
    hover) - 'both': Show both numbers and checkboxes -
    'checkbox-visible': Always show checkboxes - 'clickable-number':
    Row numbers act as selection buttons.

- rowMovable (boolean; optional):
    Allow row reordering by dragging row markers. Default: True Note:
    rowMarkers must be enabled for row moving to work.

- rowMoved (dict; optional):
    Information about the last row move (drag reorder). Fired when
    user drags a row marker to a new position. Requires rowMarkers to
    be set (not 'none') to enable row dragging. Note: You must update
    the data prop in your callback to effect the move. Format:
    {\"startIndex\": 0, \"endIndex\": 2, \"timestamp\": 1234567890}.

    `rowMoved` is a dict with keys:

    - startIndex (number; optional)

    - endIndex (number; optional)

    - timestamp (number; optional)

- rowSelect (a value equal to: 'none', 'single', 'multi'; default 'none'):
    Row selection mode. Options: 'none', 'single', 'multi'.

- rowSelectionBlending (a value equal to: 'exclusive', 'mixed'; optional):
    How row selection blends with other selections. 'exclusive' clears
    other selections, 'mixed' allows combining. Default: 'exclusive'.

- rowSelectionMode (a value equal to: 'auto', 'multi'; default 'auto'):
    Row selection behavior. 'auto' requires modifier keys for
    multi-select, 'multi' allows multi-select without modifiers.
    Default: 'auto'.

- rows (number; optional):
    Number of rows to display. If not provided, inferred from
    data.length.

- scaleToRem (boolean; default False):
    Scale theme elements to match rem sizing. Default: False.

- scrollOffsetX (number; optional):
    Initial horizontal scroll offset in pixels. Applied on mount.

- scrollOffsetY (number; optional):
    Initial vertical scroll offset in pixels. Applied on mount.

- scrollToActiveCell (boolean; default True):
    When True, the grid automatically scrolls to keep the active cell
    visible when selection changes via keyboard navigation. When
    False, the active cell may scroll out of view. Default: True.

- scrollToCell (dict; optional):
    Programmatically scroll the grid to a specific cell. When this
    prop changes, the grid will scroll to bring the specified cell
    into view.  Format: {\"col\": 5, \"row\": 10}  Optional
    properties: - direction: \"horizontal\" | \"vertical\" | \"both\"
    (default: \"both\") - paddingX: number - horizontal padding in
    pixels (default: 0) - paddingY: number - vertical padding in
    pixels (default: 0) - hAlign: \"start\" | \"center\" | \"end\" -
    horizontal alignment (default: \"start\") - vAlign: \"start\" |
    \"center\" | \"end\" - vertical alignment (default: \"start\")
    Example: {\"col\": 5, \"row\": 10, \"hAlign\": \"center\",
    \"vAlign\": \"center\"}.

    `scrollToCell` is a dict with keys:

    - col (number; required)

    - row (number; required)

    - direction (a value equal to: 'horizontal', 'vertical', 'both'; optional)

    - paddingX (number; optional)

    - paddingY (number; optional)

    - hAlign (a value equal to: 'start', 'center', 'end'; optional)

    - vAlign (a value equal to: 'start', 'center', 'end'; optional)

- searchValue (string; default ''):
    The current search query string. Updated when user types in the
    search box. Can be set from Python to programmatically trigger a
    search.

- selectedCell (dict; optional):
    Currently selected cell. Updated when user clicks a cell. Format:
    {\"col\": 0, \"row\": 1}.

    `selectedCell` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

- selectedColumns (list of numbers; optional):
    Array of selected column indices. Updated with column selection.
    Example: [0, 1].

- selectedRange (dict; optional):
    Currently selected range. Updated with range selection. Format:
    {\"startCol\": 0, \"startRow\": 0, \"endCol\": 2, \"endRow\": 3}.

    `selectedRange` is a dict with keys:

    - startCol (number; optional)

    - startRow (number; optional)

    - endCol (number; optional)

    - endRow (number; optional)

- selectedRanges (list of dicts; optional):
    Additional selected ranges when using rangeSelect=\"multi-rect\"
    mode. Updated when user Ctrl/Cmd+clicks to add additional
    selections. Each range has the same format as selectedRange. The
    primary selection is in selectedRange, additional selections are
    here.

    `selectedRanges` is a list of dicts with keys:

    - startCol (number; optional)

    - startRow (number; optional)

    - endCol (number; optional)

    - endRow (number; optional)

- selectedRows (list of numbers; optional):
    Array of selected row indices. Updated with row selection.
    Example: [0, 2, 5].

- selectionColumnMin (number; optional):
    Minimum column index that can be selected. Columns with index less
    than this value cannot be selected or included in range
    selections. Useful for preventing selection of row label columns.
    Default: 0 (no restriction).

- showCellFlash (boolean | list of a value equal to: "edit", "paste", "undo", "redo"s; default False):
    Enable cell flash effect when cells are changed. When enabled,
    cells will briefly highlight and fade out to indicate changes. Can
    be: - True: Flash on all operations (edit, paste, undo, redo) -
    False: No flash (default) - Array of strings: Flash only on
    specified operations.   Valid values: \"edit\", \"paste\",
    \"undo\", \"redo\"   Example: [\"paste\", \"undo\", \"redo\"] to
    flash on paste and undo/redo but not regular edits.

- showSearch (boolean; default False):
    Show/hide the built-in search interface. When enabled, displays a
    search box that allows users to search through grid data. Use
    searchValue to control or read the current search query. Default:
    False.

- smoothScrollX (boolean; default True):
    Enable smooth horizontal scrolling. Default: True.

- smoothScrollY (boolean; default True):
    Enable smooth vertical scrolling. Default: True.

- sortColumns (list of dicts; optional):
    Array of sorted columns. Each item specifies a column index and
    direction. For single-column sort: [{\"columnIndex\": 0,
    \"direction\": \"asc\"}] For multi-column sort: [{\"columnIndex\":
    0, \"direction\": \"asc\"}, {\"columnIndex\": 2, \"direction\":
    \"desc\"}] The order determines sort priority (first item is
    primary sort).

    `sortColumns` is a list of dicts with keys:

    - columnIndex (number; required):
        Column index to sort by.

    - direction (a value equal to: 'asc', 'desc'; required):
        Sort direction: \"asc\" or \"desc\".

- sortable (boolean; default False):
    Enable built-in column sorting. When True, clicking column headers
    will cycle through sort states (ascending → descending → none).
    Shift+click enables multi-column sorting. Default: False.

- sortingOrder (list of a value equal to: 'asc', 'desc', nulls; default ['asc', 'desc', None]):
    Defines the cycle order when clicking column headers. Default:
    [\"asc\", \"desc\", None] (ascending → descending → unsorted)
    Example: [\"asc\", \"desc\"] (never clears sort).

- spanRangeBehavior (a value equal to: 'default', 'allowPartial'; optional):
    How to handle spans in range selection. 'default' expands to
    include full spans, 'allowPartial' allows partial span selection.

- theme (dict; optional):
    Custom theme object to style the grid. Properties use camelCase.
    Example: {\"accentColor\": \"#2563eb\", \"bgCell\": \"#ffffff\"}.

    `theme` is a dict with keys:

    - accentColor (string; optional)

    - accentLight (string; optional)

    - accentFg (string; optional)

    - textDark (string; optional)

    - textMedium (string; optional)

    - textLight (string; optional)

    - textBubble (string; optional)

    - bgIconHeader (string; optional)

    - fgIconHeader (string; optional)

    - textHeader (string; optional)

    - textHeaderSelected (string; optional)

    - textGroupHeader (string; optional)

    - bgCell (string; optional)

    - bgCellMedium (string; optional)

    - bgHeader (string; optional)

    - bgHeaderHasFocus (string; optional)

    - bgHeaderHovered (string; optional)

    - bgBubble (string; optional)

    - bgBubbleSelected (string; optional)

    - bgSearchResult (string; optional)

    - borderColor (string; optional)

    - drilldownBorder (string; optional)

    - linkColor (string; optional)

    - headerFontStyle (string; optional)

    - baseFontStyle (string; optional)

    - fontFamily (string; optional)

    - editorFontSize (string; optional)

    - lineHeight (number; optional)

    - horizontalBorderColor (string; optional)

    - cellHorizontalPadding (number; optional)

    - cellVerticalPadding (number; optional)

- trailingRowOptions (dict; optional):
    Configuration options for the trailing row used to add new rows.
    When trailingRowOptions is provided, a blank row appears at the
    bottom of the grid. Clicking on this row triggers the rowAppended
    callback.  - hint: Text shown in the empty row cells (e.g., \"Add
    new...\") - sticky: If True, the trailing row stays visible at the
    bottom while scrolling - tint: If True, applies a tinted
    background to the trailing row - addIcon: Icon to show in the
    trailing row (optional) - targetColumn: Column index that
    activates the add action (optional).

    `trailingRowOptions` is a dict with keys:

    - hint (string; optional)

    - sticky (boolean; optional)

    - tint (boolean; optional)

    - addIcon (string; optional)

    - targetColumn (number; optional)

- trapFocus (boolean; default False):
    When True, prevents focus from leaving the grid via Tab key or
    arrow key navigation. Useful for modal-like grid experiences or
    when the grid should capture all keyboard input. Default: False.

- treeNodeToggled (dict; optional):
    Information about the last toggled tree node. Format: {\"col\": 0,
    \"row\": 1, \"isOpen\": True, \"depth\": 0, \"text\": \"Node\",
    \"timestamp\": 1234567890}.

    `treeNodeToggled` is a dict with keys:

    - col (number; optional)

    - row (number; optional)

    - isOpen (boolean; optional)

    - depth (number; optional)

    - text (string; optional)

    - timestamp (number; optional)

- undoRedoAction (dict; optional):
    Trigger undo or redo programmatically from Dash. Set this prop to
    trigger an undo or redo action. Format: {\"action\":
    \"undo\"|\"redo\", \"timestamp\": 1234567890} The timestamp is
    used to detect changes and should be unique for each action.

    `undoRedoAction` is a dict with keys:

    - action (a value equal to: 'undo', 'redo'; required)

    - timestamp (number; required)

- undoRedoPerformed (dict; optional):
    Information about the last undo/redo operation performed
    (read-only output prop). Emitted when an undo or redo action is
    performed. Format: {\"action\": \"undo\"|\"redo\", \"timestamp\":
    1234567890}.

    `undoRedoPerformed` is a dict with keys:

    - action (a value equal to: 'undo', 'redo'; optional)

    - timestamp (number; optional)

- unselectableColumns (list of numbers; optional):
    Array of column indices that cannot be selected. Clicks on cells
    in these columns are ignored (selection stays where it is). Useful
    for creating unselectable label columns or border columns.

- unselectableRows (list of numbers; optional):
    Array of row indices that cannot be selected. Clicks on cells in
    these rows are ignored (selection stays where it is). Useful for
    creating unselectable header rows or border rows.

- validateCell (dict; optional):
    Client-side cell validation using JavaScript functions. Allows
    synchronous validation before edits are applied.  **Setup**:
    Create `assets/dashGlideGridFunctions.js` in your app folder:
    ```javascript var dggfuncs = window.dashGlideGridFunctions =
    window.dashGlideGridFunctions || {};  dggfuncs.validatePositive =
    function(cell, newValue) {     return newValue.data > 0;  // False
    rejects, True accepts }; ```  **Usage**:
    `validateCell={\"function\": \"validatePositive(cell,
    newValue)\"}`  **Return values**: - `False`: Reject the edit
    (visual feedback shown to user) - `True`: Accept the edit -
    `GridCell object`: Coerce/transform the value  **Available
    parameters**: `cell` ([col, row]), `newValue` (GridCell), `col`,
    `row`.

    `validateCell` is a dict with keys:

    - function (string; required)

- verticalBorder (boolean; default True):
    Show vertical borders between columns. Default: True.

- visibleRegion (dict; optional):
    Information about the currently visible region of the grid.
    Updated when user scrolls or resizes the grid. Format: {\"x\": 0,
    \"y\": 0, \"width\": 10, \"height\": 20, \"tx\": 0, \"ty\": 0}.

    `visibleRegion` is a dict with keys:

    - x (number; optional)

    - y (number; optional)

    - width (number; optional)

    - height (number; optional)

    - tx (number; optional)

    - ty (number; optional)

- visibleRowIndices (list of numbers; optional):
    Array of visible row indices after filtering (original data
    indices). This is an output prop that updates when filters change.

- width (number | string; default '100%'):
    Container width. Can be a number (pixels) or string. Defaults to
    \"100%\"."""
    _children_props: typing.List[str] = []
    _base_nodes = ['children']
    _namespace = 'dash_glide_grid'
    _type = 'GlideGrid'
    ColumnsValueFormatter = TypedDict(
        "ColumnsValueFormatter",
            {
            "function": str
        }
    )

    Columns = TypedDict(
        "Columns",
            {
            "title": str,
            "id": NotRequired[str],
            "width": NotRequired[NumberType],
            "icon": NotRequired[str],
            "overlayIcon": NotRequired[str],
            "hasMenu": NotRequired[bool],
            "filterable": NotRequired[bool],
            "sortable": NotRequired[bool],
            "group": NotRequired[str],
            "themeOverride": NotRequired[dict],
            "valueFormatter": NotRequired["ColumnsValueFormatter"]
        }
    )

    RowHeight = TypedDict(
        "RowHeight",
            {
            "function": str
        }
    )

    Theme = TypedDict(
        "Theme",
            {
            "accentColor": NotRequired[str],
            "accentLight": NotRequired[str],
            "accentFg": NotRequired[str],
            "textDark": NotRequired[str],
            "textMedium": NotRequired[str],
            "textLight": NotRequired[str],
            "textBubble": NotRequired[str],
            "bgIconHeader": NotRequired[str],
            "fgIconHeader": NotRequired[str],
            "textHeader": NotRequired[str],
            "textHeaderSelected": NotRequired[str],
            "textGroupHeader": NotRequired[str],
            "bgCell": NotRequired[str],
            "bgCellMedium": NotRequired[str],
            "bgHeader": NotRequired[str],
            "bgHeaderHasFocus": NotRequired[str],
            "bgHeaderHovered": NotRequired[str],
            "bgBubble": NotRequired[str],
            "bgBubbleSelected": NotRequired[str],
            "bgSearchResult": NotRequired[str],
            "borderColor": NotRequired[str],
            "drilldownBorder": NotRequired[str],
            "linkColor": NotRequired[str],
            "headerFontStyle": NotRequired[str],
            "baseFontStyle": NotRequired[str],
            "fontFamily": NotRequired[str],
            "editorFontSize": NotRequired[str],
            "lineHeight": NotRequired[NumberType],
            "horizontalBorderColor": NotRequired[str],
            "cellHorizontalPadding": NotRequired[NumberType],
            "cellVerticalPadding": NotRequired[NumberType]
        }
    )

    SelectedCell = TypedDict(
        "SelectedCell",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType]
        }
    )

    SelectedRange = TypedDict(
        "SelectedRange",
            {
            "startCol": NotRequired[NumberType],
            "startRow": NotRequired[NumberType],
            "endCol": NotRequired[NumberType],
            "endRow": NotRequired[NumberType]
        }
    )

    SelectedRanges = TypedDict(
        "SelectedRanges",
            {
            "startCol": NotRequired[NumberType],
            "startRow": NotRequired[NumberType],
            "endCol": NotRequired[NumberType],
            "endRow": NotRequired[NumberType]
        }
    )

    CellEdited = TypedDict(
        "CellEdited",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "value": NotRequired[typing.Any],
            "timestamp": NotRequired[NumberType]
        }
    )

    CellClicked = TypedDict(
        "CellClicked",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    ButtonClicked = TypedDict(
        "ButtonClicked",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "title": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    LinkClicked = TypedDict(
        "LinkClicked",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "href": NotRequired[str],
            "title": NotRequired[str],
            "linkIndex": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    TreeNodeToggled = TypedDict(
        "TreeNodeToggled",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "isOpen": NotRequired[bool],
            "depth": NotRequired[NumberType],
            "text": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    HeaderClicked = TypedDict(
        "HeaderClicked",
            {
            "col": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    HeaderContextMenu = TypedDict(
        "HeaderContextMenu",
            {
            "col": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    HeaderMenuClicked = TypedDict(
        "HeaderMenuClicked",
            {
            "col": NotRequired[NumberType],
            "screenX": NotRequired[NumberType],
            "screenY": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    GroupHeaderClicked = TypedDict(
        "GroupHeaderClicked",
            {
            "col": NotRequired[NumberType],
            "group": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    CellContextMenu = TypedDict(
        "CellContextMenu",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    CellActivated = TypedDict(
        "CellActivated",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    ItemHovered = TypedDict(
        "ItemHovered",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "kind": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    MouseMove = TypedDict(
        "MouseMove",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "kind": NotRequired[str],
            "localEventX": NotRequired[NumberType],
            "localEventY": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    CellsEditedEdits = TypedDict(
        "CellsEditedEdits",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "value": NotRequired[typing.Any]
        }
    )

    CellsEdited = TypedDict(
        "CellsEdited",
            {
            "edits": NotRequired[typing.Sequence["CellsEditedEdits"]],
            "count": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    DeletePressedCells = TypedDict(
        "DeletePressedCells",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType]
        }
    )

    DeletePressed = TypedDict(
        "DeletePressed",
            {
            "cells": NotRequired[typing.Sequence["DeletePressedCells"]],
            "rows": NotRequired[typing.Sequence[NumberType]],
            "columns": NotRequired[typing.Sequence[NumberType]],
            "timestamp": NotRequired[NumberType]
        }
    )

    VisibleRegion = TypedDict(
        "VisibleRegion",
            {
            "x": NotRequired[NumberType],
            "y": NotRequired[NumberType],
            "width": NotRequired[NumberType],
            "height": NotRequired[NumberType],
            "tx": NotRequired[NumberType],
            "ty": NotRequired[NumberType]
        }
    )

    ColumnMoved = TypedDict(
        "ColumnMoved",
            {
            "startIndex": NotRequired[NumberType],
            "endIndex": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    RowMoved = TypedDict(
        "RowMoved",
            {
            "startIndex": NotRequired[NumberType],
            "endIndex": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    HighlightRegionsRange = TypedDict(
        "HighlightRegionsRange",
            {
            "x": NumberType,
            "y": NumberType,
            "width": NumberType,
            "height": NumberType
        }
    )

    HighlightRegions = TypedDict(
        "HighlightRegions",
            {
            "color": str,
            "range": "HighlightRegionsRange",
            "style": NotRequired[Literal["dashed", "solid", "solid-outline", "no-outline"]]
        }
    )

    TrailingRowOptions = TypedDict(
        "TrailingRowOptions",
            {
            "hint": NotRequired[str],
            "sticky": NotRequired[bool],
            "tint": NotRequired[bool],
            "addIcon": NotRequired[str],
            "targetColumn": NotRequired[NumberType]
        }
    )

    RowAppended = TypedDict(
        "RowAppended",
            {
            "timestamp": NotRequired[NumberType]
        }
    )

    ScrollToCell = TypedDict(
        "ScrollToCell",
            {
            "col": NumberType,
            "row": NumberType,
            "direction": NotRequired[Literal["horizontal", "vertical", "both"]],
            "paddingX": NotRequired[NumberType],
            "paddingY": NotRequired[NumberType],
            "hAlign": NotRequired[Literal["start", "center", "end"]],
            "vAlign": NotRequired[Literal["start", "center", "end"]]
        }
    )

    DragStarted = TypedDict(
        "DragStarted",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    DragOverCell = TypedDict(
        "DragOverCell",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    DroppedOnCell = TypedDict(
        "DroppedOnCell",
            {
            "col": NotRequired[NumberType],
            "row": NotRequired[NumberType],
            "timestamp": NotRequired[NumberType]
        }
    )

    Experimental = TypedDict(
        "Experimental",
            {
            "disableAccessibilityTree": NotRequired[bool],
            "disableMinimumCellWidth": NotRequired[bool],
            "enableFirefoxRescaling": NotRequired[bool],
            "hyperWrapping": NotRequired[bool],
            "isSubGrid": NotRequired[bool],
            "kineticScrollPerfHack": NotRequired[bool],
            "paddingBottom": NotRequired[NumberType],
            "paddingRight": NotRequired[NumberType],
            "renderStrategy": NotRequired[Literal["single-buffer", "double-buffer", "direct"]],
            "scrollbarWidthOverride": NotRequired[NumberType],
            "strict": NotRequired[bool]
        }
    )

    ValidateCell = TypedDict(
        "ValidateCell",
            {
            "function": str
        }
    )

    CoercePasteValue = TypedDict(
        "CoercePasteValue",
            {
            "function": str
        }
    )

    GetRowThemeOverride = TypedDict(
        "GetRowThemeOverride",
            {
            "function": str
        }
    )

    DrawCell = TypedDict(
        "DrawCell",
            {
            "function": str
        }
    )

    DrawHeader = TypedDict(
        "DrawHeader",
            {
            "function": str
        }
    )

    SortColumns = TypedDict(
        "SortColumns",
            {
            "columnIndex": NumberType,
            "direction": Literal["asc", "desc"]
        }
    )

    HeaderMenuConfigCustomItemsOnClick = TypedDict(
        "HeaderMenuConfigCustomItemsOnClick",
            {
            "function": str
        }
    )

    HeaderMenuConfigCustomItems = TypedDict(
        "HeaderMenuConfigCustomItems",
            {
            "id": str,
            "label": str,
            "icon": NotRequired[str],
            "onClick": NotRequired["HeaderMenuConfigCustomItemsOnClick"],
            "dividerAfter": NotRequired[bool]
        }
    )

    HeaderMenuConfig = TypedDict(
        "HeaderMenuConfig",
            {
            "menuIcon": NotRequired[Literal["chevron", "hamburger", "dots"]],
            "filterActiveColor": NotRequired[str],
            "customItems": NotRequired[typing.Sequence["HeaderMenuConfigCustomItems"]]
        }
    )

    HeaderMenuItemClicked = TypedDict(
        "HeaderMenuItemClicked",
            {
            "col": NotRequired[NumberType],
            "itemId": NotRequired[str],
            "timestamp": NotRequired[NumberType]
        }
    )

    UndoRedoAction = TypedDict(
        "UndoRedoAction",
            {
            "action": Literal["undo", "redo"],
            "timestamp": NumberType
        }
    )

    UndoRedoPerformed = TypedDict(
        "UndoRedoPerformed",
            {
            "action": NotRequired[Literal["undo", "redo"]],
            "timestamp": NotRequired[NumberType]
        }
    )


    def __init__(
        self,
        id: typing.Optional[typing.Union[str, dict]] = None,
        columns: typing.Optional[typing.Sequence["Columns"]] = None,
        data: typing.Optional[typing.Sequence[dict]] = None,
        rows: typing.Optional[NumberType] = None,
        height: typing.Optional[typing.Union[NumberType, str]] = None,
        width: typing.Optional[typing.Union[NumberType, str]] = None,
        rowHeight: typing.Optional[typing.Union[NumberType, "RowHeight"]] = None,
        headerHeight: typing.Optional[NumberType] = None,
        freezeColumns: typing.Optional[NumberType] = None,
        freezeTrailingRows: typing.Optional[NumberType] = None,
        groupHeaderHeight: typing.Optional[NumberType] = None,
        fixedShadowX: typing.Optional[bool] = None,
        fixedShadowY: typing.Optional[bool] = None,
        overscrollX: typing.Optional[NumberType] = None,
        overscrollY: typing.Optional[NumberType] = None,
        drawFocusRing: typing.Optional[bool] = None,
        preventDiagonalScrolling: typing.Optional[bool] = None,
        scaleToRem: typing.Optional[bool] = None,
        className: typing.Optional[str] = None,
        rowSelect: typing.Optional[Literal["none", "single", "multi"]] = None,
        columnSelect: typing.Optional[Literal["none", "single", "multi"]] = None,
        rangeSelect: typing.Optional[Literal["none", "cell", "rect", "multi-cell", "multi-rect"]] = None,
        rowSelectionMode: typing.Optional[Literal["auto", "multi"]] = None,
        columnSelectionBlending: typing.Optional[Literal["exclusive", "mixed"]] = None,
        rowSelectionBlending: typing.Optional[Literal["exclusive", "mixed"]] = None,
        rangeSelectionBlending: typing.Optional[Literal["exclusive", "mixed"]] = None,
        spanRangeBehavior: typing.Optional[Literal["default", "allowPartial"]] = None,
        selectionColumnMin: typing.Optional[NumberType] = None,
        unselectableColumns: typing.Optional[typing.Sequence[NumberType]] = None,
        unselectableRows: typing.Optional[typing.Sequence[NumberType]] = None,
        showSearch: typing.Optional[bool] = None,
        searchValue: typing.Optional[str] = None,
        columnResize: typing.Optional[bool] = None,
        columnMovable: typing.Optional[bool] = None,
        rowMovable: typing.Optional[bool] = None,
        minColumnWidth: typing.Optional[NumberType] = None,
        maxColumnWidth: typing.Optional[NumberType] = None,
        maxColumnAutoWidth: typing.Optional[NumberType] = None,
        rowMarkers: typing.Optional[Literal["none", "number", "checkbox", "both", "checkbox-visible", "clickable-number"]] = None,
        rowMarkerStartIndex: typing.Optional[NumberType] = None,
        rowMarkerWidth: typing.Optional[NumberType] = None,
        rowMarkerTheme: typing.Optional[dict] = None,
        smoothScrollX: typing.Optional[bool] = None,
        smoothScrollY: typing.Optional[bool] = None,
        verticalBorder: typing.Optional[bool] = None,
        readonly: typing.Optional[bool] = None,
        enableCopyPaste: typing.Optional[bool] = None,
        fillHandle: typing.Optional[bool] = None,
        allowedFillDirections: typing.Optional[Literal["horizontal", "vertical", "orthogonal", "any"]] = None,
        copyHeaders: typing.Optional[bool] = None,
        theme: typing.Optional["Theme"] = None,
        selectedCell: typing.Optional["SelectedCell"] = None,
        selectedRows: typing.Optional[typing.Sequence[NumberType]] = None,
        selectedColumns: typing.Optional[typing.Sequence[NumberType]] = None,
        selectedRange: typing.Optional["SelectedRange"] = None,
        selectedRanges: typing.Optional[typing.Sequence["SelectedRanges"]] = None,
        cellEdited: typing.Optional["CellEdited"] = None,
        cellClicked: typing.Optional["CellClicked"] = None,
        buttonClicked: typing.Optional["ButtonClicked"] = None,
        linkClicked: typing.Optional["LinkClicked"] = None,
        treeNodeToggled: typing.Optional["TreeNodeToggled"] = None,
        columnWidths: typing.Optional[typing.Sequence[NumberType]] = None,
        nClicks: typing.Optional[NumberType] = None,
        headerClicked: typing.Optional["HeaderClicked"] = None,
        headerContextMenu: typing.Optional["HeaderContextMenu"] = None,
        headerMenuClicked: typing.Optional["HeaderMenuClicked"] = None,
        groupHeaderClicked: typing.Optional["GroupHeaderClicked"] = None,
        cellContextMenu: typing.Optional["CellContextMenu"] = None,
        cellActivated: typing.Optional["CellActivated"] = None,
        itemHovered: typing.Optional["ItemHovered"] = None,
        mouseMove: typing.Optional["MouseMove"] = None,
        cellsEdited: typing.Optional["CellsEdited"] = None,
        deletePressed: typing.Optional["DeletePressed"] = None,
        allowDelete: typing.Optional[bool] = None,
        visibleRegion: typing.Optional["VisibleRegion"] = None,
        columnMoved: typing.Optional["ColumnMoved"] = None,
        rowMoved: typing.Optional["RowMoved"] = None,
        highlightRegions: typing.Optional[typing.Sequence["HighlightRegions"]] = None,
        trailingRowOptions: typing.Optional["TrailingRowOptions"] = None,
        rowAppended: typing.Optional["RowAppended"] = None,
        scrollToCell: typing.Optional["ScrollToCell"] = None,
        redrawTrigger: typing.Optional[typing.Union[NumberType, str]] = None,
        showCellFlash: typing.Optional[typing.Union[bool, typing.Sequence[Literal["edit", "paste", "undo", "redo"]]]] = None,
        scrollOffsetX: typing.Optional[NumberType] = None,
        scrollOffsetY: typing.Optional[NumberType] = None,
        keybindings: typing.Optional[dict] = None,
        isDraggable: typing.Optional[typing.Union[bool, Literal["header", "cell"]]] = None,
        dragStarted: typing.Optional["DragStarted"] = None,
        dragOverCell: typing.Optional["DragOverCell"] = None,
        droppedOnCell: typing.Optional["DroppedOnCell"] = None,
        experimental: typing.Optional["Experimental"] = None,
        validateCell: typing.Optional["ValidateCell"] = None,
        coercePasteValue: typing.Optional["CoercePasteValue"] = None,
        getRowThemeOverride: typing.Optional["GetRowThemeOverride"] = None,
        drawCell: typing.Optional["DrawCell"] = None,
        drawHeader: typing.Optional["DrawHeader"] = None,
        sortable: typing.Optional[bool] = None,
        sortColumns: typing.Optional[typing.Sequence["SortColumns"]] = None,
        sortingOrder: typing.Optional[typing.Sequence[Literal["asc", "desc", None]]] = None,
        columnFilters: typing.Optional[typing.Dict[typing.Union[str, float, int], typing.Sequence[typing.Any]]] = None,
        headerMenuConfig: typing.Optional["HeaderMenuConfig"] = None,
        visibleRowIndices: typing.Optional[typing.Sequence[NumberType]] = None,
        headerMenuItemClicked: typing.Optional["HeaderMenuItemClicked"] = None,
        hoverRow: typing.Optional[bool] = None,
        cellActivationBehavior: typing.Optional[Literal["double-click", "second-click", "single-click"]] = None,
        editorScrollBehavior: typing.Optional[Literal["default", "close-overlay-on-scroll", "lock-scroll"]] = None,
        editOnType: typing.Optional[bool] = None,
        rangeSelectionColumnSpanning: typing.Optional[bool] = None,
        trapFocus: typing.Optional[bool] = None,
        scrollToActiveCell: typing.Optional[bool] = None,
        columnSelectionMode: typing.Optional[Literal["auto", "multi"]] = None,
        enableUndoRedo: typing.Optional[bool] = None,
        maxUndoSteps: typing.Optional[NumberType] = None,
        undoRedoAction: typing.Optional["UndoRedoAction"] = None,
        canUndo: typing.Optional[bool] = None,
        canRedo: typing.Optional[bool] = None,
        undoRedoPerformed: typing.Optional["UndoRedoPerformed"] = None,
        **kwargs
    ):
        self._prop_names = ['id', 'allowDelete', 'allowedFillDirections', 'buttonClicked', 'canRedo', 'canUndo', 'cellActivated', 'cellActivationBehavior', 'cellClicked', 'cellContextMenu', 'cellEdited', 'cellsEdited', 'className', 'coercePasteValue', 'columnFilters', 'columnMovable', 'columnMoved', 'columnResize', 'columnSelect', 'columnSelectionBlending', 'columnSelectionMode', 'columnWidths', 'columns', 'copyHeaders', 'data', 'deletePressed', 'dragOverCell', 'dragStarted', 'drawCell', 'drawFocusRing', 'drawHeader', 'droppedOnCell', 'editOnType', 'editorScrollBehavior', 'enableCopyPaste', 'enableUndoRedo', 'experimental', 'fillHandle', 'fixedShadowX', 'fixedShadowY', 'freezeColumns', 'freezeTrailingRows', 'getRowThemeOverride', 'groupHeaderClicked', 'groupHeaderHeight', 'headerClicked', 'headerContextMenu', 'headerHeight', 'headerMenuClicked', 'headerMenuConfig', 'headerMenuItemClicked', 'height', 'highlightRegions', 'hoverRow', 'isDraggable', 'itemHovered', 'keybindings', 'linkClicked', 'maxColumnAutoWidth', 'maxColumnWidth', 'maxUndoSteps', 'minColumnWidth', 'mouseMove', 'nClicks', 'overscrollX', 'overscrollY', 'preventDiagonalScrolling', 'rangeSelect', 'rangeSelectionBlending', 'rangeSelectionColumnSpanning', 'readonly', 'redrawTrigger', 'rowAppended', 'rowHeight', 'rowMarkerStartIndex', 'rowMarkerTheme', 'rowMarkerWidth', 'rowMarkers', 'rowMovable', 'rowMoved', 'rowSelect', 'rowSelectionBlending', 'rowSelectionMode', 'rows', 'scaleToRem', 'scrollOffsetX', 'scrollOffsetY', 'scrollToActiveCell', 'scrollToCell', 'searchValue', 'selectedCell', 'selectedColumns', 'selectedRange', 'selectedRanges', 'selectedRows', 'selectionColumnMin', 'showCellFlash', 'showSearch', 'smoothScrollX', 'smoothScrollY', 'sortColumns', 'sortable', 'sortingOrder', 'spanRangeBehavior', 'theme', 'trailingRowOptions', 'trapFocus', 'treeNodeToggled', 'undoRedoAction', 'undoRedoPerformed', 'unselectableColumns', 'unselectableRows', 'validateCell', 'verticalBorder', 'visibleRegion', 'visibleRowIndices', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'allowDelete', 'allowedFillDirections', 'buttonClicked', 'canRedo', 'canUndo', 'cellActivated', 'cellActivationBehavior', 'cellClicked', 'cellContextMenu', 'cellEdited', 'cellsEdited', 'className', 'coercePasteValue', 'columnFilters', 'columnMovable', 'columnMoved', 'columnResize', 'columnSelect', 'columnSelectionBlending', 'columnSelectionMode', 'columnWidths', 'columns', 'copyHeaders', 'data', 'deletePressed', 'dragOverCell', 'dragStarted', 'drawCell', 'drawFocusRing', 'drawHeader', 'droppedOnCell', 'editOnType', 'editorScrollBehavior', 'enableCopyPaste', 'enableUndoRedo', 'experimental', 'fillHandle', 'fixedShadowX', 'fixedShadowY', 'freezeColumns', 'freezeTrailingRows', 'getRowThemeOverride', 'groupHeaderClicked', 'groupHeaderHeight', 'headerClicked', 'headerContextMenu', 'headerHeight', 'headerMenuClicked', 'headerMenuConfig', 'headerMenuItemClicked', 'height', 'highlightRegions', 'hoverRow', 'isDraggable', 'itemHovered', 'keybindings', 'linkClicked', 'maxColumnAutoWidth', 'maxColumnWidth', 'maxUndoSteps', 'minColumnWidth', 'mouseMove', 'nClicks', 'overscrollX', 'overscrollY', 'preventDiagonalScrolling', 'rangeSelect', 'rangeSelectionBlending', 'rangeSelectionColumnSpanning', 'readonly', 'redrawTrigger', 'rowAppended', 'rowHeight', 'rowMarkerStartIndex', 'rowMarkerTheme', 'rowMarkerWidth', 'rowMarkers', 'rowMovable', 'rowMoved', 'rowSelect', 'rowSelectionBlending', 'rowSelectionMode', 'rows', 'scaleToRem', 'scrollOffsetX', 'scrollOffsetY', 'scrollToActiveCell', 'scrollToCell', 'searchValue', 'selectedCell', 'selectedColumns', 'selectedRange', 'selectedRanges', 'selectedRows', 'selectionColumnMin', 'showCellFlash', 'showSearch', 'smoothScrollX', 'smoothScrollY', 'sortColumns', 'sortable', 'sortingOrder', 'spanRangeBehavior', 'theme', 'trailingRowOptions', 'trapFocus', 'treeNodeToggled', 'undoRedoAction', 'undoRedoPerformed', 'unselectableColumns', 'unselectableRows', 'validateCell', 'verticalBorder', 'visibleRegion', 'visibleRowIndices', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['columns', 'data']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(GlideGrid, self).__init__(**args)

setattr(GlideGrid, "__init__", _explicitize_args(GlideGrid.__init__))
