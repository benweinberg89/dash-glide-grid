/**
 * Function parser utility for executing user-defined JavaScript functions
 * Following the same pattern as Dash AG Grid's dashAgGridFunctions namespace
 */

/**
 * Namespace for user-defined functions
 * Users create assets/dashGlideGridFunctions.js with:
 *
 * var dggfuncs = window.dashGlideGridFunctions =
 *     window.dashGlideGridFunctions || {};
 *
 * dggfuncs.myValidator = function(cell, newValue) { ... };
 */
const NAMESPACE = 'dashGlideGridFunctions';

/**
 * Built-in functions available without asset files
 */
const BUILTIN_FUNCTIONS = {
    // Math functions
    Math: Math,
    Number: Number,
    parseInt: parseInt,
    parseFloat: parseFloat,
    isNaN: isNaN,
    isFinite: isFinite,

    // String functions
    String: String,

    // JSON
    JSON: JSON,

    // Intl for formatting
    Intl: typeof Intl !== 'undefined' ? Intl : undefined,

    // Debugging helper - logs params and returns them
    log: (params) => {
        console.log('[GlideGrid Debug]', params);
        return params;
    }
};

/**
 * Parse and execute a function string like "myFunc(cell, newValue)"
 *
 * @param {string} functionString - The function call string, e.g. "validateAge(cell, newValue)"
 * @param {object} params - Named parameters to make available in the function scope
 * @returns {any} - The function's return value, or undefined on error
 */
export function executeFunction(functionString, params = {}) {
    if (!functionString || typeof functionString !== 'string') {
        return undefined;
    }

    // Get the user's namespace (may not exist yet)
    const userNamespace = (typeof window !== 'undefined' && window[NAMESPACE]) || {};

    // Combine built-ins with user functions (user functions take precedence)
    const availableFunctions = { ...BUILTIN_FUNCTIONS, ...userNamespace };

    try {
        // Extract function name to validate it exists
        const funcMatch = functionString.match(/^(\w+)\s*\(/);
        if (!funcMatch) {
            console.warn(`[GlideGrid] Invalid function string: "${functionString}". Expected format: "functionName(args)"`);
            return undefined;
        }

        const funcName = funcMatch[1];

        // Check if function exists
        if (!(funcName in availableFunctions)) {
            console.warn(
                `[GlideGrid] Function "${funcName}" not found. ` +
                `Add it to window.${NAMESPACE} in your assets folder. ` +
                `Example: window.${NAMESPACE}.${funcName} = function(cell, newValue) { ... };`
            );
            return undefined;
        }

        // Build execution context with available functions
        const contextKeys = Object.keys(availableFunctions);
        const contextValues = Object.values(availableFunctions);

        // Add params to context (cell, newValue, col, row, val, etc.)
        const paramKeys = Object.keys(params);
        const paramValues = Object.values(params);

        // Create the function with all context available
        // Using Function constructor - safer than eval as it doesn't access local scope
        const fn = new Function(
            ...contextKeys,
            ...paramKeys,
            `"use strict"; return ${functionString};`
        );

        return fn(...contextValues, ...paramValues);
    } catch (error) {
        console.error(`[GlideGrid] Error executing function "${functionString}":`, error);
        return undefined;
    }
}

/**
 * Check if a prop value is a function reference object
 * Function references have the format: { function: "functionName(args)" }
 *
 * @param {any} value - The prop value to check
 * @returns {boolean} - True if this is a function reference
 */
export function isFunctionRef(value) {
    return value && typeof value === 'object' && typeof value.function === 'string';
}

/**
 * Get the namespace name for documentation purposes
 */
export function getNamespace() {
    return NAMESPACE;
}