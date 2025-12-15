/**
 * Custom TagsCellRenderer for Dash integration.
 *
 * Displays colored tags as pill-shaped badges with an editable checkbox dropdown.
 *
 * Data structure:
 * {
 *   kind: "tags-cell",
 *   tags: ["Feature", "Assigned"],           // Currently selected tag names
 *   possibleTags: [                          // All available options with colors
 *     { tag: "Bug", color: "#ef4444" },
 *     { tag: "Feature", color: "#8b5cf6" },
 *     { tag: "Assigned", color: "#22c55e" }
 *   ],
 *   readonly: false                          // Optional
 * }
 */
import { useCallback } from "react";
import { GridCellKind } from "@glideapps/glide-data-grid";

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
 * Get contrasting text color (white or black) based on background
 */
function getContrastColor(hexColor) {
    if (!hexColor) return "#ffffff";
    const hex = hexColor.replace("#", "");
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    return luminance > 0.5 ? "#000000" : "#ffffff";
}

/**
 * Editor component for tags cell - shows checkboxes for each possible tag
 */
function TagsEditor({ value, onChange }) {
    const { tags = [], possibleTags = [], readonly } = value.data;

    const handleToggle = useCallback((tagName) => {
        if (readonly) return;

        const currentTags = new Set(tags);
        if (currentTags.has(tagName)) {
            currentTags.delete(tagName);
        } else {
            currentTags.add(tagName);
        }

        onChange({
            ...value,
            data: {
                ...value.data,
                tags: Array.from(currentTags)
            }
        });
    }, [tags, readonly, value, onChange]);

    if (possibleTags.length === 0) {
        return (
            <div style={{ padding: 8, color: "#6b7280", fontSize: 13 }}>
                No options defined
            </div>
        );
    }

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            padding: 8,
            gap: 2,
            minWidth: 150,
        }}>
            {possibleTags.map((tagOption) => {
                const isSelected = tags.includes(tagOption.tag);
                const tagColor = tagOption.color || "#6b7280";

                return (
                    <label
                        key={tagOption.tag}
                        style={{
                            display: "flex",
                            alignItems: "center",
                            gap: 8,
                            padding: "4px 8px",
                            borderRadius: 6,
                            cursor: readonly ? "default" : "pointer",
                        }}
                    >
                        {!readonly && (
                            <input
                                type="checkbox"
                                checked={isSelected}
                                onChange={() => handleToggle(tagOption.tag)}
                                style={{
                                    width: 16,
                                    height: 16,
                                    accentColor: tagColor,
                                    cursor: "pointer",
                                }}
                            />
                        )}
                        <span
                            className="tags-cell-pill"
                            style={{
                                display: "inline-block",
                                padding: "2px 10px",
                                borderRadius: 10,
                                backgroundColor: isSelected ? tagColor : "transparent",
                                color: isSelected ? getContrastColor(tagColor) : tagColor,
                                fontSize: 13,
                                fontWeight: 500,
                                opacity: isSelected ? 1 : 0.8,
                                transition: "all 0.15s",
                                boxShadow: readonly ? "none" : undefined,
                            }}
                            onMouseEnter={(e) => {
                                if (!readonly) {
                                    e.currentTarget.style.boxShadow = "0 1px 4px rgba(0, 0, 0, 0.15)";
                                }
                            }}
                            onMouseLeave={(e) => {
                                if (!readonly) {
                                    e.currentTarget.style.boxShadow = "none";
                                }
                            }}
                        >
                            {tagOption.tag}
                        </span>
                    </label>
                );
            })}
        </div>
    );
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
            const { tags = [], possibleTags = [] } = cell.data;

            // Build a map of tag -> color from possibleTags
            const colorMap = new Map();
            for (const pt of possibleTags) {
                colorMap.set(pt.tag, pt.color);
            }

            if (tags.length === 0) {
                return true;
            }

            const padding = theme.cellHorizontalPadding;
            const tagHeight = 20;
            const tagPaddingX = 8;
            const tagSpacing = 6;
            const tagRadius = tagHeight / 2;

            const startY = rect.y + (rect.height - tagHeight) / 2;
            const availableWidth = rect.width - padding * 2;

            ctx.font = `12px ${theme.fontFamily}`;
            ctx.textBaseline = "middle";

            // Pre-calculate tag widths
            const tagWidths = tags.map(tagName => {
                const textWidth = ctx.measureText(tagName).width;
                return textWidth + tagPaddingX * 2;
            });

            // Calculate total width needed
            const totalWidth = tagWidths.reduce((sum, w) => sum + w + tagSpacing, 0) - tagSpacing;

            // Determine if we need overflow indicator
            let tagsToShow = tags.length;
            let showOverflow = false;
            let overflowCount = 0;

            if (totalWidth > availableWidth) {
                // Calculate how many tags fit with overflow indicator
                // Reserve space for "+N" badge (estimate max width for "+99")
                const overflowBadgeWidth = ctx.measureText("+99").width + tagPaddingX * 2;
                const maxWidthWithOverflow = availableWidth - overflowBadgeWidth - tagSpacing;

                let usedWidth = 0;
                tagsToShow = 0;

                for (let i = 0; i < tags.length; i++) {
                    const newWidth = usedWidth + tagWidths[i] + (i > 0 ? tagSpacing : 0);
                    if (newWidth <= maxWidthWithOverflow) {
                        usedWidth = newWidth;
                        tagsToShow++;
                    } else {
                        break;
                    }
                }

                // Ensure at least some indication if no tags fit
                if (tagsToShow === 0 && tags.length > 0) {
                    tagsToShow = 0;
                }

                overflowCount = tags.length - tagsToShow;
                showOverflow = overflowCount > 0;
            }

            // Draw visible tags
            let currentX = rect.x + padding;
            const currentY = startY;

            for (let i = 0; i < tagsToShow; i++) {
                const tagName = tags[i];
                const tagColor = colorMap.get(tagName) || theme.accentColor || "#6b7280";
                const tagWidth = tagWidths[i];

                roundRect(ctx, currentX, currentY, tagWidth, tagHeight, tagRadius);
                ctx.fillStyle = tagColor;
                ctx.fill();

                const textColor = getContrastColor(tagColor);
                ctx.fillStyle = textColor;
                ctx.textAlign = "center";
                ctx.fillText(tagName, currentX + tagWidth / 2, currentY + tagHeight / 2);

                currentX += tagWidth + tagSpacing;
            }

            // Draw overflow indicator
            if (showOverflow) {
                const overflowText = `+${overflowCount}`;
                const overflowTextWidth = ctx.measureText(overflowText).width;
                const overflowWidth = overflowTextWidth + tagPaddingX * 2;

                // Use theme colors for light/dark mode compatibility
                const overflowBgColor = theme.bgBubble || theme.bgCellMedium || "#e5e7eb";
                const overflowTextColor = theme.textMedium || theme.textDark || "#6b7280";

                roundRect(ctx, currentX, currentY, overflowWidth, tagHeight, tagRadius);
                ctx.fillStyle = overflowBgColor;
                ctx.fill();

                ctx.fillStyle = overflowTextColor;
                ctx.textAlign = "center";
                ctx.fillText(overflowText, currentX + overflowWidth / 2, currentY + tagHeight / 2);
            }

            ctx.textAlign = "start";
            return true;
        },

        measure: (ctx, cell, theme) => {
            const { tags = [] } = cell.data;
            if (tags.length === 0) {
                return 50;
            }

            ctx.font = `12px ${theme.fontFamily}`;
            const tagPaddingX = 8;
            const tagSpacing = 6;

            let totalWidth = theme.cellHorizontalPadding;
            for (const tagName of tags) {
                const textWidth = ctx.measureText(tagName).width;
                totalWidth += textWidth + tagPaddingX * 2 + tagSpacing;
            }

            return totalWidth + theme.cellHorizontalPadding;
        },

        onClick: () => undefined,

        provideEditor: () => ({
            editor: TagsEditor,
            disablePadding: true,
            deletedValue: (v) => ({
                ...v,
                data: { ...v.data, tags: [] }
            }),
        }),

        onPaste: (val, data) => {
            // Parse comma-separated tags, only keep those in possibleTags
            const possibleTagNames = new Set((data.possibleTags || []).map(pt => pt.tag));
            const newTags = val
                .split(",")
                .map(t => t.trim())
                .filter(t => t && possibleTagNames.has(t));
            return {
                ...data,
                tags: newTags
            };
        }
    };
}

export default createTagsCellRenderer;
