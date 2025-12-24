import React from 'react';
import PropTypes from 'prop-types';
import { GlideGrid as RealComponent } from '../LazyLoader';

/**
 * GlideGrid is a high-performance data grid component for Dash.
 * It wraps the Glide Data Grid library to provide an Excel-like grid experience
 * with support for millions of rows, multiple cell types, and rich interactions.
 */
const GlideGrid = (props) => {
    return <RealComponent {...props} />;
};

GlideGrid.defaultProps = {
    height: 400,
    width: '100%',
    rowHeight: 34,
    headerHeight: 36,
    freezeColumns: 0,
    freezeTrailingRows: 0,
    rowSelect: 'none',
    columnSelect: 'none',
    rangeSelect: 'rect',
    showSearch: false,
    searchValue: '',
    columnResize: true,
    rowMarkers: 'none',
    rowMarkerStartIndex: 1,
    smoothScrollX: true,
    smoothScrollY: true,
    verticalBorder: true,
    fixedShadowX: true,
    fixedShadowY: true,
    drawFocusRing: true,
    preventDiagonalScrolling: false,
    overscrollX: 0,
    overscrollY: 0,
    scaleToRem: false,
    readonly: false,
    enableCopyPaste: true,
    copyHeaders: false,
    fillHandle: false,
    allowedFillDirections: 'orthogonal',
    minColumnWidth: 50,
    maxColumnWidth: 500,
    rowSelectionMode: 'auto',
    selectedCell: null,
    selectedRows: [],
    selectedColumns: [],
    selectedRange: null,
    selectedRanges: [],
    nClicks: 0,
    sortable: false,
    sortColumns: [],
    sortingOrder: ['asc', 'desc', null],
    columnFilters: {},
    hoverRow: false,
    cellActivationBehavior: 'second-click',
    editOnType: true,
    rangeSelectionColumnSpanning: true,
    trapFocus: false,
    tabWrapping: false,
    scrollToActiveCell: true,
    columnSelectionMode: 'auto',
    enableUndoRedo: false,
    maxUndoSteps: 50,
    canUndo: false,
    canRedo: false,
    editorScrollBehavior: 'default',
    redrawTrigger: null,
    showCellFlash: false,
    allowDelete: true
};

