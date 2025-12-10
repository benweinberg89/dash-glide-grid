/**
 * Custom validation and formatting functions for Dash Glide Grid
 *
 * This file demonstrates the namespace pattern (same as Dash AG Grid).
 * Functions defined here can be referenced in Python using:
 *   validateCell={"function": "functionName(cell, newValue)"}
 *
 * Available parameters in validateCell functions:
 *   - cell: [col, row] array
 *   - newValue: The GridCell object with the new value
 *   - col: Column index (number)
 *   - row: Row index (number)
 *
 * Return values for validateCell:
 *   - false: Reject the edit (visual feedback shown)
 *   - true: Accept the edit
 *   - GridCell object: Coerce/transform the value
 */

// Initialize the namespace (same pattern as AG Grid)
var dggfuncs = window.dashGlideGridFunctions =
    window.dashGlideGridFunctions || {};

// ============================================================
// VALIDATION FUNCTIONS
// ============================================================

/**
 * Validate that a number is positive (> 0)
 */
dggfuncs.isPositive = function(cell, newValue) {
    if (newValue.kind === 'number') {
        return newValue.data > 0;
    }
    return true;  // Accept non-number cells
};

/**
 * Validate that a number is within a range (0-100)
 */
dggfuncs.isPercentage = function(cell, newValue) {
    if (newValue.kind === 'number') {
        const value = newValue.data;
        if (value < 0 || value > 100) {
            return false;  // Reject
        }
    }
    return true;
};

/**
 * Validate age is between 0 and 120
 */
dggfuncs.validateAge = function(cell, newValue) {
    if (newValue.kind === 'number') {
        const age = newValue.data;
        if (age < 0 || age > 120) {
            return false;
        }
    }
    return true;
};

/**
 * Validate email format (basic check)
 */
dggfuncs.validateEmail = function(cell, newValue) {
    if (newValue.kind === 'text') {
        const email = newValue.data;
        if (!email.includes('@') || !email.includes('.')) {
            return false;
        }
    }
    return true;
};

/**
 * Validate and coerce email to lowercase
 */
dggfuncs.validateAndLowercaseEmail = function(cell, newValue) {
    if (newValue.kind === 'text') {
        const email = newValue.data;
        // Check format
        if (!email.includes('@') || !email.includes('.')) {
            return false;
        }
        // Coerce to lowercase
        return {
            kind: 'text',
            data: email.toLowerCase(),
            displayData: email.toLowerCase(),
            allowOverlay: true
        };
    }
    return true;
};

/**
 * Validate text is not empty
 */
dggfuncs.notEmpty = function(cell, newValue) {
    if (newValue.kind === 'text') {
        return newValue.data.trim().length > 0;
    }
    return true;
};

/**
 * Validate text has minimum length
 */
dggfuncs.minLength3 = function(cell, newValue) {
    if (newValue.kind === 'text') {
        return newValue.data.length >= 3;
    }
    return true;
};

/**
 * Coerce text to uppercase
 */
dggfuncs.toUppercase = function(cell, newValue) {
    if (newValue.kind === 'text') {
        return {
            kind: 'text',
            data: newValue.data.toUpperCase(),
            displayData: newValue.data.toUpperCase(),
            allowOverlay: true
        };
    }
    return true;
};

/**
 * Round numbers to 2 decimal places
 */
dggfuncs.roundTo2Decimals = function(cell, newValue) {
    if (newValue.kind === 'number') {
        const rounded = Math.round(newValue.data * 100) / 100;
        return {
            kind: 'number',
            data: rounded,
            displayData: rounded.toString(),
            allowOverlay: true
        };
    }
    return true;
};

/**
 * Column-aware validation - validates based on which column is being edited
 */
dggfuncs.validateByColumn = function(cell, newValue) {
    const [col, row] = cell;

    // Column 0: Name - must not be empty
    if (col === 0) {
        if (newValue.kind === 'text') {
            return newValue.data.trim().length > 0;
        }
    }

    // Column 1: Age - must be 0-120
    if (col === 1) {
        if (newValue.kind === 'number') {
            const age = newValue.data;
            return age >= 0 && age <= 120;
        }
    }

    // Column 2: Email - must contain @
    if (col === 2) {
        if (newValue.kind === 'text') {
            return newValue.data.includes('@');
        }
    }

    // Column 3: Score - must be 0-100, round to integer
    if (col === 3) {
        if (newValue.kind === 'number') {
            const score = newValue.data;
            if (score < 0 || score > 100) {
                return false;
            }
            // Coerce to integer
            return {
                kind: 'number',
                data: Math.round(score),
                displayData: Math.round(score).toString(),
                allowOverlay: true
            };
        }
    }

    return true;  // Accept all other cases
};

