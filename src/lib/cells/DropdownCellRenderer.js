/**
 * Custom DropdownCellRenderer with fixed react-select configuration.
 *
 * This is a copy of @glideapps/glide-data-grid-cells dropdown-cell with two critical fixes:
 * - menuPosition="fixed" - positions menu relative to viewport
 * - menuShouldScrollIntoView={false} - prevents browser scroll cascade
 *
 * See docs/dropdown-scroll-issues.md for full context.
 */
import * as React from "react";
import Select, { components } from "react-select";
import CreatableSelect from "react-select/creatable";
import {
    getMiddleCenterBias,
    useTheme,
    GridCellKind,
    TextCellEntry,
    roundedRect,
    getLuminance,
    measureTextCached,
} from "@glideapps/glide-data-grid";

// Module-level image cache for icons and images rendered on the canvas
const imageCache = new Map();
function loadCachedImage(src) {
    if (imageCache.has(src)) return imageCache.get(src);
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = src;
    imageCache.set(src, null); // mark as loading
    img.onload = () => imageCache.set(src, img);
    img.onerror = () => imageCache.set(src, false);
    return null;
}

const ICON_SIZE = 16;
const ICON_GAP = 6;

const CustomMenu = (p) => {
    const { Menu } = components;
    const { children, ...rest } = p;
    return React.createElement(Menu, { ...rest }, children);
};

const wrapStyle = {
    display: "flex",
    flexDirection: "column",
    height: "100%",
};

const portalWrapStyle = {
    fontFamily: "var(--gdg-font-family)",
    fontSize: "var(--gdg-editor-font-size)",
};

const readOnlyWrapStyle = {
    display: "flex",
    alignItems: "center",
    height: "100%",
    padding: "0 8.5px",
};

