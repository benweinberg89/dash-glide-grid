/**
 * Custom functions for dash-glide-grid examples
 * This file demonstrates the cellsToUpdate prop with drawCell animations
 */

var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};

// Track pulsing cells: { "col,row": { startTime, duration } }
window.pulsingCells = window.pulsingCells || {};

// Animation duration in ms
var PULSE_DURATION = 800;

/**
 * Custom drawCell function that renders a pulse/glow effect on clicked cells.
 * The pulse state is tracked in window.pulsingCells.
 */
dggfuncs.drawPulsingCell = function(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent) {
    var key = col + "," + row;
    var pulse = window.pulsingCells[key];

    if (pulse) {
        var now = Date.now();
        var elapsed = now - pulse.startTime;
        var progress = Math.min(1, elapsed / pulse.duration);

        if (progress >= 1) {
            // Animation complete - remove from tracking
            delete window.pulsingCells[key];
        } else {
            // Calculate intensity using sine wave (0 -> 1 -> 0)
            var intensity = Math.sin(progress * Math.PI);

            // Draw glowing background
            var r = 59, g = 130, b = 246; // Blue color
            ctx.fillStyle = "rgba(" + r + "," + g + "," + b + "," + (intensity * 0.6) + ")";
            ctx.fillRect(rect.x, rect.y, rect.width, rect.height);

            // Draw a border glow too
            ctx.strokeStyle = "rgba(" + r + "," + g + "," + b + "," + (intensity * 0.9) + ")";
            ctx.lineWidth = 2;
            ctx.strokeRect(rect.x + 1, rect.y + 1, rect.width - 2, rect.height - 2);
        }
    }

    // Return false to continue with default cell rendering
    return false;
};

/**
 * Start a pulse animation on a cell.
 * Call this from a clientside callback when a cell is clicked.
 */
window.startCellPulse = function(col, row) {
    var key = col + "," + row;
    window.pulsingCells[key] = {
        startTime: Date.now(),
        duration: PULSE_DURATION
    };
};

/**
 * Get list of currently animating cells.
 * Returns array of [col, row] pairs.
 */
window.getAnimatingCells = function() {
    var cells = [];
    var now = Date.now();

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
