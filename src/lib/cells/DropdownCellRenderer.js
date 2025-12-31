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
import { getMiddleCenterBias, useTheme, GridCellKind, TextCellEntry } from "@glideapps/glide-data-grid";

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
    } = cell.data;
    const showCheckmark = selectionIndicator === "checkmark" || selectionIndicator === "both" || selectionIndicator === undefined;
    const showHighlight = selectionIndicator === "highlight" || selectionIndicator === "both";
    // When prefillSearch is enabled, pre-populate input with current value so users can edit/filter
    const shouldPrefill = prefillSearch && valueIn && !initialValue;
    const [value, setValue] = React.useState(valueIn);
    const [inputValue, setInputValue] = React.useState(initialValue ?? (shouldPrefill ? valueIn ?? "" : ""));
    const selectRef = React.useRef(null);
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

    const values = React.useMemo(() => {
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

    return React.createElement(
        "div",
        { style: wrapStyle },
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
                option: (base, { isFocused, isSelected }) => ({
                    ...base,
                    fontSize: theme.editorFontSize,
                    fontFamily: theme.fontFamily,
                    color: theme.textDark,
                    cursor: isFocused ? "pointer" : undefined,
                    paddingLeft: theme.cellHorizontalPadding,
                    paddingRight: theme.cellHorizontalPadding,
                    display: "flex",
                    alignItems: "center",
                    backgroundColor: isFocused
                        ? theme.bgBubble
                        : isSelected && showHighlight
                          ? theme.accentLight
                          : "transparent",
                    ":active": {
                        ...base[":active"],
                        color: theme.accentFg,
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
            },
            theme: (t) => {
                return {
                    ...t,
                    colors: {
                        ...t.colors,
                        neutral0: theme.bgCell,
                        neutral5: theme.bgCell,
                        neutral10: theme.bgCell,
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
                        props.label
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

const renderer = {
    kind: GridCellKind.Custom,
    isMatch: (c) => c.data.kind === "dropdown-cell",
    draw: (args, cell) => {
        const { ctx, theme, rect } = args;

        // Skip drawing if row is hidden (height <= 0)
        if (rect.height <= 0) return true;

        const { value, allowCreation, allowedValues = [] } = cell.data;
        const foundOption = allowedValues.find((opt) => {
            if (typeof opt === "string" || opt === null || opt === undefined) {
                return opt === value;
            }
            return opt.value === value;
        });
        // If option found, use its label; otherwise if allowCreation, show the raw value
        const displayText = foundOption
            ? (typeof foundOption === "string" ? foundOption : foundOption?.label ?? "")
            : (allowCreation ? value ?? "" : "");
        if (displayText) {
            ctx.fillStyle = theme.textDark;
            ctx.fillText(
                displayText,
                rect.x + theme.cellHorizontalPadding,
                rect.y + rect.height / 2 + getMiddleCenterBias(ctx, theme)
            );
        }
        return true;
    },
    measure: (ctx, cell, theme) => {
        const { value } = cell.data;
        return (value ? ctx.measureText(value).width : 0) + theme.cellHorizontalPadding * 2;
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