const Editor = (p) => {
    const { value: cell, onFinishedEditing, initialValue, portalElementRef } = p;
    const {
        allowedValues,
        value: valueIn,
        isClearable,
        isSearchable,
        placeholder,
        maxMenuHeight,
        menuPlacement,
        hideSelectedOptions,
        selectionIndicator,
        allowCreation,
        prefillSearch,
        placement,
    } = cell.data;
    const showCheckmark = selectionIndicator === "checkmark" || selectionIndicator === "both" || selectionIndicator === undefined;
    const showHighlight = selectionIndicator === "highlight" || selectionIndicator === "both";
    // When prefillSearch is enabled, pre-populate input with current value so users can edit/filter
    const shouldPrefill = prefillSearch && valueIn && !initialValue;
    const [value, setValue] = React.useState(valueIn);
    const [inputValue, setInputValue] = React.useState(initialValue ?? (shouldPrefill ? valueIn ?? "" : ""));
    const selectRef = React.useRef(null);
    const wrapRef = React.useRef(null);
    const theme = useTheme();

    // Auto-select all text when opening editor with pre-populated value
    React.useEffect(() => {
        if (shouldPrefill && selectRef.current) {
            // Small delay to ensure input is mounted and focused
            const timer = setTimeout(() => {
                const input = selectRef.current?.inputRef;
                if (input) {
                    input.select();
                }
            }, 0);
            return () => clearTimeout(timer);
        }
    }, []);

    // Reposition overlay container when placement is specified
    React.useEffect(() => {
        if (!placement || !wrapRef.current) return;
        const overlay = wrapRef.current.closest('[class*="d19meir1"]');
        if (!overlay) return;
        const cellWidth = p.target?.width ?? 0;
        const cellHeight = p.target?.height ?? 0;
        overlay.style.minHeight = "auto";
        // Constrain overlay width to cell width so it doesn't overflow right edge
        if (cellWidth > 0) {
            overlay.style.maxWidth = `${cellWidth}px`;
        }
        if (placement === "below") {
            overlay.style.transform = `translateY(${cellHeight}px)`;
        } else if (placement === "above") {
            overlay.style.transform = "translateY(-100%)";
        }
    }, []);

    const values = React.useMemo(() => {
        // Guard against undefined allowedValues
        if (!allowedValues || !Array.isArray(allowedValues)) {
            console.warn('[DropdownCellRenderer] allowedValues is not an array:', allowedValues);
            return [];
        }
        return allowedValues.map((option) => {
            if (typeof option === "string" || option === null || option === undefined) {
                return {
                    value: option,
                    label: option?.toString() ?? "",
                };
            }
            return option;
        });
    }, [allowedValues]);

    const SelectComponent = allowCreation ? CreatableSelect : Select;

    if (cell.readonly) {
        return React.createElement(
            "div",
            { style: readOnlyWrapStyle },
            React.createElement(TextCellEntry, {
                highlight: true,
                autoFocus: false,
                disabled: true,
                value: value ?? "",
                onChange: () => undefined,
            })
        );
    }

    // Check if any option has a visual (image, emoji, or icon) — enables formatOptionLabel
    const hasVisuals = values.some((v) => v.image || v.emoji || v.icon);

    return React.createElement(
        "div",
        { style: wrapStyle, ref: wrapRef },
        React.createElement(SelectComponent, {
            ref: selectRef,
            className: "glide-select",
            inputValue: inputValue,
            onInputChange: setInputValue,
            isClearable: isClearable ?? false,
            isSearchable: isSearchable ?? true,
            placeholder: placeholder ?? (allowCreation ? "Type to search or create..." : "Select..."),
            maxMenuHeight: maxMenuHeight ?? 300,
            menuPlacement: menuPlacement ?? "auto",
            hideSelectedOptions: hideSelectedOptions ?? false,
            controlShouldRenderValue: !shouldPrefill,
            noOptionsMessage: allowCreation ? () => null : () => "No matches",
            // FIX: These props prevent scroll issues
            menuPosition: "fixed",
            menuShouldScrollIntoView: false,
            closeMenuOnScroll: false,
            value: values.find((x) => x.value === value),
            styles: {
                control: (base) => ({
                    ...base,
                    border: 0,
                    boxShadow: "none",
                }),
                option: (base, { isSelected }) => ({
                    ...base,
                    fontSize: theme.editorFontSize,
                    fontFamily: theme.fontFamily,
                    color: theme.textDark,
                    cursor: "pointer",
                    paddingLeft: theme.cellHorizontalPadding,
                    paddingRight: theme.cellHorizontalPadding,
                    display: "flex",
                    alignItems: "center",
                    backgroundColor: isSelected && showHighlight ? theme.accentLight : "transparent",
                    ":hover": {
                        backgroundColor: theme.bgBubble,
                    },
                    ":active": {
                        ...base[":active"],
                        backgroundColor: theme.bgBubble,
                    },
                    ":empty::after": {
                        content: '"&nbsp;"',
                        visibility: "hidden",
                    },
                }),
                clearIndicator: (styles) => ({
                    ...styles,
                    color: theme.textLight,
                    ":hover": {
                        color: theme.textDark,
                        cursor: "pointer",
                    },
                }),
                placeholder: (styles) => ({
                    ...styles,
                    fontSize: theme.editorFontSize,
                    fontFamily: theme.fontFamily,
                    color: theme.textLight,
                }),
                noOptionsMessage: (styles) => ({
                    ...styles,
                    fontSize: theme.editorFontSize,
                    fontFamily: theme.fontFamily,
                    color: theme.textLight,
                    textAlign: "center",
                    padding: "8px 12px",
                }),
                menuPortal: (base) => {
                    // Prevent menu from overflowing viewport right edge
                    const menuWidth = base.width || 300;
                    const maxLeft = window.innerWidth - menuWidth - 8;
                    return {
                        ...base,
                        left: Math.min(base.left ?? 0, maxLeft),
                    };
                },
            },
            theme: (t) => {
                return {
                    ...t,
                    colors: {
                        ...t.colors,
                        neutral0: theme.bgCellEditor || theme.bgCell,
                        neutral5: theme.bgCellEditor || theme.bgCell,
                        neutral10: theme.bgCellEditor || theme.bgCell,
                        neutral20: theme.bgCellMedium,
                        neutral30: theme.bgCellMedium,
                        neutral40: theme.bgCellMedium,
                        neutral50: theme.textLight,
                        neutral60: theme.textMedium,
                        neutral70: theme.textMedium,
                        neutral80: theme.textDark,
                        neutral90: theme.textDark,
                        neutral100: theme.textDark,
                        primary: theme.accentColor,
                        primary75: theme.accentColor,
                        primary50: theme.accentColor,
                        primary25: theme.accentLight,
                    },
                };
            },
            menuPortalTarget: portalElementRef?.current ?? document.getElementById("portal"),
            formatOptionLabel: hasVisuals
                ? (option) => {
                      const visual = option.image || option.emoji || option.icon;
                      if (!visual) return option.label;
                      const iconStyle = { width: 24, height: 24, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, borderRadius: "4px" };
                      let iconEl;
                      if (option.image) {
                          iconEl = React.createElement("img", {
                              src: option.image,
                              width: 24,
                              height: 24,
                              style: { objectFit: "contain", borderRadius: "4px", flexShrink: 0 },
                          });
                      } else if (option.icon) {
                          // Iconify API: "mdi:dice-6" → "mdi/dice-6"
                          const src = "https://api.iconify.design/" + option.icon.replace(":", "/") + ".svg";
                          iconEl = React.createElement("img", {
                              src: src,
                              width: 24,
                              height: 24,
                              style: { objectFit: "contain", flexShrink: 0 },
                          });
                      } else {
                          // Emoji rendered at matching size
                          iconEl = React.createElement("span", {
                              style: { ...iconStyle, fontSize: "20px", lineHeight: 1 },
                          }, option.emoji);
                      }
                      return React.createElement(
                          "div",
                          { style: { display: "flex", alignItems: "center", gap: "8px" } },
                          iconEl,
                          option.label
                      );
                  }
                : undefined,
            autoFocus: true,
            openMenuOnFocus: true,
            components: {
                DropdownIndicator: () => null,
                IndicatorSeparator: () => null,
                Option: (props) => {
                    const { Option } = components;
                    return React.createElement(
                        Option,
                        { ...props },
                        props.isSelected && showCheckmark
                            ? React.createElement(
                                  "svg",
                                  {
                                      width: "14",
                                      height: "14",
                                      viewBox: "0 0 24 24",
                                      fill: "none",
                                      stroke: theme.textLight,
                                      strokeWidth: "4",
                                      strokeLinecap: "round",
                                      strokeLinejoin: "round",
                                      style: { marginRight: "6px", flexShrink: 0 },
                                  },
                                  React.createElement("polyline", { points: "20 6 9 17 4 12" })
                              )
                            : null,
                        props.children
                    );
                },
                Menu: (props) =>
                    React.createElement(
                        "div",
                        { style: portalWrapStyle },
                        React.createElement(CustomMenu, {
                            className: "click-outside-ignore",
                            ...props,
                        })
                    ),
            },
            options: values,
            onChange: async (e) => {
                const newValue = e === null ? "" : e.value;
                setValue(newValue);
                await new Promise((r) => window.requestAnimationFrame(r));
                onFinishedEditing({
                    ...cell,
                    data: {
                        ...cell.data,
                        value: newValue,
                    },
                });
            },
        })
    );
};

