/**
 * Custom SparklineCellRenderer for Dash integration.
 *
 * Renders mini charts (line, bar, area) in a cell.
 * Display-only - no editing or callbacks.
 *
 * Based on upstream @glideapps/glide-data-grid-cells sparkline-cell.
 */
import { GridCellKind } from "@glideapps/glide-data-grid";

/**
 * Parse color to rgba array (simplified version)
 */
function parseToRgba(color) {
    if (!color) return [59, 130, 246, 1];
    // Handle hex colors
    if (color.startsWith('#')) {
        const hex = color.slice(1);
        if (hex.length === 3) {
            const r = parseInt(hex[0] + hex[0], 16);
            const g = parseInt(hex[1] + hex[1], 16);
            const b = parseInt(hex[2] + hex[2], 16);
            return [r, g, b, 1];
        } else if (hex.length === 6) {
            const r = parseInt(hex.slice(0, 2), 16);
            const g = parseInt(hex.slice(2, 4), 16);
            const b = parseInt(hex.slice(4, 6), 16);
            return [r, g, b, 1];
        }
    }
    // Default fallback
    return [59, 130, 246, 1]; // blue
}

/**
 * Factory function to create a SparklineCellRenderer
 */
export function createSparklineCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "sparkline-cell",
        needsHover: true,
        needsHoverPosition: true,

        draw: (args, cell) => {
            const { ctx, theme, rect, hoverAmount = 0, hoverX } = args;

            // Skip drawing if row is hidden (height <= 0)
            if (rect.height <= 0) return true;

            let {
                values,
                yAxis,
                color,
                graphKind = "area",
                displayValues,
                hideAxis,
                hoverStyle = "line"  // "line" (vertical line + text) or "dot" (dot + tooltip box)
            } = cell.data;

            if (!values || values.length === 0) return true;
            if (!yAxis || yAxis.length !== 2) yAxis = [0, 100];

            const [minY, maxY] = yAxis;
            const originalValues = [...values]; // Keep original for display

            // Normalize values to 0-1 range
            values = values.map(x => Math.min(1, Math.max(0, (x - minY) / (maxY - minY))));

            const padX = theme.cellHorizontalPadding ?? 8;
            const drawX = padX + rect.x;
            const y = rect.y + 3;
            const height = rect.height - 6;
            const width = rect.width - padX * 2;
            const delta = maxY - minY;
            const zeroY = maxY <= 0 ? y : minY >= 0 ? y + height : y + height * (maxY / delta);

            // Draw zero line
            if (!hideAxis && minY <= 0 && maxY >= 0) {
                ctx.beginPath();
                ctx.moveTo(drawX, zeroY);
                ctx.lineTo(drawX + width, zeroY);
                ctx.globalAlpha = 0.4;
                ctx.lineWidth = 1;
                ctx.strokeStyle = theme.textLight || "#d1d5db";
                ctx.stroke();
                ctx.globalAlpha = 1;
            }

            const chartColor = color || theme.accentColor || "#3b82f6";

            if (graphKind === "bar") {
                const margin = 2;
                const spacing = (values.length - 1) * margin;
                const barWidth = (width - spacing) / values.length;

                // Calculate which bar is hovered
                let hoveredBar = -1;
                if (hoverX !== undefined && displayValues !== undefined) {
                    const relX = hoverX - padX;
                    hoveredBar = Math.floor(relX / (barWidth + margin));
                    if (hoveredBar < 0 || hoveredBar >= values.length) hoveredBar = -1;
                }

                // Draw bars
                let x = drawX;
                for (let idx = 0; idx < values.length; idx++) {
                    const val = values[idx];
                    const barY = y + height - val * height;
                    const isHovered = idx === hoveredBar;

                    ctx.beginPath();
                    ctx.moveTo(x, zeroY);
                    ctx.lineTo(x + barWidth, zeroY);
                    ctx.lineTo(x + barWidth, barY);
                    ctx.lineTo(x, barY);
                    ctx.closePath();

                    ctx.fillStyle = isHovered ? chartColor : `${chartColor}cc`;
                    ctx.fill();

                    x += barWidth + margin;
                }

                // Draw hover indicator for bar
                if (hoveredBar >= 0 && displayValues !== undefined) {
                    const barX = drawX + hoveredBar * (barWidth + margin);
                    const barCenterX = barX + barWidth / 2;

                    if (hoverStyle === "dot") {
                        // Dot + tooltip style
                        const barY = y + height - values[hoveredBar] * height;

                        // Draw dot at top of bar
                        ctx.beginPath();
                        ctx.arc(barCenterX, barY, 4, 0, Math.PI * 2);
                        ctx.fillStyle = chartColor;
                        ctx.fill();
                        ctx.strokeStyle = theme.bgCellEditor || theme.bgCell || "#ffffff";
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        // Draw tooltip
                        const displayVal = displayValues[hoveredBar];
                        ctx.font = `10px ${theme.fontFamily}`;
                        const textWidth = ctx.measureText(displayVal).width;
                        const tooltipPadding = 4;
                        const tooltipWidth = textWidth + tooltipPadding * 2;
                        const tooltipHeight = 16;
                        let tooltipX = barCenterX - tooltipWidth / 2;
                        tooltipX = Math.max(rect.x + 2, Math.min(tooltipX, rect.x + rect.width - tooltipWidth - 2));
                        const tooltipY = barY > y + height / 2 ? rect.y + 2 : rect.y + rect.height - tooltipHeight - 2;

                        ctx.fillStyle = theme.bgCellEditor || theme.bgCell || "#ffffff";
                        ctx.fillRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);
                        ctx.strokeStyle = theme.borderColor || "#e5e7eb";
                        ctx.lineWidth = 1;
                        ctx.strokeRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);

                        ctx.fillStyle = theme.textDark || "#111827";
                        ctx.textBaseline = "middle";
                        ctx.fillText(displayVal, tooltipX + tooltipPadding, tooltipY + tooltipHeight / 2);
                    } else {
                        // Line style (default)
                        ctx.beginPath();
                        ctx.moveTo(barCenterX, rect.y + 1);
                        ctx.lineTo(barCenterX, rect.y + rect.height);
                        ctx.lineWidth = 1;
                        ctx.strokeStyle = theme.textLight || "#d1d5db";
                        ctx.stroke();

                        ctx.save();
                        ctx.font = `8px ${theme.fontFamily}`;
                        ctx.fillStyle = theme.textMedium || "#6b7280";
                        ctx.textBaseline = "top";
                        ctx.fillText(displayValues[hoveredBar], drawX, rect.y + (theme.cellVerticalPadding ?? 3));
                        ctx.restore();
                    }
                }
            } else {
                // Line or Area chart
                if (values.length === 1) {
                    values = [values[0], values[0]];
                    if (displayValues) {
                        displayValues = [displayValues[0], displayValues[0]];
                    }
                }

                // Draw line
                ctx.beginPath();
                const xStep = (rect.width - 16) / (values.length - 1);
                const points = values.map((val, ind) => ({
                    x: drawX + xStep * ind,
                    y: y + height - val * height,
                }));

                ctx.moveTo(points[0].x, points[0].y);
                let i = 0;
                if (points.length > 2) {
                    for (i = 1; i < points.length - 2; i++) {
                        const xControl = (points[i].x + points[i + 1].x) / 2;
                        const yControl = (points[i].y + points[i + 1].y) / 2;
                        ctx.quadraticCurveTo(points[i].x, points[i].y, xControl, yControl);
                    }
                }
                ctx.quadraticCurveTo(points[i].x, points[i].y, points[i + 1].x, points[i + 1].y);
                ctx.strokeStyle = chartColor;
                ctx.lineWidth = 1 + hoverAmount * 0.5;
                ctx.stroke();

                ctx.lineTo(rect.x + rect.width - padX, zeroY);
                ctx.lineTo(rect.x + padX, zeroY);
                ctx.closePath();

                if (graphKind === "area") {
                    ctx.globalAlpha = 0.2 + 0.2 * hoverAmount;
                    const grad = ctx.createLinearGradient(0, y, 0, y + height * 1.4);
                    grad.addColorStop(0, chartColor);
                    const [r, g, b] = parseToRgba(chartColor);
                    grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);
                    ctx.fillStyle = grad;
                    ctx.fill();
                    ctx.globalAlpha = 1;
                }

                // Draw hover indicator only if displayValues provided
                if (hoverX !== undefined && displayValues !== undefined) {
                    const closest = Math.min(values.length - 1, Math.max(0, Math.round((hoverX - padX) / xStep)));
                    const pointX = drawX + closest * xStep;
                    const pointY = points[closest].y;

                    if (hoverStyle === "dot") {
                        // Dot + tooltip style
                        // Draw dot
                        ctx.beginPath();
                        ctx.arc(pointX, pointY, 4, 0, Math.PI * 2);
                        ctx.fillStyle = chartColor;
                        ctx.fill();
                        ctx.strokeStyle = theme.bgCellEditor || theme.bgCell || "#ffffff";
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        // Draw tooltip
                        const displayVal = displayValues[closest];
                        ctx.font = `10px ${theme.fontFamily}`;
                        const textWidth = ctx.measureText(displayVal).width;
                        const tooltipPadding = 4;
                        const tooltipWidth = textWidth + tooltipPadding * 2;
                        const tooltipHeight = 16;
                        let tooltipX = pointX - tooltipWidth / 2;
                        tooltipX = Math.max(rect.x + 2, Math.min(tooltipX, rect.x + rect.width - tooltipWidth - 2));
                        const tooltipY = pointY > y + height / 2 ? rect.y + 2 : rect.y + rect.height - tooltipHeight - 2;

                        ctx.fillStyle = theme.bgCellEditor || theme.bgCell || "#ffffff";
                        ctx.fillRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);
                        ctx.strokeStyle = theme.borderColor || "#e5e7eb";
                        ctx.lineWidth = 1;
                        ctx.strokeRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);

                        ctx.fillStyle = theme.textDark || "#111827";
                        ctx.textBaseline = "middle";
                        ctx.fillText(displayVal, tooltipX + tooltipPadding, tooltipY + tooltipHeight / 2);
                    } else {
                        // Line style (default, like upstream)
                        ctx.beginPath();
                        ctx.moveTo(pointX, rect.y + 1);
                        ctx.lineTo(pointX, rect.y + rect.height);
                        ctx.lineWidth = 1;
                        ctx.strokeStyle = theme.textLight || "#d1d5db";
                        ctx.stroke();

                        ctx.save();
                        ctx.font = `8px ${theme.fontFamily}`;
                        ctx.fillStyle = theme.textMedium || "#6b7280";
                        ctx.textBaseline = "top";
                        ctx.fillText(displayValues[closest], drawX, rect.y + (theme.cellVerticalPadding ?? 3));
                        ctx.restore();
                    }
                }
            }

            return true;
        },

        measure: (ctx, cell, theme) => {
            return 120;
        },

        onClick: () => undefined,

        // No visual editor, but provide deletedValue for clearing
        provideEditor: () => ({
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, values: [] }
            }),
        }),

        onPaste: (val, data) => {
            const values = val.split(",").map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
            // Keep original if no valid numbers found
            return values.length > 0 ? { ...data, values } : data;
        }
    };
}

export default createSparklineCellRenderer;
