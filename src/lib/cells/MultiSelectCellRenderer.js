/**
 * Custom MultiSelectCellRenderer with fixed react-select configuration.
 *
 * This is a copy of @glideapps/glide-data-grid-cells multi-select-cell with two critical fixes:
 * - menuPosition="fixed" - positions menu relative to viewport
 * - menuShouldScrollIntoView={false} - prevents browser scroll cascade
 *
 * See docs/dropdown-scroll-issues.md for full context.
 */
import * as React from "react";
import {
    measureTextCached,
    getMiddleCenterBias,
    useTheme,
    GridCellKind,
    roundedRect,
    getLuminance,
} from "@glideapps/glide-data-grid";
import Select, { components } from "react-select";
import CreatableSelect from "react-select/creatable";

/* This prefix is used when allowDuplicates is enabled to make sure that
all underlying values are unique. */
const VALUE_PREFIX = "__value";
const VALUE_PREFIX_REGEX = new RegExp(`^${VALUE_PREFIX}\\d+__`);

const wrapStyle = {
    display: "flex",
    flexDirection: "column",
    height: "100%",
};

const portalWrapStyle = {
    fontFamily: "var(--gdg-font-family)",
    fontSize: "var(--gdg-editor-font-size)",
};

/**
 * Prepares the options for usage with the react-select component.
 */
export const prepareOptions = (options) => {
    return options.map((option) => {
        if (typeof option === "string" || option === null || option === undefined) {
            return {
                value: option,
                label: option ?? "",
                color: undefined,
            };
        }
        return {
            value: option.value,
            label: option.label ?? option.value ?? "",
            color: option.color ?? undefined,
        };
    });
};

/**
 * Resolve a list values to values compatible with react-select.
 * If allowDuplicates is true, the values will be prefixed with a numbered prefix to
 * make sure that all values are unique.
 */
export const resolveValues = (values, options, allowDuplicates) => {
    if (values === undefined || values === null) {
        return [];
    }
    return values.map((value, index) => {
        const valuePrefix = allowDuplicates ? `${VALUE_PREFIX}${index}__` : "";
        const matchedOption = options.find((option) => {
            return option.value === value;
        });
        if (matchedOption) {
            return {
                ...matchedOption,
                value: `${valuePrefix}${matchedOption.value}`,
            };
        }
        return {
            value: `${valuePrefix}${value}`,
            label: value,
        };
    });
};

const CustomMenu = (p) => {
    const { Menu } = components;
    const { children, ...rest } = p;
    return React.createElement(Menu, { ...rest }, children);
};

