/**
 * Custom ButtonCellRenderer for Dash integration.
 *
 * This is a custom implementation that fires Dash callbacks via setProps
 * instead of requiring a JavaScript onClick function in the cell data.
 *
 * Uses a factory function pattern to inject the callback.
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
 * Check if a point is within the button bounds
 * Note: posX and posY are relative to the cell (0,0 is top-left of cell)
 */
function isPointInButton(posX, posY, rect, theme) {
    const padding = theme.cellHorizontalPadding;
    // Button position relative to cell (not absolute)
    const buttonX = padding;
    const buttonY = 4;
    const buttonWidth = rect.width - padding * 2;
    const buttonHeight = rect.height - 8;

    return (
        posX >= buttonX &&
        posX <= buttonX + buttonWidth &&
        posY >= buttonY &&
        posY <= buttonY + buttonHeight
    );
}

/**
 * Factory function to create a ButtonCellRenderer with a click callback
 * @param {Function} onButtonClick - Callback receiving { col, row, title }
 */
export function createButtonCellRenderer(onButtonClick) {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "button-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect, hoverX, hoverY } = args;
            const { title, backgroundColor, color, borderColor, borderRadius } = cell.data;

            const padding = theme.cellHorizontalPadding;
            const buttonX = rect.x + padding;
            const buttonY = rect.y + 4;
            const buttonWidth = rect.width - padding * 2;
            const buttonHeight = rect.height - 8;
            const radius = borderRadius ?? 6;

            // Default colors
            const bgColor = backgroundColor ?? theme.accentColor ?? "#3b82f6";
            const textColor = color ?? "#ffffff";
            const border = borderColor ?? null;

            // Check if mouse is hovering over the button
            // hoverX/hoverY are relative to cell, so use relative button coordinates
            const relButtonX = padding;
            const relButtonY = 4;
            const isHovered = hoverX !== undefined && hoverY !== undefined &&
                hoverX >= relButtonX && hoverX <= relButtonX + buttonWidth &&
                hoverY >= relButtonY && hoverY <= relButtonY + buttonHeight;

            // Draw button background
            roundRect(ctx, buttonX, buttonY, buttonWidth, buttonHeight, radius);
            ctx.fillStyle = bgColor;
            ctx.fill();

            // Apply hover effect - darken by drawing semi-transparent black overlay
            if (isHovered) {
                ctx.globalAlpha = 0.15;
                ctx.fillStyle = "#000000";
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            // Draw border if specified
            if (border) {
                roundRect(ctx, buttonX, buttonY, buttonWidth, buttonHeight, radius);
                ctx.strokeStyle = border;
                ctx.lineWidth = 1;
                ctx.stroke();
            }

            // Draw text
            ctx.fillStyle = textColor;
            ctx.font = `${theme.baseFontStyle} ${theme.fontFamily}`;
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";

            const textX = buttonX + buttonWidth / 2;
            const textY = rect.y + rect.height / 2 + getMiddleCenterBias(ctx, theme);
            ctx.fillText(title ?? "Button", textX, textY);

            // Reset text align for other cells
            ctx.textAlign = "start";

            return true; // We handled the drawing
        },

        measure: (ctx, cell, theme) => {
            const { title } = cell.data;
            const textWidth = ctx.measureText(title ?? "Button").width;
            // Add padding for the button
            return textWidth + theme.cellHorizontalPadding * 2 + 24;
        },

        onClick: (args) => {
            const { cell, posX, posY, bounds, theme, location } = args;

            // Check if click is within button bounds
            if (isPointInButton(posX, posY, bounds, theme)) {
                if (onButtonClick) {
                    onButtonClick({
                        col: location[0],
                        row: location[1],
                        title: cell.data.title ?? "Button"
                    });
                }
            }

            // Return undefined to not open an editor
            return undefined;
        },

        // Show pointer cursor when hovering over button
        onPointerEnter: () => ({ cursor: "pointer" }),
        onPointerLeave: () => undefined,

        // Prevent cell selection when clicking button - must call preventDefault
        onSelect: (args) => {
            args.preventDefault();
        },

        // No editor for buttons
        provideEditor: undefined,

        // Copy the button title
        onPaste: (val, data) => ({
            ...data,
            title: val
        })
    };
}

export default createButtonCellRenderer;
