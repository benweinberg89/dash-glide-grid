/**
 * Custom StarCellRenderer for Dash integration.
 *
 * Displays a star rating (e.g., 1-5 stars) with editable dropdown.
 *
 * Data structure:
 * {
 *   kind: "star-cell",
 *   rating: 4,        // Current rating (0 to maxStars)
 *   maxStars: 5       // Optional, defaults to 5
 * }
 */
import { useCallback, useEffect } from "react";
import { GridCellKind } from "@glideapps/glide-data-grid";

/**
 * Draw a 5-pointed star on canvas
 */
function drawStar(ctx, cx, cy, outerRadius, innerRadius) {
    const points = 5;
    const step = Math.PI / points;

    ctx.beginPath();
    for (let i = 0; i < 2 * points; i++) {
        const radius = i % 2 === 0 ? outerRadius : innerRadius;
        const angle = i * step - Math.PI / 2;
        const x = cx + Math.cos(angle) * radius;
        const y = cy + Math.sin(angle) * radius;
        if (i === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    }
    ctx.closePath();
}

/**
 * Editor component for star cell - shows clickable stars
 */
function StarEditor({ value, onChange, onFinishedEditing }) {
    const { rating = 0, maxStars = 5, readonly } = value.data;

    // Handle Escape key to close editor
    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                onFinishedEditing(value, [0, 0]);
            }
        };
        document.addEventListener('keydown', handleKeyDown);
        return () => document.removeEventListener('keydown', handleKeyDown);
    }, [value, onFinishedEditing]);

    const handleClick = useCallback((newRating) => {
        if (readonly) return;

        onChange({
            ...value,
            data: {
                ...value.data,
                rating: newRating
            }
        });
    }, [readonly, value, onChange]);

    return (
        <div style={{
            display: "flex",
            alignItems: "center",
            padding: "8px 12px",
            gap: 4,
        }}>
            {Array.from({ length: maxStars }).map((_, i) => {
                const starIndex = i + 1;
                const isFilled = starIndex <= rating;

                return (
                    <button
                        key={i}
                        onClick={() => handleClick(starIndex === rating ? 0 : starIndex)}
                        disabled={readonly}
                        style={{
                            background: "none",
                            border: "none",
                            padding: 2,
                            cursor: readonly ? "default" : "pointer",
                            fontSize: 20,
                            lineHeight: 1,
                            color: isFilled ? "#fbbf24" : "#d1d5db",
                            transition: "color 0.15s, transform 0.1s",
                        }}
                        onMouseEnter={(e) => {
                            if (!readonly) {
                                e.currentTarget.style.transform = "scale(1.2)";
                            }
                        }}
                        onMouseLeave={(e) => {
                            e.currentTarget.style.transform = "scale(1)";
                        }}
                    >
                        ★
                    </button>
                );
            })}
            <span style={{
                marginLeft: 8,
                fontSize: 13,
                color: "#6b7280",
            }}>
                {rating} / {maxStars}
            </span>
        </div>
    );
}

/**
 * Factory function to create a StarCellRenderer
 */
export function createStarCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "star-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect } = args;
            const { rating = 0, maxStars = 5 } = cell.data;

            const padding = theme.cellHorizontalPadding;
            const starSize = 14;
            const outerRadius = starSize / 2;
            const innerRadius = outerRadius * 0.38; // Proper star shape ratio
            const spacing = 4;

            const startX = rect.x + padding;
            const centerY = rect.y + rect.height / 2;

            // Colors for filled and empty stars
            const filledColor = "#fbbf24"; // Amber/gold
            const emptyColor = theme.bgBubble || "#e5e7eb";

            for (let i = 0; i < maxStars; i++) {
                const starCenterX = startX + i * (starSize + spacing) + starSize / 2;
                const isFilled = i < rating;

                drawStar(ctx, starCenterX, centerY, outerRadius, innerRadius);
                ctx.fillStyle = isFilled ? filledColor : emptyColor;
                ctx.fill();
            }

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { maxStars = 5 } = cell.data;
            const starSize = 14;
            const spacing = 4;
            const padding = theme.cellHorizontalPadding;

            return padding * 2 + maxStars * starSize + (maxStars - 1) * spacing;
        },

        onClick: () => undefined,

        provideEditor: () => ({
            editor: StarEditor,
            disablePadding: true,
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, rating: 0 }
            }),
        }),

        onPaste: (val, data) => {
            const parsed = parseInt(val, 10);
            const maxStars = data.maxStars || 5;
            if (isNaN(parsed)) {
                return data;
            }
            return {
                ...data,
                rating: Math.max(0, Math.min(parsed, maxStars))
            };
        }
    };
}

export default createStarCellRenderer;