const Editor = (p) => {
    const { value: cell, initialValue, onChange, onFinishedEditing, portalElementRef } = p;
    const { options: optionsIn, values: valuesIn, allowCreation, allowDuplicates } = cell.data;
    const theme = useTheme();
    const [value, setValue] = React.useState(valuesIn);
    const [menuOpen, setMenuOpen] = React.useState(true);
    const [inputValue, setInputValue] = React.useState(initialValue ?? "");

    const options = React.useMemo(() => {
        return prepareOptions(optionsIn ?? []);
    }, [optionsIn]);

    const menuDisabled = allowCreation && allowDuplicates && options.length === 0;

    // Prevent the grid from handling the keydown as long as the menu is open
    const onKeyDown = React.useCallback(
        (e) => {
            if (menuOpen) {
                e.stopPropagation();
            }
        },
        [menuOpen]
    );

    // Apply styles to the react-select component
    const colorStyles = {
        control: (base, state) => ({
            ...base,
            border: 0,
            boxShadow: "none",
            backgroundColor: theme.bgCell,
            pointerEvents: state.isDisabled ? "auto" : base.pointerEvents,
            cursor: state.isDisabled ? "default" : base.cursor,
        }),
        valueContainer: (base) => ({
            ...base,
            flexWrap: base.flexWrap ?? "wrap",
            overflowX: "auto",
            overflowY: "hidden",
        }),
        menu: (styles) => ({
            ...styles,
            backgroundColor: theme.bgCell,
        }),
        option: (styles, state) => {
            return {
                ...styles,
                fontSize: theme.editorFontSize,
                fontFamily: theme.fontFamily,
                color: theme.textDark,
                ...(state.isFocused
                    ? {
                          backgroundColor: theme.accentLight,
                          cursor: "pointer",
                      }
                    : {}),
                ":active": {
                    ...styles[":active"],
                    color: theme.accentFg,
                    backgroundColor: theme.accentColor,
                },
            };
        },
        input: (styles, { isDisabled }) => {
            if (isDisabled) {
                return { display: "none" };
            }
            return {
                ...styles,
                fontSize: theme.editorFontSize,
                fontFamily: theme.fontFamily,
                color: theme.textDark,
            };
        },
        placeholder: (styles) => {
            return {
                ...styles,
                fontSize: theme.editorFontSize,
                fontFamily: theme.fontFamily,
                color: theme.textLight,
            };
        },
        noOptionsMessage: (styles) => {
            return {
                ...styles,
                fontSize: theme.editorFontSize,
                fontFamily: theme.fontFamily,
                color: theme.textLight,
            };
        },
        clearIndicator: (styles) => {
            return {
                ...styles,
                color: theme.textLight,
                ":hover": {
                    color: theme.textDark,
                    cursor: "pointer",
                },
            };
        },
        multiValue: (styles, { data }) => {
            return {
                ...styles,
                backgroundColor: data.color ?? theme.bgBubble,
                borderRadius: `${theme.roundingRadius ?? theme.bubbleHeight / 2}px`,
                flexShrink: 0,
                whiteSpace: "nowrap",
            };
        },
        multiValueLabel: (styles, { data, isDisabled }) => {
            return {
                ...styles,
                paddingRight: isDisabled ? theme.bubblePadding : 0,
                paddingLeft: theme.bubblePadding,
                paddingTop: 0,
                paddingBottom: 0,
                color: data.color
                    ? getLuminance(data.color) > 0.5
                        ? "black"
                        : "white"
                    : theme.textBubble,
                fontSize: theme.editorFontSize,
                fontFamily: theme.fontFamily,
                justifyContent: "center",
                alignItems: "center",
                display: "flex",
                height: theme.bubbleHeight,
                whiteSpace: "nowrap",
            };
        },
        multiValueRemove: (styles, { data, isDisabled, isFocused }) => {
            if (isDisabled) {
                return { display: "none" };
            }
            return {
                ...styles,
                color: data.color
                    ? getLuminance(data.color) > 0.5
                        ? "black"
                        : "white"
                    : theme.textBubble,
                backgroundColor: undefined,
                borderRadius: isFocused ? `${theme.roundingRadius ?? theme.bubbleHeight / 2}px` : undefined,
                ":hover": {
                    cursor: "pointer",
                },
            };
        },
    };

    // This is used to submit the values to the grid
    const submitValues = React.useCallback(
        (values) => {
            const mappedValues = values.map((v) => {
                return allowDuplicates && v.startsWith(VALUE_PREFIX)
                    ? v.replace(new RegExp(VALUE_PREFIX_REGEX), "")
                    : v;
            });
            setValue(mappedValues);
            onChange({
                ...cell,
                data: {
                    ...cell.data,
                    values: mappedValues,
                },
            });
        },
        [cell, onChange, allowDuplicates]
    );

    const handleKeyDown = (event) => {
        switch (event.key) {
            case "Enter":
            case "Tab":
                if (!inputValue) {
                    onFinishedEditing(cell, [0, 1]);
                    return;
                }
                if (allowDuplicates && allowCreation) {
                    setInputValue("");
                    submitValues([...(value ?? []), inputValue]);
                    setMenuOpen(false);
                    event.preventDefault();
                }
        }
    };

    const SelectComponent = allowCreation ? CreatableSelect : Select;

    return React.createElement(
        "div",
        { style: wrapStyle, onKeyDown: onKeyDown, "data-testid": "multi-select-cell" },
        React.createElement(SelectComponent, {
            className: "gdg-multi-select",
            isMulti: true,
            isDisabled: cell.readonly,
            isClearable: true,
            isSearchable: true,
            inputValue: inputValue,
            onInputChange: setInputValue,
            options: options,
            placeholder: cell.readonly ? "" : allowCreation ? "Add..." : undefined,
            noOptionsMessage: (input) => {
                return allowCreation && allowDuplicates && input.inputValue
                    ? `Create "${input.inputValue}"`
                    : undefined;
            },
            menuIsOpen: cell.readonly ? false : menuOpen,
            onMenuOpen: () => setMenuOpen(true),
            onMenuClose: () => setMenuOpen(false),
            value: resolveValues(value, options, allowDuplicates),
            onKeyDown: cell.readonly ? undefined : handleKeyDown,
            menuPlacement: "auto",
            // FIX: These props prevent scroll issues
            menuPosition: "fixed",
            menuShouldScrollIntoView: false,
            closeMenuOnScroll: false,
            menuPortalTarget: portalElementRef?.current ?? document.getElementById("portal"),
            autoFocus: true,
            openMenuOnFocus: true,
            openMenuOnClick: true,
            closeMenuOnSelect: true,
            backspaceRemovesValue: true,
            escapeClearsValue: false,
            styles: colorStyles,
            components: {
                DropdownIndicator: () => null,
                IndicatorSeparator: () => null,
                Menu: (props) => {
                    if (menuDisabled) {
                        return null;
                    }
                    return React.createElement(
                        "div",
                        { style: portalWrapStyle },
                        React.createElement(CustomMenu, {
                            className: "click-outside-ignore",
                            ...props,
                        })
                    );
                },
            },
            onChange: async (e) => {
                if (e === null) {
                    return;
                }
                submitValues(e.map((x) => x.value));
            },
        })
    );
};

