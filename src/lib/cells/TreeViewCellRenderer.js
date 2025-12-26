/**
 * Custom TreeViewCellRenderer for Dash integration.
 *
 * Renders hierarchical tree data with expand/collapse functionality.
 * Fires Dash callbacks when a node is toggled.
 */
import { GridCellKind, getMiddleCenterBias } from "@glideapps/glide-data-grid";

// Constants for tree layout
const DEPTH_SHIFT = 16; // Pixels per indentation level
const ICON_SIZE = 16;   // Size of expand/collapse icon area
const DEFAULT_PADDING = 8;

/**
 * Calculate the icon X position (relative to cell left edge)
 */
function getIconRelativeX(depth, padding) {
    const inset = depth * DEPTH_SHIFT;
    return padding + inset + ICON_SIZE / 2;
}

/**
 * Draw a chevron icon (expand/collapse indicator)
 * @param {CanvasRenderingContext2D} ctx
 * @param {number} x - Center X of icon
 * @param {number} y - Center Y of icon
 * @param {boolean} isOpen - Whether node is expanded
 * @param {string} color - Icon color
 */
function drawChevron(ctx, x, y, isOpen, color) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.lineWidth = 1.5;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";

    const size = 4; // Half-size of chevron

    ctx.beginPath();
    if (isOpen) {
        // Downward chevron (expanded)
        ctx.moveTo(x - size, y - size / 2);
        ctx.lineTo(x, y + size / 2);
        ctx.lineTo(x + size, y - size / 2);
    } else {
        // Rightward chevron (collapsed)
        ctx.moveTo(x - size / 2, y - size);
        ctx.lineTo(x + size / 2, y);
        ctx.lineTo(x - size / 2, y + size);
    }
    ctx.stroke();
    ctx.restore();
}

/**
 * Check if a point is within the icon bounds
 * posX is relative to cell left, iconX is relative to cell left
 */
function isPointOverIcon(posX, iconX) {
    const halfIcon = ICON_SIZE / 2;
    return posX >= iconX - halfIcon && posX <= iconX + halfIcon;
}

/**
 * Factory function to create a TreeViewCellRenderer with a toggle callback
 * @param {Function} onToggle - Callback receiving { col, row, isOpen, depth, text }
 */
export function createTreeViewCellRenderer(onToggle) {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "tree-view-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect, hoverX } = args;
            const { text = "", depth = 0, isOpen = false, canOpen = false } = cell.data;

            const padding = theme.cellHorizontalPadding ?? DEFAULT_PADDING;
            const inset = depth * DEPTH_SHIFT;
            const iconRelX = getIconRelativeX(depth, padding);
            const iconAbsX = rect.x + iconRelX;
            const iconY = rect.y + rect.height / 2;
            const textX = rect.x + padding + inset + (canOpen ? ICON_SIZE + 4 : 0);
            const textY = rect.y + rect.height / 2 + getMiddleCenterBias(ctx, theme);

            // Check if hovering over icon (hoverX is relative to cell)
            const isHoveringIcon = canOpen && hoverX !== undefined && isPointOverIcon(hoverX, iconRelX);

            // Draw expand/collapse icon if node has children
            if (canOpen) {
                const iconColor = isHoveringIcon
                    ? (theme.accentColor || "#3b82f6")
                    : (theme.textMedium || "#6b7280");
                drawChevron(ctx, iconAbsX, iconY, isOpen, iconColor);
            }

            // Draw text
            ctx.font = `${theme.baseFontStyle} ${theme.fontFamily}`;
            ctx.fillStyle = theme.textDark || "#111827";
            ctx.textAlign = "start";
            ctx.textBaseline = "middle";
            ctx.fillText(text, textX, textY);

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { text = "", depth = 0, canOpen = false } = cell.data;
            const padding = theme.cellHorizontalPadding ?? DEFAULT_PADDING;
            const inset = depth * DEPTH_SHIFT;
            const textWidth = ctx.measureText(text).width;
            return padding * 2 + inset + (canOpen ? ICON_SIZE + 4 : 0) + textWidth;
        },

        onClick: (args) => {
            const { cell, posX, location } = args;
            const { canOpen, isOpen, depth, text } = cell.data;

            if (!canOpen) return undefined;

            // Recalculate icon position from depth (don't rely on stored _iconX)
            const iconRelX = getIconRelativeX(depth, DEFAULT_PADDING);

            // Check if click is on the icon (posX is relative to cell)
            if (isPointOverIcon(posX, iconRelX)) {
                if (onToggle) {
                    onToggle({
                        col: location[0],
                        row: location[1],
                        isOpen: !isOpen,  // The new state after toggle
                        depth: depth,
                        text: text
                    });
                }
            }

            return undefined;
        },

        // Show pointer cursor when hovering over expand/collapse icon
        onPointerEnter: (args) => {
            const { cell, posX } = args;
            const { canOpen, depth } = cell.data;

            if (!canOpen) return undefined;

            const iconRelX = getIconRelativeX(depth, DEFAULT_PADDING);

            if (isPointOverIcon(posX, iconRelX)) {
                return { cursor: "pointer" };
            }
            return undefined;
        },
        onPointerLeave: () => undefined,

        // Prevent cell selection when clicking icon
        onSelect: (args) => {
            const { cell, posX } = args;
            const { canOpen, depth } = cell.data;

            if (!canOpen) return;

            const iconRelX = getIconRelativeX(depth, DEFAULT_PADDING);

            if (isPointOverIcon(posX, iconRelX)) {
                args.preventDefault();
            }
        },

        // No visual editor, but provide deletedValue for clearing
        provideEditor: () => ({
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, text: '' }
            }),
        }),

        // Parse pasted tree data - supports format: text|depth|canOpen|isOpen
        onPaste: (val, data) => {
            // Check for pipe-delimited format: text|depth|canOpen|isOpen
            const parts = val.split('|');
            if (parts.length >= 4) {
                return {
                    ...data,
                    text: parts[0],
                    depth: parseInt(parts[1], 10) || 0,
                    canOpen: parts[2] === 'true',
                    isOpen: parts[3] === 'true'
                };
            }
            // Plain text - just update the text, keep other properties
            return { ...data, text: val };
        }
    };
}

export default createTreeViewCellRenderer;
