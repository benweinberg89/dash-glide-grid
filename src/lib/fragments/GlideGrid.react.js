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
import 'react-responsive-carousel/lib/styles/carousel.min.css';
import { executeFunction, isFunctionRef } from '../utils/functionParser';
import HeaderMenu from './HeaderMenu.react';

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
            !c.isMatch?.({ data: { kind: 'range-cell' } })
    ),
    DropdownCellRenderer,
    MultiSelectCellRenderer,
    createTagsCellRenderer(),
    createUserProfileCellRenderer(),
    createSpinnerCellRenderer(),
    createStarCellRenderer(),
    createDatePickerCellRenderer(),
    createRangeCellRenderer(),
];

/**
 * Draw hamburger icon (three horizontal lines) for header menu
 */
function drawHamburgerIcon(ctx, bounds, theme) {
    const { x, y, width, height } = bounds;
    const centerX = x + width / 2;
    const centerY = y + height / 2;
    const lineWidth = 10;
    const lineHeight = 2;
    const gap = 3;

    ctx.fillStyle = theme.textHeader || theme.textDark || '#000';

    // Top bar
    ctx.fillRect(centerX - lineWidth / 2, centerY - gap - lineHeight / 2, lineWidth, lineHeight);
    // Middle bar
    ctx.fillRect(centerX - lineWidth / 2, centerY - lineHeight / 2, lineWidth, lineHeight);
    // Bottom bar
    ctx.fillRect(centerX - lineWidth / 2, centerY + gap - lineHeight / 2, lineWidth, lineHeight);
}

/**
 * Draw dots icon (three vertical dots) for header menu
 */
function drawDotsIcon(ctx, bounds, theme) {
    const { x, y, width, height } = bounds;
    const centerX = x + width / 2;
    const centerY = y + height / 2;
    const dotRadius = 1.5;
    const gap = 4;

    ctx.fillStyle = theme.textHeader || theme.textDark || '#000';

    // Top dot
    ctx.beginPath();
    ctx.arc(centerX, centerY - gap, dotRadius, 0, Math.PI * 2);
    ctx.fill();
    // Middle dot
    ctx.beginPath();
    ctx.arc(centerX, centerY, dotRadius, 0, Math.PI * 2);
    ctx.fill();
    // Bottom dot
    ctx.beginPath();
    ctx.arc(centerX, centerY + gap, dotRadius, 0, Math.PI * 2);
    ctx.fill();
}

/**
 * Helper function to auto-detect cell type from simple JavaScript values
 */
