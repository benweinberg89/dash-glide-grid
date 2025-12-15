/**
 * Custom functions for dash-glide-grid examples
 * This file demonstrates high-performance drawCell animations
 */

var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};

// Track pulsing cells: { "col,row": { startTime, duration } }
window.pulsingCells = window.pulsingCells || {};

// Cached render time - set ONCE per frame before setProps, used by all cells
window._renderTime = 0;

/**
 * Custom drawCell function that renders a pulse/glow effect on cells.
 * Uses window._renderTime (cached once per frame) instead of Date.now() per cell.
 * Draws grid lines manually to preserve them during partial updateCells() redraws.
 */
dggfuncs.drawPulsingCell = function(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent) {
    var key = col + "," + row;
    var pulse = window.pulsingCells[key];

    if (pulse) {
        // Use cached time (set once per frame in animation loop)
        var now = window._renderTime;
        var elapsed = now - pulse.startTime;
        var progress = elapsed / pulse.duration;

        if (progress >= 1) {
            delete window.pulsingCells[key];
        } else {
            // Simple fade: start bright, fade to dark
            var intensity = 1 - progress;
            // Direct color calculation (no string parsing)
            var r = Math.round(59 + (30 - 59) * progress);  // 59 -> 30
            var g = Math.round(130 + (41 - 130) * progress); // 130 -> 41
            var b = Math.round(246 + (59 - 246) * progress); // 246 -> 59
            var alpha = 0.3 + intensity * 0.7;

            ctx.fillStyle = "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
            ctx.fillRect(rect.x, rect.y, rect.width, rect.height);
        }
    }

    // Always draw grid lines (right and bottom borders) to preserve them during partial redraws
    // Use hardcoded color since theme.borderColor is set to transparent to disable grid's own borders
    ctx.strokeStyle = "#334155";
    ctx.lineWidth = 1;

    // Right border
    ctx.beginPath();
    ctx.moveTo(rect.x + rect.width - 0.5, rect.y);
    ctx.lineTo(rect.x + rect.width - 0.5, rect.y + rect.height);
    ctx.stroke();

    // Bottom border
    ctx.beginPath();
    ctx.moveTo(rect.x, rect.y + rect.height - 0.5);
    ctx.lineTo(rect.x + rect.width, rect.y + rect.height - 0.5);
    ctx.stroke();

    return false;
};

/**
 * Start a pulse animation on a cell.
 * Call this from a clientside callback when a cell is clicked.
 */
window.startCellPulse = function(col, row) {
    var key = col + "," + row;
    window.pulsingCells[key] = {
        startTime: performance.now(),
        duration: 800
    };
};

/**
 * Get list of currently animating cells.
 * Returns array of [col, row] pairs.
 */
window.getAnimatingCells = function() {
    var cells = [];
    var now = performance.now();

    for (var key in window.pulsingCells) {
        var pulse = window.pulsingCells[key];
        var elapsed = now - pulse.startTime;

        if (elapsed < pulse.duration) {
            var parts = key.split(",");
            cells.push([parseInt(parts[0]), parseInt(parts[1])]);
        } else {
            // Clean up expired animations
            delete window.pulsingCells[key];
        }
    }

    return cells;
};

/**
 * getCellContent function that returns cells with themeOverride for animation colors.
 * Used by example 43 - demonstrates themeOverride approach (alternative to custom drawCell).
 * Grid lines are preserved automatically since we're using the built-in renderer.
 */
dggfuncs.getAnimatedCell = function(col, row, colId, rowData, columns) {
    var key = col + "," + row;
    var pulse = window.pulsingCells ? window.pulsingCells[key] : null;

    if (pulse) {
        var now = window._renderTime || performance.now();
        var elapsed = now - pulse.startTime;
        var progress = Math.min(elapsed / pulse.duration, 1);

        if (progress < 1) {
            // Calculate color: bright blue fading to dark background
            var intensity = 1 - progress;
            var r = Math.round(30 + (59 - 30) * intensity);   // 30 -> 59 (base) -> 30
            var g = Math.round(41 + (130 - 41) * intensity);  // 41 -> 130 -> 41
            var b = Math.round(59 + (246 - 59) * intensity);  // 59 -> 246 -> 59

            return {
                kind: "text",
                data: "",
                displayData: "",
                themeOverride: {
                    bgCell: "rgb(" + r + "," + g + "," + b + ")"
                }
            };
        }
    }

    // Default: no animation, use base theme
    return {
        kind: "text",
        data: "",
        displayData: ""
    };
};