function drawVisual(ctx, emoji, iconId, imageUrl, color, x, y, textY) {
    if (emoji) {
        // Draw emoji at the same baseline as the label text
        ctx.fillStyle = color;
        ctx.fillText(emoji, x, textY);
    } else if (iconId) {
        const hexColor = encodeURIComponent(color);
        const src = `https://api.iconify.design/${iconId.replace(":", "/")}.svg?color=${hexColor}`;
        const img = loadCachedImage(src);
        if (img) ctx.drawImage(img, x, y, ICON_SIZE, ICON_SIZE);
    } else if (imageUrl) {
        const img = loadCachedImage(imageUrl);
        if (img) ctx.drawImage(img, x, y, ICON_SIZE, ICON_SIZE);
    }
}

const renderer = {
    kind: GridCellKind.Custom,
    isMatch: (c) => c.data.kind === "dropdown-cell",
    draw: (args, cell) => {
        const { ctx, theme, rect, highlighted } = args;

        // Skip drawing if row is hidden (height <= 0)
        if (rect.height <= 0) return true;

        const { value, allowCreation, allowedValues = [], showBubble } = cell.data;

        // Find matching option
        const foundOption = allowedValues.find((opt) => {
            if (typeof opt === "string" || opt === null || opt === undefined) {
                return opt === value;
            }
            return opt.value === value;
        });

        // If option found, use its label; otherwise if allowCreation, show the raw value
        const displayText = foundOption
            ? typeof foundOption === "string"
                ? foundOption
                : (foundOption?.label ?? "")
            : allowCreation
              ? (value ?? "")
              : "";

        if (!displayText) return true;

        // Check for visual (emoji, icon, or image) on the matched option
        const emoji = typeof foundOption === "object" ? foundOption.emoji : undefined;
        const iconId = typeof foundOption === "object" ? foundOption.icon : undefined;
        const imageUrl = typeof foundOption === "object" ? foundOption.image : undefined;
        const hasVisual = !!(emoji || iconId || imageUrl);
        const visualOffset = hasVisual ? ICON_SIZE + ICON_GAP : 0;

        if (showBubble) {
            // Get color from option or use theme default
            const bubbleColor =
                typeof foundOption === "object" && foundOption?.color
                    ? foundOption.color
                    : highlighted
                      ? theme.bgBubbleSelected
                      : theme.bgBubble;

            // Calculate bubble dimensions
            const metrics = measureTextCached(displayText, ctx);
            const bubbleWidth = visualOffset + metrics.width + theme.bubblePadding * 2;
            const bubbleHeight = theme.bubbleHeight;
            const x = rect.x + theme.cellHorizontalPadding;
            const y = rect.y + (rect.height - bubbleHeight) / 2;

            // Draw bubble background
            ctx.fillStyle = bubbleColor;
            ctx.beginPath();
            roundedRect(ctx, x, y, bubbleWidth, bubbleHeight, theme.roundingRadius ?? bubbleHeight / 2);
            ctx.fill();

            const textColor = getLuminance(bubbleColor) > 0.5 ? "#000000" : "#ffffff";
            const textY = y + bubbleHeight / 2 + getMiddleCenterBias(ctx, theme);

            // Draw visual inside bubble
            if (hasVisual) {
                const vx = x + theme.bubblePadding;
                const vy = y + (bubbleHeight - ICON_SIZE) / 2;
                drawVisual(ctx, emoji, iconId, imageUrl, textColor, vx, vy, textY);
            }

            // Draw text with smart contrast based on actual background color
            ctx.fillStyle = textColor;
            ctx.fillText(displayText, x + theme.bubblePadding + visualOffset, textY);
        } else {
            const x = rect.x + theme.cellHorizontalPadding;
            const textY = rect.y + rect.height / 2 + getMiddleCenterBias(ctx, theme);

            // Draw visual before text
            if (hasVisual) {
                const vy = rect.y + (rect.height - ICON_SIZE) / 2;
                drawVisual(ctx, emoji, iconId, imageUrl, theme.textDark, x, vy, textY);
            }

            // Default text rendering
            ctx.fillStyle = theme.textDark;
            ctx.fillText(displayText, x + visualOffset, textY);
        }
        return true;
    },
    measure: (ctx, cell, theme) => {
        const { value, allowedValues = [], showBubble } = cell.data;
        const textWidth = value ? ctx.measureText(value).width : 0;
        const foundOption = allowedValues.find((opt) =>
            typeof opt === "object" && opt !== null ? opt.value === value : opt === value
        );
        const hasVisual = typeof foundOption === "object" && (foundOption.emoji || foundOption.icon || foundOption.image);
        const visualOffset = hasVisual ? ICON_SIZE + ICON_GAP : 0;
        if (showBubble) {
            return visualOffset + textWidth + theme.bubblePadding * 2 + theme.cellHorizontalPadding * 2;
        }
        return visualOffset + textWidth + theme.cellHorizontalPadding * 2;
    },
    provideEditor: () => ({
        editor: Editor,
        disablePadding: true,
        deletedValue: (v) => ({
            ...v,
            copyData: "",
            data: {
                ...v.data,
                value: "",
            },
        }),
    }),
    onPaste: (v, cell) => {
        // cell is the full cell object: {kind, data, copyData}
        // data contains: {value, allowedValues, allowCreation, ...}
        const d = cell.data;

        // If allowCreation is enabled, accept any pasted value
        if (d.allowCreation) {
            return {
                ...cell,
                copyData: v,
                data: { ...d, value: v },
            };
        }

        // Otherwise, only accept if value is in allowedValues
        const isValid = d.allowedValues?.some((option) => {
            if (option === null || option === undefined) return false;
            if (typeof option === "string") return option === v;
            return option.value === v;
        });

        if (!isValid) return undefined; // reject paste

        return {
            ...cell,
            copyData: v,
            data: { ...d, value: v },
        };
    },
};

export default renderer;
