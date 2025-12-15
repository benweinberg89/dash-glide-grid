/**
 * Custom DatePickerCellRenderer for Dash integration.
 *
 * Displays a date/time value with native HTML5 date picker editor.
 *
 * Data structure:
 * {
 *   kind: "date-picker-cell",
 *   date: "2024-01-15",           // ISO date string, or null/undefined
 *   displayDate: "Jan 15, 2024",  // Formatted display string (optional)
 *   format: "date",               // "date" | "time" | "datetime-local"
 *   min: "2024-01-01",            // Optional min constraint (ISO string)
 *   max: "2024-12-31",            // Optional max constraint (ISO string)
 *   step: "1"                     // Optional step for time inputs
 * }
 */
import { useCallback, useEffect, useRef } from "react";
import { GridCellKind } from "@glideapps/glide-data-grid";

/**
 * Format a date for display based on format type
 */
function formatDateForDisplay(dateStr, format) {
    if (!dateStr) return "";

    try {
        if (format === "time") {
            // Time string like "14:30"
            return dateStr;
        }

        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return dateStr;

        if (format === "datetime-local") {
            return date.toLocaleString(undefined, {
                year: "numeric",
                month: "short",
                day: "numeric",
                hour: "2-digit",
                minute: "2-digit",
            });
        }

        // Default: date format
        return date.toLocaleDateString(undefined, {
            year: "numeric",
            month: "short",
            day: "numeric",
        });
    } catch {
        return dateStr;
    }
}

/**
 * Convert date string to HTML input value format
 */
function toInputValue(dateStr, format) {
    if (!dateStr) return "";

    try {
        if (format === "time") {
            // Already in HH:mm format
            return dateStr;
        }

        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return "";

        if (format === "datetime-local") {
            // Format: YYYY-MM-DDTHH:mm
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, "0");
            const day = String(date.getDate()).padStart(2, "0");
            const hours = String(date.getHours()).padStart(2, "0");
            const minutes = String(date.getMinutes()).padStart(2, "0");
            return `${year}-${month}-${day}T${hours}:${minutes}`;
        }

        // Default: date format YYYY-MM-DD
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, "0");
        const day = String(date.getDate()).padStart(2, "0");
        return `${year}-${month}-${day}`;
    } catch {
        return "";
    }
}

/**
 * Editor component for date picker cell - native HTML5 input
 */
function DatePickerEditor({ value, onChange, theme }) {
    const { date, format = "date", min, max, step, readonly } = value.data;
    const inputRef = useRef(null);

    // Detect dark mode from theme
    const isDark = theme?.bgCell && (
        theme.bgCell.startsWith("#1") ||
        theme.bgCell.startsWith("#2") ||
        theme.bgCell.startsWith("#0")
    );

    // Auto-focus on mount
    useEffect(() => {
        if (inputRef.current && !readonly) {
            inputRef.current.focus();
        }
    }, [readonly]);

    const handleChange = useCallback((e) => {
        if (readonly) return;

        const newValue = e.target.value;
        let newDate = newValue;
        let displayDate = "";

        if (newValue) {
            if (format === "time") {
                displayDate = newValue;
            } else {
                const dateObj = new Date(newValue);
                if (!isNaN(dateObj.getTime())) {
                    newDate = dateObj.toISOString();
                    displayDate = formatDateForDisplay(newDate, format);
                }
            }
        }

        onChange({
            ...value,
            data: {
                ...value.data,
                date: newDate || null,
                displayDate: displayDate,
            }
        });
    }, [readonly, value, onChange, format]);

    const inputValue = toInputValue(date, format);

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            padding: "8px 12px",
            minWidth: format === "datetime-local" ? 240 : 180,
            backgroundColor: isDark ? "#1f2937" : "#ffffff",
            colorScheme: isDark ? "dark" : "light",
        }}>
            <input
                ref={inputRef}
                type={format}
                value={inputValue}
                onChange={handleChange}
                disabled={readonly}
                min={min}
                max={max}
                step={step}
                style={{
                    flex: 1,
                    padding: "4px 8px",
                    fontSize: 14,
                    border: `1px solid ${isDark ? "#4b5563" : "#d1d5db"}`,
                    borderRadius: 4,
                    outline: "none",
                    cursor: readonly ? "default" : "pointer",
                    backgroundColor: isDark ? "#374151" : "#ffffff",
                    color: isDark ? "#f3f4f6" : "#111827",
                    colorScheme: isDark ? "dark" : "light",
                }}
            />
        </div>
    );
}