// ============================================================
// PASTE COERCION FUNCTIONS
// ============================================================

/**
 * Parse pasted values with smart type detection based on TARGET cell type
 */
dggfuncs.smartPaste = function(val, cell) {
    const trimmed = val.trim().toLowerCase();

    // Boolean coercion - only when pasting INTO a boolean cell
    if (cell.kind === 'boolean') {
        if (trimmed === 'true' || trimmed === 'yes' || trimmed === '1') {
            return { kind: 'boolean', data: true, allowOverlay: true };
        }
        if (trimmed === 'false' || trimmed === 'no' || trimmed === '0') {
            return { kind: 'boolean', data: false, allowOverlay: true };
        }
        // Keep original cell if not a valid boolean string
        return cell;
    }

    // Number coercion - only when pasting INTO a number cell
    if (cell.kind === 'number') {
        const num = parseFloat(val);
        if (!isNaN(num)) {
            return {
                kind: 'number',
                data: num,
                displayData: num.toString(),
                allowOverlay: true
            };
        }
        // Keep original cell if not a valid number
        return cell;
    }

    // Default: return undefined to use default parsing
    return undefined;
};

// ============================================================
// DEBUGGING HELPER
// ============================================================

/**
 * Log the parameters to console and accept the edit
 * Useful for understanding what data is available
 */
dggfuncs.debugValidation = function(cell, newValue) {
    console.log('[GlideGrid Validation Debug]', {
        cell: cell,
        newValue: newValue,
        col: cell[0],
        row: cell[1],
        kind: newValue.kind,
        data: newValue.data
    });
    return true;  // Accept all edits
};

// ============================================================
// ROW THEME OVERRIDE FUNCTIONS (Conditional Row Styling)
// ============================================================

/**
 * Color rows based on a status column value
 * Use with: getRowThemeOverride={"function": "rowThemeByStatus(row, rowData)"}
 */
dggfuncs.rowThemeByStatus = function(row, rowData) {
    if (!rowData) return undefined;

    // Status is in column 4 (index 4): Name, Age, Email, Score, Status
    const status = rowData[4];

    // Get cell value - handle both simple values and cell objects
    const getValue = (cell) => {
        if (cell && typeof cell === 'object' && 'data' in cell) {
            return cell.data;
        }
        return cell;
    };

    const statusValue = getValue(status);

    if (statusValue === 'error' || statusValue === 'failed') {
        return {
            bgCell: 'rgba(255, 82, 82, 0.15)',  // Light red
            textDark: '#c62828'
        };
    }
    if (statusValue === 'success' || statusValue === 'completed') {
        return {
            bgCell: 'rgba(76, 175, 80, 0.15)',  // Light green
            textDark: '#2e7d32'
        };
    }
    if (statusValue === 'pending' || statusValue === 'in_progress') {
        return {
            bgCell: 'rgba(33, 150, 243, 0.15)',  // Light blue
            textDark: '#1565c0'
        };
    }
    if (statusValue === 'warning') {
        return {
            bgCell: 'rgba(255, 193, 7, 0.15)',  // Light yellow
            textDark: '#f57f17'
        };
    }

    return undefined;  // Default theme
};

/**
 * Color rows based on a numeric value (e.g., score)
 * Rows with score >= 90 are green, < 50 are red
 */
dggfuncs.rowThemeByScore = function(row, rowData) {
    if (!rowData) return undefined;

    // Assume score is in column 3 (index 3)
    const scoreCell = rowData[3];

    // Get numeric value
    const getValue = (cell) => {
        if (cell && typeof cell === 'object' && 'data' in cell) {
            return cell.data;
        }
        return cell;
    };

    const score = getValue(scoreCell);

    if (typeof score !== 'number') return undefined;

    if (score >= 90) {
        return { bgCell: 'rgba(76, 175, 80, 0.15)' };  // Green
    }
    if (score >= 70) {
        return { bgCell: 'rgba(33, 150, 243, 0.1)' };  // Light blue
    }
    if (score < 50) {
        return { bgCell: 'rgba(255, 82, 82, 0.15)' };  // Red
    }

    return undefined;
};