GlideGrid.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    // ========== CORE DATA PROPS ==========

    /**
     * Array of column definitions. Each column must have at least a title and width.
     * Example: [{"title": "Name", "width": 200, "id": "name_col"}]
     */
    columns: PropTypes.arrayOf(PropTypes.shape({
        /** Column header text */
        title: PropTypes.string.isRequired,
        /** Column identifier (defaults to title if not provided) */
        id: PropTypes.string,
        /** Column width in pixels */
        width: PropTypes.number,
        /** Icon name to display in header */
        icon: PropTypes.string,
        /** Overlay icon name */
        overlayIcon: PropTypes.string,
        /** Whether column has a menu dropdown arrow */
        hasMenu: PropTypes.bool,
        /** Whether this column is filterable. Shows filter menu with unique values. */
        filterable: PropTypes.bool,
        /** Whether this column is sortable (when grid-level sortable=true). Default: true */
        sortable: PropTypes.bool,
        /** Group name for column grouping */
        group: PropTypes.string,
        /** Column-specific theme overrides */
        themeOverride: PropTypes.object,
        /**
         * Custom value formatter for display. Formats the cell value for display
         * without changing the underlying data.
         *
         * **Usage**: `valueFormatter={"function": "formatCurrency(value)"}`
         *
         * **Setup**: Create `assets/dashGlideGridFunctions.js`:
         * ```javascript
         * var dggfuncs = window.dashGlideGridFunctions =
         *     window.dashGlideGridFunctions || {};
         *
         * dggfuncs.formatCurrency = function(value) {
         *     return new Intl.NumberFormat('en-US', {
         *         style: 'currency',
         *         currency: 'USD'
         *     }).format(value);
         * };
         * ```
         *
         * **Parameters passed to function**:
         * - `value`: The cell's raw data value
         * - `cell`: The full cell object
         * - `row`: Row index
         * - `col`: Column index
         *
         * **Return**: String to display (or undefined to use default)
         */
        valueFormatter: PropTypes.shape({
            function: PropTypes.string.isRequired
        })
    })).isRequired,

    /**
     * Array of row data objects (records format). Each row is a dict where keys
     * match column `id` values. Compatible with `df.to_dict('records')`.
     *
     * **Example**:
     * ```python
     * columns = [
     *     {'title': 'Name', 'id': 'name'},
     *     {'title': 'Price', 'id': 'price'},
     * ]
     * data = [
     *     {'name': 'Laptop', 'price': 1299.99},
     *     {'name': 'Mouse', 'price': 29.99},
     * ]
     * # Or from pandas:
     * data = df.to_dict('records')
     * ```
     *
     * **Simple values** (auto-detected types):
     * - String → Text cell
     * - Number → Number cell
     * - Boolean → Checkbox cell
     * - null/undefined → Empty cell
     *
     * **Cell object properties** (for explicit control):
     * - `kind`: Cell type - "text", "number", "boolean", "markdown", "uri", "image", "bubble", "dropdown-cell", "multi-select-cell"
     * - `data`: The cell's value (type depends on kind)
     * - `allowOverlay`: (boolean) If true, double-click opens editor popup. Required for editing. Default: true
     * - `copyData`: (string) Text copied to clipboard on Ctrl+C. Required for copy to work on custom cells
     * - `displayData`: (string) Text shown in cell (for text/number). Defaults to data value
     * - `readonly`: (boolean) If true, cell cannot be edited even with allowOverlay
     * - `themeOverride`: (object) Custom colors for this cell, e.g. {"bgCell": "#fff"}
     * - `span`: ([start, end]) For merged cells - column indices this cell spans
     * - `contentAlign`: ("left"|"right"|"center") Text alignment hint for the cell
     * - `cursor`: (string) CSS cursor override when hovering, e.g. "pointer"
     *
     * **Number cell props** (kind: "number"):
     * - `fixedDecimals`: (number) Fixed number of decimal places in editor
     * - `allowNegative`: (boolean) Allow negative numbers. Default: true
     * - `thousandSeparator`: (boolean|string) Add thousand separators. true for default, or custom string
     * - `decimalSeparator`: (string) Custom decimal separator, e.g. "," for European format
     *
     * **Boolean cell props** (kind: "boolean"):
     * - `maxSize`: (number) Maximum size of the checkbox in pixels
     *
     * **Uri cell props** (kind: "uri"):
     * - `hoverEffect`: (boolean) If true, underline on hover with pointer cursor
     *
     * **Image cell props** (kind: "image"):
     * - `rounding`: (number) Corner radius for rounded images in pixels
     * - `displayData`: (string[]) Reduced-size image URLs for display (full URLs in data for overlay)
     *
     * **Dropdown cell example**:
     * ```
     * {
     *   "kind": "dropdown-cell",
     *   "data": {
     *     "value": "active",
     *     "options": [{"value": "active", "label": "Active", "color": "#10b981"}],
     *     "allowedValues": ["active", "pending"]
     *   },
     *   "allowOverlay": true,
     *   "copyData": "active"
     * }
     * ```
     *
     * **Multi-select cell example**:
     * ```
     * {
     *   "kind": "multi-select-cell",
     *   "data": {
     *     "values": ["python", "react"],
     *     "options": [{"value": "python", "label": "Python", "color": "#3776ab"}],
     *     "allowedValues": ["python", "react", "sql"]
     *   },
     *   "allowOverlay": true,
     *   "copyData": "python, react"
     * }
     * ```
     */
    data: PropTypes.arrayOf(PropTypes.object).isRequired,

    /**
     * Number of rows to display. If not provided, inferred from data.length.
     */
    rows: PropTypes.number,

    // ========== DISPLAY & LAYOUT PROPS ==========

    /**
     * Container height (REQUIRED). Can be a number (pixels) or string ("600px", "100vh").
     * The grid requires an explicit height to render properly.
     */
    height: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.string
    ]),

    /**
     * Container width. Can be a number (pixels) or string. Defaults to "100%".
     */
    width: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.string
    ]),

    /**
     * Height of each data row in pixels, or a function for variable row heights.
     * Can be a number (e.g., 34) or an object with a function string.
     * Function format: {"function": "getRowHeight(rowIndex)"} where the function
     * receives rowIndex and should return a number.
     * Default: 34
     */
    rowHeight: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.shape({
            function: PropTypes.string.isRequired
        })
    ]),

    /**
     * Height of the header row in pixels. Default: 36
     */
    headerHeight: PropTypes.number,

    /**
     * Number of columns to freeze on the left side. Default: 0
     */
    freezeColumns: PropTypes.number,

    /**
     * Number of rows to freeze at the bottom of the grid. Default: 0
     * Useful for totals or summary rows.
     */
    freezeTrailingRows: PropTypes.number,

    /**
     * Height of column group headers in pixels. Defaults to headerHeight.
     */
    groupHeaderHeight: PropTypes.number,

    /**
     * Show shadow behind frozen columns. Default: true
     */
    fixedShadowX: PropTypes.bool,

    /**
     * Show shadow behind header row(s). Default: true
     */
    fixedShadowY: PropTypes.bool,

    /**
     * Extra horizontal scroll space beyond content. Default: 0
     */
    overscrollX: PropTypes.number,

    /**
     * Extra vertical scroll space beyond content. Default: 0
     */
    overscrollY: PropTypes.number,

    /**
     * Show focus ring around selected cell. Default: true
     */
    drawFocusRing: PropTypes.bool,

    /**
     * Only allow horizontal or vertical scrolling, not diagonal. Default: false
     */
    preventDiagonalScrolling: PropTypes.bool,

    /**
     * Scale theme elements to match rem sizing. Default: false
     */
    scaleToRem: PropTypes.bool,

    /**
     * CSS class name to apply to the grid container.
     */
    className: PropTypes.string,

    // ========== SELECTION PROPS ==========

    /**
     * Row selection mode. Options: 'none', 'single', 'multi'
     */
    rowSelect: PropTypes.oneOf(['none', 'single', 'multi']),

    /**
     * Column selection mode. Options: 'none', 'single', 'multi'
     */
    columnSelect: PropTypes.oneOf(['none', 'single', 'multi']),

    /**
     * Range selection mode. Options: 'none', 'cell', 'rect', 'multi-cell', 'multi-rect'
     */
    rangeSelect: PropTypes.oneOf(['none', 'cell', 'rect', 'multi-cell', 'multi-rect']),

    /**
     * Row selection behavior. 'auto' requires modifier keys for multi-select,
     * 'multi' allows multi-select without modifiers. Default: 'auto'
     */
    rowSelectionMode: PropTypes.oneOf(['auto', 'multi']),

    /**
     * How column selection blends with other selections.
     * 'exclusive' clears other selections, 'mixed' allows combining. Default: 'exclusive'
     */
    columnSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How row selection blends with other selections.
     * 'exclusive' clears other selections, 'mixed' allows combining. Default: 'exclusive'
     */
    rowSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How range selection blends with other selections.
     * 'exclusive' clears other selections, 'mixed' allows combining. Default: 'exclusive'
     */
    rangeSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How to handle spans in range selection.
     * 'default' expands to include full spans, 'allowPartial' allows partial span selection.
     */
    spanRangeBehavior: PropTypes.oneOf(['default', 'allowPartial']),

    /**
     * Minimum column index that can be selected. Columns with index less than this
     * value cannot be selected or included in range selections. Useful for preventing
     * selection of row label columns. Default: 0 (no restriction)
     */
    selectionColumnMin: PropTypes.number,

    /**
     * Array of column indices that cannot be selected. Clicks on cells in these columns
     * are ignored (selection stays where it is). Useful for creating unselectable
     * label columns or border columns.
     */
    unselectableColumns: PropTypes.arrayOf(PropTypes.number),

    /**
     * Array of row indices that cannot be selected. Clicks on cells in these rows
     * are ignored (selection stays where it is). Useful for creating unselectable
     * header rows or border rows.
     */
    unselectableRows: PropTypes.arrayOf(PropTypes.number),

    // ========== FEATURE TOGGLES ==========

    /**
     * Show/hide the built-in search interface. When enabled, displays a search box
     * that allows users to search through grid data. Use searchValue to control
     * or read the current search query. Default: false
     */
    showSearch: PropTypes.bool,

    /**
     * The current search query string. Updated when user types in the search box.
     * Can be set from Python to programmatically trigger a search.
     */
    searchValue: PropTypes.string,

    /**
     * Allow column resizing by dragging column edges. Default: true
     */
    columnResize: PropTypes.bool,

    /**
     * Allow column reordering by dragging column headers. Default: true
     */
    columnMovable: PropTypes.bool,

    /**
     * Allow row reordering by dragging row markers. Default: true
     * Note: rowMarkers must be enabled for row moving to work.
     */
    rowMovable: PropTypes.bool,

    /**
     * Minimum width users can resize columns to. Default: 50
     */
    minColumnWidth: PropTypes.number,

    /**
     * Maximum width users can resize columns to. Default: 500
     */
    maxColumnWidth: PropTypes.number,

    /**
     * Maximum width for auto-sized columns. Defaults to maxColumnWidth.
     */
    maxColumnAutoWidth: PropTypes.number,

    /**
     * Row marker style. Options:
     * - 'none': No row markers
     * - 'number': Show row numbers
     * - 'checkbox': Show selection checkboxes (on hover)
     * - 'both': Show both numbers and checkboxes
     * - 'checkbox-visible': Always show checkboxes
     * - 'clickable-number': Row numbers act as selection buttons
     */
    rowMarkers: PropTypes.oneOf(['none', 'number', 'checkbox', 'both', 'checkbox-visible', 'clickable-number']),

    /**
     * Starting index for row numbers. Default: 1
     */
    rowMarkerStartIndex: PropTypes.number,

    /**
     * Width of the row marker column in pixels. Auto-calculated if not set.
     */
    rowMarkerWidth: PropTypes.number,

    /**
     * Theme overrides for the row marker column.
     */
    rowMarkerTheme: PropTypes.object,

    /**
     * Enable smooth horizontal scrolling. Default: true
     */
    smoothScrollX: PropTypes.bool,

    /**
     * Enable smooth vertical scrolling. Default: true
     */
    smoothScrollY: PropTypes.bool,

    /**
     * Show vertical borders between columns. Default: true
     */
    verticalBorder: PropTypes.bool,

    // ========== EDITING PROPS ==========

    /**
     * Make the entire grid read-only. Default: false
     */
    readonly: PropTypes.bool,

    /**
     * Enable copy/paste functionality. Default: true
     */
    enableCopyPaste: PropTypes.bool,

    /**
     * Enable fill handle for dragging to fill cells (Excel-like). Default: false
     * When enabled, users can drag a small square at the bottom-right of a selection
     * to fill adjacent cells with the selected pattern.
     */
    fillHandle: PropTypes.bool,

    /**
     * Allowed directions for fill handle. Default: 'orthogonal'
     * - 'horizontal': Only fill left/right
     * - 'vertical': Only fill up/down
     * - 'orthogonal': Fill horizontally or vertically (not diagonal)
     * - 'any': Fill in any direction including diagonal
     */
    allowedFillDirections: PropTypes.oneOf(['horizontal', 'vertical', 'orthogonal', 'any']),

    /**
     * Include column headers when copying to clipboard. Default: false
     */
    copyHeaders: PropTypes.bool,

    // ========== THEME PROPS ==========

    /**
     * Custom theme object to style the grid. Properties use camelCase.
     * Example: {"accentColor": "#2563eb", "bgCell": "#ffffff"}
     */
    theme: PropTypes.shape({
        accentColor: PropTypes.string,
        accentLight: PropTypes.string,
        accentFg: PropTypes.string,
        textDark: PropTypes.string,
        textMedium: PropTypes.string,
        textLight: PropTypes.string,
        textBubble: PropTypes.string,
        bgIconHeader: PropTypes.string,
        fgIconHeader: PropTypes.string,
        textHeader: PropTypes.string,
        textHeaderSelected: PropTypes.string,
        textGroupHeader: PropTypes.string,
        bgCell: PropTypes.string,
        bgCellMedium: PropTypes.string,
        bgHeader: PropTypes.string,
        bgHeaderHasFocus: PropTypes.string,
        bgHeaderHovered: PropTypes.string,
        bgBubble: PropTypes.string,
        bgBubbleSelected: PropTypes.string,
        bgSearchResult: PropTypes.string,
        borderColor: PropTypes.string,
        drilldownBorder: PropTypes.string,
        linkColor: PropTypes.string,
        headerFontStyle: PropTypes.string,
        baseFontStyle: PropTypes.string,
        fontFamily: PropTypes.string,
        editorFontSize: PropTypes.string,
        lineHeight: PropTypes.number,
        horizontalBorderColor: PropTypes.string,
        cellHorizontalPadding: PropTypes.number,
        cellVerticalPadding: PropTypes.number
    }),

    // ========== OUTPUT PROPS (Updated by component) ==========

    /**
     * Currently selected cell. Updated when user clicks a cell.
     * Format: {"col": 0, "row": 1}
     */
    selectedCell: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number
    }),

    /**
     * Array of selected row indices. Updated with row selection.
     * Example: [0, 2, 5]
     */
    selectedRows: PropTypes.arrayOf(PropTypes.number),

    /**
     * Array of selected column indices. Updated with column selection.
     * Example: [0, 1]
     */
    selectedColumns: PropTypes.arrayOf(PropTypes.number),

    /**
     * Currently selected range. Updated with range selection.
     * Format: {"startCol": 0, "startRow": 0, "endCol": 2, "endRow": 3}
     */
    selectedRange: PropTypes.shape({
        startCol: PropTypes.number,
        startRow: PropTypes.number,
        endCol: PropTypes.number,
        endRow: PropTypes.number
    }),

    /**
     * Additional selected ranges when using rangeSelect="multi-rect" mode.
     * Updated when user Ctrl/Cmd+clicks to add additional selections.
     * Each range has the same format as selectedRange.
     * The primary selection is in selectedRange, additional selections are here.
     */
    selectedRanges: PropTypes.arrayOf(PropTypes.shape({
        startCol: PropTypes.number,
        startRow: PropTypes.number,
        endCol: PropTypes.number,
        endRow: PropTypes.number
    })),

    /**
     * Information about the last edited cell.
     * Format: {"col": 0, "row": 1, "value": "new value", "timestamp": 1234567890}
     */
    cellEdited: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        value: PropTypes.any,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last clicked cell.
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    cellClicked: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last clicked button cell.
     * Format: {"col": 0, "row": 1, "title": "Button Text", "timestamp": 1234567890}
     */
    buttonClicked: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        title: PropTypes.string,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last clicked link in a links cell.
     * Format: {"col": 0, "row": 1, "href": "https://example.com", "title": "Link", "linkIndex": 0, "timestamp": 1234567890}
     */
    linkClicked: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        href: PropTypes.string,
        title: PropTypes.string,
        linkIndex: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last toggled tree node.
     * Format: {"col": 0, "row": 1, "isOpen": true, "depth": 0, "text": "Node", "timestamp": 1234567890}
     */
    treeNodeToggled: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        isOpen: PropTypes.bool,
        depth: PropTypes.number,
        text: PropTypes.string,
        timestamp: PropTypes.number
    }),

    /**
     * Array of column widths (updated when columns are resized).
     * Example: [200, 150, 300]
     */
    columnWidths: PropTypes.arrayOf(PropTypes.number),

    /**
     * Total number of cell clicks (increments with each click).
     */
    nClicks: PropTypes.number,

    // ========== HEADER INTERACTION EVENTS ==========

    /**
     * Information about the last clicked column header.
     * Useful for implementing column sorting.
     * Format: {"col": 0, "timestamp": 1234567890}
     */
    headerClicked: PropTypes.shape({
        col: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last right-clicked column header.
     * Useful for implementing column context menus.
     * Format: {"col": 0, "timestamp": 1234567890}
     */
    headerContextMenu: PropTypes.shape({
        col: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last clicked header menu icon.
     * Fired when user clicks the dropdown arrow on columns with hasMenu=true.
     * Format: {"col": 0, "screenX": 100, "screenY": 50, "timestamp": 1234567890}
     */
    headerMenuClicked: PropTypes.shape({
        col: PropTypes.number,
        screenX: PropTypes.number,
        screenY: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last clicked group header.
     * Format: {"col": 0, "group": "Group Name", "timestamp": 1234567890}
     */
    groupHeaderClicked: PropTypes.shape({
        col: PropTypes.number,
        group: PropTypes.string,
        timestamp: PropTypes.number
    }),

    // ========== CELL INTERACTION EVENTS ==========

    /**
     * Information about the last right-clicked cell.
     * Useful for implementing cell context menus.
     * Format: {"col": 0, "row": 1, "screenX": 100, "screenY": 200, "timestamp": 1234567890}
     */
    cellContextMenu: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        screenX: PropTypes.number,
        screenY: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Configuration for built-in cell context menu.
     * Provide an array of menu items to display when right-clicking a cell.
     * Example: { "items": [{"id": "edit", "label": "Edit"}, {"id": "delete", "label": "Delete"}] }
     */
    cellContextMenuConfig: PropTypes.shape({
        items: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            icon: PropTypes.string,
            /** CSS font-size for the icon (e.g., '18px', '1.2em') */
            iconSize: PropTypes.string,
            /** CSS color for the icon */
            iconColor: PropTypes.string,
            /** CSS font-weight for the icon (e.g., 'bold', '600') */
            iconWeight: PropTypes.string,
            /** CSS color for the label text */
            color: PropTypes.string,
            /** CSS font-weight for the label text (e.g., 'bold', '600') */
            fontWeight: PropTypes.string,
            dividerAfter: PropTypes.bool,
            disabled: PropTypes.bool,
            /** Built-in action: 'copyClickedCell', 'copySelection', 'pasteAtClickedCell', 'pasteAtSelection' */
            action: PropTypes.oneOf(['copyClickedCell', 'copySelection', 'pasteAtClickedCell', 'pasteAtSelection'])
        }))
    }),

    /**
     * Information about the last clicked cell context menu item.
     * Format: {"col": 0, "row": 1, "itemId": "edit", "timestamp": 1234567890}
     */
    cellContextMenuItemClicked: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        itemId: PropTypes.string,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last activated cell (Enter, Space, or double-click).
     * Useful for implementing drill-down or detail views.
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    cellActivated: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the currently hovered item.
     * Kind can be: "cell", "header", "group-header", "out-of-bounds"
     * Format: {"col": 0, "row": 1, "kind": "cell", "timestamp": 1234567890}
     */
    itemHovered: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        kind: PropTypes.string,
        timestamp: PropTypes.number
    }),

    /**
     * Information about mouse movement over the grid.
     * Fires on every mouse move, providing raw position data.
     * More granular than itemHovered - useful for custom tooltips or highlighting.
     * Format: {"col": 0, "row": 1, "kind": "cell", "localEventX": 150, "localEventY": 75, "timestamp": 1234567890}
     */
    mouseMove: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        kind: PropTypes.string,
        localEventX: PropTypes.number,
        localEventY: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about batch cell edits (paste or fill operations).
     * Fires when multiple cells are edited at once, such as when pasting
     * data or using the fill handle.
     * Format: {"edits": [{"col": 0, "row": 0, "value": "x"}, ...], "count": 5, "timestamp": 1234567890}
     */
    cellsEdited: PropTypes.shape({
        edits: PropTypes.arrayOf(PropTypes.shape({
            col: PropTypes.number,
            row: PropTypes.number,
            value: PropTypes.any
        })),
        count: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about delete key press events.
     * Fires when user presses Delete/Backspace on selected cells.
     * Use with allowDelete prop to control whether deletion is allowed.
     * Format: {"cells": [{"col": 0, "row": 0}, ...], "rows": [0, 1], "columns": [2], "timestamp": 1234567890}
     */
    deletePressed: PropTypes.shape({
        cells: PropTypes.arrayOf(PropTypes.shape({
            col: PropTypes.number,
            row: PropTypes.number
        })),
        rows: PropTypes.arrayOf(PropTypes.number),
        columns: PropTypes.arrayOf(PropTypes.number),
        timestamp: PropTypes.number
    }),

    /**
     * Controls whether the Delete key clears cell contents.
     * When true (default), pressing Delete clears selected cells.
     * When false, Delete key is disabled and deletePressed still fires for custom handling.
     * Default: true
     */
    allowDelete: PropTypes.bool,

    // ========== VISIBLE REGION ==========

    /**
     * Information about the currently visible region of the grid.
     * Updated when user scrolls or resizes the grid.
     * Format: {"x": 0, "y": 0, "width": 10, "height": 20, "tx": 0, "ty": 0}
     */
    visibleRegion: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number,
        width: PropTypes.number,
        height: PropTypes.number,
        tx: PropTypes.number,
        ty: PropTypes.number
    }),

    // ========== ROW/COLUMN REORDERING ==========

    /**
     * Information about the last column move (drag reorder).
     * Fired when user drags a column header to a new position.
     * Note: You must update the columns prop in your callback to effect the move.
     * Format: {"startIndex": 0, "endIndex": 2, "timestamp": 1234567890}
     */
    columnMoved: PropTypes.shape({
        startIndex: PropTypes.number,
        endIndex: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about the last row move (drag reorder).
     * Fired when user drags a row marker to a new position.
     * Requires rowMarkers to be set (not 'none') to enable row dragging.
     * Note: You must update the data prop in your callback to effect the move.
     * Format: {"startIndex": 0, "endIndex": 2, "timestamp": 1234567890}
     */
    rowMoved: PropTypes.shape({
        startIndex: PropTypes.number,
        endIndex: PropTypes.number,
        timestamp: PropTypes.number
    }),

    // ========== HIGHLIGHT REGIONS ==========

    /**
     * Array of highlight regions to display on the grid.
     * Each region is drawn with a background color and dashed border.
     * Useful for conditional formatting, search highlights, or validation errors.
     *
     * Format: [{"color": "rgba(255,0,0,0.2)", "range": {"x": 0, "y": 0, "width": 2, "height": 3}}]
     *
     * - color: CSS color string (use rgba for transparency to allow overlapping regions to blend)
     * - range: Rectangle defining the region (x=start column, y=start row, width=columns, height=rows)
     * - style: Border style - "dashed" (default), "solid", "solid-outline", or "no-outline"
     */
    highlightRegions: PropTypes.arrayOf(PropTypes.shape({
        color: PropTypes.string.isRequired,
        range: PropTypes.shape({
            x: PropTypes.number.isRequired,
            y: PropTypes.number.isRequired,
            width: PropTypes.number.isRequired,
            height: PropTypes.number.isRequired
        }).isRequired,
        style: PropTypes.oneOf(["dashed", "solid", "solid-outline", "no-outline"])
    })),

    // ========== TRAILING ROW (ADD ROW) ==========

    /**
     * Configuration options for the trailing row used to add new rows.
     * When trailingRowOptions is provided, a blank row appears at the bottom of the grid.
     * Clicking on this row triggers the rowAppended callback.
     *
     * - hint: Text shown in the empty row cells (e.g., "Add new...")
     * - sticky: If true, the trailing row stays visible at the bottom while scrolling
     * - tint: If true, applies a tinted background to the trailing row
     * - addIcon: Icon to show in the trailing row (optional)
     * - targetColumn: Column index that activates the add action (optional)
     */
    trailingRowOptions: PropTypes.shape({
        hint: PropTypes.string,
        sticky: PropTypes.bool,
        tint: PropTypes.bool,
        addIcon: PropTypes.string,
        targetColumn: PropTypes.number
    }),

    /**
     * Information about the last row append event.
     * Fired when user clicks on the trailing row to add a new row.
     * Note: You must handle adding the new row to your data in your callback.
     * Format: {"timestamp": 1234567890}
     */
    rowAppended: PropTypes.shape({
        timestamp: PropTypes.number
    }),

    // ========== SCROLL CONTROL ==========

    /**
     * Programmatically scroll the grid to a specific cell.
     * When this prop changes, the grid will scroll to bring the specified cell into view.
     *
     * Format: {"col": 5, "row": 10}
     *
     * Optional properties:
     * - direction: "horizontal" | "vertical" | "both" (default: "both")
     * - paddingX: number - horizontal padding in pixels (default: 0)
     * - paddingY: number - vertical padding in pixels (default: 0)
     * - hAlign: "start" | "center" | "end" - horizontal alignment (default: "start")
     * - vAlign: "start" | "center" | "end" - vertical alignment (default: "start")
     *
     * Example: {"col": 5, "row": 10, "hAlign": "center", "vAlign": "center"}
     */
    scrollToCell: PropTypes.shape({
        col: PropTypes.number.isRequired,
        row: PropTypes.number.isRequired,
        direction: PropTypes.oneOf(['horizontal', 'vertical', 'both']),
        paddingX: PropTypes.number,
        paddingY: PropTypes.number,
        hAlign: PropTypes.oneOf(['start', 'center', 'end']),
        vAlign: PropTypes.oneOf(['start', 'center', 'end'])
    }),

    /**
     * Trigger a grid redraw. Change this value (e.g., increment a counter or use timestamp)
     * to force the grid to re-render. Useful for custom drawCell functions that need
     * periodic updates (animations, hover effects, etc.)
     */
    redrawTrigger: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),

    /**
     * Enable cell flash effect when cells are changed.
     * When enabled, cells will briefly highlight and fade out to indicate changes.
     * Can be:
     * - true: Flash on all operations (edit, paste, undo, redo)
     * - false: No flash (default)
     * - Array of strings: Flash only on specified operations.
     *   Valid values: "edit", "paste", "undo", "redo"
     *   Example: ["paste", "undo", "redo"] to flash on paste and undo/redo but not regular edits
     */
    showCellFlash: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.arrayOf(PropTypes.oneOf(["edit", "paste", "undo", "redo"]))
    ]),

    /**
     * Initial horizontal scroll offset in pixels. Applied on mount.
     */
    scrollOffsetX: PropTypes.number,

    /**
     * Initial vertical scroll offset in pixels. Applied on mount.
     */
    scrollOffsetY: PropTypes.number,

    // ========== ADVANCED PROPS ==========

    /**
     * Customize keyboard shortcuts. Each key can be set to:
     * - true: Enable the default keybinding
     * - false: Disable the keybinding
     * - string: Custom key combination (e.g., "ctrl+shift+c")
     *
     * Available keybindings:
     * - Navigation: goToFirstColumn, goToLastColumn, goToFirstCell, goToLastCell,
     *   goToFirstRow, goToLastRow, goToNextPage, goToPreviousPage,
     *   goUpCell, goDownCell, goLeftCell, goRightCell
     * - Selection: selectAll, selectRow, selectColumn, selectToFirstColumn,
     *   selectToLastColumn, selectToFirstCell, selectToLastCell,
     *   selectGrowUp, selectGrowDown, selectGrowLeft, selectGrowRight
     * - Actions: copy, cut, paste, delete, clear, search, activateCell,
     *   downFill, rightFill, scrollToSelectedCell
     * - Overlay: closeOverlay, acceptOverlayDown, acceptOverlayUp,
     *   acceptOverlayLeft, acceptOverlayRight
     */
    keybindings: PropTypes.object,

    /**
     * Makes the grid draggable for external drag-and-drop operations.
     * - true: Entire grid is draggable
     * - "header": Only headers are draggable
     * - "cell": Only cells are draggable
     *
     * When enabled, the dragStarted output will fire with drag information.
     */
    isDraggable: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.oneOf(['header', 'cell'])
    ]),

    /**
     * Information about drag start events (when isDraggable is enabled).
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    dragStarted: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about external drag-over events on cells.
     * Fires when something is dragged over a cell from outside the grid.
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    dragOverCell: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about external drop events on cells.
     * Fires when something is dropped onto a cell from outside the grid.
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    droppedOnCell: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Experimental options. These are not considered stable API.
     * Use with caution as they may change or be removed.
     *
     * Options:
     * - disableAccessibilityTree: Disable the accessibility tree for performance
     * - disableMinimumCellWidth: Allow cells narrower than the default minimum
     * - enableFirefoxRescaling: Enable rescaling fixes for Firefox
     * - hyperWrapping: Enable hyper text wrapping mode
     * - isSubGrid: Mark this grid as a sub-grid
     * - kineticScrollPerfHack: Performance hack for kinetic scrolling
     * - paddingBottom: Extra padding at the bottom
     * - paddingRight: Extra padding on the right
     * - renderStrategy: "single-buffer", "double-buffer", or "direct"
     * - scrollbarWidthOverride: Override the detected scrollbar width
     * - strict: Enable strict mode for debugging
     */
    experimental: PropTypes.shape({
        disableAccessibilityTree: PropTypes.bool,
        disableMinimumCellWidth: PropTypes.bool,
        enableFirefoxRescaling: PropTypes.bool,
        hyperWrapping: PropTypes.bool,
        isSubGrid: PropTypes.bool,
        kineticScrollPerfHack: PropTypes.bool,
        paddingBottom: PropTypes.number,
        paddingRight: PropTypes.number,
        renderStrategy: PropTypes.oneOf(['single-buffer', 'double-buffer', 'direct']),
        scrollbarWidthOverride: PropTypes.number,
        strict: PropTypes.bool
    }),

    // ========== CLIENT-SIDE VALIDATION ==========

    /**
     * Client-side cell validation using JavaScript functions.
     * Allows synchronous validation before edits are applied.
     *
     * **Setup**: Create `assets/dashGlideGridFunctions.js` in your app folder:
     * ```javascript
     * var dggfuncs = window.dashGlideGridFunctions =
     *     window.dashGlideGridFunctions || {};
     *
     * dggfuncs.validatePositive = function(cell, newValue) {
     *     return newValue.data > 0;  // false rejects, true accepts
     * };
     * ```
     *
     * **Usage**: `validateCell={"function": "validatePositive(cell, newValue)"}`
     *
     * **Return values**:
     * - `false`: Reject the edit (visual feedback shown to user)
     * - `true`: Accept the edit
     * - `GridCell object`: Coerce/transform the value
     *
     * **Available parameters**: `cell` ([col, row]), `newValue` (GridCell), `col`, `row`
     */
    validateCell: PropTypes.shape({
        function: PropTypes.string.isRequired
    }),

    /**
     * Client-side paste value coercion using JavaScript functions.
     * Transforms pasted strings into proper cell types.
     *
     * **Setup**: Create `assets/dashGlideGridFunctions.js` in your app folder:
     * ```javascript
     * var dggfuncs = window.dashGlideGridFunctions =
     *     window.dashGlideGridFunctions || {};
     *
     * dggfuncs.parsePaste = function(val, cell) {
     *     if (cell.kind === 'boolean') {
     *         return {
     *             kind: 'boolean',
     *             data: val.toLowerCase() === 'true' || val === '1'
     *         };
     *     }
     *     return undefined;  // Use default parsing
     * };
     * ```
     *
     * **Usage**: `coercePasteValue={"function": "parsePaste(val, cell)"}`
     *
     * **Return values**:
     * - `GridCell object`: Use this transformed value
     * - `undefined`: Use default paste behavior
     *
     * **Available parameters**: `val` (pasted string), `cell` (target GridCell), `value` (alias for val)
     */
    coercePasteValue: PropTypes.shape({
        function: PropTypes.string.isRequired
    }),

    /**
     * Client-side row theme override using JavaScript functions.
     * Allows dynamic row styling based on row data (conditional formatting).
     *
     * **Setup**: Create `assets/dashGlideGridFunctions.js` in your app folder:
     * ```javascript
     * var dggfuncs = window.dashGlideGridFunctions =
     *     window.dashGlideGridFunctions || {};
     *
     * dggfuncs.rowThemeByStatus = function(row, rowData) {
     *     if (!rowData) return undefined;
     *     // rowData is a dict with keys matching column ids
     *     const status = rowData.status;  // e.g., column with id='status'
     *     if (status === 'error') {
     *         return { bgCell: 'rgba(255, 0, 0, 0.1)' };  // Light red
     *     }
     *     if (status === 'success') {
     *         return { bgCell: 'rgba(0, 255, 0, 0.1)' };  // Light green
     *     }
     *     return undefined;  // Default theme
     * };
     * ```
     *
     * **Usage**: `getRowThemeOverride={"function": "rowThemeByStatus(row, rowData)"}`
     *
     * **Return values**:
     * - `Theme object`: Override theme properties for this row (e.g., bgCell, textDark)
     * - `undefined`: Use default theme
     *
     * **Available parameters**: `row` (row index), `rowData` (dict of cell values keyed by column id), `data` (full grid data)
     */
    getRowThemeOverride: PropTypes.shape({
        function: PropTypes.string.isRequired
    }),

    /**
     * Custom cell rendering using JavaScript Canvas API.
     * Allows complete control over how cells are drawn.
     *
     * **Usage**: `drawCell={"function": "drawCircularWell(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent)"}`
     *
     * **Return values**:
     * - `true`: Custom drawing complete, skip default rendering
     * - `false` or `undefined`: Draw default content after custom drawing
     *
     * **Available parameters**:
     * - `ctx`: CanvasRenderingContext2D for drawing
     * - `cell`: The GridCell object
     * - `theme`: Theme object with colors
     * - `rect`: {x, y, width, height} of the cell
     * - `col`: Column index
     * - `row`: Row index
     * - `hoverAmount`: 0-1 hover state
     * - `highlighted`: Whether cell is selected
     * - `cellData`: The cell data from your data array
     * - `rowData`: The full row data array
     * - `drawContent`: Function to draw default cell content
     */
    drawCell: PropTypes.shape({
        function: PropTypes.string.isRequired
    }),

    /**
     * Custom header rendering using JavaScript Canvas API.
     * Allows complete control over how column headers are drawn.
     *
     * **Usage**: `drawHeader={"function": "drawCenteredHeader(ctx, column, theme, rect, columnIndex, isSelected, hoverAmount, drawContent)"}`
     *
     * **Available parameters**:
     * - `ctx`: CanvasRenderingContext2D for drawing
     * - `column`: The column definition object
     * - `theme`: Theme object with colors
     * - `rect`: {x, y, width, height} of the header cell
     * - `columnIndex`: Column index
     * - `isSelected`: Whether column is selected
     * - `hoverAmount`: 0-1 hover state
     * - `drawContent`: Function to draw default header content
     */
    drawHeader: PropTypes.shape({
        function: PropTypes.string.isRequired
    }),

    // ========== SORTING PROPS ==========

    /**
     * Enable built-in column sorting. When true, clicking column headers
     * will cycle through sort states (ascending → descending → none).
     * Shift+click enables multi-column sorting.
     * Default: false
     */
    sortable: PropTypes.bool,

    /**
     * Array of sorted columns. Each item specifies a column index and direction.
     * For single-column sort: [{"columnIndex": 0, "direction": "asc"}]
     * For multi-column sort: [{"columnIndex": 0, "direction": "asc"}, {"columnIndex": 2, "direction": "desc"}]
     * The order determines sort priority (first item is primary sort).
     */
    sortColumns: PropTypes.arrayOf(PropTypes.shape({
        /** Column index to sort by */
        columnIndex: PropTypes.number.isRequired,
        /** Sort direction: "asc" or "desc" */
        direction: PropTypes.oneOf(['asc', 'desc']).isRequired
    })),

    /**
     * Defines the cycle order when clicking column headers.
     * Default: ["asc", "desc", null] (ascending → descending → unsorted)
     * Example: ["asc", "desc"] (never clears sort)
     */
    sortingOrder: PropTypes.arrayOf(PropTypes.oneOf(['asc', 'desc', null])),

    // ========== COLUMN FILTER PROPS ==========

    /**
     * Column filter state. Maps column index to array of selected values.
     * Set to {} to clear all filters.
     *
     * Example: {"0": ["Active", "Pending"], "2": ["Sales", "Marketing"]}
     *
     * This prop is bidirectional - you can read the current filter state
     * and also set it from Dash to programmatically filter columns.
     */
    columnFilters: PropTypes.objectOf(PropTypes.arrayOf(PropTypes.any)),

    /**
     * Configuration for the header filter menu.
     *
     * - customItems: Array of custom menu items with onClick handlers
     * - filterActiveColor: Color for header when filter is active (default: theme accentColor)
     *
     * Example:
     * ```
     * headerMenuConfig={
     *     "filterActiveColor": "#2563eb",
     *     "customItems": [
     *         {
     *             "id": "export",
     *             "label": "Export Column",
     *             "onClick": {"function": "exportColumn(col, columns, data)"}
     *         }
     *     ]
     * }
     * ```
     */
    headerMenuConfig: PropTypes.shape({
        menuIcon: PropTypes.oneOf(['chevron', 'hamburger', 'dots']),
        filterActiveColor: PropTypes.string,
        customItems: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            icon: PropTypes.string,
            onClick: PropTypes.shape({
                function: PropTypes.string.isRequired
            }),
            dividerAfter: PropTypes.bool
        }))
    }),

    /**
     * Array of visible row indices after filtering (original data indices).
     * This is an output prop that updates when filters change.
     */
    visibleRowIndices: PropTypes.arrayOf(PropTypes.number),

    /**
     * Information about the last clicked custom menu item.
     * Format: {"col": 0, "itemId": "export", "timestamp": 1234567890}
     */
    headerMenuItemClicked: PropTypes.shape({
        col: PropTypes.number,
        itemId: PropTypes.string,
        timestamp: PropTypes.number
    }),

    // ========== ROW HOVER ==========

    /**
     * Enable row hover effect. When true, the entire row is visually highlighted
     * when the mouse hovers over any cell in that row.
     * Customize the color via theme.bgRowHovered (default: 'rgba(0, 0, 0, 0.04)').
     * Default: false
     */
    hoverRow: PropTypes.bool,

    // ========== CELL ACTIVATION ==========

    /**
     * Controls when a cell is considered "activated" and will open for editing.
     * - "double-click": Activate on double-click only
     * - "second-click": Activate on second click (click selected cell again) - DEFAULT
     * - "single-click": Activate immediately on single click
     *
     * When activated, the cell fires onCellActivated and opens in edit mode.
     * Default: "second-click"
     */
    cellActivationBehavior: PropTypes.oneOf(['double-click', 'second-click', 'single-click']),

    /**
     * Controls how the grid behaves when the user scrolls while an editor is open.
     * - "default": Editor stays at original position (standard Glide behavior)
     * - "close-overlay-on-scroll": Entire editor overlay closes on scroll
     * - "lock-scroll": Scrolling is prevented while editor is open
     * Default: "default"
     */
    editorScrollBehavior: PropTypes.oneOf(['default', 'close-overlay-on-scroll', 'lock-scroll']),

    /**
     * When true, typing on a selected cell will immediately start editing.
     * When false, users must explicitly activate the cell (double-click, Enter, etc.)
     * before typing will enter edit mode.
     * Default: true
     */
    editOnType: PropTypes.bool,

    /**
     * When true, range selections can span across multiple columns.
     * When false, range selections are restricted to a single column only.
     * Useful for spreadsheet-like interfaces where column-based selection is preferred.
     * Default: true
     */
    rangeSelectionColumnSpanning: PropTypes.bool,

    /**
     * When true, prevents focus from leaving the grid via Tab key or arrow key navigation.
     * Useful for modal-like grid experiences or when the grid should capture all keyboard input.
     * Default: false
     */
    trapFocus: PropTypes.bool,

    /**
     * When true, Tab key navigation wraps at row boundaries.
     * Tab at end of row moves to first cell of next row.
     * Shift+Tab at start of row moves to last cell of previous row.
     * Works in both selection mode (just moves selection) and edit mode (opens editor on new cell).
     * At grid boundaries (first/last cell), stays put.
     * Default: false
     */
    tabWrapping: PropTypes.bool,

    /**
     * When true, the grid automatically scrolls to keep the active cell visible
     * when selection changes via keyboard navigation.
     * When false, the active cell may scroll out of view.
     * Default: true
     */
    scrollToActiveCell: PropTypes.bool,

    /**
     * Column selection modifier key behavior.
     * - "auto": Requires Ctrl/Cmd for multi-column selection (default)
     * - "multi": Allows multi-column selection without modifier keys
     * Default: "auto"
     */
    columnSelectionMode: PropTypes.oneOf(['auto', 'multi']),

    // ========== UNDO/REDO ==========

    /**
     * Enable undo/redo functionality.
     * When enabled, cell edits can be undone/redone using Cmd+Z/Cmd+Shift+Z (Mac)
     * or Ctrl+Z/Ctrl+Y (Windows/Linux), or programmatically via undoRedoAction.
     * Default: false
     */
    enableUndoRedo: PropTypes.bool,

    /**
     * Maximum number of undo steps to track.
     * Older edits beyond this limit will be discarded.
     * Default: 50
     */
    maxUndoSteps: PropTypes.number,

    /**
     * Trigger undo or redo programmatically from Dash.
     * Set this prop to trigger an undo or redo action.
     * Format: {"action": "undo"|"redo", "timestamp": 1234567890}
     * The timestamp is used to detect changes and should be unique for each action.
     */
    undoRedoAction: PropTypes.shape({
        action: PropTypes.oneOf(['undo', 'redo']).isRequired,
        timestamp: PropTypes.number.isRequired
    }),

    /**
     * Whether undo is available (read-only output prop).
     * True when there are edits that can be undone.
     */
    canUndo: PropTypes.bool,

    /**
     * Whether redo is available (read-only output prop).
     * True when there are undone edits that can be redone.
     */
    canRedo: PropTypes.bool,

    /**
     * Information about the last undo/redo operation performed (read-only output prop).
     * Emitted when an undo or redo action is performed.
     * Format: {"action": "undo"|"redo", "timestamp": 1234567890}
     */
    undoRedoPerformed: PropTypes.shape({
        action: PropTypes.oneOf(['undo', 'redo']),
        timestamp: PropTypes.number
    }),

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default GlideGrid;

export const defaultProps = GlideGrid.defaultProps;
export const propTypes = GlideGrid.propTypes;