function autoDetectCellType(value) {
    if (value === null || value === undefined) {
        return {
            kind: GridCellKind.Text,
            data: '',
            allowOverlay: false,
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
    ];
    if (customCellKinds.includes(cellObj.kind)) {
        // Read-only cell types that don't need overlay editors
        const readOnlyCellKinds = ['button-cell', 'user-profile-cell', 'spinner-cell'];
        const result = {
            kind: GridCellKind.Custom,
            allowOverlay: !readOnlyCellKinds.includes(cellObj.kind) && cellObj.allowOverlay !== false,
            copyData: cellObj.copyData || cellObj.title || cellObj.name || '',
            data: {
                kind: cellObj.kind,
                ...cellObj
            }
        };

        // Add optional properties if present
        if (cellObj.readonly !== undefined) {
            result.readonly = cellObj.readonly;
        }
        if (cellObj.themeOverride) {
            result.themeOverride = cellObj.themeOverride;
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
        result.displayData = cellObj.displayData || String(cellObj.data || '');
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

    // Handle specific cell type properties
    if (cellKind === GridCellKind.Uri && cellObj.data) {
        result.data = cellObj.data;
    }
    if (cellKind === GridCellKind.Image && cellObj.data) {
        result.data = Array.isArray(cellObj.data) ? cellObj.data : [cellObj.data];
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
        selectionColumnMin,
        unselectableColumns,
        unselectableRows,
        hoverRow,
        cellActivationBehavior,
        editOnType,
        rangeSelectionColumnSpanning,
        trapFocus,
        scrollToActiveCell,
        columnSelectionMode,
        enableUndoRedo,
        maxUndoSteps,
        undoRedoAction,
        editorScrollBehavior,
        redrawTrigger,
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

    // Local state for column filters (synced with Dash prop)
    const [localFilters, setLocalFilters] = useState(columnFilters || {});

    // State for the filter menu
    const [filterMenuState, setFilterMenuState] = useState({
        isOpen: false,
        columnIndex: null,
        position: null
    });

    // State for row hover effect
    const [hoveredRow, setHoveredRow] = useState(null);

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

    // ========== UNDO/REDO STATE ==========
    // Undo/redo history stacks
    const [undoStack, setUndoStack] = useState([]);  // Array of edit batches
    const [redoStack, setRedoStack] = useState([]);  // Array of undone batches

    // Refs for undo/redo tracking (to avoid stale closures and prevent circular updates)
    const isApplyingUndoRedoRef = useRef(false);     // Prevent tracking edits during undo/redo
    const batchTimeoutRef = useRef(null);            // For batching rapid edits
    const currentBatchRef = useRef([]);              // Current batch of edits being collected
    const lastUndoRedoActionRef = useRef(null);      // Track last processed undoRedoAction

    // Keep refs in sync with state
    useEffect(() => {
        localDataRef.current = localData;
    }, [localData]);

    useEffect(() => {
        localColumnsRef.current = localColumns;
    }, [localColumns]);

    // Sync local data with props when props change from outside (but not from our own updates)
    useEffect(() => {
        // If the incoming data is the same as what we just sent, ignore it
        if (lastSentData.current && JSON.stringify(data) === JSON.stringify(lastSentData.current)) {
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
        if (cellValue === null || cellValue === undefined) {
            return '(Blank)';
        }
        if (typeof cellValue === 'object' && cellValue.kind) {
            // Cell object - extract data
            const data = cellValue.data;
            if (data === null || data === undefined || data === '') {
                return '(Blank)';
            }
            return data;
        }
        if (cellValue === '') {
            return '(Blank)';
        }
        return cellValue;
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
                    const valA = localData[a]?.[columnId];
                    const valB = localData[b]?.[columnId];

                    // Handle null/undefined
                    if (valA == null && valB == null) continue;
                    if (valA == null) return direction === 'asc' ? 1 : -1;
                    if (valB == null) return direction === 'asc' ? -1 : 1;

                    // Compare based on type
                    let comparison = 0;
                    if (typeof valA === 'number' && typeof valB === 'number') {
                        comparison = valA - valB;
                    } else if (typeof valA === 'boolean' && typeof valB === 'boolean') {
                        comparison = (valA === valB) ? 0 : (valA ? -1 : 1);
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
    }, [localData, localColumns, localFilters, sortable, localSortColumns, getCellDisplayValue]);

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

    // Custom renderers including button cell with click handler
    const customRenderers = useMemo(() => [
        ...staticRenderers,
        createButtonCellRenderer(buttonClickHandler)
    ], [buttonClickHandler]);

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

    // Detect editor close via MutationObserver (for Escape/click-outside)
    useEffect(() => {
        if (!isEditorOpen) return;

        const portal = document.getElementById('portal');
        if (!portal) return;

        const observer = new MutationObserver((mutations) => {
            // Check if editor overlay was removed
            const hasEditorChild = portal.querySelector('[class*="overlay-editor"], [class*="gdg-"]');
            if (!hasEditorChild && portal.children.length === 0) {
                setIsEditorOpen(false);
            }
        });

        observer.observe(portal, { childList: true, subtree: true });
        return () => observer.disconnect();
    }, [isEditorOpen]);

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
                // 1. Dispatch to input (closes react-select dropdown)
                const input = portal.querySelector('input, textarea, [contenteditable]');
                if (input) {
                    input.dispatchEvent(escapeEvent);
                }

                // 2. Dispatch to overlay container
                if (portal.firstElementChild) {
                    portal.firstElementChild.dispatchEvent(escapeEvent);
                }
            }

            // 3. Dispatch to document
            document.dispatchEvent(escapeEvent);

            // 4. Focus the grid to trigger blur on editor
            if (gridRef.current) {
                gridRef.current.focus();
            }

            // MutationObserver will detect when overlay closes and update isEditorOpen
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
                    textHeader: filterActiveColor
                };
            }

            return {
                title: title,
                id: col.id || col.title,
                width: col.width || 150,
                icon: col.icon,
                overlayIcon: col.overlayIcon,
                hasMenu: showMenu,
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

        return cellResult;
    }, [localData, localColumns, sortedIndices]);

    // Handle cell clicks
    const handleCellClicked = useCallback((cell) => {
        if (setProps) {
            setProps({
                cellClicked: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                },
                nClicks: (nClicks || 0) + 1
            });
        }
    }, [setProps, nClicks]);

    // Handle cell edits
    const handleCellEdited = useCallback((cell, newValue) => {
        setIsEditorOpen(false);
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
                // For custom cells, newValue.data IS the cell value
                // (e.g., {kind: "tags-cell", tags: [...], possibleTags: [...]})
                newCellValue = newValue.data;
            } else {
                // Update the data property while preserving the object structure
                newCellValue = { ...oldValue, data: newValue.data };
            }
        } else {
            // Simple value - extract the data from the GridCell
            newCellValue = newValue.data;
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

        // Sync with Dash (report actualRow so it matches data array indices)
        setProps({
            data: newData,
            cellEdited: {
                col: col,
                row: actualRow,
                value: newValue.kind === GridCellKind.Custom ? newValue.data : newValue.data,
                timestamp: Date.now()
            }
        });

        return true;
    }, [setProps, readonly, sortedIndices, addEditToBatch]);

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

        // Apply pasted data to the grid
        for (let i = 0; i < values.length; i++) {
            const displayRow = targetRow + i;
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

                // Preserve format (object vs simple value) and convert pasted string to appropriate type
                let newCellValue;
                if (oldValue && typeof oldValue === 'object' && oldValue.kind) {
                    // Cell object - update data property with type conversion
                    if (oldValue.kind === 'number') {
                        const num = parseFloat(pastedValue);
                        newCellValue = { ...oldValue, data: isNaN(num) ? 0 : num };
                    } else if (oldValue.kind === 'boolean') {
                        newCellValue = { ...oldValue, data: pastedValue.toLowerCase() === 'true' };
                    } else {
                        newCellValue = { ...oldValue, data: pastedValue };
                    }
                } else {
                    // Simple value - try to preserve type
                    if (typeof oldValue === 'number') {
                        const num = parseFloat(pastedValue);
                        newCellValue = isNaN(num) ? 0 : num;
                    } else if (typeof oldValue === 'boolean') {
                        newCellValue = pastedValue.toLowerCase() === 'true';
                    } else {
                        newCellValue = pastedValue;
                    }
                }

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
                value: `Pasted ${values.length}x${values[0]?.length || 0} range`,
                timestamp: Date.now()
            }
        });

        return true;
    }, [setProps, readonly, sortedIndices, addEditToBatch]);

    // Handle selection changes
    const handleSelectionChanged = useCallback((selection) => {
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
    }, [setProps, selectionColumnMin, unselectableColumns, unselectableRows]);

    // Handle column resize
    const handleColumnResize = useCallback((column, newSize, columnIndex) => {
        if (!setProps || !localColumns) return;

        // Update local columns immediately for visual feedback
        const newColumns = localColumns.map((col, idx) => {
            if (idx === columnIndex) {
                return { ...col, width: newSize };
            }
            return col;
        });

        setLocalColumns(newColumns);

        // Send new widths to Dash
        const newWidths = newColumns.map(col => col.width || 150);
        setProps({
            columnWidths: newWidths
        });
    }, [setProps, localColumns]);

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
    }, [setProps, readonly, sortedIndices, addEditToBatch]);

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

    // Custom header drawing callback for menu icon customization
    const handleDrawHeader = useCallback((args, drawContent) => {
        const { ctx, column, theme: headerTheme, menuBounds, hoverAmount, isSelected, hasSelectedCell } = args;

        // First, draw the default header content
        drawContent();

        // If no custom menu icon or column has no menu, we're done
        const menuIcon = headerMenuConfig?.menuIcon;
        if (!menuIcon || menuIcon === 'chevron' || !column.hasMenu) {
            return;
        }

        // Only draw custom icon when hovering (hoverAmount > 0)
        // This matches Glide's default behavior of fading in the menu icon
        if (hoverAmount <= 0) {
            return;
        }

        // Determine base background color based on selection state
        // Priority: selected > normal
        let bgBase;
        if (isSelected || hasSelectedCell) {
            bgBase = headerTheme.bgHeaderHasFocus || headerTheme.bgHeader || '#f7f7f8';
        } else {
            bgBase = headerTheme.bgHeader || '#f7f7f8';
        }
        const bgHovered = headerTheme.bgHeaderHovered || bgBase;

        // Simple color interpolation (works for hex colors)
        const interpolateColor = (c1, c2, t) => {
            const parse = (c) => {
                // Handle rgb() format
                if (c.startsWith('rgb')) {
                    const match = c.match(/\d+/g);
                    return { r: parseInt(match[0]), g: parseInt(match[1]), b: parseInt(match[2]) };
                }
                // Handle hex format
                const hex = c.replace('#', '');
                return {
                    r: parseInt(hex.substr(0, 2), 16),
                    g: parseInt(hex.substr(2, 2), 16),
                    b: parseInt(hex.substr(4, 2), 16)
                };
            };
            const p1 = parse(c1);
            const p2 = parse(c2);
            const r = Math.round(p1.r + (p2.r - p1.r) * t);
            const g = Math.round(p1.g + (p2.g - p1.g) * t);
            const b = Math.round(p1.b + (p2.b - p1.b) * t);
            return `rgb(${r},${g},${b})`;
        };

        // Get interpolated background color based on hover amount
        const bgColor = interpolateColor(bgBase, bgHovered, hoverAmount);

        // Clear the menu area with the interpolated background color
        ctx.fillStyle = bgColor;
        ctx.fillRect(menuBounds.x, menuBounds.y, menuBounds.width, menuBounds.height);

        // Save alpha and set for icon fade-in
        const prevAlpha = ctx.globalAlpha;
        ctx.globalAlpha = hoverAmount;

        // Draw the custom icon
        if (menuIcon === 'hamburger') {
            drawHamburgerIcon(ctx, menuBounds, headerTheme);
        } else if (menuIcon === 'dots') {
            drawDotsIcon(ctx, menuBounds, headerTheme);
        }

        // Restore alpha
        ctx.globalAlpha = prevAlpha;
    }, [headerMenuConfig]);

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
    const handleCellContextMenu = useCallback((cell, event) => {
        if (setProps) {
            setProps({
                cellContextMenu: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

    // Handle cell activation (Enter, Space, or double-click)
    const handleCellActivated = useCallback((cell) => {
        setIsEditorOpen(true);
        if (setProps) {
            setProps({
                cellActivated: {
                    col: cell[0],
                    row: cell[1],
                    timestamp: Date.now()
                }
            });
        }
    }, [setProps]);

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
    }, [setProps, editorScrollBehavior, isEditorOpen]);

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
    }, [getRowThemeOverride, data, hoverRow, hoveredRow, theme?.bgRowHovered]);

    // Create drawCell callback for custom cell rendering
    // Allows complete control over cell drawing via Canvas API
    const handleDrawCell = useMemo(() => {
        if (!drawCell || !isFunctionRef(drawCell)) {
            return undefined;
        }

        return (args, drawContent) => {
            const { ctx, cell, theme: cellTheme, rect, col, row, hoverAmount, highlighted } = args;

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
        };
    }, [drawCell, data]);

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
    }, [rowHeight]);

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

    // Theme is passed directly (camelCase)
    const glideTheme = theme;

    // Keyboard handler for undo/redo shortcuts
    const handleKeyDown = useCallback((e) => {
        if (!enableUndoRedo) return;

        const isMod = e.metaKey || e.ctrlKey;

        // Undo: Cmd+Z (Mac) or Ctrl+Z (Windows/Linux)
        if (isMod && e.key === 'z' && !e.shiftKey) {
            e.preventDefault();
            e.stopPropagation();
            performUndo();
        }
        // Redo: Cmd+Shift+Z (Mac) or Ctrl+Shift+Z or Ctrl+Y (Windows/Linux)
        else if ((isMod && e.key === 'z' && e.shiftKey) || (isMod && e.key === 'y')) {
            e.preventDefault();
            e.stopPropagation();
            performRedo();
        }
    }, [enableUndoRedo, performUndo, performRedo]);

    // Container style with explicit height
    const containerStyle = {
        height: typeof height === 'number' ? `${height}px` : height,
        width: typeof width === 'number' ? `${width}px` : width,
    };

    return (
        <div id={id} ref={containerRef} style={containerStyle} className={className} onKeyDown={enableUndoRedo ? handleKeyDown : undefined}>
            <DataEditor
                ref={gridRef}
                columns={glideColumns}
                rows={numRows}
                getCellContent={getCellContent}
                gridSelection={gridSelection}
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
                getCellsForSelection={enableCopyPaste}
                showSearch={showSearch}
                searchValue={localSearchValue}
                onSearchClose={handleSearchClose}
                onSearchValueChange={handleSearchValueChange}
                onHeaderClicked={handleHeaderClicked}
                onHeaderContextMenu={handleHeaderContextMenu}
                onHeaderMenuClick={handleHeaderMenuClick}
                drawHeader={handleDrawHeaderCustom || (headerMenuConfig?.menuIcon && headerMenuConfig.menuIcon !== 'chevron' ? handleDrawHeader : undefined)}
                onGroupHeaderClicked={handleGroupHeaderClicked}
                onCellContextMenu={handleCellContextMenu}
                onCellActivated={handleCellActivated}
                cellActivationBehavior={cellActivationBehavior}
                editOnType={editOnType}
                rangeSelectionColumnSpanning={rangeSelectionColumnSpanning}
                trapFocus={trapFocus}
                scrollToActiveCell={scrollToActiveCell}
                columnSelectionMode={columnSelectionMode}
                onItemHovered={handleItemHovered}
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
    scrollToActiveCell: true,
    columnSelectionMode: 'auto',
    enableUndoRedo: false,
    maxUndoSteps: 50,
    canUndo: false,
    canRedo: false,
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
     * Format: {"col": 0, "row": 1, "timestamp": 1234567890}
     */
    cellContextMenu: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number,
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