/**
 * Alternate row coloring (zebra stripes)
 */
dggfuncs.zebraStripes = function(row, rowData) {
    if (row % 2 === 0) {
        return { bgCell: 'rgba(0, 0, 0, 0.02)' };
    }
    return undefined;
};

/**
 * Highlight rows where a specific column has a value
 * Useful for highlighting rows with errors or special conditions
 */
dggfuncs.highlightNonEmpty = function(row, rowData) {
    if (!rowData) return undefined;

    // Check if column 4 (index 4) has a value
    const cell = rowData[4];
    const getValue = (c) => {
        if (c && typeof c === 'object' && 'data' in c) {
            return c.data;
        }
        return c;
    };

    const value = getValue(cell);

    if (value && value !== '' && value !== null) {
        return { bgCell: 'rgba(255, 193, 7, 0.2)' };  // Yellow highlight
    }

    return undefined;
};

/**
 * Multi-condition row styling
 * Combines multiple conditions for complex formatting
 */
dggfuncs.multiConditionTheme = function(row, rowData) {
    if (!rowData) return undefined;

    const getValue = (cell) => {
        if (cell && typeof cell === 'object' && 'data' in cell) {
            return cell.data;
        }
        return cell;
    };

    // Example: Check if age (col 1) is out of valid range
    const age = getValue(rowData[1]);
    if (typeof age === 'number' && (age < 0 || age > 120)) {
        return {
            bgCell: 'rgba(255, 82, 82, 0.2)',
            textDark: '#b71c1c'
        };
    }

    // Example: Check if score (col 3) is perfect
    const score = getValue(rowData[3]);
    if (score === 100) {
        return {
            bgCell: 'rgba(76, 175, 80, 0.2)',
            textDark: '#1b5e20'
        };
    }

    return undefined;
};

// ============================================================
// VALUE FORMATTER FUNCTIONS
// ============================================================

/**
 * Format numbers as currency (USD)
 * Usage: valueFormatter={"function": "formatCurrency(value)"}
 */
dggfuncs.formatCurrency = function(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return value;
    }
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(value);
};

/**
 * Format numbers as percentage
 * Usage: valueFormatter={"function": "formatPercent(value)"}
 */
dggfuncs.formatPercent = function(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return value;
    }
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 1,
        maximumFractionDigits: 1
    }).format(value / 100);
};

/**
 * Format numbers with thousands separator
 * Usage: valueFormatter={"function": "formatNumber(value)"}
 */
dggfuncs.formatNumber = function(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return value;
    }
    return new Intl.NumberFormat('en-US').format(value);
};

/**
 * Format dates (assuming value is a timestamp or ISO string)
 * Usage: valueFormatter={"function": "formatDate(value)"}
 */
dggfuncs.formatDate = function(value) {
    if (!value) return '';
    try {
        const date = new Date(value);
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(date);
    } catch (e) {
        return value;
    }
};

/**
 * Format numbers with fixed decimals
 * Usage: valueFormatter={"function": "formatFixed2(value)"}
 */
dggfuncs.formatFixed2 = function(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return value;
    }
    return value.toFixed(2);
};

/**
 * Format text to uppercase
 * Usage: valueFormatter={"function": "formatUppercase(value)"}
 */
dggfuncs.formatUppercase = function(value) {
    if (typeof value !== 'string') {
        return value;
    }
    return value.toUpperCase();
};

/**
 * Format with prefix and suffix
 * Usage: valueFormatter={"function": "formatWithUnits(value)"}
 * Adds "kg" suffix to numbers
 */
dggfuncs.formatWithUnits = function(value) {
    if (typeof value !== 'number' || isNaN(value)) {
        return value;
    }
    return `${value.toFixed(1)} kg`;
};

console.log('[dashGlideGridFunctions] Loaded successfully. Available functions:', Object.keys(dggfuncs));