/**
 * Factory function to create a DatePickerCellRenderer
 */
export function createDatePickerCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "date-picker-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect } = args;
            const { date, displayDate, format = "date" } = cell.data;

            const padding = theme.cellHorizontalPadding;

            // Determine what to display
            let text = displayDate || "";
            if (!text && date) {
                text = formatDateForDisplay(date, format);
            }

            // Draw placeholder if empty
            if (!text) {
                ctx.font = `12px ${theme.fontFamily}`;
                ctx.fillStyle = theme.textLight || "#9ca3af";
                ctx.textBaseline = "middle";
                ctx.fillText(
                    format === "time" ? "Select time..." : "Select date...",
                    rect.x + padding,
                    rect.y + rect.height / 2
                );
                return true;
            }

            // Draw the date text
            ctx.font = `12px ${theme.fontFamily}`;
            ctx.fillStyle = theme.textDark || "#374151";
            ctx.textBaseline = "middle";
            ctx.fillText(text, rect.x + padding, rect.y + rect.height / 2);

            // Draw calendar icon on the right
            const iconSize = 14;
            const iconX = rect.x + rect.width - padding - iconSize;
            const iconY = rect.y + (rect.height - iconSize) / 2;

            ctx.fillStyle = theme.textLight || "#9ca3af";
            ctx.font = `${iconSize}px Arial`;
            ctx.fillText("📅", iconX, iconY + iconSize - 2);

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { displayDate, date, format = "date" } = cell.data;
            const padding = theme.cellHorizontalPadding;
            const iconSpace = 20;

            let text = displayDate || "";
            if (!text && date) {
                text = formatDateForDisplay(date, format);
            }

            if (!text) {
                text = format === "time" ? "Select time..." : "Select date...";
            }

            ctx.font = `12px ${theme.fontFamily}`;
            const textWidth = ctx.measureText(text).width;

            return padding * 2 + textWidth + iconSpace;
        },

        onClick: () => undefined,

        provideEditor: () => ({
            editor: DatePickerEditor,
            disablePadding: true,
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, date: null, displayDate: "" }
            }),
        }),

        onPaste: (val, data) => {
            if (!val || !val.trim()) {
                return { ...data, date: null, displayDate: "" };
            }

            const format = data.format || "date";

            // Try parsing as timestamp (milliseconds)
            const timestamp = parseInt(val, 10);
            if (!isNaN(timestamp) && String(timestamp).length > 8) {
                const date = new Date(timestamp);
                if (!isNaN(date.getTime())) {
                    return {
                        ...data,
                        date: date.toISOString(),
                        displayDate: formatDateForDisplay(date.toISOString(), format)
                    };
                }
            }

            // Try parsing as time string (HH:mm or HH:mm:ss)
            if (format === "time" && /^\d{1,2}:\d{2}(:\d{2})?$/.test(val)) {
                return {
                    ...data,
                    date: val,
                    displayDate: val
                };
            }

            // Try parsing as ISO date string
            try {
                const date = new Date(val);
                if (!isNaN(date.getTime())) {
                    return {
                        ...data,
                        date: date.toISOString(),
                        displayDate: formatDateForDisplay(date.toISOString(), format)
                    };
                }
            } catch {
                // Fall through
            }

            return data;
        }
    };
}

export default createDatePickerCellRenderer;
