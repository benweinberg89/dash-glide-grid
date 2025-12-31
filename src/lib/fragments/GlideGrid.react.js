import React, { useCallback, useMemo, useState, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import DataEditor, { GridCellKind, CompactSelection } from '@glideapps/glide-data-grid';
import '@glideapps/glide-data-grid/dist/index.css';
import { allCells } from '@glideapps/glide-data-grid-cells';
import '@glideapps/glide-data-grid-cells/dist/index.css';
import DropdownCellRenderer from '../cells/DropdownCellRenderer';
import MultiSelectCellRenderer from '../cells/MultiSelectCellRenderer';
import { createButtonCellRenderer } from '../cells/ButtonCellRenderer';
import { createTagsCellRenderer } from '../cells/TagsCellRenderer';
import { createUserProfileCellRenderer } from '../cells/UserProfileCellRenderer';
import { createSpinnerCellRenderer } from '../cells/SpinnerCellRenderer';
import { createStarCellRenderer } from '../cells/StarCellRenderer';
import { createDatePickerCellRenderer } from '../cells/DatePickerCellRenderer';
import { createRangeCellRenderer } from '../cells/RangeCellRenderer';
import { createLinksCellRenderer } from '../cells/LinksCellRenderer';
import { createSparklineCellRenderer } from '../cells/SparklineCellRenderer';
import { createTreeViewCellRenderer } from '../cells/TreeViewCellRenderer';
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { executeFunction, isFunctionRef } from '../utils/functionParser';
import HeaderMenu from './HeaderMenu.react';
import ContextMenu from './ContextMenu.react';

// Static cell renderers: replace library's versions with custom versions
// Button renderer is added dynamically inside component to access setProps
const staticRenderers = [
    ...allCells.filter(
        (c) =>
            !c.isMatch?.({ data: { kind: 'dropdown-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'multi-select-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'button-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'tags-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'user-profile-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'spinner-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'star-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'date-picker-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'range-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'links-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'sparkline-cell' } }) &&
            !c.isMatch?.({ data: { kind: 'tree-view-cell' } })
    ),
    DropdownCellRenderer,
    MultiSelectCellRenderer,
    createTagsCellRenderer(),
    createUserProfileCellRenderer(),
    createSpinnerCellRenderer(),
    createStarCellRenderer(),
    createDatePickerCellRenderer(),
    createRangeCellRenderer(),
    createSparklineCellRenderer(),
];

/**
 * Helper function to auto-detect cell type from simple JavaScript values
 */
function autoDetectCellType(value) {
    if (value === null || value === undefined) {
        return {
            kind: GridCellKind.Text,
            data: '',
            allowOverlay: true,
            displayData: ''
        };
    }

    if (typeof value === 'boolean') {
        return {
            kind: GridCellKind.Boolean,
            data: value,
            allowOverlay: true
        };
    }

    if (typeof value === 'number') {
        return {
            kind: GridCellKind.Number,
            data: value,
            allowOverlay: true,
            displayData: value.toString()
        };
    }

    // Default to text
    return {
        kind: GridCellKind.Text,
        data: String(value),
        allowOverlay: true,
        displayData: String(value)
    };
}

/**
 * Helper function to transform cell objects from Python format to Glide format
 */
function transformCellObject(cellObj) {
    const kindMap = {
        'text': GridCellKind.Text,
        'number': GridCellKind.Number,
        'markdown': GridCellKind.Markdown,
        'uri': GridCellKind.Uri,
        'image': GridCellKind.Image,
        'bubble': GridCellKind.Bubble,
        'boolean': GridCellKind.Boolean,
        'drilldown': GridCellKind.Drilldown,
        'loading': GridCellKind.Loading,
        'rowid': GridCellKind.RowID,
        'protected': GridCellKind.Protected
    };

    // Handle custom cell types (dropdown, multiselect, button, tags, user-profile, spinner, etc.)
    const customCellKinds = [
        'dropdown-cell',
        'multi-select-cell',
        'button-cell',
        'tags-cell',
        'user-profile-cell',
        'spinner-cell',
        'star-cell',
        'date-picker-cell',
        'range-cell',
        'links-cell',
        'sparkline-cell',
        'tree-view-cell',
    ];
    if (customCellKinds.includes(cellObj.kind)) {
        // Read-only cell types that don't need overlay editors
        const readOnlyCellKinds = ['button-cell', 'user-profile-cell', 'spinner-cell', 'links-cell', 'sparkline-cell', 'tree-view-cell'];
        // Cells that require nested data structure: {"kind": "...", "data": {...}}
        const nestedDataCells = ['dropdown-cell', 'multi-select-cell'];
        // For dropdown/multi-select, data must be in nested format
        const cellData = nestedDataCells.includes(cellObj.kind)
            ? (cellObj.data || {})  // nested format required
            : cellObj;

        // Auto-derive copyData from cell value if not explicitly provided
        const deriveCopyData = () => {
            if (cellObj.copyData) return cellObj.copyData;
            switch (cellObj.kind) {
                case 'dropdown-cell':
                    return cellData.value || '';
                case 'multi-select-cell':
                    return Array.isArray(cellData.values) ? cellData.values.join(', ') : '';
                case 'tags-cell':
                    return Array.isArray(cellData.tags) ? cellData.tags.join(', ') : '';
                case 'star-cell':
                    return cellData.rating != null ? String(cellData.rating) : '';
                case 'date-picker-cell':
                    return cellData.displayDate || cellData.date || '';
                case 'range-cell':
                    return cellData.label || (cellData.value != null ? String(cellData.value) : '');
                case 'links-cell':
                    // Use markdown format [title](url) to preserve both title and href
                    return Array.isArray(cellData.links)
                        ? cellData.links.map(l => {
                            const title = l.title || l.href || '';
                            const href = l.href || '';
                            // Only use markdown if title differs from href
                            return title === href ? href : `[${title}](${href})`;
                        }).join(', ')
                        : '';
                case 'sparkline-cell':
                    return Array.isArray(cellData.values) ? cellData.values.join(', ') : '';
                case 'tree-view-cell':
                    // Use pipe-delimited format to preserve tree structure: text|depth|canOpen|isOpen
                    return `${cellData.text || ''}|${cellData.depth || 0}|${cellData.canOpen || false}|${cellData.isOpen || false}`;
                case 'user-profile-cell':
                    return cellData.name || '';
                case 'button-cell':
                    return cellData.title || '';
                case 'spinner-cell':
                default:
                    return cellObj.title || cellObj.name || '';
            }
        };

        const result = {
            kind: GridCellKind.Custom,
            allowOverlay: !readOnlyCellKinds.includes(cellObj.kind) && cellObj.allowOverlay !== false,
            copyData: deriveCopyData(),
            data: {
                kind: cellObj.kind,
                ...cellData
            }
        };

        // Add optional properties if present
        if (cellObj.readonly !== undefined) {
            result.readonly = cellObj.readonly;
        }
        if (cellObj.themeOverride) {
            result.themeOverride = cellObj.themeOverride;
        }
        if (cellObj.lastUpdated !== undefined) {
            result.lastUpdated = cellObj.lastUpdated;
        }

        return result;
    }

    const cellKind = kindMap[cellObj.kind] || GridCellKind.Text;

    const result = {
        kind: cellKind,
        data: cellObj.data,
        allowOverlay: cellObj.allowOverlay !== false,
    };

    // Only set displayData for cell types that use it (not Image, Loading, or Protected cells)
    if (cellKind !== GridCellKind.Image && cellKind !== GridCellKind.Loading && cellKind !== GridCellKind.Protected) {
        // Use ?? instead of || to preserve falsy values like 0 and false
        result.displayData = cellObj.displayData ?? String(cellObj.data ?? '');
    }

    // Add optional properties if present
    if (cellObj.readonly !== undefined) {
        result.readonly = cellObj.readonly;
    }
    if (cellObj.themeOverride) {
        result.themeOverride = cellObj.themeOverride;
    }
    if (cellObj.span !== undefined && Array.isArray(cellObj.span) && cellObj.span.length === 2) {
        result.span = cellObj.span;
    }
    if (cellObj.allowWrapping !== undefined) {
        result.allowWrapping = cellObj.allowWrapping;
    }
    if (cellObj.lastUpdated !== undefined) {
        result.lastUpdated = cellObj.lastUpdated;
    }
    if (cellObj.contentAlign !== undefined) {
        result.contentAlign = cellObj.contentAlign;
    }
    if (cellObj.cursor !== undefined) {
        result.cursor = cellObj.cursor;
    }

    // Handle NumberCell specific properties
    if (cellKind === GridCellKind.Number) {
        if (cellObj.fixedDecimals !== undefined) {
            result.fixedDecimals = cellObj.fixedDecimals;
        }
        if (cellObj.allowNegative !== undefined) {
            result.allowNegative = cellObj.allowNegative;
        }
        if (cellObj.thousandSeparator !== undefined) {
            result.thousandSeparator = cellObj.thousandSeparator;
        }
        if (cellObj.decimalSeparator !== undefined) {
            result.decimalSeparator = cellObj.decimalSeparator;
        }
    }

    // Handle BooleanCell specific properties
    if (cellKind === GridCellKind.Boolean) {
        if (cellObj.maxSize !== undefined) {
            result.maxSize = cellObj.maxSize;
        }
    }

    // Handle specific cell type properties
    if (cellKind === GridCellKind.Uri) {
        if (cellObj.data) {
            result.data = cellObj.data;
        }
        if (cellObj.hoverEffect !== undefined) {
            result.hoverEffect = cellObj.hoverEffect;
        }
    }
    if (cellKind === GridCellKind.Image) {
        if (cellObj.data) {
            result.data = Array.isArray(cellObj.data) ? cellObj.data : [cellObj.data];
        }
        if (cellObj.displayData) {
            result.displayData = Array.isArray(cellObj.displayData) ? cellObj.displayData : [cellObj.displayData];
        }
        if (cellObj.rounding !== undefined) {
            result.rounding = cellObj.rounding;
        }
    }
    if (cellKind === GridCellKind.Bubble && cellObj.data) {
        result.data = Array.isArray(cellObj.data) ? cellObj.data : [cellObj.data];
    }
    if (cellKind === GridCellKind.Drilldown && cellObj.data) {
        // Drilldown data is an array of objects with text and optional img
        result.data = Array.isArray(cellObj.data) ? cellObj.data : [cellObj.data];
    }
    if (cellKind === GridCellKind.Loading) {
        // Loading cells don't need data, just the kind and optional skeleton dimensions
        result.allowOverlay = false;
        if (cellObj.skeletonWidth !== undefined) {
            result.skeletonWidth = cellObj.skeletonWidth;
        }
        if (cellObj.skeletonHeight !== undefined) {
            result.skeletonHeight = cellObj.skeletonHeight;
        }
        if (cellObj.skeletonWidthVariability !== undefined) {
            result.skeletonWidthVariability = cellObj.skeletonWidthVariability;
        }
    }

    return result;
}

/**
 * GlideGrid is a high-performance data grid component for Dash.
 * It wraps the Glide Data Grid library to provide an Excel-like grid experience
 * with support for millions of rows, multiple cell types, and rich interactions.
 */
const GlideGrid = (props) => {
    const {
        id,
        columns,
        data,
        rows,
        height,
        width,
        rowHeight,
        headerHeight,
        freezeColumns,
        freezeTrailingRows,
        groupHeaderHeight,
        fixedShadowX,
        fixedShadowY,
        overscrollX,
        overscrollY,
        drawFocusRing,
        preventDiagonalScrolling,
        scaleToRem,
        className,
        rowSelect,
        columnSelect,
        rangeSelect,
        rowSelectionMode,
        columnSelectionBlending,
        rowSelectionBlending,
        rangeSelectionBlending,
        spanRangeBehavior,
        showSearch,
        searchValue,
        columnResize,
        minColumnWidth,
        maxColumnWidth,
        maxColumnAutoWidth,
        rowMarkers,
        rowMarkerStartIndex,
        rowMarkerWidth,
        rowMarkerTheme,
        smoothScrollX,
        smoothScrollY,
        verticalBorder,
        readonly,
        enableCopyPaste,
        copyHeaders,
        fillHandle,
        allowedFillDirections,
        theme,
        selectedCell,
        selectedRows,
        selectedColumns,
        selectedRange,
        selectedRanges,
        nClicks,
        highlightRegions,
        trailingRowOptions,
        scrollToCell,
        scrollOffsetX,
        scrollOffsetY,
        keybindings,
        isDraggable,
        columnMovable,
        rowMovable,
        experimental,
        validateCell,
        coercePasteValue,
        getRowThemeOverride,
        drawCell,
        drawHeader,
        sortable,
        sortColumns,
        sortingOrder,
        columnFilters,
        headerMenuConfig,
        contextMenuConfig,
        selectionColumnMin,
        unselectableColumns,
        unselectableRows,
        rowSelectOnCellClick,
        hoverRow,
        cellActivationBehavior,
        editOnType,
        rangeSelectionColumnSpanning,
        trapFocus,
        tabWrapping,
        scrollToActiveCell,
        columnSelectionMode,
        enableUndoRedo,
        maxUndoSteps,
        undoRedoAction,
        editorScrollBehavior,
        contextMenuScrollBehavior,
        redrawTrigger,
        remeasureColumns,
        showCellFlash,
        allowDelete,
        hiddenRows,
        hiddenRowsConfig,
        setProps
    } = props;

    // Internal state for grid selection (for visual feedback and editing)
    const [gridSelection, setGridSelection] = useState({
        columns: CompactSelection.empty(),
        rows: CompactSelection.empty(),
    });

    // Local state for optimistic updates (so edits appear immediately)
    const [localData, setLocalData] = useState(data);
    const [localColumns, setLocalColumns] = useState(columns);
    const [localSearchValue, setLocalSearchValue] = useState(searchValue || '');

    // Local state for sorting (to enable immediate UI updates)
    const [localSortColumns, setLocalSortColumns] = useState(sortColumns || []);

    // Editor scroll behavior state
    const [isEditorOpen, setIsEditorOpen] = useState(false);
    const scrollPositionRef = useRef({ x: 0, y: 0 });

    // Context menu scroll behavior state
    const contextMenuScrollPositionRef = useRef({ x: 0, y: 0 });
    const contextMenuWheelHandlerRef = useRef(null);
    const contextMenuScrollHandlerRef = useRef(null);

    // Local state for column filters (synced with Dash prop)
    const [localFilters, setLocalFilters] = useState(columnFilters || {});

    // State for the filter menu
    const [filterMenuState, setFilterMenuState] = useState({
        isOpen: false,
        columnIndex: null,
        position: null
    });

    // State for the cell context menu
    const [contextMenuState, setContextMenuState] = useState({
        isOpen: false,
        col: null,
        row: null,
        position: null
    });

    // Ref to track the last right-click mouse position (for context menu positioning)
    const lastContextMenuPosition = useRef({ x: 0, y: 0 });

    // State for row hover effect
    const [hoveredRow, setHoveredRow] = useState(null);

    // Create Set for O(1) hidden row lookups
    const hiddenRowsSet = useMemo(() => {
        return new Set(hiddenRows || []);
    }, [hiddenRows]);

    // Extract hidden rows config options (all default to true - skip hidden rows)
    const {
        skipOnCopy = true,
        skipOnPaste = true,
        skipOnFill = true,
        skipOnDelete = true,
        skipOnNavigation = true,
    } = hiddenRowsConfig || {};

    // Ref to track current data (to avoid stale closures in rapid callbacks)
    const localDataRef = useRef(data);

    // Ref to track current columns (to avoid stale closures in rapid callbacks)
    const localColumnsRef = useRef(columns);

    // Ref to track the last data we sent to Dash (to prevent overwriting our own updates)
    const lastSentData = useRef(null);

    // Ref to track the last search value we sent to Dash
    const lastSentSearchValue = useRef(null);

    // Ref to track current search value (to avoid stale closures)
    const localSearchValueRef = useRef(searchValue || '');

    // Ref to track when we should ignore empty strings (Glide bug workaround)
    // Glide calls onSearchValueChange with '' multiple times after setting a value
    const ignoreEmptyUntil = useRef(0);

    // Ref for the container div to detect scrolling
    const containerRef = useRef(null);

    // Ref for the DataEditor to control scroll position
    const gridRef = useRef(null);

    // Capture native contextmenu event to get accurate mouse position
    useEffect(() => {
        const container = containerRef.current;
        if (!container) return;

        const handleNativeContextMenu = (e) => {
            // Store the mouse position for use in the Glide callback
            lastContextMenuPosition.current = { x: e.clientX, y: e.clientY };
        };

        // Use capture phase to get the position before Glide handles the event
        container.addEventListener('contextmenu', handleNativeContextMenu, true);
        return () => {
            container.removeEventListener('contextmenu', handleNativeContextMenu, true);
        };
    }, []);

    // ========== LAST UPDATED STATE ==========
    // Track lastUpdated timestamps for cells (for flash effect on edit/undo/redo)
    // Map of "row,col" -> timestamp (performance.now())
    const [lastUpdatedCells, setLastUpdatedCells] = useState({});

    // Helper to check if flash should be triggered for a specific operation
    const shouldFlash = useCallback((operation) => {
        if (showCellFlash === true) return true;
        if (showCellFlash === false || !showCellFlash) return false;
        if (Array.isArray(showCellFlash)) return showCellFlash.includes(operation);
        return false;
    }, [showCellFlash]);

    // Helper to trigger flash effect for copied cells
    const triggerCopyFlash = useCallback(() => {
        if (!gridSelection.current) return;

        const now = performance.now();
        const updatedCells = {};

        // Handle range selection
        if (gridSelection.current.range) {
            const range = gridSelection.current.range;
            for (let row = range.y; row < range.y + range.height; row++) {
                for (let col = range.x; col < range.x + range.width; col++) {
                    // Get actual row index if sorted
                    const actualRow = sortedIndices ? sortedIndices[row] : row;
                    if (actualRow !== undefined && actualRow < (localData?.length || 0)) {
                        updatedCells[`${actualRow},${col}`] = now;
                    }
                }
            }
        }
        // Handle single cell (no range, just the focused cell)
        else if (gridSelection.current.cell) {
            const [col, row] = gridSelection.current.cell;
            const actualRow = sortedIndices ? sortedIndices[row] : row;
            if (actualRow !== undefined && actualRow < (localData?.length || 0)) {
                updatedCells[`${actualRow},${col}`] = now;
            }
        }

        if (Object.keys(updatedCells).length > 0) {
            setLastUpdatedCells(prev => ({ ...prev, ...updatedCells }));
        }
    }, [gridSelection, sortedIndices, localData]);

    // ========== UNDO/REDO STATE ==========
    // Undo/redo history stacks
    const [undoStack, setUndoStack] = useState([]);  // Array of edit batches
    const [redoStack, setRedoStack] = useState([]);  // Array of undone batches

    // Refs for undo/redo tracking (to avoid stale closures and prevent circular updates)
    const isApplyingUndoRedoRef = useRef(false);     // Prevent tracking edits during undo/redo
    const batchTimeoutRef = useRef(null);            // For batching rapid edits
    const currentBatchRef = useRef([]);              // Current batch of edits being collected
    const lastUndoRedoActionRef = useRef(null);      // Track last processed undoRedoAction
    const lastRemeasureColumnsRef = useRef(null);    // Track last processed remeasureColumns action
    const pendingWrapRef = useRef(null);             // Track pending Tab wrap for row boundaries

    // Refs for rowSelectOnCellClick feature
    const lastSelectedRowRef = useRef(null);         // Track last selected row for shift+click range selection
    const currentRowSelectionRef = useRef(CompactSelection.empty()); // Track current row selection state
    const modifierKeysRef = useRef({ shiftKey: false, ctrlKey: false, metaKey: false }); // Track modifier keys globally

    // Refs for column multi-range selection
    const lastSelectedColumnRef = useRef(null);      // Track last selected column for shift+click range selection
    const currentColumnSelectionRef = useRef(CompactSelection.empty()); // Track current column selection state

    // Ref to hold custom renderers for use in handlePaste
    const customRenderersRef = useRef(null);

    // Keep refs in sync with state
    useEffect(() => {
        localDataRef.current = localData;
    }, [localData]);

    useEffect(() => {
        localColumnsRef.current = localColumns;
    }, [localColumns]);

    // Track modifier keys globally for row marker shift+click detection
    useEffect(() => {
        const handleModifierChange = (e) => {
            modifierKeysRef.current = {
                shiftKey: e.shiftKey,
                ctrlKey: e.ctrlKey,
                metaKey: e.metaKey
            };
        };

        window.addEventListener('keydown', handleModifierChange);
        window.addEventListener('keyup', handleModifierChange);
        window.addEventListener('mousedown', handleModifierChange, true);

        return () => {
            window.removeEventListener('keydown', handleModifierChange);
            window.removeEventListener('keyup', handleModifierChange);
            window.removeEventListener('mousedown', handleModifierChange, true);
        };
    }, []);

    // Sync local data with props when props change from outside (but not from our own updates)
    useEffect(() => {
        // If the incoming data is the same as what we just sent, ignore it
        // Clear lastSentData after matching to prevent stale comparisons blocking future updates
        if (lastSentData.current && JSON.stringify(data) === JSON.stringify(lastSentData.current)) {
            lastSentData.current = null;
            return;
        }

        setLocalData(data);
    }, [data]);

    // Sync local columns with props when columns change from outside
    useEffect(() => {
        setLocalColumns(columns);
    }, [columns]);

    // Sync local sort columns with props when sortColumns change from outside
    useEffect(() => {
        setLocalSortColumns(sortColumns || []);
    }, [sortColumns]);

    // Sync local filters with props when columnFilters change from outside
    useEffect(() => {
        setLocalFilters(columnFilters || {});
    }, [columnFilters]);

    // ========== UNDO/REDO FUNCTIONS ==========

    // Helper to add an edit to the current batch
    const addEditToBatch = useCallback((edit) => {
        if (!enableUndoRedo || isApplyingUndoRedoRef.current) return;

        // Add edit to current batch
        currentBatchRef.current.push(edit);

        // Clear existing timeout
        if (batchTimeoutRef.current) {
            clearTimeout(batchTimeoutRef.current);
        }

        // Set new timeout to finalize batch
        batchTimeoutRef.current = setTimeout(() => {
            if (currentBatchRef.current.length > 0) {
                const batch = [...currentBatchRef.current];
                currentBatchRef.current = [];

                // Limit undo stack size
                const maxSteps = maxUndoSteps || 50;
                setUndoStack(prev => {
                    const newStack = [...prev, batch];
                    if (newStack.length > maxSteps) {
                        return newStack.slice(-maxSteps);
                    }
                    return newStack;
                });

                // Clear redo stack when new edit is made
                setRedoStack([]);
            }
        }, 100);  // 100ms batch window
    }, [enableUndoRedo, maxUndoSteps]);

    // Perform undo operation
    const performUndo = useCallback(() => {
        if (!enableUndoRedo || undoStack.length === 0) return;

        const batch = undoStack[undoStack.length - 1];
        const currentData = localDataRef.current;
        const newData = currentData.map(r => ({ ...r }));

        // Apply edits in reverse order, restoring old values
        isApplyingUndoRedoRef.current = true;

        for (let i = batch.length - 1; i >= 0; i--) {
            const edit = batch[i];
            newData[edit.row] = { ...newData[edit.row], [edit.columnId]: edit.oldValue };
        }

        // Update local state
        setLocalData(newData);
        localDataRef.current = newData;
        lastSentData.current = newData;

        // Move batch to redo stack
        setUndoStack(prev => prev.slice(0, -1));
        setRedoStack(prev => [...prev, batch]);

        // Set lastUpdated timestamps for flash effect on all affected cells
        if (shouldFlash('undo')) {
            const now = performance.now();
            const updatedCells = {};
            for (const edit of batch) {
                updatedCells[`${edit.row},${edit.col}`] = now;
            }
            setLastUpdatedCells(prev => ({ ...prev, ...updatedCells }));
        }

        // Sync with Dash
        if (setProps) {
            setProps({
                data: newData,
                undoRedoPerformed: {
                    action: 'undo',
                    timestamp: Date.now()
                }
            });
        }

        // Refresh grid display
        if (gridRef.current) {
            gridRef.current.updateCells(
                batch.map(edit => ({ cell: [edit.col, edit.row] }))
            );
        }

        isApplyingUndoRedoRef.current = false;
    }, [enableUndoRedo, undoStack, setProps]);

    // Perform redo operation
    const performRedo = useCallback(() => {
        if (!enableUndoRedo || redoStack.length === 0) return;

        const batch = redoStack[redoStack.length - 1];
        const currentData = localDataRef.current;
        const newData = currentData.map(r => ({ ...r }));

        // Apply edits in forward order, applying new values
        isApplyingUndoRedoRef.current = true;

        for (const edit of batch) {
            newData[edit.row] = { ...newData[edit.row], [edit.columnId]: edit.newValue };
        }

        // Update local state
        setLocalData(newData);
        localDataRef.current = newData;
        lastSentData.current = newData;

        // Move batch to undo stack
        setRedoStack(prev => prev.slice(0, -1));
        setUndoStack(prev => [...prev, batch]);

        // Set lastUpdated timestamps for flash effect on all affected cells
        if (shouldFlash('redo')) {
            const now = performance.now();
            const updatedCells = {};
            for (const edit of batch) {
                updatedCells[`${edit.row},${edit.col}`] = now;
            }
            setLastUpdatedCells(prev => ({ ...prev, ...updatedCells }));
        }

        // Sync with Dash
        if (setProps) {
            setProps({
                data: newData,
                undoRedoPerformed: {
                    action: 'redo',
                    timestamp: Date.now()
                }
            });
        }

        // Refresh grid display
        if (gridRef.current) {
            gridRef.current.updateCells(
                batch.map(edit => ({ cell: [edit.col, edit.row] }))
            );
        }

        isApplyingUndoRedoRef.current = false;
    }, [enableUndoRedo, redoStack, setProps]);

    // Sync canUndo/canRedo to Dash
    useEffect(() => {
        if (setProps && enableUndoRedo) {
            setProps({
                canUndo: undoStack.length > 0,
                canRedo: redoStack.length > 0
            });
        }
    }, [undoStack.length, redoStack.length, enableUndoRedo, setProps]);

    // Handle undoRedoAction prop from Dash
    useEffect(() => {
        if (!undoRedoAction || !enableUndoRedo) return;

        // Avoid processing the same action twice
        if (lastUndoRedoActionRef.current &&
            lastUndoRedoActionRef.current.timestamp === undoRedoAction.timestamp) {
            return;
        }
        lastUndoRedoActionRef.current = undoRedoAction;

        if (undoRedoAction.action === 'undo') {
            performUndo();
        } else if (undoRedoAction.action === 'redo') {
            performRedo();
        }
    }, [undoRedoAction, enableUndoRedo, performUndo, performRedo]);

    // Handle remeasureColumns prop from Dash - triggers column auto-resize
    useEffect(() => {
        if (!remeasureColumns || !gridRef.current) return;

        // Avoid processing the same action twice
        if (lastRemeasureColumnsRef.current &&
            lastRemeasureColumnsRef.current.timestamp === remeasureColumns.timestamp) {
            return;
        }
        lastRemeasureColumnsRef.current = remeasureColumns;

        // Build CompactSelection from column indices
        const columnIndices = remeasureColumns.columns;
        let selection;

        if (!columnIndices || columnIndices.length === 0) {
            // Remeasure all columns
            const numCols = localColumns ? localColumns.length : 0;
            selection = CompactSelection.empty();
            for (let i = 0; i < numCols; i++) {
                selection = selection.add(i);
            }
        } else {
            // Remeasure specific columns
            selection = CompactSelection.empty();
            for (const idx of columnIndices) {
                selection = selection.add(idx);
            }
        }

        gridRef.current.remeasureColumns(selection);
    }, [remeasureColumns, localColumns]);

    // Clear undo/redo history when data changes externally
    useEffect(() => {
        // Only clear if we're not the ones who changed the data
        if (lastSentData.current && JSON.stringify(data) !== JSON.stringify(lastSentData.current)) {
            setUndoStack([]);
            setRedoStack([]);
            currentBatchRef.current = [];
            if (batchTimeoutRef.current) {
                clearTimeout(batchTimeoutRef.current);
                batchTimeoutRef.current = null;
            }
        }
    }, [data]);

    // Helper to get display value from a cell for filtering
    const getCellDisplayValue = useCallback((cellValue) => {
        // Handle null/undefined/empty
        if (cellValue === null || cellValue === undefined) {
            return '(Blank)';
        }
        if (cellValue === '') {
            return '(Blank)';
        }

        // Handle primitives directly
        if (typeof cellValue !== 'object') {
            return cellValue;
        }

        // Handle cell objects with kind property
        const kind = cellValue.kind;

        if (!kind) {
            // Legacy object without kind
            const data = cellValue.data;
            if (data === null || data === undefined || data === '') {
                return '(Blank)';
            }
            if (typeof data !== 'object') {
                return data;
            }
            return JSON.stringify(data);
        }

        // Handle custom cell types
        switch (kind) {
            case 'dropdown-cell': {
                const value = cellValue.data?.value;
                if (!value) return '(Blank)';
                // Try to find matching option with label
                const options = cellValue.data?.options || cellValue.data?.allowedValues || [];
                const matchedOption = options.find(opt =>
                    (typeof opt === 'object' ? opt.value : opt) === value
                );
                if (matchedOption && typeof matchedOption === 'object' && matchedOption.label) {
                    return matchedOption.label;
                }
                return value;
            }

            case 'multi-select-cell': {
                const values = cellValue.data?.values || [];
                if (values.length === 0) return '(Blank)';
                // Try to resolve labels
                const options = cellValue.data?.options || [];
                const labels = values.map(v => {
                    const opt = options.find(o =>
                        (typeof o === 'object' ? o.value : o) === v
                    );
                    return (opt && typeof opt === 'object' && opt.label) ? opt.label : v;
                });
                return labels.join(', ');
            }

            case 'button-cell':
                return cellValue.title || 'Button';

            case 'tags-cell': {
                const tags = cellValue.tags || [];
                if (tags.length === 0) return '(Blank)';
                return tags.join(', ');
            }

            case 'user-profile-cell':
                return cellValue.name || '(Blank)';

            case 'spinner-cell':
                return '(Loading)';

            case 'star-cell': {
                const rating = cellValue.rating || 0;
                const maxStars = cellValue.maxStars || 5;
                return `${rating}/${maxStars}`;
            }

            case 'date-picker-cell': {
                if (cellValue.displayDate) return cellValue.displayDate;
                if (!cellValue.date) return '(Blank)';
                try {
                    const d = new Date(cellValue.date);
                    if (!isNaN(d.getTime())) {
                        return d.toLocaleDateString();
                    }
                } catch {
                    // Fall through
                }
                return cellValue.date;
            }

            case 'range-cell': {
                if (cellValue.label !== undefined && cellValue.label !== null) {
                    return String(cellValue.label);
                }
                return cellValue.value ?? 0;
            }

            case 'links-cell': {
                const links = cellValue.links || [];
                if (links.length === 0) return '(Blank)';
                const titles = links.map(l => l.title || l.href || 'Link');
                return titles.join(', ');
            }

            case 'sparkline-cell': {
                const values = cellValue.values || [];
                if (values.length === 0) return '(Blank)';
                const sum = values.reduce((a, b) => a + (b || 0), 0);
                const avg = sum / values.length;
                return `Sparkline (avg: ${avg.toFixed(1)})`;
            }

            case 'tree-view-cell':
                return cellValue.text || '(Blank)';

            // Built-in cell types
            case 'markdown':
                return cellValue.data || '(Blank)';

            case 'uri':
                // Use displayData if available, otherwise the URL
                return cellValue.displayData || cellValue.data || '(Blank)';

            case 'image': {
                // Image data is an array of URLs
                const images = cellValue.data || [];
                if (images.length === 0) return '(Blank)';
                return `${images.length} image${images.length > 1 ? 's' : ''}`;
            }

            case 'bubble': {
                // Bubble data is an array of strings
                const bubbles = cellValue.data || [];
                if (bubbles.length === 0) return '(Blank)';
                return bubbles.join(', ');
            }

            case 'drilldown': {
                // Drilldown data is an array of objects with text property
                const items = cellValue.data || [];
                if (items.length === 0) return '(Blank)';
                return items.map(item => item.text || '').filter(Boolean).join(', ');
            }

            case 'loading':
                return '(Loading)';

            case 'rowid':
                return cellValue.data || '(Blank)';

            case 'protected':
                return '(Protected)';

            default: {
                // Unknown cell type - try data property
                const innerData = cellValue.data;
                if (innerData === null || innerData === undefined || innerData === '') {
                    return '(Blank)';
                }
                if (typeof innerData !== 'object') {
                    return innerData;
                }
                return JSON.stringify(innerData);
            }
        }
    }, []);

    // Helper to extract a sortable value from any cell type
    const extractSortValue = useCallback((cellValue) => {
        // Handle null/undefined
        if (cellValue === null || cellValue === undefined) {
            return { value: null, type: 'string' };
        }

        // Handle primitives directly
        if (typeof cellValue !== 'object') {
            if (typeof cellValue === 'number') {
                return { value: cellValue, type: 'number' };
            }
            if (typeof cellValue === 'boolean') {
                return { value: cellValue ? 1 : 0, type: 'number' };
            }
            return { value: String(cellValue), type: 'string' };
        }

        // Handle cell objects with kind property
        const kind = cellValue.kind;

        if (!kind) {
            // Legacy object without kind - try to extract meaningful value
            if (cellValue.data !== undefined) {
                return extractSortValue(cellValue.data);
            }
            // Fallback to JSON stringification
            try {
                return { value: JSON.stringify(cellValue), type: 'string' };
            } catch {
                return { value: '', type: 'string' };
            }
        }

        // Handle custom cell types
        switch (kind) {
            case 'dropdown-cell':
                return { value: cellValue.data?.value || '', type: 'string' };

            case 'multi-select-cell': {
                const values = cellValue.data?.values || [];
                return { value: [...values].sort().join(', '), type: 'string' };
            }

            case 'button-cell':
                // Buttons are not meaningfully sortable
                return { value: null, type: 'unsortable' };

            case 'tags-cell': {
                const tags = cellValue.tags || [];
                return { value: [...tags].sort().join(', '), type: 'string' };
            }

            case 'user-profile-cell':
                return { value: cellValue.name || '', type: 'string' };

            case 'spinner-cell':
                // Spinners are not sortable (loading state)
                return { value: null, type: 'unsortable' };

            case 'star-cell':
                return { value: cellValue.rating || 0, type: 'number' };

            case 'date-picker-cell':
                // ISO date strings sort correctly with localeCompare
                return { value: cellValue.date || '', type: 'date' };

            case 'range-cell':
                return { value: cellValue.value ?? 0, type: 'number' };

            case 'links-cell': {
                const links = cellValue.links || [];
                if (links.length === 0) return { value: '', type: 'string' };
                return { value: links[0]?.title || links[0]?.href || '', type: 'string' };
            }

            case 'sparkline-cell': {
                const sparkValues = cellValue.values || [];
                if (sparkValues.length === 0) return { value: 0, type: 'number' };
                const sum = sparkValues.reduce((acc, v) => acc + (v || 0), 0);
                const avg = sum / sparkValues.length;
                return { value: avg, type: 'number' };
            }

            case 'tree-view-cell':
                return { value: cellValue.text || '', type: 'string' };

            // Built-in cell types
            case 'markdown':
                return { value: cellValue.data || '', type: 'string' };

            case 'uri':
                // Sort by displayData if available, otherwise URL
                return { value: cellValue.displayData || cellValue.data || '', type: 'string' };

            case 'image': {
                // Sort by number of images
                const images = cellValue.data || [];
                return { value: images.length, type: 'number' };
            }

            case 'bubble': {
                // Sort by joined bubble values
                const bubbles = cellValue.data || [];
                return { value: [...bubbles].sort().join(', '), type: 'string' };
            }

            case 'drilldown': {
                // Sort by first item's text
                const items = cellValue.data || [];
                if (items.length === 0) return { value: '', type: 'string' };
                return { value: items[0]?.text || '', type: 'string' };
            }

            case 'loading':
                // Loading cells are not meaningfully sortable
                return { value: null, type: 'unsortable' };

            case 'rowid':
                return { value: cellValue.data || '', type: 'string' };

            case 'protected':
                // Protected cells are not meaningfully sortable
                return { value: null, type: 'unsortable' };

            default: {
                // Unknown custom cell - try to extract data property
                if (cellValue.data !== undefined) {
                    return extractSortValue(cellValue.data);
                }
                try {
                    return { value: JSON.stringify(cellValue), type: 'string' };
                } catch {
                    return { value: '', type: 'string' };
                }
            }
        }
    }, []);

    // Compute unique values for a column (for filter menu)
    const getUniqueColumnValues = useCallback((colIndex) => {
        if (!localData || !localColumns) return [];
        // Get column id to access dict key
        const columnDef = localColumns[colIndex];
        const columnId = columnDef?.id || columnDef?.title;

        const valueSet = new Set();
        localData.forEach(row => {
            if (row) {
                const val = getCellDisplayValue(row[columnId]);
                valueSet.add(val);
            }
        });
        // Sort with (Blank) first
        return Array.from(valueSet).sort((a, b) => {
            if (a === '(Blank)') return -1;
            if (b === '(Blank)') return 1;
            return String(a).localeCompare(String(b));
        });
    }, [localData, localColumns, getCellDisplayValue]);

    // Compute display indices - combines filtering and sorting
    // Maps display row index to original data row index
    const displayIndices = useMemo(() => {
        if (!localData) return null;

        // Start with all indices
        let indices = localData.map((_, i) => i);

        // Step 1: Apply filters
        const filterEntries = Object.entries(localFilters);
        if (filterEntries.length > 0) {
            indices = indices.filter(idx => {
                const rowData = localData[idx];
                if (!rowData) return false;

                // Check all active filters
                for (const [colIndexStr, selectedValues] of filterEntries) {
                    const colIndex = parseInt(colIndexStr, 10);
                    // Get column id to access dict key
                    const columnDef = localColumns?.[colIndex];
                    const columnId = columnDef?.id || columnDef?.title;

                    const cellValue = getCellDisplayValue(rowData[columnId]);

                    // If selectedValues is null or empty array, filter out everything
                    if (!selectedValues || selectedValues.length === 0) {
                        return false;
                    }

                    // Check if this cell's value is in the selected values
                    if (!selectedValues.includes(cellValue)) {
                        return false;
                    }
                }
                return true;
            });
        }

        // Step 2: Apply sorting (only if sortable and we have sort columns)
        if (sortable && localSortColumns && localSortColumns.length > 0) {
            indices.sort((a, b) => {
                for (const sortCol of localSortColumns) {
                    const { columnIndex, direction } = sortCol;
                    // Get column id to access dict key
                    const columnDef = localColumns?.[columnIndex];
                    const columnId = columnDef?.id || columnDef?.title;

                    // Extract sortable values using our helper
                    const extractedA = extractSortValue(localData[a]?.[columnId]);
                    const extractedB = extractSortValue(localData[b]?.[columnId]);

                    const valA = extractedA.value;
                    const valB = extractedB.value;
                    const typeA = extractedA.type;
                    const typeB = extractedB.type;

                    // Skip unsortable cells (treat as equal)
                    if (typeA === 'unsortable' && typeB === 'unsortable') continue;
                    if (typeA === 'unsortable') return direction === 'asc' ? 1 : -1;
                    if (typeB === 'unsortable') return direction === 'asc' ? -1 : 1;

                    // Handle null/undefined (nulls sort to end)
                    if (valA == null && valB == null) continue;
                    if (valA == null) return direction === 'asc' ? 1 : -1;
                    if (valB == null) return direction === 'asc' ? -1 : 1;

                    // Compare based on extracted type
                    let comparison = 0;

                    if (typeA === 'number' && typeB === 'number') {
                        // Numeric comparison
                        comparison = valA - valB;
                    } else if (typeA === 'date' && typeB === 'date') {
                        // Date comparison (ISO strings compare correctly with localeCompare)
                        comparison = String(valA).localeCompare(String(valB));
                    } else {
                        // String comparison (case-insensitive)
                        const strA = String(valA).toLowerCase();
                        const strB = String(valB).toLowerCase();
                        comparison = strA.localeCompare(strB);
                    }

                    if (comparison !== 0) {
                        return direction === 'asc' ? comparison : -comparison;
                    }
                }
                return 0;
            });
        }

        // Return null if no filtering/sorting applied (identity mapping)
        if (indices.length === localData.length &&
            filterEntries.length === 0 &&
            (!sortable || !localSortColumns || localSortColumns.length === 0)) {
            return null;
        }

        return indices;
    }, [localData, localColumns, localFilters, sortable, localSortColumns, getCellDisplayValue, extractSortValue]);

    // Alias for backwards compatibility - displayIndices now handles both filtering and sorting
    const sortedIndices = displayIndices;

    // Button cell click handler - fires buttonClicked prop to Dash
    const buttonClickHandler = useCallback((info) => {
        const actualRow = sortedIndices ? sortedIndices[info.row] : info.row;
        if (setProps) {
            setProps({
                buttonClicked: {
                    col: info.col,
                    row: actualRow,
                    title: info.title,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, sortedIndices]);

    // Link cell click handler - fires linkClicked prop to Dash
    const linkClickHandler = useCallback((info) => {
        const actualRow = sortedIndices ? sortedIndices[info.row] : info.row;
        if (setProps) {
            setProps({
                linkClicked: {
                    col: info.col,
                    row: actualRow,
                    href: info.href,
                    title: info.title,
                    linkIndex: info.linkIndex,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, sortedIndices]);

    // Tree node toggle handler - fires treeNodeToggled prop to Dash
    const treeNodeToggleHandler = useCallback((info) => {
        const actualRow = sortedIndices ? sortedIndices[info.row] : info.row;
        if (setProps) {
            setProps({
                treeNodeToggled: {
                    col: info.col,
                    row: actualRow,
                    isOpen: info.isOpen,
                    depth: info.depth,
                    text: info.text,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, sortedIndices]);

    // Custom renderers including button cell, links cell, and tree view cell with click handlers
    const customRenderers = useMemo(() => [
        ...staticRenderers,
        createButtonCellRenderer(buttonClickHandler),
        createLinksCellRenderer(linkClickHandler),
        createTreeViewCellRenderer(treeNodeToggleHandler)
    ], [buttonClickHandler, linkClickHandler, treeNodeToggleHandler]);

    // Keep customRenderers ref in sync for use in handlePaste
    useEffect(() => {
        customRenderersRef.current = customRenderers;
    }, [customRenderers]);

    // Keep search value ref in sync with state
    useEffect(() => {
        localSearchValueRef.current = localSearchValue;
    }, [localSearchValue]);

    // Sync local search value with props when it changes from outside
    useEffect(() => {
        // If the incoming search value is the same as what we just sent, ignore it
        if (lastSentSearchValue.current !== null && searchValue === lastSentSearchValue.current) {
            lastSentSearchValue.current = null; // Reset for next time
            return;
        }

        setLocalSearchValue(searchValue || '');
    }, [searchValue]);

    // Handle programmatic scroll control via scrollToCell prop
    useEffect(() => {
        if (!scrollToCell || !gridRef.current) return;

        const { col, row, direction, paddingX, paddingY, hAlign, vAlign } = scrollToCell;

        // Build options object if alignment is specified
        const options = (hAlign || vAlign) ? {
            hAlign: hAlign,
            vAlign: vAlign
        } : undefined;

        // Call the scrollTo method on the DataEditor ref
        gridRef.current.scrollTo(
            col,
            row,
            direction || 'both',
            paddingX || 0,
            paddingY || 0,
            options
        );
    }, [scrollToCell]);

    // Handle programmatic redraw via redrawTrigger prop
    useEffect(() => {
        if (redrawTrigger === undefined || redrawTrigger === null) return;

        // Force full canvas redraw by dispatching resize event
        // This is more reliable than updateCells([]) which is a no-op with empty array
        window.dispatchEvent(new Event('resize'));
    }, [redrawTrigger]);

    // Expose gridRef for direct updateCells access (bypasses React for high-perf animations)
    useEffect(() => {
        if (gridRef.current && id) {
            window._glideGridRefs = window._glideGridRefs || {};
            window._glideGridRefs[id] = gridRef.current;
        }
        return () => {
            if (id && window._glideGridRefs) {
                delete window._glideGridRefs[id];
            }
        };
    }, [id, gridRef.current]);

    // Create portal div for Glide Data Grid overlay editor
    useEffect(() => {
        if (typeof document !== 'undefined' && containerRef.current) {
            let portalDiv = document.getElementById('portal');
            if (!portalDiv) {
                portalDiv = document.createElement('div');
                portalDiv.id = 'portal';
                // Position fixed per Glide docs
                portalDiv.style.position = 'fixed';
                portalDiv.style.top = '0';
                portalDiv.style.left = '0';
                portalDiv.style.pointerEvents = 'none';
                portalDiv.style.zIndex = '9999';
                // Add CSS to allow pointer events on children (overlay editors)
                const style = document.createElement('style');
                style.textContent = `
                    #portal > * { pointer-events: auto; }
                `;
                document.head.appendChild(style);

                // Append to body per Glide requirements
                document.body.appendChild(portalDiv);
            }
        }
    }, []);

    // Detect editor close via MutationObserver (for Escape/click-outside/Tab-without-edit)
    useEffect(() => {
        if (!isEditorOpen) return;

        const portal = document.getElementById('portal');
        if (!portal) return;

        const observer = new MutationObserver((mutations) => {
            // Check if editor overlay was removed
            const hasEditorChild = portal.querySelector('[class*="overlay-editor"], [class*="gdg-"]');
            if (!hasEditorChild && portal.children.length === 0) {
                setIsEditorOpen(false);

                // Apply pending Tab wrap if editor closed without triggering handleCellEdited
                // (e.g., user opened editor then pressed Tab without making changes)
                if (pendingWrapRef.current) {
                    const { col: newCol, row: newRow } = pendingWrapRef.current;
                    pendingWrapRef.current = null;

                    setTimeout(() => {
                        const newSelection = {
                            columns: CompactSelection.empty(),
                            rows: CompactSelection.empty(),
                            current: {
                                cell: [newCol, newRow],
                                range: { x: newCol, y: newRow, width: 1, height: 1 },
                                rangeStack: []
                            }
                        };
                        setGridSelection(newSelection);

                        if (setProps) {
                            setProps({
                                selectedCell: { col: newCol, row: newRow },
                                selectedRange: {
                                    startCol: newCol,
                                    startRow: newRow,
                                    endCol: newCol,
                                    endRow: newRow
                                }
                            });
                        }

                        if (gridRef.current) {
                            gridRef.current.scrollTo(newCol, newRow);
                            gridRef.current.focus();
                            gridRef.current.updateCells([{ cell: [newCol, newRow] }]);
                        }
                    }, 50);
                } else {
                    // No pending wrap - just focus the grid so Tab continues to work
                    setTimeout(() => {
                        if (gridRef.current) {
                            gridRef.current.focus();
                        }
                    }, 0);
                }
            }
        });

        observer.observe(portal, { childList: true, subtree: true });
        return () => observer.disconnect();
    }, [isEditorOpen, setProps]);

    // "close-overlay-on-scroll" behavior: close entire editor overlay on scroll
    useEffect(() => {
        if (editorScrollBehavior !== 'close-overlay-on-scroll' || !isEditorOpen) return;

        // Block scrolling at CSS level while editor is open
        const originalOverflow = document.documentElement.style.overflow;
        document.documentElement.style.overflow = 'hidden';

        const closeOverlay = () => {
            const portal = document.getElementById('portal');
            const escapeEvent = new KeyboardEvent('keydown', {
                key: 'Escape',
                code: 'Escape',
                keyCode: 27,
                which: 27,
                bubbles: true,
                cancelable: true
            });

            if (portal) {
                // 1. Dispatch Escape to input (closes react-select dropdown)
                const input = portal.querySelector('input, textarea, [contenteditable]');
                if (input) {
                    input.dispatchEvent(escapeEvent);
                }

                // 2. Dispatch Escape to overlay container
                if (portal.firstElementChild) {
                    portal.firstElementChild.dispatchEvent(escapeEvent);
                }
            }

            // 3. Dispatch Escape to document
            document.dispatchEvent(escapeEvent);

            // 4. Focus the grid to trigger blur on editor
            if (gridRef.current) {
                gridRef.current.focus();
            }

            // 5. Fallback: If overlay still exists after escape attempts, just unlock scroll
            // Don't manually remove DOM nodes - let React/Glide handle cleanup
            // This handles built-in Glide overlays (image, drilldown) that don't respond to escape
            setTimeout(() => {
                const portalAfter = document.getElementById('portal');
                if (portalAfter && portalAfter.children.length > 0) {
                    setIsEditorOpen(false);
                }
            }, 50);
        };

        const handleWheel = (e) => {
            // Allow scrolling within dropdown menus (react-select)
            // The menu is rendered in the portal element
            const portal = document.getElementById('portal');
            if (portal && portal.contains(e.target)) {
                return;
            }

            // Event is outside dropdown - close the overlay
            e.preventDefault();
            e.stopPropagation();
            closeOverlay();
        };

        const handleScroll = (e) => {
            // Ignore scroll events from within the portal (dropdown menu scrolling)
            const portal = document.getElementById('portal');
            if (portal && portal.contains(e.target)) {
                return;
            }
            closeOverlay();
        };

        window.addEventListener('scroll', handleScroll, true);
        document.addEventListener('wheel', handleWheel, { capture: true, passive: false });

        return () => {
            document.documentElement.style.overflow = originalOverflow;
            window.removeEventListener('scroll', handleScroll, true);
            document.removeEventListener('wheel', handleWheel, { capture: true });
        };
    }, [editorScrollBehavior, isEditorOpen]);

    // "lock-scroll" behavior: prevent scrolling while editor is open
    const wheelHandlerRef = useRef(null);
    const scrollHandlerRef = useRef(null);

    useEffect(() => {
        if (editorScrollBehavior !== 'lock-scroll') return;

        if (isEditorOpen) {
            // Save current scroll position
            scrollPositionRef.current = {
                x: window.scrollX,
                y: window.scrollY
            };

            // Create wheel handler to prevent scroll (but allow dropdown menu scrolling)
            wheelHandlerRef.current = (e) => {
                const portal = document.getElementById('portal');
                if (portal && portal.contains(e.target)) {
                    // Allow scrolling within dropdown menus
                    return;
                }
                e.preventDefault();
                e.stopPropagation();
            };

            // Create scroll handler to restore position if scroll somehow happens
            scrollHandlerRef.current = () => {
                window.scrollTo(scrollPositionRef.current.x, scrollPositionRef.current.y);
            };

            // Prevent wheel events
            document.addEventListener('wheel', wheelHandlerRef.current, { passive: false });
            // Also prevent touchmove for mobile
            document.addEventListener('touchmove', wheelHandlerRef.current, { passive: false });
            // Restore scroll position if it changes
            window.addEventListener('scroll', scrollHandlerRef.current);

            // Set overflow hidden on html element (less layout shift than body fixed)
            document.documentElement.style.overflow = 'hidden';
        }

        return () => {
            // Cleanup
            document.documentElement.style.overflow = '';
            if (wheelHandlerRef.current) {
                document.removeEventListener('wheel', wheelHandlerRef.current);
                document.removeEventListener('touchmove', wheelHandlerRef.current);
                wheelHandlerRef.current = null;
            }
            if (scrollHandlerRef.current) {
                window.removeEventListener('scroll', scrollHandlerRef.current);
                scrollHandlerRef.current = null;
            }
        };
    }, [editorScrollBehavior, isEditorOpen]);

    // "close-overlay-on-scroll" behavior for context menu: close menu on scroll
    useEffect(() => {
        if (contextMenuScrollBehavior !== 'close-overlay-on-scroll' || !contextMenuState.isOpen) return;

        const handleWheel = (e) => {
            // Allow scrolling within the context menu itself (when maxHeight creates scrollable content)
            const contextMenu = e.target.closest('[data-context-menu="true"]');
            if (contextMenu) {
                return;
            }

            // Event is outside context menu - close it and prevent this wheel event
            e.preventDefault();
            e.stopPropagation();
            handleContextMenuClose();
        };

        const handleScroll = (e) => {
            // Ignore scroll events from within the context menu
            const contextMenu = e.target.closest('[data-context-menu="true"]');
            if (contextMenu) {
                return;
            }
            handleContextMenuClose();
        };

        window.addEventListener('scroll', handleScroll, true);
        document.addEventListener('wheel', handleWheel, { capture: true, passive: false });

        return () => {
            window.removeEventListener('scroll', handleScroll, true);
            document.removeEventListener('wheel', handleWheel, { capture: true });
        };
    }, [contextMenuScrollBehavior, contextMenuState.isOpen, handleContextMenuClose]);

    // "lock-scroll" behavior for context menu: prevent all external scrolling
    useEffect(() => {
        if (contextMenuScrollBehavior !== 'lock-scroll') return;

        if (contextMenuState.isOpen) {
            // Save current scroll position
            contextMenuScrollPositionRef.current = {
                x: window.scrollX,
                y: window.scrollY
            };

            // Create wheel handler to prevent scroll (but allow context menu scrolling)
            contextMenuWheelHandlerRef.current = (e) => {
                const contextMenu = e.target.closest('[data-context-menu="true"]');
                if (contextMenu) {
                    // Allow scrolling within context menu
                    return;
                }
                e.preventDefault();
                e.stopPropagation();
            };

            // Create scroll handler to restore position if scroll somehow happens
            contextMenuScrollHandlerRef.current = () => {
                window.scrollTo(contextMenuScrollPositionRef.current.x, contextMenuScrollPositionRef.current.y);
            };

            // Prevent wheel events
            document.addEventListener('wheel', contextMenuWheelHandlerRef.current, { passive: false });
            // Also prevent touchmove for mobile
            document.addEventListener('touchmove', contextMenuWheelHandlerRef.current, { passive: false });
            // Restore scroll position if it changes
            window.addEventListener('scroll', contextMenuScrollHandlerRef.current);

            // Set overflow hidden on html element
            document.documentElement.style.overflow = 'hidden';
        }

        return () => {
            // Cleanup
            document.documentElement.style.overflow = '';
            if (contextMenuWheelHandlerRef.current) {
                document.removeEventListener('wheel', contextMenuWheelHandlerRef.current);
                document.removeEventListener('touchmove', contextMenuWheelHandlerRef.current);
                contextMenuWheelHandlerRef.current = null;
            }
            if (contextMenuScrollHandlerRef.current) {
                window.removeEventListener('scroll', contextMenuScrollHandlerRef.current);
                contextMenuScrollHandlerRef.current = null;
            }
        };
    }, [contextMenuScrollBehavior, contextMenuState.isOpen]);

    // Transform columns to Glide format (including sort indicators)
    const glideColumns = useMemo(() => {
        if (!localColumns || !Array.isArray(localColumns)) {
            return [];
        }
        return localColumns.map((col, colIndex) => {
            // Check if this column is sorted
            const sortIndex = localSortColumns.findIndex(sc => sc.columnIndex === colIndex);
            const sortInfo = sortIndex >= 0 ? localSortColumns[sortIndex] : null;

            // Build title with sort indicator for multi-sort
            let title = col.title;
            if (sortInfo && localSortColumns.length > 1) {
                // Show priority number for multi-column sort
                const arrow = sortInfo.direction === 'asc' ? '↑' : '↓';
                title = `${col.title} ${arrow}${sortIndex + 1}`;
            } else if (sortInfo) {
                // Single column sort - just show arrow
                const arrow = sortInfo.direction === 'asc' ? '↑' : '↓';
                title = `${col.title} ${arrow}`;
            }

            // Check if this column has an active filter
            const hasActiveFilter = localFilters && localFilters[colIndex] !== undefined;

            // Determine if column should show menu (hasMenu or filterable)
            const showMenu = col.hasMenu || col.filterable || false;

            // Build themeOverride for active filter styling
            let columnThemeOverride = col.themeOverride;
            if (hasActiveFilter) {
                const filterActiveColor = headerMenuConfig?.filterActiveColor || theme?.accentColor || '#2563eb';
                columnThemeOverride = {
                    ...col.themeOverride,
                    bgIconHeader: filterActiveColor,
                    fgIconHeader: filterActiveColor,
                    textHeader: filterActiveColor
                };
            }

            // Map menuIcon value: 'chevron' means use default (undefined), otherwise pass through
            const menuIconValue = headerMenuConfig?.menuIcon === 'chevron' ? undefined : headerMenuConfig?.menuIcon;

            return {
                title: title,
                id: col.id || col.title,
                width: col.width,
                icon: col.icon,
                overlayIcon: col.overlayIcon,
                hasMenu: showMenu,
                menuIcon: showMenu ? menuIconValue : undefined,
                group: col.group,
                themeOverride: columnThemeOverride
            };
        });
    }, [localColumns, localSortColumns, localFilters, headerMenuConfig, theme]);

    // Calculate number of rows (use filtered count if filtering is active)
    const numRows = useMemo(() => {
        if (rows) return rows;
        if (displayIndices) return displayIndices.length;
        return localData ? localData.length : 0;
    }, [rows, displayIndices, localData]);

    // getCellContent callback - transforms data to Glide cell format
    const getCellContent = useCallback((cell) => {
        const [col, row] = cell;

        // Translate row index if sorting is active
        const actualRow = sortedIndices ? sortedIndices[row] : row;

        // Handle out of bounds
        if (!localData || actualRow >= localData.length || actualRow < 0) {
            return {
                kind: GridCellKind.Text,
                data: '',
                allowOverlay: false,
                displayData: ''
            };
        }

        const rowData = localData[actualRow];
        if (!rowData) {
            return {
                kind: GridCellKind.Text,
                data: '',
                allowOverlay: false,
                displayData: ''
            };
        }

        // Get column id to access dict key
        const columnDef = localColumns && localColumns[col];
        const columnId = columnDef?.id || columnDef?.title;
        const cellValue = rowData[columnId];

        // Get the cell object
        let cellResult;
        if (cellValue && typeof cellValue === 'object' && cellValue.kind) {
            cellResult = transformCellObject(cellValue);
        } else {
            cellResult = autoDetectCellType(cellValue);
        }

        // Apply valueFormatter if defined for this column
        if (columnDef && isFunctionRef(columnDef.valueFormatter)) {
            try {
                const formattedValue = executeFunction(
                    columnDef.valueFormatter.function,
                    { value: cellResult.data, cell: cellResult, row, col }
                );
                if (formattedValue !== undefined) {
                    cellResult = {
                        ...cellResult,
                        displayData: String(formattedValue)
                    };
                }
            } catch (e) {
                console.warn('[GlideGrid] valueFormatter error:', e);
            }
        }

        // Apply lastUpdated timestamp if this cell was recently edited
        const cellKey = `${actualRow},${col}`;
        if (lastUpdatedCells[cellKey]) {
            cellResult = {
                ...cellResult,
                lastUpdated: lastUpdatedCells[cellKey]
            };
        }

        return cellResult;
    }, [localData, localColumns, sortedIndices, lastUpdatedCells]);

    // Handle cell clicks
    const handleCellClicked = useCallback((cell, event) => {
        const [col, row] = cell;

        // Fire the cellClicked Dash event
        if (setProps) {
            setProps({
                cellClicked: {
                    col: col,
                    row: row,
                    timestamp: Date.now()
                },
                nClicks: (nClicks || 0) + 1
            });
        }

        // Handle row selection on cell click
        if (rowSelectOnCellClick && (rowSelect === 'single' || rowSelect === 'multi')) {
            // Skip row marker column clicks (col < 0)
            if (col < 0) return;

            // Check if row is unselectable
            if (unselectableRows && unselectableRows.includes(row)) return;

            const isCtrlOrCmd = event.ctrlKey || event.metaKey;
            const isShift = event.shiftKey;

            let newRows;
            const currentRows = currentRowSelectionRef.current || CompactSelection.empty();

            if (rowSelect === 'single') {
                // Single mode: select only the clicked row
                newRows = CompactSelection.empty().add(row);
                lastSelectedRowRef.current = row;
            } else {
                // Multi selection mode
                if (isShift && lastSelectedRowRef.current !== null) {
                    // Shift+click: range selection from last selected row
                    // Always preserve existing selection (AG Grid style multi-range support)
                    const start = Math.min(lastSelectedRowRef.current, row);
                    const end = Math.max(lastSelectedRowRef.current, row);
                    newRows = currentRows;
                    for (let i = start; i <= end; i++) {
                        if (!unselectableRows || !unselectableRows.includes(i)) {
                            newRows = newRows.add(i);
                        }
                    }
                } else if (rowSelectionMode === 'multi') {
                    // 'multi' mode: always toggle (Ctrl/Cmd not required)
                    if (currentRows.hasIndex(row)) {
                        newRows = currentRows.remove(row);
                    } else {
                        newRows = currentRows.add(row);
                        lastSelectedRowRef.current = row;
                    }
                } else {
                    // 'auto' mode: respect modifier keys
                    if (isCtrlOrCmd) {
                        // Toggle row
                        if (currentRows.hasIndex(row)) {
                            newRows = currentRows.remove(row);
                        } else {
                            newRows = currentRows.add(row);
                            lastSelectedRowRef.current = row;
                        }
                    } else {
                        // Select only this row
                        newRows = CompactSelection.empty().add(row);
                        lastSelectedRowRef.current = row;
                    }
                }
            }

            // Update the row selection ref
            currentRowSelectionRef.current = newRows;

            // Update grid selection with new rows
            setGridSelection(prev => ({
                ...prev,
                rows: newRows,
                columns: rowSelectionBlending === 'mixed' ? prev.columns : CompactSelection.empty()
            }));

            // Update Dash props
            if (setProps) {
                setProps({
                    selectedRows: [...newRows]
                });
            }
        }
    }, [setProps, nClicks, rowSelectOnCellClick, rowSelect, rowSelectionMode, rowSelectionBlending, unselectableRows]);

    // Handle cell edits
    const handleCellEdited = useCallback((cell, newValue) => {
        setIsEditorOpen(false);

        // Check if we have a pending wrap from Tab at row boundary
        if (pendingWrapRef.current) {
            const { col: newCol, row: newRow } = pendingWrapRef.current;
            pendingWrapRef.current = null;

            // Apply the wrap after a short delay
            setTimeout(() => {
                const newSelection = {
                    columns: CompactSelection.empty(),
                    rows: CompactSelection.empty(),
                    current: {
                        cell: [newCol, newRow],
                        range: { x: newCol, y: newRow, width: 1, height: 1 },
                        rangeStack: []
                    }
                };
                setGridSelection(newSelection);

                if (setProps) {
                    setProps({
                        selectedCell: { col: newCol, row: newRow },
                        selectedRange: {
                            startCol: newCol,
                            startRow: newRow,
                            endCol: newCol,
                            endRow: newRow
                        }
                    });
                }

                if (gridRef.current) {
                    gridRef.current.scrollTo(newCol, newRow);
                    gridRef.current.focus();
                    gridRef.current.updateCells([{ cell: [newCol, newRow] }]);
                }
            }, 50);
        } else {
            // Focus the grid after editor closes so Tab continues to work
            if (gridRef.current) {
                setTimeout(() => {
                    if (gridRef.current) {
                        gridRef.current.focus();
                    }
                }, 0);
            }
        }

        if (!setProps || readonly) return;

        const [col, row] = cell;

        // Translate row index if sorting is active (row is display index, actualRow is data index)
        const actualRow = sortedIndices ? sortedIndices[row] : row;

        // Use ref to get the most current data (avoids stale closures)
        const currentData = localDataRef.current;
        const currentColumns = localColumnsRef.current;
        if (!currentData || !currentColumns) return;

        // Get column id to access dict key
        const columnDef = currentColumns[col];
        const columnId = columnDef?.id || columnDef?.title;

        // Create a deep copy of the data (array of objects)
        const newData = currentData.map(r => ({...r}));

        // Get the old value to determine format (use actualRow for data access)
        const oldValue = newData[actualRow][columnId];

        // Preserve format (object vs simple value)
        let newCellValue;
        if (oldValue && typeof oldValue === 'object' && oldValue.kind) {
            // Handle custom cells (dropdown, multiselect, tags, etc.)
            if (newValue.kind === GridCellKind.Custom) {
                // For custom cells, newValue.data contains {kind: "...", value/values, allowedValues, ...}
                // We need to preserve the nested format for dropdown/multi-select cells
                const nestedDataCells = ['dropdown-cell', 'multi-select-cell'];
                if (nestedDataCells.includes(newValue.data.kind) && oldValue.data) {
                    // Reconstruct nested format: {kind, data: {...}, copyData}
                    const { kind, ...innerData } = newValue.data;

                    // Derive copyData from the NEW value (editors don't update copyData)
                    let derivedCopyData = '';
                    if (kind === 'dropdown-cell') {
                        derivedCopyData = innerData.value || '';
                    } else if (kind === 'multi-select-cell') {
                        derivedCopyData = Array.isArray(innerData.values)
                            ? innerData.values.join(', ')
                            : '';
                    }

                    newCellValue = {
                        kind: kind,
                        data: innerData,
                        copyData: derivedCopyData,
                    };
                } else {
                    // Other custom cells use flat format
                    newCellValue = newValue.data;
                }
            } else {
                // Update the data property while preserving the object structure
                // Always derive displayData from the new data - Glide passes stale displayData
                newCellValue = {
                    ...oldValue,
                    data: newValue.data,
                    displayData: String(newValue.data ?? '')
                };
            }
        } else {
            // Simple value - extract the data from the GridCell
            // Convert undefined to empty string for JSON serialization (undefined is stripped)
            newCellValue = newValue.data ?? '';
        }

        newData[actualRow] = { ...newData[actualRow], [columnId]: newCellValue };

        // Track edit for undo/redo
        addEditToBatch({
            col: col,
            row: actualRow,
            columnId: columnId,
            oldValue: oldValue,
            newValue: newCellValue
        });

        // Update local state immediately (optimistic update)
        setLocalData(newData);

        // CRITICAL: Update the ref immediately so next edit sees the updated data
        localDataRef.current = newData;

        // Store this data so we can ignore it when it comes back from Dash
        lastSentData.current = newData;

        // Set lastUpdated timestamp for flash effect
        if (shouldFlash('edit')) {
            const cellKey = `${actualRow},${col}`;
            setLastUpdatedCells(prev => ({ ...prev, [cellKey]: performance.now() }));
        }

        // Sync with Dash (report actualRow so it matches data array indices)
        setProps({
            data: newData,
            cellEdited: {
                col: col,
                row: actualRow,
                value: (newValue.kind === GridCellKind.Custom ? newValue.data : newValue.data) ?? '',
                timestamp: Date.now()
            }
        });

        return true;
    }, [setProps, readonly, sortedIndices, addEditToBatch]);

    // Coerce a pasted string value to match the target cell's type
    // Used by both handlePaste and context menu paste actions
    const coercePastedValue = useCallback((pastedValue, oldValue) => {
        // Preserve format (object vs simple value) and convert pasted string to appropriate type
        if (oldValue && typeof oldValue === 'object' && oldValue.kind) {
            // Cell object - check for custom cell renderer with onPaste method
            const renderer = customRenderersRef.current?.find(r =>
                r.isMatch?.({ data: oldValue })
            );
            if (renderer?.onPaste) {
                // Call custom renderer's onPaste to transform the pasted value
                const transformed = renderer.onPaste(pastedValue, oldValue);
                // If onPaste returns undefined, keep the old value (reject paste)
                return transformed !== undefined ? transformed : oldValue;
            } else if (oldValue.kind === 'number') {
                const num = parseFloat(pastedValue);
                // Reject paste if not a valid number - keep old value
                return isNaN(num) ? oldValue : { ...oldValue, data: num };
            } else if (oldValue.kind === 'boolean') {
                const lowerVal = pastedValue.toLowerCase().trim();
                if (lowerVal === 'true') {
                    return { ...oldValue, data: true };
                } else if (lowerVal === 'false') {
                    return { ...oldValue, data: false };
                } else {
                    // Reject paste - keep old value
                    return { ...oldValue };
                }
            } else if (oldValue.kind === 'bubble') {
                // Bubble data is an array of strings - parse comma-separated values
                const bubbles = pastedValue
                    .split(',')
                    .map(s => s.trim())
                    .filter(s => s.length > 0);
                return { ...oldValue, data: bubbles };
            } else if (oldValue.kind === 'drilldown') {
                // Drilldown data is an array of objects with text property
                const items = pastedValue
                    .split(',')
                    .map(s => s.trim())
                    .filter(s => s.length > 0)
                    .map(text => ({ text }));
                return { ...oldValue, data: items };
            } else {
                return { ...oldValue, data: pastedValue };
            }
        } else {
            // Simple value - try to preserve type
            if (typeof oldValue === 'number') {
                const num = parseFloat(pastedValue);
                // Reject paste if not a valid number - keep old value
                return isNaN(num) ? oldValue : num;
            } else if (typeof oldValue === 'boolean') {
                const lowerVal = pastedValue.toLowerCase().trim();
                if (lowerVal === 'true') {
                    return true;
                } else if (lowerVal === 'false') {
                    return false;
                } else {
                    // Reject paste - keep old value
                    return oldValue;
                }
            } else {
                return pastedValue;
            }
        }
    }, []);

    // Get the cleared/empty value for a cell using the renderer's deletedValue
    // Takes col, row to get the properly transformed cell via getCellContent
    const getClearedValue = useCallback((col, row, oldValue) => {
        // Get the Glide-format cell via getCellContent
        const cell = getCellContent([col, row]);
        if (!cell) return oldValue;

        // For custom cells, find the renderer and use its deletedValue
        if (cell.kind === GridCellKind.Custom && cell.data?.kind) {
            const renderer = customRenderersRef.current?.find(r =>
                r.isMatch?.(cell)
            );
            const deletedValue = renderer?.provideEditor?.()?.deletedValue;
            if (deletedValue) {
                const clearedCell = deletedValue(cell);
                // Convert back to stored format
                const nestedDataCells = ['dropdown-cell', 'multi-select-cell'];
                if (nestedDataCells.includes(clearedCell.data.kind)) {
                    // Reconstruct nested format: {kind, data: {...}, copyData}
                    const { kind, ...innerData } = clearedCell.data;
                    return {
                        kind: kind,
                        data: innerData,
                        copyData: clearedCell.copyData || ''
                    };
                } else {
                    // Other custom cells use flat format
                    return clearedCell.data;
                }
            }
            // Fallback - return unchanged
            return oldValue;
        }

        // For built-in Glide cell types
        switch (cell.kind) {
            case GridCellKind.Number:
                // Return empty string for numbers - null would make cell non-editable
                // Empty string becomes an editable text cell; typing a number restores it
                if (oldValue && typeof oldValue === 'object') {
                    return { ...oldValue, data: '', displayData: '' };
                }
                return '';
            case GridCellKind.Boolean:
                if (oldValue && typeof oldValue === 'object') {
                    return { ...oldValue, data: false };
                }
                return false;
            case GridCellKind.Text:
            case GridCellKind.Uri:
            case GridCellKind.Markdown:
                if (oldValue && typeof oldValue === 'object') {
                    return { ...oldValue, data: '', displayData: '' };
                }
                return '';
            case GridCellKind.Bubble:
            case GridCellKind.Drilldown:
                if (oldValue && typeof oldValue === 'object') {
                    return { ...oldValue, data: [] };
                }
                return [];
            case GridCellKind.Image:
                // Clear image to empty array, preserving object structure
                if (oldValue && typeof oldValue === 'object') {
                    return { ...oldValue, data: [] };
                }
                return { kind: 'image', data: [] };
            default:
                return oldValue;
        }
    }, [getCellContent]);

    // Extract a copyable string value from a cell by using getCellContent
    // This ensures context menu copy uses the same logic as native Cmd+C
    const getCellCopyValue = useCallback((col, row) => {
        const cell = getCellContent([col, row]);
        if (!cell) return '';
        // For custom cells, copyData is populated by deriveCopyData in getCellContent
        if (cell.copyData !== undefined) {
            return String(cell.copyData);
        }
        // For built-in cells, extract from data/displayData
        if (cell.kind === GridCellKind.Number) {
            return cell.displayData ?? String(cell.data ?? '');
        } else if (cell.kind === GridCellKind.Boolean) {
            return String(cell.data ?? false);
        } else if (cell.kind === GridCellKind.Text || cell.kind === GridCellKind.Uri || cell.kind === GridCellKind.Markdown) {
            return cell.data ?? cell.displayData ?? '';
        } else if (cell.kind === GridCellKind.Bubble) {
            return Array.isArray(cell.data) ? cell.data.join(', ') : '';
        } else if (cell.kind === GridCellKind.Drilldown) {
            return Array.isArray(cell.data) ? cell.data.map(d => d.text || '').join(', ') : '';
        } else if (cell.kind === GridCellKind.Image) {
            return Array.isArray(cell.data) ? cell.data[0] || '' : '';
        }
        return '';
    }, [getCellContent]);

    // Handle paste events (for multi-cell paste like Excel)
    const handlePaste = useCallback((target, values) => {
        if (!setProps || readonly) {
            return false;
        }

        const [targetCol, targetRow] = target;

        // Use ref to get the most current data (avoids stale closures)
        const currentData = localDataRef.current;
        const currentColumns = localColumnsRef.current;
        if (!currentData || !currentColumns) {
            return false;
        }

        // Create a deep copy of the data (array of objects)
        const newData = currentData.map(r => ({...r}));

        // Build list of visible target rows if skipping hidden rows
        let targetRows = [];
        if (skipOnPaste && hiddenRowsSet.size > 0) {
            // Collect visible rows starting from targetRow, up to values.length rows needed
            let row = targetRow;
            while (targetRows.length < values.length && row < currentData.length) {
                if (!hiddenRowsSet.has(row)) {
                    targetRows.push(row);
                }
                row++;
            }
        } else {
            // No hidden row skipping - use sequential rows
            for (let i = 0; i < values.length; i++) {
                const row = targetRow + i;
                if (row < currentData.length) {
                    targetRows.push(row);
                }
            }
        }

        // Apply pasted data to visible target rows only
        for (let i = 0; i < targetRows.length; i++) {
            const displayRow = targetRows[i];
            if (displayRow >= newData.length) break;

            // Translate display row to actual data row if sorting is active
            const actualPasteRow = sortedIndices ? sortedIndices[displayRow] : displayRow;
            if (actualPasteRow >= newData.length) break;

            for (let j = 0; j < values[i].length; j++) {
                const pasteCol = targetCol + j;
                if (pasteCol >= currentColumns.length) break;

                // Get column id to access dict key
                const columnDef = currentColumns[pasteCol];
                const columnId = columnDef?.id || columnDef?.title;

                const pastedValue = values[i][j];
                const oldValue = newData[actualPasteRow][columnId];
                const newCellValue = coercePastedValue(pastedValue, oldValue);

                newData[actualPasteRow] = { ...newData[actualPasteRow], [columnId]: newCellValue };

                // Track edit for undo/redo
                addEditToBatch({
                    col: pasteCol,
                    row: actualPasteRow,
                    columnId: columnId,
                    oldValue: oldValue,
                    newValue: newCellValue
                });
            }
        }

        // Set lastUpdated timestamps for flash effect on all pasted cells
        if (shouldFlash('paste')) {
            const now = performance.now();
            const updatedCells = {};
            for (let i = 0; i < targetRows.length; i++) {
                const displayRow = targetRows[i];
                if (displayRow >= newData.length) break;
                const actualPasteRow = sortedIndices ? sortedIndices[displayRow] : displayRow;
                if (actualPasteRow >= newData.length) break;
                for (let j = 0; j < values[i].length; j++) {
                    const pasteCol = targetCol + j;
                    if (pasteCol >= currentColumns.length) break;
                    updatedCells[`${actualPasteRow},${pasteCol}`] = now;
                }
            }
            setLastUpdatedCells(prev => ({ ...prev, ...updatedCells }));
        }

        // Update local state immediately (optimistic update)
        setLocalData(newData);

        // CRITICAL: Update the ref immediately so next paste sees the updated data
        localDataRef.current = newData;

        // Store this data so we can ignore it when it comes back from Dash
        lastSentData.current = newData;

        // Translate targetRow for the event
        const actualTargetRow = sortedIndices ? sortedIndices[targetRow] : targetRow;

        // Sync with Dash
        setProps({
            data: newData,
            cellEdited: {
                col: targetCol,
                row: actualTargetRow,
                value: `Pasted ${targetRows.length}x${values[0]?.length || 0} range`,
                timestamp: Date.now()
            }
        });

        // Return false to prevent grid from also trying to paste (we handled it)
        return false;
    }, [setProps, readonly, sortedIndices, addEditToBatch, skipOnPaste, hiddenRowsSet]);

    // Handle selection changes
    const handleSelectionChanged = useCallback((selection) => {
        // If rangeSelect is 'none', strip cell/range selection but preserve row/column selection
        if (rangeSelect === 'none') {
            let rowsToUse;

            if (rowSelectOnCellClick && (rowSelect === 'single' || rowSelect === 'multi')) {
                if (!selection.current?.cell) {
                    // Row marker action or column header click (no cell)
                    const glideRows = selection.rows || CompactSelection.empty();
                    const isShift = modifierKeysRef.current.shiftKey;
                    const ourRows = currentRowSelectionRef.current || CompactSelection.empty();

                    if (isShift && ourRows.length > 0 && rowSelect === 'multi') {
                        // Shift+click on row marker: merge glide's range with our previous selection
                        let mergedRows = ourRows;
                        for (const row of glideRows) {
                            mergedRows = mergedRows.add(row);
                        }
                        rowsToUse = mergedRows;
                        currentRowSelectionRef.current = mergedRows;
                        // Update lastSelectedRowRef to the last row in the new range
                        if (glideRows.length > 0) {
                            let lastRow = 0;
                            for (const row of glideRows) {
                                lastRow = row;
                            }
                            lastSelectedRowRef.current = lastRow;
                        }
                    } else {
                        // Normal click or cmd+click: sync with glide's selection
                        rowsToUse = glideRows;
                        currentRowSelectionRef.current = glideRows;
                        if (glideRows.length > 0) {
                            let lastRow = 0;
                            for (const row of glideRows) {
                                lastRow = row;
                            }
                            lastSelectedRowRef.current = lastRow;
                        } else {
                            lastSelectedRowRef.current = null;
                        }
                    }
                } else {
                    // Cell click - check if blending cleared our rows
                    const glideRows = selection.rows || CompactSelection.empty();
                    const ourRows = currentRowSelectionRef.current || CompactSelection.empty();
                    const hasColumnSelection = (selection.columns?.length || 0) > 0;

                    // Respect blending: if glide cleared rows due to column selection with exclusive blending
                    const blendingClearedRows = ourRows.length > 0 && glideRows.length === 0 && hasColumnSelection;

                    if (blendingClearedRows) {
                        // Blending mode cleared our rows - sync with glide
                        rowsToUse = glideRows;
                        currentRowSelectionRef.current = glideRows;
                    } else {
                        // Normal cell click - preserve our row selection (updated in handleCellClicked)
                        rowsToUse = ourRows;
                    }
                }
            } else {
                // Not using rowSelectOnCellClick - use glide's selection
                rowsToUse = selection.rows || CompactSelection.empty();
            }

            const strippedSelection = {
                columns: selection.columns || CompactSelection.empty(),
                rows: rowsToUse,
                current: undefined  // No cell or range selection
            };
            setGridSelection(strippedSelection);

            // Still update row/column selections if setProps available
            if (setProps) {
                const updates = {};
                if (strippedSelection.rows && strippedSelection.rows.length > 0) {
                    const rowsArray = [];
                    for (const row of strippedSelection.rows) {
                        rowsArray.push(row);
                    }
                    updates.selectedRows = rowsArray;
                } else {
                    // Explicitly set empty array when no rows selected
                    updates.selectedRows = [];
                }
                if (strippedSelection.columns && strippedSelection.columns.length > 0) {
                    const colsArray = [];
                    for (const col of strippedSelection.columns) {
                        colsArray.push(col);
                    }
                    updates.selectedColumns = colsArray;
                }
                if (Object.keys(updates).length > 0) {
                    setProps(updates);
                }
            }
            return;
        }

        let adjustedSelection = selection;

        // Apply selectionColumnMin restriction if set
        if (selectionColumnMin != null && selectionColumnMin > 0 && selection.current) {
            const cell = selection.current.cell;
            const range = selection.current.range;

            // Check if selection touches restricted columns
            if (cell && cell[0] < selectionColumnMin) {
                // Cell is in restricted area - adjust to minimum column
                const newCell = [selectionColumnMin, cell[1]];
                const newRange = range ? {
                    ...range,
                    x: Math.max(selectionColumnMin, range.x),
                    width: Math.max(1, range.x + range.width - selectionColumnMin)
                } : { x: selectionColumnMin, y: cell[1], width: 1, height: 1 };

                // Ensure width is valid after adjustment
                if (newRange.width <= 0) {
                    newRange.x = selectionColumnMin;
                    newRange.width = 1;
                }

                adjustedSelection = {
                    ...selection,
                    current: {
                        ...selection.current,
                        cell: newCell,
                        range: newRange
                    }
                };
            } else if (range && range.x < selectionColumnMin) {
                // Range starts in restricted area - adjust range start
                const newX = selectionColumnMin;
                const newWidth = Math.max(1, range.x + range.width - selectionColumnMin);

                adjustedSelection = {
                    ...selection,
                    current: {
                        ...selection.current,
                        range: {
                            ...range,
                            x: newX,
                            width: newWidth
                        }
                    }
                };
            }

            // Filter out restricted columns from column selection
            if (selection.columns && selection.columns.length > 0) {
                let newColumns = CompactSelection.empty();
                for (const col of selection.columns) {
                    if (col >= selectionColumnMin) {
                        newColumns = newColumns.add(col);
                    }
                }
                adjustedSelection = {
                    ...adjustedSelection,
                    columns: newColumns
                };
            }
        }

        // Apply unselectableColumns restriction - ignore clicks on these cells and clip ranges
        if (unselectableColumns && unselectableColumns.length > 0) {
            if (adjustedSelection.current) {
                const cell = adjustedSelection.current.cell;
                if (cell && unselectableColumns.includes(cell[0])) {
                    // Ignore the selection change - keep previous selection
                    return;
                }

                // Clip range to exclude unselectable columns
                const range = adjustedSelection.current.range;
                if (range) {
                    let newX = range.x;
                    let newWidth = range.width;

                    // Clip range from left if it starts in unselectable column
                    while (newWidth > 0 && unselectableColumns.includes(newX)) {
                        newX++;
                        newWidth--;
                    }

                    // Clip range from right if it extends into unselectable column
                    while (newWidth > 0 && unselectableColumns.includes(newX + newWidth - 1)) {
                        newWidth--;
                    }

                    if (newWidth > 0 && (newX !== range.x || newWidth !== range.width)) {
                        adjustedSelection = {
                            ...adjustedSelection,
                            current: {
                                ...adjustedSelection.current,
                                range: { ...range, x: newX, width: newWidth }
                            }
                        };
                    }
                }
            }

            // Filter column selections
            if (adjustedSelection.columns && adjustedSelection.columns.length > 0) {
                let newColumns = CompactSelection.empty();
                for (const col of adjustedSelection.columns) {
                    if (!unselectableColumns.includes(col)) {
                        newColumns = newColumns.add(col);
                    }
                }
                adjustedSelection = {
                    ...adjustedSelection,
                    columns: newColumns
                };
            }
        }

        // Apply unselectableRows restriction - ignore clicks on these cells and clip ranges
        if (unselectableRows && unselectableRows.length > 0) {
            if (adjustedSelection.current) {
                const cell = adjustedSelection.current.cell;
                if (cell && unselectableRows.includes(cell[1])) {
                    // Ignore the selection change - keep previous selection
                    return;
                }

                // Clip range to exclude unselectable rows
                const range = adjustedSelection.current.range;
                if (range) {
                    let newY = range.y;
                    let newHeight = range.height;

                    // Clip range from top if it starts in unselectable row
                    while (newHeight > 0 && unselectableRows.includes(newY)) {
                        newY++;
                        newHeight--;
                    }

                    // Clip range from bottom if it extends into unselectable row
                    while (newHeight > 0 && unselectableRows.includes(newY + newHeight - 1)) {
                        newHeight--;
                    }

                    if (newHeight > 0 && (newY !== range.y || newHeight !== range.height)) {
                        adjustedSelection = {
                            ...adjustedSelection,
                            current: {
                                ...adjustedSelection.current,
                                range: { ...adjustedSelection.current.range, y: newY, height: newHeight }
                            }
                        };
                    }
                }
            }

            // Filter row selections
            if (adjustedSelection.rows && adjustedSelection.rows.length > 0) {
                let newRows = CompactSelection.empty();
                for (const row of adjustedSelection.rows) {
                    if (!unselectableRows.includes(row)) {
                        newRows = newRows.add(row);
                    }
                }
                adjustedSelection = {
                    ...adjustedSelection,
                    rows: newRows
                };
            }
        }

        // Handle rowSelectOnCellClick row selection syncing
        if (rowSelectOnCellClick && (rowSelect === 'single' || rowSelect === 'multi')) {
            if (!selection.current?.cell) {
                // Row marker action or column header click (no cell selected)
                const glideRows = adjustedSelection.rows || CompactSelection.empty();
                const isShift = modifierKeysRef.current.shiftKey;
                const ourRows = currentRowSelectionRef.current || CompactSelection.empty();

                if (isShift && ourRows.length > 0 && rowSelect === 'multi') {
                    // Shift+click on row marker: merge glide's range with our previous selection
                    // This enables AG Grid-style multi-range selection
                    let mergedRows = ourRows;
                    for (const row of glideRows) {
                        mergedRows = mergedRows.add(row);
                    }
                    currentRowSelectionRef.current = mergedRows;
                    adjustedSelection = {
                        ...adjustedSelection,
                        rows: mergedRows
                    };
                    // Update lastSelectedRowRef to the last row in the new range
                    if (glideRows.length > 0) {
                        let lastRow = 0;
                        for (const row of glideRows) {
                            lastRow = row;
                        }
                        lastSelectedRowRef.current = lastRow;
                    }
                } else {
                    // Normal click or cmd+click: sync with glide's selection
                    currentRowSelectionRef.current = glideRows;
                    // Update lastSelectedRowRef to the last selected row
                    if (glideRows.length > 0) {
                        let lastRow = 0;
                        for (const row of glideRows) {
                            lastRow = row;
                        }
                        lastSelectedRowRef.current = lastRow;
                    } else {
                        lastSelectedRowRef.current = null;
                    }
                }
            } else {
                // Cell is selected - need to determine if we should preserve our row selection
                // or respect glide's blending logic

                // Check if blending has cleared our rows:
                // - If rowSelectionBlending='exclusive' and columns are selected, rows get cleared
                // - If rangeSelectionBlending='exclusive' and a multi-column range is selected, rows get cleared
                // - If glide's selection has no rows but we have rows, blending cleared them
                // Note: For range selection, we only consider width > 1 (multi-column) as a "real" range.
                // Shift+click for row selection creates height > 1 but width = 1, which should preserve rows.
                const glideRows = adjustedSelection.rows || CompactSelection.empty();
                const ourRows = currentRowSelectionRef.current || CompactSelection.empty();
                const hasColumnSelection = (adjustedSelection.columns?.length || 0) > 0;
                const hasMultiColumnRange = adjustedSelection.current?.range &&
                    adjustedSelection.current.range.width > 1;

                // Respect blending: if glide cleared rows due to column or multi-column range selection
                const blendingClearedRows = ourRows.length > 0 && glideRows.length === 0 &&
                    (hasColumnSelection || hasMultiColumnRange);

                if (blendingClearedRows) {
                    // Blending mode cleared our rows - sync with glide
                    currentRowSelectionRef.current = glideRows;
                } else {
                    // Normal cell click - preserve our row selection (handled in handleCellClicked)
                    adjustedSelection = {
                        ...adjustedSelection,
                        rows: ourRows
                    };
                }
            }
        } else {
            // Not using rowSelectOnCellClick - sync our ref with glide's selection
            if (adjustedSelection.rows) {
                currentRowSelectionRef.current = adjustedSelection.rows;
            }
        }

        // Handle column multi-range selection (shift+click on column headers)
        if (columnSelect === 'multi' && !selection.current?.cell) {
            const glideColumns = adjustedSelection.columns || CompactSelection.empty();
            const isShift = modifierKeysRef.current.shiftKey;
            const ourColumns = currentColumnSelectionRef.current || CompactSelection.empty();

            if (isShift && ourColumns.length > 0 && glideColumns.length > 0) {
                // Shift+click on column header: merge glide's range with our previous selection
                let mergedColumns = ourColumns;
                for (const col of glideColumns) {
                    mergedColumns = mergedColumns.add(col);
                }
                currentColumnSelectionRef.current = mergedColumns;
                adjustedSelection = {
                    ...adjustedSelection,
                    columns: mergedColumns
                };
                // Update lastSelectedColumnRef to the last column in the new range
                let lastCol = 0;
                for (const col of glideColumns) {
                    lastCol = col;
                }
                lastSelectedColumnRef.current = lastCol;
            } else {
                // Normal click or cmd+click: sync with glide's selection
                currentColumnSelectionRef.current = glideColumns;
                if (glideColumns.length > 0) {
                    let lastCol = 0;
                    for (const col of glideColumns) {
                        lastCol = col;
                    }
                    lastSelectedColumnRef.current = lastCol;
                } else {
                    lastSelectedColumnRef.current = null;
                }
            }
        } else if (adjustedSelection.columns) {
            // Sync our ref with glide's selection when not in multi mode
            currentColumnSelectionRef.current = adjustedSelection.columns;
        }

        // Update internal state for visual feedback and editing
        setGridSelection(adjustedSelection);

        if (!setProps) return;

        const updates = {};

        // Handle cell selection
        if (adjustedSelection.current) {
            const cellSelection = adjustedSelection.current.cell;
            if (cellSelection) {
                updates.selectedCell = {
                    col: cellSelection[0],
                    row: cellSelection[1]
                };
            }

            // Handle range selection
            const range = adjustedSelection.current.range;
            if (range) {
                updates.selectedRange = {
                    startCol: range.x,
                    startRow: range.y,
                    endCol: range.x + range.width - 1,
                    endRow: range.y + range.height - 1
                };
            }

            // Handle multi-range selection (rangeStack for multi-rect mode)
            const rangeStack = adjustedSelection.current.rangeStack;
            if (rangeStack && rangeStack.length > 0) {
                updates.selectedRanges = rangeStack.map(r => ({
                    startCol: r.x,
                    startRow: r.y,
                    endCol: r.x + r.width - 1,
                    endRow: r.y + r.height - 1
                }));
            } else {
                updates.selectedRanges = [];
            }
        }

        // Handle row selection (CompactSelection to array)
        if (adjustedSelection.rows && adjustedSelection.rows.length > 0) {
            const rowsArray = [];
            // CompactSelection is iterable, use for...of instead of forEach
            for (const row of adjustedSelection.rows) {
                rowsArray.push(row);
            }
            updates.selectedRows = rowsArray;
        }

        // Handle column selection (CompactSelection to array)
        if (adjustedSelection.columns && adjustedSelection.columns.length > 0) {
            const colsArray = [];
            // CompactSelection is iterable, use for...of instead of forEach
            for (const col of adjustedSelection.columns) {
                colsArray.push(col);
            }
            updates.selectedColumns = colsArray;
        }

        if (Object.keys(updates).length > 0) {
            setProps(updates);
        }
    }, [setProps, selectionColumnMin, unselectableColumns, unselectableRows, rowSelectOnCellClick, rowSelect, rangeSelect, columnSelect]);

    // Handle column resize
    const handleColumnResize = useCallback((column, newSize, columnIndex) => {
        if (!setProps) return;

        // Use functional update to avoid stale closure when multiple resizes fire rapidly
        // (e.g., from remeasureColumns triggering resize events for multiple columns)
        setLocalColumns(prevColumns => {
            if (!prevColumns) return prevColumns;

            const newColumns = prevColumns.map((col, idx) => {
                if (idx === columnIndex) {
                    return { ...col, width: newSize };
                }
                return col;
            });

            // Send new widths to Dash
            const newWidths = newColumns.map(col => col.width || 150);
            setProps({
                columnWidths: newWidths
            });

            return newColumns;
        });
    }, [setProps]);

    // Handle search close
    const handleSearchClose = useCallback(() => {
        // Update local state immediately
        setLocalSearchValue('');

        if (setProps) {
            setProps({
                showSearch: false,
                searchValue: ''
            });
        }
    }, [setProps]);

    // Handle search value change
    const handleSearchValueChange = useCallback((newValue) => {
        const currentSearchValue = localSearchValueRef.current;
        const now = Date.now();

        // Glide DataGrid bug workaround: it calls onSearchValueChange with '' multiple times
        // immediately after setting any non-empty value. Ignore these spurious calls.
        if (newValue === '' && now < ignoreEmptyUntil.current) {
            return;
        }

        // Only update if the value actually changed
        if (newValue === currentSearchValue) {
            return;
        }

        // Update local state immediately for optimistic update
        setLocalSearchValue(newValue);

        // CRITICAL: Update ref immediately (synchronously) so the next call to this handler
        // sees the updated value. This prevents the cascade of empty string updates.
        localSearchValueRef.current = newValue;

        // If we just set a non-empty value, ignore empty strings for the next 100ms
        // This handles all spurious empty string calls from Glide DataGrid
        if (newValue !== '') {
            ignoreEmptyUntil.current = now + 100;
        }

        if (setProps) {
            // Store this search value so we can ignore it when it comes back from Dash
            lastSentSearchValue.current = newValue;

            setProps({
                searchValue: newValue
            });
        }
    }, [setProps]);

    // Handle fill pattern (Excel-like fill handle drag)
    const handleFillPattern = useCallback((event) => {
        // Always prevent default to stop Glide's built-in fill behavior
        // We handle all fill operations ourselves for proper hidden row filtering
        event.preventDefault();

        if (!setProps || readonly) {
            return;
        }

        // Use ref to get the most current data (avoids stale closures)
        const currentData = localDataRef.current;
        const currentColumns = localColumnsRef.current;
        if (!currentData || !currentColumns) {
            return;
        }

        const { patternSource, fillDestination } = event;

        // Create a deep copy of the data (array of objects)
        const newData = currentData.map(r => ({...r}));

        // Get source pattern dimensions
        const sourceWidth = patternSource.width;
        const sourceHeight = patternSource.height;

        // Fill the destination with pattern from source
        for (let destRow = fillDestination.y; destRow < fillDestination.y + fillDestination.height; destRow++) {
            // Skip hidden rows (only if skipOnFill is enabled)
            if (skipOnFill && hiddenRowsSet.has(destRow)) continue;

            // Translate display row to actual data row if sorting is active
            const actualDestRow = sortedIndices ? sortedIndices[destRow] : destRow;
            if (actualDestRow >= newData.length) break;

            for (let destCol = fillDestination.x; destCol < fillDestination.x + fillDestination.width; destCol++) {
                if (destCol >= currentColumns.length) break;

                // Get column id to access dict key
                const destColumnDef = currentColumns[destCol];
                const destColumnId = destColumnDef?.id || destColumnDef?.title;

                // Calculate which cell in the pattern to copy from (display indices)
                const displaySourceRow = patternSource.y + ((destRow - fillDestination.y) % sourceHeight);
                const sourceCol = patternSource.x + ((destCol - fillDestination.x) % sourceWidth);

                // Translate source row to actual data row
                const actualSourceRow = sortedIndices ? sortedIndices[displaySourceRow] : displaySourceRow;

                // Get source column id
                const sourceColumnDef = currentColumns[sourceCol];
                const sourceColumnId = sourceColumnDef?.id || sourceColumnDef?.title;

                // Get old value before overwriting
                const oldValue = newData[actualDestRow][destColumnId];

                // Copy the value from source to destination
                const sourceValue = newData[actualSourceRow][sourceColumnId];
                newData[actualDestRow] = { ...newData[actualDestRow], [destColumnId]: sourceValue };

                // Track edit for undo/redo
                addEditToBatch({
                    col: destCol,
                    row: actualDestRow,
                    columnId: destColumnId,
                    oldValue: oldValue,
                    newValue: sourceValue
                });
            }
        }

        // Update local state immediately (optimistic update)
        setLocalData(newData);

        // CRITICAL: Update the ref immediately so next edit sees the updated data
        localDataRef.current = newData;

        // Store this data so we can ignore it when it comes back from Dash
        lastSentData.current = newData;

        // Translate row for the event
        const actualFillRow = sortedIndices ? sortedIndices[fillDestination.y] : fillDestination.y;

        // Sync with Dash
        setProps({
            data: newData,
            cellEdited: {
                col: fillDestination.x,
                row: actualFillRow,
                value: `Filled ${fillDestination.height}x${fillDestination.width} range`,
                timestamp: Date.now()
            }
        });
    }, [setProps, readonly, sortedIndices, addEditToBatch, hiddenRowsSet, skipOnFill]);

    // ========== PHASE 2: EVENT HANDLERS ==========

    // Handle header clicks (for sorting)
    const handleHeaderClicked = useCallback((colIndex, event) => {
        // Always emit the headerClicked event
        if (setProps) {
            setProps({
                headerClicked: {
                    col: colIndex,
                    timestamp: Date.now()
                }
            });
        }

        // Handle built-in sorting if enabled
        if (!sortable) return;

        // Check if this column is sortable (column-level override)
        const columnDef = localColumns && localColumns[colIndex];
        if (columnDef && columnDef.sortable === false) return;

        // Get the current sort order cycle (default: asc -> desc -> none)
        const cycle = sortingOrder || ['asc', 'desc', null];

        // Check if Shift key is held for multi-column sort
        const isShiftHeld = event?.shiftKey || false;

        // Find if this column is already in the sort
        const existingSortIndex = localSortColumns.findIndex(sc => sc.columnIndex === colIndex);
        const existingSort = existingSortIndex >= 0 ? localSortColumns[existingSortIndex] : null;

        let newSortColumns;

        if (isShiftHeld && localSortColumns.length > 0) {
            // Multi-column sort: add or toggle this column
            if (existingSort) {
                // Column already in sort - cycle its direction
                const currentDirIndex = cycle.indexOf(existingSort.direction);
                const nextDirIndex = (currentDirIndex + 1) % cycle.length;
                const nextDir = cycle[nextDirIndex];

                if (nextDir === null) {
                    // Remove this column from sort
                    newSortColumns = localSortColumns.filter((_, i) => i !== existingSortIndex);
                } else {
                    // Update direction
                    newSortColumns = localSortColumns.map((sc, i) =>
                        i === existingSortIndex ? { ...sc, direction: nextDir } : sc
                    );
                }
            } else {
                // Add this column to the sort
                const firstDir = cycle.find(d => d !== null) || 'asc';
                newSortColumns = [...localSortColumns, { columnIndex: colIndex, direction: firstDir }];
            }
        } else {
            // Single-column sort: replace all sorting with this column
            if (existingSort && localSortColumns.length === 1) {
                // Same column clicked - cycle direction
                const currentDirIndex = cycle.indexOf(existingSort.direction);
                const nextDirIndex = (currentDirIndex + 1) % cycle.length;
                const nextDir = cycle[nextDirIndex];

                if (nextDir === null) {
                    // Clear sorting
                    newSortColumns = [];
                } else {
                    newSortColumns = [{ columnIndex: colIndex, direction: nextDir }];
                }
            } else {
                // Different column or first sort - start with first direction in cycle
                const firstDir = cycle.find(d => d !== null) || 'asc';
                newSortColumns = [{ columnIndex: colIndex, direction: firstDir }];
            }
        }

        // Update local state immediately
        setLocalSortColumns(newSortColumns);

        // Sync with Dash
        if (setProps) {
            setProps({
                sortColumns: newSortColumns
            });
        }
    }, [setProps, sortable, localColumns, sortingOrder, localSortColumns]);

    // Handle header context menu (right-click)
    const handleHeaderContextMenu = useCallback((colIndex, event) => {
        if (setProps) {
            setProps({
                headerContextMenu: {
                    col: colIndex,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // Sync visibleRowIndices to Dash when displayIndices changes
    useEffect(() => {
        if (setProps) {
            const indices = displayIndices || (localData ? localData.map((_, i) => i) : []);
            setProps({
                visibleRowIndices: indices
            });
        }
    }, [displayIndices, localData, setProps]);

    // Handle filter change from HeaderMenu
    const handleFilterChange = useCallback((columnIndex, selectedValues) => {
        const newFilters = { ...localFilters };

        if (selectedValues === null) {
            // Clear filter for this column
            delete newFilters[columnIndex];
        } else {
            // Set filter for this column
            newFilters[columnIndex] = selectedValues;
        }

        setLocalFilters(newFilters);

        // Sync filter state to Dash
        if (setProps) {
            setProps({
                columnFilters: newFilters
            });
        }
    }, [localFilters, setProps]);

    // Handle filter menu close
    const handleFilterMenuClose = useCallback(() => {
        setFilterMenuState({
            isOpen: false,
            columnIndex: null,
            position: null
        });
    }, []);

    // Handle custom menu item click
    const handleCustomItemClick = useCallback((itemId, columnIndex) => {
        const item = headerMenuConfig?.customItems?.find(i => i.id === itemId);
        if (item && isFunctionRef(item.onClick)) {
            executeFunction(item.onClick.function, {
                col: columnIndex,
                columns: localColumns,
                data: localData
            });
        }

        if (setProps) {
            setProps({
                headerMenuItemClicked: {
                    col: columnIndex,
                    itemId: itemId,
                    timestamp: Date.now()
                }
            });
        }
    }, [headerMenuConfig, localColumns, localData, setProps]);

    // Handle cell context menu close
    const handleContextMenuClose = useCallback(() => {
        setContextMenuState({
            isOpen: false,
            col: null,
            row: null,
            position: null
        });
    }, []);

    // Handle cell context menu item click
    const handleContextMenuItemClick = useCallback((item) => {
        const { col, row } = contextMenuState;
        const itemId = item.id;
        const action = item.action;

        // Handle built-in actions
        if (action === 'copyClickedCell') {
            // Copy the clicked cell value to clipboard
            if (localData && localColumns && col !== null && row !== null) {
                navigator.clipboard.writeText(getCellCopyValue(col, row)).catch(err => {
                    console.error('Failed to copy cell:', err);
                });
                // Trigger flash for the copied cell
                if (shouldFlash('copy')) {
                    const actualRow = sortedIndices ? sortedIndices[row] : row;
                    setLastUpdatedCells(prev => ({
                        ...prev,
                        [`${actualRow},${col}`]: performance.now()
                    }));
                }
            }
        } else if (action === 'copySelection') {
            // Copy the current selection as TSV
            if (localData && localColumns && gridSelection.current?.range) {
                const range = gridSelection.current.range;
                const startCol = range.x;
                const endCol = range.x + range.width - 1;
                const startRow = range.y;
                const endRow = range.y + range.height - 1;

                const lines = [];
                for (let r = startRow; r <= endRow; r++) {
                    if (r < localData.length) {
                        const rowValues = [];
                        for (let c = startCol; c <= endCol; c++) {
                            rowValues.push(getCellCopyValue(c, r));
                        }
                        lines.push(rowValues.join('\t'));
                    }
                }
                navigator.clipboard.writeText(lines.join('\n')).catch(err => {
                    console.error('Failed to copy selection:', err);
                });
                // Trigger flash for all copied cells
                if (shouldFlash('copy')) {
                    const now = performance.now();
                    const updatedCells = {};
                    for (let r = startRow; r <= endRow; r++) {
                        const actualRow = sortedIndices ? sortedIndices[r] : r;
                        for (let c = startCol; c <= endCol; c++) {
                            updatedCells[`${actualRow},${c}`] = now;
                        }
                    }
                    setLastUpdatedCells(prev => ({ ...prev, ...updatedCells }));
                }
            } else if (col !== null && row !== null) {
                // No range selection, copy single cell
                navigator.clipboard.writeText(getCellCopyValue(col, row)).catch(err => {
                    console.error('Failed to copy cell:', err);
                });
                // Trigger flash for the copied cell
                if (shouldFlash('copy')) {
                    const actualRow = sortedIndices ? sortedIndices[row] : row;
                    setLastUpdatedCells(prev => ({
                        ...prev,
                        [`${actualRow},${col}`]: performance.now()
                    }));
                }
            }
        } else if (action === 'pasteAtClickedCell') {
            // Paste from clipboard starting at clicked cell
            if (col !== null && row !== null && localData && localColumns) {
                navigator.clipboard.readText().then(text => {
                    if (!text) return;

                    // Parse TSV/CSV content
                    const lines = text.split('\n').filter(line => line.length > 0);
                    const newData = [...localData];
                    const edits = [];

                    lines.forEach((line, lineIdx) => {
                        const targetRow = row + lineIdx;
                        if (targetRow >= newData.length) return;

                        const values = line.split('\t');
                        const newRowData = { ...newData[targetRow] };

                        values.forEach((val, valIdx) => {
                            const targetCol = col + valIdx;
                            if (targetCol >= localColumns.length) return;

                            const columnDef = localColumns[targetCol];
                            const columnId = columnDef?.id;
                            if (columnId && !columnDef.readonly) {
                                const oldValue = newRowData[columnId];
                                const newValue = coercePastedValue(val, oldValue);
                                newRowData[columnId] = newValue;
                                edits.push({ col: targetCol, row: targetRow, value: newValue });
                            }
                        });

                        newData[targetRow] = newRowData;
                    });

                    if (edits.length > 0) {
                        setLocalData(newData);
                        if (setProps) {
                            setProps({
                                data: newData,
                                cellsEdited: {
                                    edits,
                                    count: edits.length,
                                    timestamp: Date.now()
                                }
                            });
                        }
                    }
                }).catch(err => {
                    console.error('Failed to paste:', err);
                });
            }
        } else if (action === 'pasteAtSelection') {
            // Paste from clipboard starting at top-left of current selection
            if (localData && localColumns && gridSelection.current?.range) {
                const range = gridSelection.current.range;
                const startCol = range.x;
                const startRow = range.y;

                navigator.clipboard.readText().then(text => {
                    if (!text) return;

                    // Parse TSV/CSV content
                    const lines = text.split('\n').filter(line => line.length > 0);
                    const newData = [...localData];
                    const edits = [];

                    lines.forEach((line, lineIdx) => {
                        const targetRow = startRow + lineIdx;
                        if (targetRow >= newData.length) return;

                        const values = line.split('\t');
                        const newRowData = { ...newData[targetRow] };

                        values.forEach((val, valIdx) => {
                            const targetCol = startCol + valIdx;
                            if (targetCol >= localColumns.length) return;

                            const columnDef = localColumns[targetCol];
                            const columnId = columnDef?.id;
                            if (columnId && !columnDef.readonly) {
                                const oldValue = newRowData[columnId];
                                const newValue = coercePastedValue(val, oldValue);
                                newRowData[columnId] = newValue;
                                edits.push({ col: targetCol, row: targetRow, value: newValue });
                            }
                        });

                        newData[targetRow] = newRowData;
                    });

                    if (edits.length > 0) {
                        setLocalData(newData);
                        if (setProps) {
                            setProps({
                                data: newData,
                                cellsEdited: {
                                    edits,
                                    count: edits.length,
                                    timestamp: Date.now()
                                }
                            });
                        }
                    }
                }).catch(err => {
                    console.error('Failed to paste selection:', err);
                });
            } else if (col !== null && row !== null && localData && localColumns) {
                // No range selection, fall back to paste at clicked cell
                navigator.clipboard.readText().then(text => {
                    if (!text) return;

                    const lines = text.split('\n').filter(line => line.length > 0);
                    const newData = [...localData];
                    const edits = [];

                    lines.forEach((line, lineIdx) => {
                        const targetRow = row + lineIdx;
                        if (targetRow >= newData.length) return;

                        const values = line.split('\t');
                        const newRowData = { ...newData[targetRow] };

                        values.forEach((val, valIdx) => {
                            const targetCol = col + valIdx;
                            if (targetCol >= localColumns.length) return;

                            const columnDef = localColumns[targetCol];
                            const columnId = columnDef?.id;
                            if (columnId && !columnDef.readonly) {
                                const oldValue = newRowData[columnId];
                                const newValue = coercePastedValue(val, oldValue);
                                newRowData[columnId] = newValue;
                                edits.push({ col: targetCol, row: targetRow, value: newValue });
                            }
                        });

                        newData[targetRow] = newRowData;
                    });

                    if (edits.length > 0) {
                        setLocalData(newData);
                        if (setProps) {
                            setProps({
                                data: newData,
                                cellsEdited: {
                                    edits,
                                    count: edits.length,
                                    timestamp: Date.now()
                                }
                            });
                        }
                    }
                }).catch(err => {
                    console.error('Failed to paste:', err);
                });
            }
        } else if (action === 'clearClickedCell') {
            // Clear the clicked cell value
            if (col !== null && row !== null && localData && localColumns) {
                const columnDef = localColumns[col];
                const columnId = columnDef?.id;
                if (columnId && !columnDef.readonly) {
                    const oldValue = localData[row]?.[columnId];
                    const newValue = getClearedValue(col, row, oldValue);
                    const newData = [...localData];
                    newData[row] = { ...newData[row], [columnId]: newValue };
                    setLocalData(newData);
                    if (setProps) {
                        setProps({
                            data: newData,
                            cellsEdited: {
                                edits: [{ col, row, value: newValue }],
                                count: 1,
                                timestamp: Date.now()
                            }
                        });
                    }
                }
            }
        } else if (action === 'clearSelection') {
            // Clear all cells in the current selection
            if (localData && localColumns && gridSelection.current?.range) {
                const range = gridSelection.current.range;
                const newData = [...localData];
                const edits = [];

                for (let r = range.y; r < range.y + range.height; r++) {
                    if (r >= newData.length) continue;
                    const newRowData = { ...newData[r] };

                    for (let c = range.x; c < range.x + range.width; c++) {
                        if (c >= localColumns.length) continue;
                        const columnDef = localColumns[c];
                        const columnId = columnDef?.id;
                        if (columnId && !columnDef.readonly) {
                            const oldValue = newRowData[columnId];
                            const newValue = getClearedValue(c, r, oldValue);
                            newRowData[columnId] = newValue;
                            edits.push({ col: c, row: r, value: newValue });
                        }
                    }
                    newData[r] = newRowData;
                }

                if (edits.length > 0) {
                    setLocalData(newData);
                    if (setProps) {
                        setProps({
                            data: newData,
                            cellsEdited: {
                                edits,
                                count: edits.length,
                                timestamp: Date.now()
                            }
                        });
                    }
                }
            } else if (col !== null && row !== null && localData && localColumns) {
                // No range selection, fall back to clear single clicked cell
                const columnDef = localColumns[col];
                const columnId = columnDef?.id;
                if (columnId && !columnDef.readonly) {
                    const oldValue = localData[row]?.[columnId];
                    const newValue = getClearedValue(col, row, oldValue);
                    const newData = [...localData];
                    newData[row] = { ...newData[row], [columnId]: newValue };
                    setLocalData(newData);
                    if (setProps) {
                        setProps({
                            data: newData,
                            cellsEdited: {
                                edits: [{ col, row, value: newValue }],
                                count: 1,
                                timestamp: Date.now()
                            }
                        });
                    }
                }
            }
        } else if (isFunctionRef(action)) {
            // Handle clientside function action
            const columnDef = localColumns?.[col];
            const columnId = columnDef?.id;
            const rowData = localData?.[row];
            const cellData = rowData?.[columnId];

            // Build utility functions
            const utils = {
                setData: (newData) => {
                    setLocalData(newData);
                    if (setProps) {
                        setProps({ data: newData });
                    }
                },
                setCells: (edits) => {
                    const newData = [...localData];
                    edits.forEach(edit => {
                        const colIdx = typeof edit.col === 'number'
                            ? edit.col
                            : localColumns.findIndex(c => c.id === edit.columnId);
                        const colId = localColumns[colIdx]?.id;
                        if (colId && edit.row >= 0 && edit.row < newData.length) {
                            newData[edit.row] = { ...newData[edit.row], [colId]: edit.value };
                        }
                    });
                    setLocalData(newData);
                    if (setProps) {
                        setProps({
                            data: newData,
                            cellsEdited: {
                                edits: edits.map(e => ({ col: e.col, row: e.row, value: e.value })),
                                count: edits.length,
                                timestamp: Date.now()
                            }
                        });
                    }
                },
                getClipboard: () => navigator.clipboard.readText(),
                setClipboard: (text) => navigator.clipboard.writeText(text)
            };

            const params = {
                col,
                row,
                columnId,
                cellData,
                rowData,
                selection: {
                    range: gridSelection.current?.range || null,
                    cell: gridSelection.current?.cell || null
                },
                columns: localColumns,
                data: localData,
                utils
            };

            // Helper to emit callback and close menu
            const emitAndClose = () => {
                if (setProps) {
                    setProps({
                        contextMenuItemClicked: {
                            col,
                            row,
                            itemId,
                            timestamp: Date.now()
                        }
                    });
                }
                handleContextMenuClose();
            };

            // Execute the function (may be async)
            try {
                const result = executeFunction(action.function, params);
                // Handle async functions - wait for completion before emitting callback
                Promise.resolve(result).then(emitAndClose).catch((err) => {
                    console.error('[GlideGrid] Error executing context menu action:', err);
                    emitAndClose();
                });
            } catch (err) {
                console.error('[GlideGrid] Error executing context menu action:', err);
                emitAndClose();
            }

            // Return early - callback and close handled above
            return;
        }

        // Always emit the event for Python callbacks
        if (setProps) {
            setProps({
                contextMenuItemClicked: {
                    col,
                    row,
                    itemId,
                    timestamp: Date.now()
                }
            });
        }
        handleContextMenuClose();
    }, [setProps, contextMenuState, handleContextMenuClose, localData, localColumns, gridSelection, getClearedValue]);

    // Handle header menu click (dropdown arrow on columns with hasMenu or filterable)
    const handleHeaderMenuClick = useCallback((col, screenPosition) => {
        // Check if this column is filterable
        const columnDef = localColumns && localColumns[col];
        const isFilterable = columnDef && columnDef.filterable;

        if (isFilterable) {
            // Open the filter menu
            setFilterMenuState({
                isOpen: true,
                columnIndex: col,
                position: { x: screenPosition.x, y: screenPosition.y }
            });
        }

        // Always emit the event for backwards compatibility
        if (setProps) {
            setProps({
                headerMenuClicked: {
                    col: col,
                    screenX: screenPosition.x,
                    screenY: screenPosition.y,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, localColumns]);

    // Handle group header clicks
    const handleGroupHeaderClicked = useCallback((colIndex, event) => {
        if (setProps) {
            // Try to get the group name from the columns
            const groupName = localColumns && localColumns[colIndex] ? localColumns[colIndex].group : undefined;
            setProps({
                groupHeaderClicked: {
                    col: colIndex,
                    group: groupName,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, localColumns]);

    // Handle cell context menu (right-click on cell)
    const handleContextMenu = useCallback((cell, event) => {
        // Ignore context menu on hidden rows
        if (hiddenRowsSet.has(cell[1])) {
            event.preventDefault();
            return;
        }

        const hasConfig = contextMenuConfig?.items?.length > 0;

        // Prevent browser's default context menu
        event.preventDefault();

        // Use the mouse position captured by our native event listener
        const screenX = lastContextMenuPosition.current.x;
        const screenY = lastContextMenuPosition.current.y;

        // Open built-in context menu if configured
        if (hasConfig) {
            setContextMenuState({
                isOpen: true,
                col: cell[0],
                row: cell[1],
                position: { x: screenX, y: screenY }
            });
        }

        // Always emit prop for backwards compatibility (now with position)
        if (setProps) {
            setProps({
                contextMenu: {
                    col: cell[0],
                    row: cell[1],
                    screenX,
                    screenY,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, contextMenuConfig, hiddenRowsSet]);

    // Handle cell activation (Enter, Space, or double-click)
    const handleCellActivated = useCallback((cell) => {
        // Get the cell content to check if it has an overlay editor
        const cellContent = getCellContent(cell);

        // Only set isEditorOpen if the cell actually supports overlays
        // This prevents scroll locking for cells like button, spinner, links, etc.
        if (cellContent.allowOverlay) {
            setIsEditorOpen(true);

            // Safety fallback: if portal is still empty after a short delay,
            // the overlay didn't actually open (e.g., cell renderer has no provideEditor)
            setTimeout(() => {
                const portal = document.getElementById('portal');
                if (portal && portal.children.length === 0) {
                    setIsEditorOpen(false);
                }
            }, 50);
        }

        if (setProps) {
            setProps({
                cellActivated: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, getCellContent]);

    // Handle item hover changes
    const handleItemHovered = useCallback((args) => {
        // Don't update hover state while editor is open - prevents re-renders
        // that would reset dropdown scroll position
        if (isEditorOpen) {
            return;
        }

        // Update internal hover state for row highlighting
        if (args.kind === 'cell' && args.location) {
            setHoveredRow(args.location[1]);
        } else {
            setHoveredRow(null);
        }

        if (setProps) {
            setProps({
                itemHovered: {
                    col: args.location ? args.location[0] : undefined,
                    row: args.location ? args.location[1] : undefined,
                    kind: args.kind,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, isEditorOpen]);

    // Handle mouse move events (raw mouse movement, fires on every move)
    // Skip when editor is open to prevent re-renders that interfere with text input
    const handleMouseMove = useCallback((args) => {
        if (setProps && !isEditorOpen) {
            setProps({
                mouseMove: {
                    col: args.location ? args.location[0] : undefined,
                    row: args.location ? args.location[1] : undefined,
                    kind: args.kind,
                    localEventX: args.localEventX,
                    localEventY: args.localEventY,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps, isEditorOpen]);

    // Handle batch cell edits (paste/fill operations affecting multiple cells)
    const handleCellsEdited = useCallback((edits) => {
        if (setProps) {
            // Transform edits to a Dash-friendly format
            const editsList = edits.map(edit => ({
                col: edit.location[0],
                row: edit.location[1],
                value: (edit.value?.data ?? edit.value) ?? ''
            }));

            setProps({
                cellsEdited: {
                    edits: editsList,
                    count: editsList.length,
                    timestamp: Date.now()
                }
            });
        }
        // Return undefined to allow onCellEdited to still be called for single edits.
        // Our onCellEdited/onPaste/onFillPattern handlers do the actual data updates.
        // Returning true would prevent onCellEdited from firing.
        return undefined;
    }, [setProps]);

    // Handle delete key press
    const handleDelete = useCallback((selection) => {
        // Extract selection info for Dash callback
        const selectedCells = [];
        const selectedRowIndices = [];
        const selectedColIndices = [];

        // Get selected rows
        if (selection.rows) {
            for (const row of selection.rows) {
                selectedRowIndices.push(row);
            }
        }

        // Get selected columns
        if (selection.columns) {
            for (const col of selection.columns) {
                selectedColIndices.push(col);
            }
        }

        // Get selected cell/range
        if (selection.current) {
            const range = selection.current.range;
            if (range) {
                for (let row = range.y; row < range.y + range.height; row++) {
                    for (let col = range.x; col < range.x + range.width; col++) {
                        selectedCells.push({ col, row });
                    }
                }
            }
        }

        // Fire deletePressed callback for user notification
        if (setProps) {
            setProps({
                deletePressed: {
                    cells: selectedCells,
                    rows: selectedRowIndices,
                    columns: selectedColIndices,
                    timestamp: Date.now()
                }
            });
        }

        // If deletion is disabled or grid is readonly, prevent deletion
        if (allowDelete === false || readonly || !setProps) {
            return false;
        }

        // Handle deletion ourselves using getClearedValue
        // This ensures all cell types (including Bubble, Drilldown, Image, custom cells)
        // are properly cleared, unlike Glide's internal clearing which only handles basic types
        const currentData = localDataRef.current;
        const currentColumns = localColumnsRef.current;
        if (!currentData || !currentColumns) {
            return false;
        }

        const newData = currentData.map(r => ({...r}));
        const edits = [];

        // Process range selection
        if (selection.current?.range) {
            const range = selection.current.range;
            for (let displayRow = range.y; displayRow < range.y + range.height; displayRow++) {
                // Skip hidden rows (only if skipOnDelete is enabled)
                if (skipOnDelete && hiddenRowsSet.has(displayRow)) continue;

                // Translate display row to data row if sorting is active
                const dataRow = sortedIndices ? sortedIndices[displayRow] : displayRow;
                if (dataRow >= newData.length) continue;

                for (let col = range.x; col < range.x + range.width; col++) {
                    if (col >= currentColumns.length) continue;
                    const columnDef = currentColumns[col];
                    const columnId = columnDef?.id;
                    if (columnId && !columnDef.readonly) {
                        const oldValue = newData[dataRow][columnId];
                        const newValue = getClearedValue(col, displayRow, oldValue);
                        newData[dataRow][columnId] = newValue;
                        edits.push({ col, row: displayRow, value: newValue });
                    }
                }
            }
        }

        if (edits.length > 0) {
            setLocalData(newData);
            setProps({
                data: newData,
                cellsEdited: {
                    edits,
                    count: edits.length,
                    timestamp: Date.now()
                }
            });
        }

        // Return false to prevent Glide from doing its own clearing
        // We've already handled all the cell clearing ourselves
        return false;
    }, [setProps, allowDelete, readonly, getClearedValue, sortedIndices, hiddenRowsSet, skipOnDelete]);

    // Handle visible region changes
    const handleVisibleRegionChanged = useCallback((range, tx, ty, extras) => {
        // Close editor on grid internal scroll if behavior is set
        if (editorScrollBehavior === 'close-on-scroll' && isEditorOpen) {
            const portal = document.getElementById('portal');
            if (portal && portal.children.length > 0) {
                const escapeEvent = new KeyboardEvent('keydown', {
                    key: 'Escape',
                    code: 'Escape',
                    keyCode: 27,
                    which: 27,
                    bubbles: true,
                    cancelable: true
                });
                portal.dispatchEvent(escapeEvent);
                if (portal.firstElementChild) {
                    portal.firstElementChild.dispatchEvent(escapeEvent);
                }
            }
            setIsEditorOpen(false);
        }

        // Close context menu on grid internal scroll if behavior is set
        if (contextMenuScrollBehavior === 'close-overlay-on-scroll' && contextMenuState.isOpen) {
            handleContextMenuClose();
        }

        if (setProps) {
            setProps({
                visibleRegion: {
                    x: range.x,
                    y: range.y,
                    width: range.width,
                    height: range.height,
                    tx: tx,
                    ty: ty
                }
            });
        }
    }, [setProps, editorScrollBehavior, isEditorOpen, contextMenuScrollBehavior, contextMenuState.isOpen, handleContextMenuClose]);

    // ========== PHASE 3: ROW/COLUMN REORDERING ==========

    // Handle column moved (drag reorder)
    const handleColumnMoved = useCallback((startIndex, endIndex) => {
        // Optimistic update: reorder local columns immediately to prevent jitter
        setLocalColumns(prevColumns => {
            const newColumns = [...prevColumns];
            const [moved] = newColumns.splice(startIndex, 1);
            newColumns.splice(endIndex, 0, moved);
            return newColumns;
        });

        // Notify Dash
        if (setProps) {
            setProps({
                columnMoved: {
                    startIndex: startIndex,
                    endIndex: endIndex,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // Handle row moved (drag reorder)
    const handleRowMoved = useCallback((startIndex, endIndex) => {
        // Optimistic update: reorder local data immediately to prevent jitter
        setLocalData(prevData => {
            const newData = [...prevData];
            const [moved] = newData.splice(startIndex, 1);
            newData.splice(endIndex, 0, moved);
            return newData;
        });

        // Notify Dash
        if (setProps) {
            setProps({
                rowMoved: {
                    startIndex: startIndex,
                    endIndex: endIndex,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // ========== PHASE 5: TRAILING ROW (ADD ROW) ==========

    // Handle row appended (trailing row clicked)
    const handleRowAppended = useCallback(() => {
        if (setProps) {
            setProps({
                rowAppended: {
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // ========== ADVANCED: DRAG AND DROP HANDLERS ==========

    // Handle drag start (when isDraggable is enabled)
    const handleDragStart = useCallback((args) => {
        if (setProps) {
            setProps({
                dragStarted: {
                    col: args.location ? args.location[0] : undefined,
                    row: args.location ? args.location[1] : undefined,
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // Handle drag over cell (external drag)
    const handleDragOverCell = useCallback((cell, dataTransfer) => {
        if (setProps) {
            setProps({
                dragOverCell: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // Handle drop on cell (external drag)
    const handleDrop = useCallback((cell, dataTransfer) => {
        if (setProps) {
            setProps({
                droppedOnCell: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // ========== CLIENT-SIDE VALIDATION ==========

    // Create validateCell callback for Glide DataEditor
    // This executes user-defined JS functions from window.dashGlideGridFunctions
    const handleValidateCell = useMemo(() => {
        if (!validateCell || !isFunctionRef(validateCell)) {
            return undefined;
        }

        return (cell, newValue) => {
            const [col, row] = cell;

            const result = executeFunction(
                validateCell.function,
                { cell, newValue, col, row }
            );

            // Handle return values:
            // - false: reject the edit
            // - true or undefined: accept the edit
            // - GridCell object: coerce to this value
            if (result === false) {
                return false;
            }
            if (result && typeof result === 'object' && result.kind) {
                return result;
            }
            return true;
        };
    }, [validateCell]);

    // Create coercePasteValue callback for Glide DataEditor
    // Transforms pasted strings into proper cell types
    const handleCoercePasteValue = useMemo(() => {
        if (!coercePasteValue || !isFunctionRef(coercePasteValue)) {
            return undefined;
        }

        return (val, cell) => {
            const result = executeFunction(
                coercePasteValue.function,
                { val, cell, value: val }
            );

            // Return the coerced GridCell or undefined to use default
            if (result && typeof result === 'object' && result.kind) {
                return result;
            }
            return undefined;
        };
    }, [coercePasteValue]);

    // Create getRowThemeOverride callback for Glide DataEditor
    // Combines user-defined row theme with row hover effect
    const handleGetRowThemeOverride = useCallback((rowIndex) => {
        // Hidden rows get fully transparent theme (hides row marker and cells)
        if (hiddenRowsSet.has(rowIndex)) {
            return {
                bgCell: 'transparent',
                bgCellMedium: 'transparent',
                textDark: 'transparent',
                textMedium: 'transparent',
                textLight: 'transparent',
                textBubble: 'transparent',
                bgBubble: 'transparent',
                bgBubbleSelected: 'transparent',
                textHeader: 'transparent',
                textHeaderSelected: 'transparent',
                accentColor: 'transparent',
                accentLight: 'transparent',
                borderColor: 'transparent',
                horizontalBorderColor: 'transparent',
                drilldownBorder: 'transparent',
                linkColor: 'transparent',
                cellHorizontalPadding: 0,
                cellVerticalPadding: 0,
            };
        }

        let themeOverride = undefined;

        // Apply row hover effect if enabled
        if (hoverRow && rowIndex === hoveredRow) {
            const rowColor = theme?.bgRowHovered || 'rgba(0, 0, 0, 0.04)';
            themeOverride = {
                bgCell: rowColor,
                bgCellMedium: rowColor
            };
        }

        // Apply user-defined row theme override (if provided)
        if (getRowThemeOverride && isFunctionRef(getRowThemeOverride)) {
            const rowData = data && data[rowIndex] ? data[rowIndex] : null;
            const userOverride = executeFunction(
                getRowThemeOverride.function,
                { row: rowIndex, rowData, data }
            );

            if (userOverride && typeof userOverride === 'object') {
                // Merge user override with hover highlight (user takes precedence)
                themeOverride = { ...themeOverride, ...userOverride };
            }
        }

        return themeOverride;
    }, [getRowThemeOverride, data, hoverRow, hoveredRow, theme?.bgRowHovered, hiddenRowsSet]);

    // Create drawCell callback for custom cell rendering
    // Allows complete control over cell drawing via Canvas API
    // Also handles fix for drawFocusRing=false losing row/column accent highlighting
    const handleDrawCell = useMemo(() => {
        // When drawFocusRing=false, the focused cell loses its accent background
        // even if it's part of a selected row/column. We need to compensate.
        const needsFocusHighlightFix = drawFocusRing === false;

        // Skip if no fix needed and no custom drawCell
        if (!needsFocusHighlightFix && (!drawCell || !isFunctionRef(drawCell))) {
            return undefined;
        }

        return (args, drawContent) => {
            const { ctx, cell, theme: cellTheme, rect, col, row, hoverAmount, highlighted } = args;

            // Fix: Draw accent background for focused cell when drawFocusRing=false
            // Only apply if the cell's row or column is selected (should have highlighting)
            if (needsFocusHighlightFix && gridSelection.current?.cell) {
                const [focusCol, focusRow] = gridSelection.current.cell;
                if (col === focusCol && row === focusRow) {
                    // Check if row or column is selected
                    const rowSelected = gridSelection.rows?.hasIndex?.(row);
                    const colSelected = gridSelection.columns?.hasIndex?.(col);

                    if (rowSelected || colSelected) {
                        const accentLight = cellTheme?.accentLight || 'rgba(62, 116, 253, 0.1)';
                        ctx.save();
                        ctx.fillStyle = accentLight;
                        ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
                        ctx.restore();
                    }
                }
            }

            // Execute user's custom drawCell if provided
            if (drawCell && isFunctionRef(drawCell)) {
                // Get row data for context
                const rowData = data && data[row] ? data[row] : null;
                // Get column id to access dict key
                const columnDef = columns?.[col];
                const columnId = columnDef?.id || columnDef?.title;
                const cellData = rowData ? rowData[columnId] : null;

                // Execute the custom draw function
                // The function can return true to skip default drawing, or call drawContent() itself
                const result = executeFunction(
                    drawCell.function,
                    {
                        ctx,
                        cell,
                        theme: cellTheme,
                        rect,
                        col,
                        row,
                        hoverAmount,
                        highlighted,
                        cellData,
                        rowData,
                        drawContent
                    }
                );

                // If function returns true, it handled drawing; otherwise draw default content
                if (result !== true) {
                    drawContent();
                }
            } else {
                // No custom drawCell, just draw default content
                drawContent();
            }
        };
    }, [drawCell, drawFocusRing, gridSelection, data, columns]);

    // Create custom drawHeader callback for header rendering
    // Allows complete control over header drawing via Canvas API
    const handleDrawHeaderCustom = useMemo(() => {
        if (!drawHeader || !isFunctionRef(drawHeader)) {
            return undefined;
        }

        return (args, drawContent) => {
            const { ctx, column, theme: headerTheme, rect, columnIndex, isSelected, hoverAmount } = args;

            // Execute the custom draw function
            const result = executeFunction(
                drawHeader.function,
                {
                    ctx,
                    column,
                    theme: headerTheme,
                    rect,
                    columnIndex,
                    isSelected,
                    hoverAmount,
                    drawContent
                }
            );

            // If function returns true, it handled drawing; otherwise draw default content
            if (result !== true) {
                drawContent();
            }
        };
    }, [drawHeader]);

    // Process rowHeight - can be a number or an object with a function
    // Function format: rowHeight={"function": "getRowHeight(rowIndex)"}
    const processedRowHeight = useMemo(() => {
        // If we have hidden rows, always return a function that checks hiddenRowsSet
        if (hiddenRowsSet.size > 0) {
            return (rowIndex) => {
                // Hidden rows get height 0
                if (hiddenRowsSet.has(rowIndex)) {
                    return 0;
                }
                // Otherwise use configured height
                if (typeof rowHeight === 'number') {
                    return rowHeight;
                }
                if (rowHeight && isFunctionRef(rowHeight)) {
                    const result = executeFunction(
                        rowHeight.function,
                        { rowIndex }
                    );
                    return typeof result === 'number' ? result : 34;
                }
                return 34;
            };
        }
        // No hidden rows - use original logic
        if (typeof rowHeight === 'number') {
            return rowHeight;
        }
        if (rowHeight && isFunctionRef(rowHeight)) {
            return (rowIndex) => {
                const result = executeFunction(
                    rowHeight.function,
                    { rowIndex }
                );
                return typeof result === 'number' ? result : 34; // Default fallback
            };
        }
        return 34; // Default row height
    }, [rowHeight, hiddenRowsSet]);

    // Note: Row hover effect is handled via getRowThemeOverride (no dashed border)

    // Convert rowMarkers prop to Glide format
    const getRowMarkerFormat = () => {
        if (rowMarkers === 'none') return undefined;
        if (rowMarkers === 'number') return 'number';
        if (rowMarkers === 'checkbox') return 'checkbox';
        if (rowMarkers === 'both') return 'both';
        if (rowMarkers === 'checkbox-visible') return 'checkbox-visible';
        if (rowMarkers === 'clickable-number') return 'clickable-number';
        return undefined;
    };

    // Theme with override for fgIconHeader to ensure custom menu icons are visible
    // Native menu icons (dots, triangle) use textHeader for color, but custom icons
    // via headerIcons receive fgIconHeader. Many themes set fgIconHeader to white
    // (for use with bgIconHeader background circle), making custom icons invisible.
    // Force fgIconHeader to match textHeader so custom menu icons match native ones.
    const glideTheme = useMemo(() => {
        if (!theme) {
            return { fgIconHeader: '#000000' };
        }
        return {
            ...theme,
            // Override fgIconHeader to use textHeader (like native menu icons do)
            fgIconHeader: theme.textHeader || theme.textDark || '#000000'
        };
    }, [theme]);

    // Custom header icons for menu (hamburger, filter)
    const headerIcons = useMemo(() => ({
        hamburger: ({ fgColor }) => `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="5" y="6" width="10" height="2" rx="0.5" fill="${fgColor}"/>
            <rect x="5" y="9" width="10" height="2" rx="0.5" fill="${fgColor}"/>
            <rect x="5" y="12" width="10" height="2" rx="0.5" fill="${fgColor}"/>
        </svg>`,
        filter: ({ fgColor }) => `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 5h12l-4.5 5v5l-3-1.5V10L4 5z" stroke="${fgColor}" fill="none" stroke-width="1.5" stroke-linejoin="round"/>
        </svg>`
    }), []);

    // Keyboard handler for undo/redo shortcuts and copy flash
    const handleKeyDown = useCallback((e) => {
        const isMod = e.metaKey || e.ctrlKey;

        // Undo: Cmd+Z (Mac) or Ctrl+Z (Windows/Linux)
        if (enableUndoRedo && isMod && e.key === 'z' && !e.shiftKey) {
            e.preventDefault();
            e.stopPropagation();
            performUndo();
        }
        // Redo: Cmd+Shift+Z (Mac) or Ctrl+Shift+Z or Ctrl+Y (Windows/Linux)
        else if (enableUndoRedo && ((isMod && e.key === 'z' && e.shiftKey) || (isMod && e.key === 'y'))) {
            e.preventDefault();
            e.stopPropagation();
            performRedo();
        }
        // Copy: Cmd+C (Mac) or Ctrl+C (Windows/Linux) - trigger flash effect
        else if (isMod && e.key === 'c' && !e.shiftKey) {
            // Don't prevent default - let Glide handle the actual copy
            // Just trigger the flash effect
            if (shouldFlash('copy') && enableCopyPaste) {
                triggerCopyFlash();
            }
        }
    }, [enableUndoRedo, performUndo, performRedo, shouldFlash, enableCopyPaste, triggerCopyFlash]);

    // ========== TAB WRAPPING NAVIGATION ==========

    // Helper to calculate next/previous cell with row wrapping
    const getNextCellWithWrapping = useCallback((currentCol, currentRow, direction) => {
        // direction: 1 for Tab (forward), -1 for Shift+Tab (backward)
        const numCols = glideColumns.length;
        const numRows = localDataRef.current?.length || 0;

        if (numCols === 0 || numRows === 0) {
            return { col: currentCol, row: currentRow, wrapped: false };
        }

        let nextCol = currentCol + direction;
        let nextRow = currentRow;

        if (direction === 1) {
            // Tab forward
            if (nextCol >= numCols) {
                // Wrap to next row
                nextCol = 0;
                nextRow = currentRow + 1;
                if (nextRow >= numRows) {
                    // At last cell of grid - stay put
                    return { col: currentCol, row: currentRow, wrapped: false };
                }
            }
        } else {
            // Shift+Tab backward
            if (nextCol < 0) {
                // Wrap to previous row
                nextCol = numCols - 1;
                nextRow = currentRow - 1;
                if (nextRow < 0) {
                    // At first cell of grid - stay put
                    return { col: currentCol, row: currentRow, wrapped: false };
                }
            }
        }

        // Skip unselectable columns (recursively find next valid cell)
        if (unselectableColumns && unselectableColumns.length > 0) {
            let attempts = 0;
            const maxAttempts = numCols * numRows; // Prevent infinite loops
            while (unselectableColumns.includes(nextCol) && attempts < maxAttempts) {
                attempts++;
                nextCol += direction;
                if (direction === 1 && nextCol >= numCols) {
                    nextCol = 0;
                    nextRow++;
                    if (nextRow >= numRows) {
                        return { col: currentCol, row: currentRow, wrapped: false };
                    }
                } else if (direction === -1 && nextCol < 0) {
                    nextCol = numCols - 1;
                    nextRow--;
                    if (nextRow < 0) {
                        return { col: currentCol, row: currentRow, wrapped: false };
                    }
                }
            }
            if (attempts >= maxAttempts) {
                return { col: currentCol, row: currentRow, wrapped: false };
            }
        }

        // Skip unselectable rows
        if (unselectableRows && unselectableRows.length > 0) {
            let attempts = 0;
            const maxAttempts = numRows;
            while (unselectableRows.includes(nextRow) && attempts < maxAttempts) {
                attempts++;
                nextRow += direction;
                if (nextRow >= numRows || nextRow < 0) {
                    return { col: currentCol, row: currentRow, wrapped: false };
                }
            }
        }

        // Skip hidden rows (only if skipOnNavigation is enabled)
        if (skipOnNavigation && hiddenRowsSet.size > 0) {
            let attempts = 0;
            const maxAttempts = numRows;
            while (hiddenRowsSet.has(nextRow) && attempts < maxAttempts) {
                attempts++;
                nextRow += direction;
                if (nextRow >= numRows || nextRow < 0) {
                    return { col: currentCol, row: currentRow, wrapped: false };
                }
            }
        }

        return { col: nextCol, row: nextRow, wrapped: true };
    }, [glideColumns.length, unselectableColumns, unselectableRows, hiddenRowsSet, skipOnNavigation]);

    // Keyboard navigation handler for tab wrapping and arrow key skipping over hidden rows
    const handleKeyboardNavigation = useCallback((e) => {
        // Handle Tab wrapping
        if (tabWrapping && e.key === 'Tab') {
            const direction = e.shiftKey ? -1 : 1;
            const numCols = glideColumns.length;

            if (!gridSelection.current?.cell) return;
            const [currentCol, currentRow] = gridSelection.current.cell;

            const needsWrap = (direction === 1 && currentCol === numCols - 1) ||
                              (direction === -1 && currentCol === 0);

            if (!needsWrap) return;

            // Prevent default and handle wrap (only fires when not editing)
            e.preventDefault();
            e.stopPropagation();

            const { col: newCol, row: newRow, wrapped } = getNextCellWithWrapping(
                currentCol, currentRow, direction
            );

            if (!wrapped) return;

            const newSelection = {
                columns: CompactSelection.empty(),
                rows: CompactSelection.empty(),
                current: {
                    cell: [newCol, newRow],
                    range: { x: newCol, y: newRow, width: 1, height: 1 },
                    rangeStack: []
                }
            };
            setGridSelection(newSelection);

            if (setProps) {
                setProps({
                    selectedCell: { col: newCol, row: newRow },
                    selectedRange: {
                        startCol: newCol,
                        startRow: newRow,
                        endCol: newCol,
                        endRow: newRow
                    }
                });
            }

            if (gridRef.current) {
                gridRef.current.scrollTo(newCol, newRow);
                gridRef.current.focus();
            }
            return;
        }

        // Note: Arrow key handling for hidden rows is done via capture phase listener
        // in a separate useEffect to ensure it runs before Glide's internal handling
    }, [tabWrapping, gridSelection, glideColumns.length,
        getNextCellWithWrapping, setProps]);

    // Use capture phase on DOCUMENT to intercept Tab before the editor sees it
    // (Editor is in a portal outside our container, so container-level capture doesn't work)
    useEffect(() => {
        if (!tabWrapping) return;

        const handleTabCapture = (e) => {
            if (e.key !== 'Tab') return;

            const direction = e.shiftKey ? -1 : 1;
            const numCols = glideColumns.length;

            if (!gridSelection.current?.cell) return;
            const [currentCol, currentRow] = gridSelection.current.cell;

            const needsWrap = (direction === 1 && currentCol === numCols - 1) ||
                              (direction === -1 && currentCol === 0);

            if (!needsWrap) return;

            const numRows = localDataRef.current?.length || 0;
            let newCol, newRow;

            if (direction === 1) {
                // Tab forward - wrap to next row
                newCol = 0;
                newRow = currentRow + 1;
                if (newRow >= numRows) return; // At last cell - stay put
            } else {
                // Shift+Tab backward - wrap to previous row
                newCol = numCols - 1;
                newRow = currentRow - 1;
                if (newRow < 0) return; // At first cell - stay put
            }

            // If editor is open, let Glide handle Tab to close the editor,
            // but set a pending wrap that handleCellEdited will apply
            if (isEditorOpen) {
                pendingWrapRef.current = { col: newCol, row: newRow };
                return; // Don't prevent default - let Glide close the editor
            }

            // Not editing - prevent default and handle the wrap ourselves
            e.preventDefault();
            e.stopPropagation();

            const newSelection = {
                columns: CompactSelection.empty(),
                rows: CompactSelection.empty(),
                current: {
                    cell: [newCol, newRow],
                    range: { x: newCol, y: newRow, width: 1, height: 1 },
                    rangeStack: []
                }
            };
            setGridSelection(newSelection);

            if (setProps) {
                setProps({
                    selectedCell: { col: newCol, row: newRow },
                    selectedRange: {
                        startCol: newCol,
                        startRow: newRow,
                        endCol: newCol,
                        endRow: newRow
                    }
                });
            }

            if (gridRef.current) {
                gridRef.current.scrollTo(newCol, newRow);
                gridRef.current.focus();
                gridRef.current.updateCells([{ cell: [newCol, newRow] }]);
            }
        };

        document.addEventListener('keydown', handleTabCapture, true);
        return () => document.removeEventListener('keydown', handleTabCapture, true);
    }, [tabWrapping, glideColumns.length, gridSelection, isEditorOpen, setProps]);

    // Use capture phase on DOCUMENT to intercept Arrow keys before Glide handles them
    // This is needed because Glide's internal arrow handling happens before onKeyDown fires
    useEffect(() => {
        if (!skipOnNavigation || hiddenRowsSet.size === 0) return;

        const handleArrowCapture = (e) => {
            if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') return;

            if (!gridSelection.current?.cell) return;
            const [currentCol, currentRow] = gridSelection.current.cell;

            const numRows = localDataRef.current?.length || 0;
            const direction = e.key === 'ArrowDown' ? 1 : -1;
            let nextRow = currentRow + direction;

            // Check if the immediate next row is hidden
            if (!hiddenRowsSet.has(nextRow)) {
                // Not hidden, let Glide handle it normally
                return;
            }

            // Skip over hidden rows
            while (hiddenRowsSet.has(nextRow) && nextRow >= 0 && nextRow < numRows) {
                nextRow += direction;
            }

            // If we went out of bounds, stay put
            if (nextRow < 0 || nextRow >= numRows) {
                e.preventDefault();
                e.stopPropagation();
                return;
            }

            // We found a visible row, navigate to it
            e.preventDefault();
            e.stopPropagation();

            const newSelection = {
                columns: CompactSelection.empty(),
                rows: CompactSelection.empty(),
                current: {
                    cell: [currentCol, nextRow],
                    range: { x: currentCol, y: nextRow, width: 1, height: 1 },
                    rangeStack: []
                }
            };
            setGridSelection(newSelection);

            if (setProps) {
                setProps({
                    selectedCell: { col: currentCol, row: nextRow },
                    selectedRange: {
                        startCol: currentCol,
                        startRow: nextRow,
                        endCol: currentCol,
                        endRow: nextRow
                    }
                });
            }

            if (gridRef.current) {
                gridRef.current.scrollTo(currentCol, nextRow);
                gridRef.current.focus();
                gridRef.current.updateCells([{ cell: [currentCol, nextRow] }]);
            }
        };

        document.addEventListener('keydown', handleArrowCapture, true);
        return () => document.removeEventListener('keydown', handleArrowCapture, true);
    }, [hiddenRowsSet, gridSelection, setProps, skipOnNavigation]);

    // Filter hidden rows from gridSelection for visual display
    // This prevents selection highlighting on hidden rows while preserving
    // the full selection state internally (for when rows unhide)
    const filteredGridSelection = useMemo(() => {
        if (hiddenRowsSet.size === 0) {
            return gridSelection;
        }

        // Filter rows: remove hidden rows from the CompactSelection
        let filteredRows = gridSelection.rows;
        if (filteredRows && filteredRows.length > 0) {
            // Build a new CompactSelection excluding hidden rows
            let newRows = CompactSelection.empty();
            for (const row of filteredRows) {
                if (!hiddenRowsSet.has(row)) {
                    newRows = newRows.add(row);
                }
            }
            filteredRows = newRows;
        }

        // Filter current cell selection only if focused cell is on a hidden row
        // Range selections that span hidden rows are allowed - the hidden rows
        // won't show selection due to height 0 and transparent theme
        let filteredCurrent = gridSelection.current;
        if (filteredCurrent && filteredCurrent.cell) {
            const [cellCol, cellRow] = filteredCurrent.cell;
            if (hiddenRowsSet.has(cellRow)) {
                // Focused cell is on hidden row - find nearest visible row
                const numRows = localDataRef.current?.length || 0;
                let newRow = cellRow;

                // Search downward first
                while (hiddenRowsSet.has(newRow) && newRow < numRows) {
                    newRow++;
                }

                // If no visible row found below, search upward
                if (newRow >= numRows || hiddenRowsSet.has(newRow)) {
                    newRow = cellRow;
                    while (hiddenRowsSet.has(newRow) && newRow >= 0) {
                        newRow--;
                    }
                }

                // If we found a visible row, move focus there
                if (newRow >= 0 && newRow < numRows && !hiddenRowsSet.has(newRow)) {
                    filteredCurrent = {
                        ...filteredCurrent,
                        cell: [cellCol, newRow],
                        range: { x: cellCol, y: newRow, width: 1, height: 1 },
                        rangeStack: []
                    };
                } else {
                    // No visible rows at all - clear selection
                    filteredCurrent = undefined;
                }
            }
        }

        return {
            ...gridSelection,
            rows: filteredRows,
            current: filteredCurrent
        };
    }, [gridSelection, hiddenRowsSet]);

    // Custom getCellsForSelection that filters out hidden rows from copy operations
    const getCellsForSelectionFiltered = useCallback((selection) => {
        // selection is a Rectangle: { x, y, width, height }
        const result = [];
        for (let row = selection.y; row < selection.y + selection.height; row++) {
            // Skip hidden rows (only if skipOnCopy is enabled)
            if (skipOnCopy && hiddenRowsSet.has(row)) continue;

            const rowCells = [];
            for (let col = selection.x; col < selection.x + selection.width; col++) {
                rowCells.push(getCellContent([col, row]));
            }
            result.push(rowCells);
        }
        return result;
    }, [getCellContent, hiddenRowsSet, skipOnCopy]);

    // Container style with explicit height
    const containerStyle = {
        height: typeof height === 'number' ? `${height}px` : height,
        width: typeof width === 'number' ? `${width}px` : width,
    };

    return (
        <div id={id} ref={containerRef} style={containerStyle} className={className} onKeyDown={(enableUndoRedo || shouldFlash('copy')) ? handleKeyDown : undefined}>
            <DataEditor
                ref={gridRef}
                columns={glideColumns}
                rows={numRows}
                getCellContent={getCellContent}
                gridSelection={filteredGridSelection}
                onCellClicked={handleCellClicked}
                onCellEdited={!readonly ? handleCellEdited : undefined}
                onPaste={!readonly && enableCopyPaste ? handlePaste : undefined}
                onGridSelectionChange={handleSelectionChanged}
                onColumnResize={columnResize ? handleColumnResize : undefined}
                fillHandle={fillHandle}
                onFillPattern={fillHandle && !readonly ? handleFillPattern : undefined}
                allowedFillDirections={allowedFillDirections}
                freezeColumns={freezeColumns}
                freezeTrailingRows={freezeTrailingRows}
                rowHeight={processedRowHeight}
                headerHeight={headerHeight}
                groupHeaderHeight={groupHeaderHeight}
                smoothScrollX={smoothScrollX}
                smoothScrollY={smoothScrollY}
                verticalBorder={verticalBorder}
                fixedShadowX={fixedShadowX}
                fixedShadowY={fixedShadowY}
                drawFocusRing={drawFocusRing}
                overscrollX={overscrollX}
                overscrollY={overscrollY}
                preventDiagonalScrolling={preventDiagonalScrolling}
                scaleToRem={scaleToRem}
                rowMarkers={getRowMarkerFormat()}
                rowMarkerStartIndex={rowMarkerStartIndex}
                rowMarkerWidth={rowMarkerWidth}
                rowMarkerTheme={rowMarkerTheme}
                rowSelect={rowSelect}
                columnSelect={columnSelect}
                rangeSelect={rangeSelect}
                rowSelectionMode={rowSelectionMode}
                columnSelectionBlending={columnSelectionBlending}
                rowSelectionBlending={rowSelectionBlending}
                rangeSelectionBlending={rangeSelectionBlending}
                spanRangeBehavior={spanRangeBehavior}
                minColumnWidth={minColumnWidth}
                maxColumnWidth={maxColumnWidth}
                maxColumnAutoWidth={maxColumnAutoWidth}
                copyHeaders={copyHeaders}
                theme={glideTheme}
                headerIcons={headerIcons}
                getCellsForSelection={enableCopyPaste ? (skipOnCopy && hiddenRowsSet.size > 0 ? getCellsForSelectionFiltered : true) : undefined}
                showSearch={showSearch}
                searchValue={localSearchValue}
                onSearchClose={handleSearchClose}
                onSearchValueChange={handleSearchValueChange}
                onHeaderClicked={handleHeaderClicked}
                onHeaderContextMenu={handleHeaderContextMenu}
                onHeaderMenuClick={handleHeaderMenuClick}
                drawHeader={handleDrawHeaderCustom}
                onGroupHeaderClicked={handleGroupHeaderClicked}
                onCellContextMenu={handleContextMenu}
                onCellActivated={handleCellActivated}
                cellActivationBehavior={cellActivationBehavior}
                editOnType={editOnType}
                rangeSelectionColumnSpanning={rangeSelectionColumnSpanning}
                trapFocus={trapFocus}
                onKeyDown={(tabWrapping || hiddenRowsSet.size > 0) ? handleKeyboardNavigation : undefined}
                scrollToActiveCell={scrollToActiveCell}
                columnSelectionMode={columnSelectionMode}
                onItemHovered={handleItemHovered}
                onMouseMove={handleMouseMove}
                onCellsEdited={handleCellsEdited}
                onDelete={!readonly ? handleDelete : undefined}
                onVisibleRegionChanged={handleVisibleRegionChanged}
                onColumnMoved={columnMovable !== false ? handleColumnMoved : undefined}
                onRowMoved={rowMovable !== false ? handleRowMoved : undefined}
                highlightRegions={highlightRegions}
                trailingRowOptions={trailingRowOptions}
                onRowAppended={trailingRowOptions ? handleRowAppended : undefined}
                scrollOffsetX={scrollOffsetX}
                scrollOffsetY={scrollOffsetY}
                keybindings={keybindings}
                isDraggable={isDraggable}
                onDragStart={isDraggable ? handleDragStart : undefined}
                onDragOverCell={handleDragOverCell}
                onDrop={handleDrop}
                experimental={experimental}
                validateCell={handleValidateCell}
                coercePasteValue={handleCoercePasteValue}
                getRowThemeOverride={handleGetRowThemeOverride}
                drawCell={handleDrawCell}
                customRenderers={customRenderers}
                width="100%"
                height="100%"
            />
            {/* Header Filter Menu */}
            <HeaderMenu
                isOpen={filterMenuState.isOpen}
                onClose={handleFilterMenuClose}
                position={filterMenuState.position}
                columnIndex={filterMenuState.columnIndex}
                columnTitle={filterMenuState.columnIndex !== null && localColumns?.[filterMenuState.columnIndex]?.title}
                uniqueValues={filterMenuState.columnIndex !== null ? getUniqueColumnValues(filterMenuState.columnIndex) : []}
                selectedValues={filterMenuState.columnIndex !== null ? localFilters[filterMenuState.columnIndex] || null : null}
                onFilterChange={handleFilterChange}
                theme={theme}
                customItems={headerMenuConfig?.customItems}
                onCustomItemClick={handleCustomItemClick}
                anchorToHeader={headerMenuConfig?.anchorToHeader !== false}
                zIndex={headerMenuConfig?.zIndex}
            />
            {/* Cell Context Menu */}
            <ContextMenu
                isOpen={contextMenuState.isOpen}
                onClose={handleContextMenuClose}
                position={contextMenuState.position}
                cellInfo={{ col: contextMenuState.col, row: contextMenuState.row }}
                items={contextMenuConfig?.items}
                onItemClick={handleContextMenuItemClick}
                theme={theme}
                maxHeight={contextMenuConfig?.maxHeight}
            />
        </div>
    );
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
    unselectableColumns: [],
    unselectableRows: [],
    rowSelectOnCellClick: false,
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
    showCellFlash: false,
    allowDelete: true,
    hiddenRows: [],
    hiddenRowsConfig: {},
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
     */
    freezeTrailingRows: PropTypes.number,

    /**
     * Height of column group headers in pixels.
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
     * How column selection blends with other selections. Default: 'exclusive'
     */
    columnSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How row selection blends with other selections. Default: 'exclusive'
     */
    rowSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How range selection blends with other selections. Default: 'exclusive'
     */
    rangeSelectionBlending: PropTypes.oneOf(['exclusive', 'mixed']),

    /**
     * How to handle spans in range selection.
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

    /**
     * Array of row indices to hide. Hidden rows:
     * - Have height 0 (visually collapsed)
     * - Have fully transparent theme (invisible row marker and cells)
     * - Are excluded from visual selection highlighting
     * - Preserve their original row numbers (unlike filtering)
     * - Keep their selection state internally (reappears when unhidden)
     *
     * Useful for tree view collapse/expand functionality where child rows
     * need to hide/show while maintaining their identity and selection state.
     */
    hiddenRows: PropTypes.arrayOf(PropTypes.number),

    /**
     * Configuration object controlling how hidden rows affect grid operations.
     * All options default to true, meaning hidden rows are skipped by default.
     * Set specific options to false to include hidden rows in those operations.
     */
    hiddenRowsConfig: PropTypes.shape({
        /** Skip hidden rows during copy operations (Cmd/Ctrl+C). Default: true */
        skipOnCopy: PropTypes.bool,
        /** Skip hidden rows during paste operations (Cmd/Ctrl+V). Default: true */
        skipOnPaste: PropTypes.bool,
        /** Skip hidden rows during fill handle drag operations. Default: true */
        skipOnFill: PropTypes.bool,
        /** Skip hidden rows during delete operations (Delete/Backspace). Default: true */
        skipOnDelete: PropTypes.bool,
        /** Skip hidden rows during keyboard navigation (Tab, Arrow keys). Default: true */
        skipOnNavigation: PropTypes.bool,
    }),

    /**
     * When True, clicking on any cell will select its entire row. Works with
     * rowSelect ('single' or 'multi') and respects rowSelectionMode for modifier
     * key behavior (Ctrl/Cmd for toggle, Shift for range). Also respects
     * rowSelectionBlending and unselectableRows. Default: False.
     */
    rowSelectOnCellClick: PropTypes.bool,

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
     * Maximum width for auto-sized columns.
     */
    maxColumnAutoWidth: PropTypes.number,

    /**
     * Row marker style. Options: 'none', 'number', 'checkbox', 'both', 'checkbox-visible', 'clickable-number'
     */
    rowMarkers: PropTypes.oneOf(['none', 'number', 'checkbox', 'both', 'checkbox-visible', 'clickable-number']),

    /**
     * Starting index for row numbers. Default: 1
     */
    rowMarkerStartIndex: PropTypes.number,

    /**
     * Width of the row marker column in pixels.
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
    contextMenu: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        screenX: PropTypes.number,
        screenY: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Configuration for built-in cell context menu.
     * Provide an array of menu items to display when right-clicking a cell.
     * maxHeight constrains the menu height (e.g., 100 or "100px"). Only px units supported.
     * Example: { "items": [{"id": "edit", "label": "Edit"}], "maxHeight": "150px" }
     */
    contextMenuConfig: PropTypes.shape({
        items: PropTypes.arrayOf(PropTypes.shape({
            id: PropTypes.string.isRequired,
            label: PropTypes.string.isRequired,
            icon: PropTypes.string,
            dividerAfter: PropTypes.bool,
            disabled: PropTypes.bool,
            /** Action to execute when item is clicked.
             * Built-in (string): 'copyClickedCell', 'copySelection', 'pasteAtClickedCell', 'pasteAtSelection'
             * Clientside function (object): {function: 'myFunc(col, row, cellData, rowData, selection, columns, data, utils)'}
             */
            action: PropTypes.oneOfType([
                PropTypes.string,
                PropTypes.shape({
                    function: PropTypes.string
                })
            ])
        })),
        maxHeight: PropTypes.oneOfType([PropTypes.number, PropTypes.string])
    }),

    /**
     * Information about the last clicked cell context menu item.
     * Format: {"col": 0, "row": 1, "itemId": "edit", "timestamp": 1234567890}
     */
    contextMenuItemClicked: PropTypes.shape({
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
     */
    highlightRegions: PropTypes.arrayOf(PropTypes.shape({
        color: PropTypes.string.isRequired,
        range: PropTypes.shape({
            x: PropTypes.number.isRequired,
            y: PropTypes.number.isRequired,
            width: PropTypes.number.isRequired,
            height: PropTypes.number.isRequired
        }).isRequired
    })),

    // ========== TRAILING ROW (ADD ROW) ==========

    /**
     * Configuration options for the trailing row used to add new rows.
     * When trailingRowOptions is provided, a blank row appears at the bottom of the grid.
     * Clicking on this row triggers the rowAppended callback.
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
     * Initial horizontal scroll offset in pixels.
     */
    scrollOffsetX: PropTypes.number,

    /**
     * Initial vertical scroll offset in pixels.
     */
    scrollOffsetY: PropTypes.number,

    // ========== UNDO/REDO ==========

    /**
     * Enable undo/redo functionality.
     * When enabled, cell edits can be undone/redone using Cmd+Z/Cmd+Shift+Z (Mac)
     * or Ctrl+Z/Ctrl+Y (Windows/Linux), or programmatically via undoRedoAction.
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

    // ========== ADVANCED PROPS ==========

    /**
     * Customize keyboard shortcuts.
     */
    keybindings: PropTypes.object,

    /**
     * Makes the grid draggable for external drag-and-drop.
     */
    isDraggable: PropTypes.oneOfType([
        PropTypes.bool,
        PropTypes.oneOf(['header', 'cell'])
    ]),

    /**
     * Information about drag start events.
     */
    dragStarted: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about external drag-over events.
     */
    dragOverCell: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Information about external drop events.
     */
    droppedOnCell: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
        timestamp: PropTypes.number
    }),

    /**
     * Experimental options.
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
     * **Setup**: Create `assets/dashGlideGridFunctions.js`:
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
     * **Setup**: Create `assets/dashGlideGridFunctions.js`:
     * ```javascript
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
     * **Setup**: Create `assets/dashGlideGridFunctions.js`:
     * ```javascript
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
     * **Setup**: Create `assets/dashGlideGridFunctions.js`:
     * ```javascript
     * dggfuncs.drawCircularWell = function(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent) {
     *     // Skip first column (row labels)
     *     if (col === 0) {
     *         drawContent();  // Use default rendering
     *         return true;
     *     }
     *
     *     // Draw circular well
     *     const centerX = rect.x + rect.width / 2;
     *     const centerY = rect.y + rect.height / 2;
     *     const radius = Math.min(rect.width, rect.height) / 2 - 4;
     *
     *     ctx.beginPath();
     *     ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
     *     ctx.fillStyle = highlighted ? theme.bgCellMedium : theme.bgCell;
     *     ctx.fill();
     *     ctx.strokeStyle = theme.borderColor;
     *     ctx.lineWidth = 1;
     *     ctx.stroke();
     *
     *     return true;  // We handled the drawing
     * };
     * ```
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
     * **Return values**:
     * - `true`: Custom drawing complete, skip default rendering
     * - `false` or `undefined`: Draw default content after custom drawing
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
     * - menuIcon: Icon style for the menu dropdown ("chevron" | "hamburger" | "dots")
     * - customItems: Array of custom menu items with onClick handlers
     * - filterActiveColor: Color for header when filter is active (default: theme accentColor)
     * - anchorToHeader: Whether menu stays anchored to header when page scrolls (default: true)
     *
     * Example:
     * ```
     * headerMenuConfig={
     *     "menuIcon": "hamburger",
     *     "filterActiveColor": "#2563eb",
     *     "anchorToHeader": true,
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
        anchorToHeader: PropTypes.bool,
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

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};

export default GlideGrid;
