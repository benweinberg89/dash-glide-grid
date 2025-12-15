/**
 * Custom RangeCellRenderer for Dash integration.
 *
 * Displays a horizontal range/progress bar with optional label.
 * Editable via HTML range slider.
 *
 * Data structure:
 * {
 *   kind: "range-cell",
 *   value: 75,          // Current value
 *   min: 0,             // Minimum value
 *   max: 100,           // Maximum value
 *   step: 1,            // Step increment (optional, defaults to 1)
 *   label: "75%"        // Optional display label
 * }
 */
import { useCallback, useState } from "react";
import { GridCellKind } from "@glideapps/glide-data-grid";

/**
 * Draw a rounded rectangle on canvas
 */
function roundRect(ctx, x, y, width, height, radius) {
    const r = Math.min(radius, height / 2, width / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.lineTo(x + width - r, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + r);
    ctx.lineTo(x + width, y + height - r);
    ctx.quadraticCurveTo(x + width, y + height, x + width - r, y + height);
    ctx.lineTo(x + r, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - r);
    ctx.lineTo(x, y + r);
    ctx.quadraticCurveTo(x, y, x + r, y);
    ctx.closePath();
}

/**
 * Editor component for range cell - shows slider input
 */
function RangeEditor({ value, onChange }) {
    const { value: currentValue = 0, min = 0, max = 100, step = 1, readonly } = value.data;
    const [localValue, setLocalValue] = useState(currentValue);

    const handleChange = useCallback((e) => {
        if (readonly) return;

        const newValue = parseFloat(e.target.value);
        setLocalValue(newValue);

        // Preserve label format (e.g., "75%" -> "80%")
        const originalLabel = value.data.label;
        let newLabel = `${newValue}`;
        if (typeof originalLabel === 'string') {
            // Check for common suffixes and preserve them
            const suffixMatch = originalLabel.match(/[\d.]+(.*)$/);
            if (suffixMatch && suffixMatch[1]) {
                newLabel = `${newValue}${suffixMatch[1]}`;
            }
        }

        onChange({
            ...value,
            data: {
                ...value.data,
                value: newValue,
                label: newLabel
            }
        });
    }, [readonly, value, onChange]);

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            padding: "8px 12px",
            gap: 12,
            minWidth: 200,
        }}>
            <input
                type="range"
                min={min}
                max={max}
                step={step}
                value={localValue}
                onChange={handleChange}
                disabled={readonly}
                style={{
                    flex: 1,
                    height: 6,
                    cursor: readonly ? "default" : "pointer",
                    accentColor: "#8b5cf6",
                }}
            />
            <span style={{
                fontSize: 13,
                color: "#374151",
                minWidth: 40,
                textAlign: "right",
                fontVariantNumeric: "tabular-nums",
            }}>
                {localValue}
            </span>
        </div>
    );
}

/**
 * Factory function to create a RangeCellRenderer
 */
export function createRangeCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "range-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect } = args;
            const { value = 0, min = 0, max = 100, label } = cell.data;

            const padding = theme.cellHorizontalPadding;
            const barHeight = 8;
            const barRadius = barHeight / 2;

            // Calculate label width if present
            let labelWidth = 0;
            const labelSpacing = 8;
            if (label !== undefined && label !== null) {
                ctx.font = `12px ${theme.fontFamily}`;
                labelWidth = ctx.measureText(String(label)).width + labelSpacing;
            }

            // Calculate bar dimensions
            const barWidth = rect.width - padding * 2 - labelWidth;
            const barX = rect.x + padding;
            const barY = rect.y + (rect.height - barHeight) / 2;

            // Calculate fill percentage
            const range = max - min;
            const percentage = range > 0 ? (value - min) / range : 0;
            const fillWidth = Math.max(0, Math.min(barWidth * percentage, barWidth));

            // Draw background track
            const trackColor = theme.bgBubble || "#e5e7eb";
            roundRect(ctx, barX, barY, barWidth, barHeight, barRadius);
            ctx.fillStyle = trackColor;
            ctx.fill();

            // Draw filled portion with gradient
            if (fillWidth > 0) {
                const gradient = ctx.createLinearGradient(barX, barY, barX + fillWidth, barY);
                const accentColor = theme.accentColor || "#8b5cf6";
                gradient.addColorStop(0, accentColor);
                gradient.addColorStop(1, accentColor);

                ctx.save();
                roundRect(ctx, barX, barY, barWidth, barHeight, barRadius);
                ctx.clip();

                ctx.fillStyle = gradient;
                ctx.fillRect(barX, barY, fillWidth, barHeight);
                ctx.restore();
            }

            // Draw label if present
            if (label !== undefined && label !== null) {
                ctx.font = `12px ${theme.fontFamily}`;
                ctx.fillStyle = theme.textDark || "#374151";
                ctx.textBaseline = "middle";
                ctx.textAlign = "right";
                ctx.fillText(String(label), rect.x + rect.width - padding, rect.y + rect.height / 2);
                ctx.textAlign = "start";
            }

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { label } = cell.data;
            const minBarWidth = 80;
            const padding = theme.cellHorizontalPadding;

            let labelWidth = 0;
            if (label !== undefined && label !== null) {
                ctx.font = `12px ${theme.fontFamily}`;
                labelWidth = ctx.measureText(String(label)).width + 8;
            }

            return padding * 2 + minBarWidth + labelWidth;
        },

        onClick: () => undefined,

        provideEditor: () => ({
            editor: RangeEditor,
            disablePadding: true,
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, value: v.data.min || 0 }
            }),
        }),

        onPaste: (val, data) => {
            const parsed = parseFloat(val);
            if (isNaN(parsed)) {
                return data;
            }
            const min = data.min || 0;
            const max = data.max || 100;
            const clampedValue = Math.max(min, Math.min(parsed, max));

            // Preserve label format (e.g., "75%" -> "80%")
            let newLabel = `${clampedValue}`;
            if (typeof data.label === 'string') {
                const suffixMatch = data.label.match(/[\d.]+(.*)$/);
                if (suffixMatch && suffixMatch[1]) {
                    newLabel = `${clampedValue}${suffixMatch[1]}`;
                }
            }

            return {
                ...data,
                value: clampedValue,
                label: newLabel
            };
        }
    };
}

export default createRangeCellRenderer;