const renderer = {
    kind: GridCellKind.Custom,
    isMatch: (c) => c.data.kind === "multi-select-cell",
    draw: (args, cell) => {
        const { ctx, theme, rect, highlighted } = args;
        const { values, options: optionsIn } = cell.data;
        if (values === undefined || values === null) {
            return true;
        }
        const options = prepareOptions(optionsIn ?? []);
        const drawArea = {
            x: rect.x + theme.cellHorizontalPadding,
            y: rect.y + theme.cellVerticalPadding,
            width: rect.width - 2 * theme.cellHorizontalPadding,
            height: rect.height - 2 * theme.cellVerticalPadding,
        };
        const rows = Math.max(1, Math.floor(drawArea.height / (theme.bubbleHeight + theme.bubblePadding)));
        let { x } = drawArea;
        let row = 1;
        let y =
            rows === 1
                ? drawArea.y + (drawArea.height - theme.bubbleHeight) / 2
                : drawArea.y +
                  (drawArea.height - rows * theme.bubbleHeight - (rows - 1) * theme.bubblePadding) / 2;
        for (const value of values) {
            const matchedOption = options.find((t) => t.value === value);
            const color = matchedOption?.color ?? (highlighted ? theme.bgBubbleSelected : theme.bgBubble);
            const displayText = matchedOption?.label ?? value;
            const metrics = measureTextCached(displayText, ctx);
            const width = metrics.width + theme.bubblePadding * 2;
            const textY = theme.bubbleHeight / 2;
            if (x !== drawArea.x && x + width > drawArea.x + drawArea.width && row < rows) {
                row++;
                y += theme.bubbleHeight + theme.bubblePadding;
                x = drawArea.x;
            }
            ctx.fillStyle = color;
            ctx.beginPath();
            roundedRect(ctx, x, y, width, theme.bubbleHeight, theme.roundingRadius ?? theme.bubbleHeight / 2);
            ctx.fill();
            ctx.fillStyle = matchedOption?.color
                ? getLuminance(color) > 0.5
                    ? "#000000"
                    : "#ffffff"
                : theme.textBubble;
            ctx.fillText(displayText, x + theme.bubblePadding, y + textY + getMiddleCenterBias(ctx, theme));
            x += width + theme.bubbleMargin;
            if (x > drawArea.x + drawArea.width + theme.cellHorizontalPadding && row >= rows) {
                break;
            }
        }
        return true;
    },
    measure: (ctx, cell, theme) => {
        const { values, options } = cell.data;
        if (!values) {
            return theme.cellHorizontalPadding * 2;
        }
        const labels = resolveValues(values, prepareOptions(options ?? []), cell.data.allowDuplicates).map(
            (x) => x.label ?? x.value
        );
        const bubblesWidth = labels.reduce(
            (acc, data) => ctx.measureText(data).width + acc + theme.bubblePadding * 2 + theme.bubbleMargin,
            0
        );
        if (labels.length === 0) {
            return theme.cellHorizontalPadding * 2;
        }
        return bubblesWidth + 2 * theme.cellHorizontalPadding - theme.bubbleMargin;
    },
    provideEditor: () => ({
        editor: Editor,
        disablePadding: true,
        deletedValue: (v) => ({
            ...v,
            copyData: "",
            data: {
                ...v.data,
                values: [],
            },
        }),
    }),
    onPaste: (val, cell) => {
        if (!val || !val.trim()) {
            return {
                ...cell,
                values: [],
            };
        }
        let values = val.split(",").map((s) => s.trim());
        if (!cell.allowDuplicates) {
            values = values.filter((v, index) => values.indexOf(v) === index);
        }
        if (!cell.allowCreation) {
            const options = prepareOptions(cell.options ?? []);
            values = values.filter((v) => options.find((o) => o.value === v));
        }
        if (values.length === 0) {
            return undefined;
        }
        return {
            ...cell,
            values,
        };
    },
};

export default renderer;
