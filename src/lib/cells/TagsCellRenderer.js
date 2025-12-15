/**
 * Custom TagsCellRenderer for Dash integration.
 *
 * Displays colored tags as pill-shaped badges. Read-only.
 *
 * Data structure:
 * {
 *   kind: "tags-cell",
 *   tags: [
 *     { tag: "python", color: "#3776ab" },
 *     { tag: "react", color: "#61dafb" }
 *   ]
 * }
 */
import { GridCellKind, getMiddleCenterBias } from "@glideapps/glide-data-grid";

/**
 * Draw a rounded rectangle on canvas
 */
function roundRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
}

/**
 * Factory function to create a TagsCellRenderer
 */
export function createTagsCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "tags-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect } = args;
            const { tags } = cell.data;

            if (!tags || tags.length === 0) {
                return true;
            }

            const padding = theme.cellHorizontalPadding;
            const tagHeight = 20;
            const tagPaddingX = 8;
            const tagSpacing = 6;
            const tagRadius = tagHeight / 2;
            const verticalPadding = 4;

            // Calculate vertical centering for single row
            const startY = rect.y + (rect.height - tagHeight) / 2;
            let currentX = rect.x + padding;
            let currentY = startY;
            const maxX = rect.x + rect.width - padding;

            // Set up text style
            ctx.font = `12px ${theme.fontFamily}`;
            ctx.textBaseline = "middle";

            for (const tagData of tags) {
                const tagText = tagData.tag || "";
                const tagColor = tagData.color || theme.accentColor || "#3b82f6";

                // Measure text
                const textWidth = ctx.measureText(tagText).width;
                const tagWidth = textWidth + tagPaddingX * 2;

                // Check if we need to wrap to next row
                if (currentX + tagWidth > maxX && currentX > rect.x + padding) {
                    currentX = rect.x + padding;
                    currentY += tagHeight + verticalPadding;

                    // Stop if we've exceeded the cell height
                    if (currentY + tagHeight > rect.y + rect.height - verticalPadding) {
                        break;
                    }
                }

                // Draw tag background
                roundRect(ctx, currentX, currentY, tagWidth, tagHeight, tagRadius);
                ctx.fillStyle = tagColor;
                ctx.fill();

                // Draw tag text (white or dark based on background)
                const textColor = getContrastColor(tagColor);
                ctx.fillStyle = textColor;
                ctx.textAlign = "center";
                ctx.fillText(tagText, currentX + tagWidth / 2, currentY + tagHeight / 2);

                currentX += tagWidth + tagSpacing;
            }

            // Reset text align
            ctx.textAlign = "start";

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { tags } = cell.data;
            if (!tags || tags.length === 0) {
                return 50;
            }

            ctx.font = `12px ${theme.fontFamily}`;
            const tagPaddingX = 8;
            const tagSpacing = 6;

            let totalWidth = theme.cellHorizontalPadding;
            for (const tagData of tags) {
                const textWidth = ctx.measureText(tagData.tag || "").width;
                totalWidth += textWidth + tagPaddingX * 2 + tagSpacing;
            }

            return totalWidth + theme.cellHorizontalPadding;
        },

        // No click handling - read only
        onClick: () => undefined,

        // No editor - read only
        provideEditor: undefined,

        // Copy tags as comma-separated string
        onPaste: (val, data) => {
            // Parse comma-separated tags
            const newTags = val.split(",").map(t => t.trim()).filter(t => t);
            return {
                ...data,
                tags: newTags.map(tag => ({ tag, color: "#6b7280" }))
            };
        }
    };
}

/**
 * Get contrasting text color (white or black) based on background
 */
function getContrastColor(hexColor) {
    // Default to white if no color
    if (!hexColor) return "#ffffff";

    // Remove # if present
    const hex = hexColor.replace("#", "");

    // Parse RGB
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);

    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

    return luminance > 0.5 ? "#000000" : "#ffffff";
}

export default createTagsCellRenderer;
