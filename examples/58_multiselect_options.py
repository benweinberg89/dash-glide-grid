"""
Example 58: MultiSelect Cell Options
Demonstrates all configurable options for multi-select cells.
Includes dark/light mode toggle.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Theme configurations
DARK_THEME = {
    "accentColor": "#8b5cf6",
    "accentLight": "rgba(139, 92, 246, 0.2)",
    "bgCell": "#1f2937",
    "bgCellMedium": "#374151",
    "bgHeader": "#111827",
    "bgHeaderHasFocus": "#374151",
    "bgHeaderHovered": "#374151",
    "bgBubble": "#4b5563",
    "textDark": "#f3f4f6",
    "textMedium": "#9ca3af",
    "textLight": "#6b7280",
    "textHeader": "#f3f4f6",
    "textBubble": "#f3f4f6",
    "borderColor": "rgba(255, 255, 255, 0.1)",
    "horizontalBorderColor": "rgba(255, 255, 255, 0.1)",
}

LIGHT_THEME = {
    "accentColor": "#8b5cf6",
    "accentLight": "rgba(139, 92, 246, 0.1)",
    "bgCell": "#ffffff",
    "bgCellMedium": "#f9fafb",
    "bgHeader": "#f3f4f6",
    "bgHeaderHasFocus": "#e5e7eb",
    "bgHeaderHovered": "#e5e7eb",
    "bgBubble": "#e5e7eb",
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "textLight": "#9ca3af",
    "textHeader": "#111827",
    "textBubble": "#374151",
    "borderColor": "#e5e7eb",
    "horizontalBorderColor": "#e5e7eb",
}

TAG_OPTIONS = [
    {"value": "react", "color": "#61dafb", "label": "React"},
    {"value": "python", "color": "#3776ab", "label": "Python"},
    {"value": "javascript", "color": "#f7df1e", "label": "JavaScript"},
    {"value": "typescript", "color": "#3178c6", "label": "TypeScript"},
    {"value": "rust", "color": "#dea584", "label": "Rust"},
    {"value": "go", "color": "#00add8", "label": "Go"},
]

COLUMNS = [
    {"title": "Project", "id": "project", "width": 150},
    {"title": "Tags", "id": "tags", "width": 200},
]


def make_multiselect_cell(values, **options):
    """Helper to create a multi-select cell with custom options."""
    return {
        "kind": "multi-select-cell",
        "data": {
            "values": values,
            "options": TAG_OPTIONS,
            "allowCreation": True,
            "allowDuplicates": False,
            **options,
        },
        "copyData": ",".join(values),
    }


def get_initial_data(options):
    """Generate initial data with the given options applied."""
    return [
        {"project": "Frontend App", "tags": make_multiselect_cell(["react", "typescript"], **options)},
        {"project": "Backend API", "tags": make_multiselect_cell(["python", "rust"], **options)},
        {"project": "CLI Tool", "tags": make_multiselect_cell(["go"], **options)},
        {"project": "Full Stack", "tags": make_multiselect_cell(["react", "python", "javascript"], **options)},
    ]


app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("MultiSelect Cell Options", id="title"),
        html.P("Toggle the options below to see how they affect the multi-select cells. Changes apply immediately.", id="subtitle"),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Options", style={"marginTop": 0}),
                                html.Button(
                                    "Toggle Dark Mode",
                                    id="theme-toggle",
                                    style={
                                        "marginBottom": "15px",
                                        "padding": "8px 16px",
                                        "cursor": "pointer",
                                        "borderRadius": "6px",
                                        "border": "1px solid #d1d5db",
                                        "backgroundColor": "#f3f4f6",
                                    },
                                ),
                            ],
                            style={"display": "flex", "justifyContent": "space-between", "alignItems": "center"},
                        ),
                        dcc.Checklist(
                            id="boolean-options",
                            options=[
                                {"label": " closeMenuOnSelect - Close dropdown after each selection", "value": "closeMenuOnSelect"},
                                {"label": " isClearable - Show X button to clear all values (default: on)", "value": "isClearable"},
                                {"label": " isSearchable - Enable typing to filter options (default: on)", "value": "isSearchable"},
                                {"label": " backspaceRemovesValue - Backspace removes last value (default: on)", "value": "backspaceRemovesValue"},
                                {"label": " hideSelectedOptions - Hide selected options from dropdown", "value": "hideSelectedOptions"},
                                {"label": " showOverflowCount - Show +N badge when values overflow cell width", "value": "showOverflowCount"},
                            ],
                            value=["isClearable", "isSearchable", "backspaceRemovesValue"],
                            style={"marginBottom": "16px"},
                            labelStyle={"display": "block", "marginBottom": "8px"},
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label("selectionIndicator: ", style={"fontWeight": "bold"}),
                                        dcc.Dropdown(
                                            id="opt-selectionIndicator",
                                            options=[
                                                {"label": "checkmark (default)", "value": "checkmark"},
                                                {"label": "highlight", "value": "highlight"},
                                                {"label": "both", "value": "both"},
                                            ],
                                            value="checkmark",
                                            style={"width": "180px"},
                                            clearable=False,
                                        ),
                                    ],
                                    style={"display": "inline-block", "marginRight": "24px"},
                                ),
                                html.Div(
                                    [
                                        html.Label("placeholder: ", style={"fontWeight": "bold"}),
                                        dcc.Input(
                                            id="opt-placeholder",
                                            type="text",
                                            placeholder="Custom placeholder...",
                                            style={"width": "200px"},
                                            debounce=True,
                                        ),
                                    ],
                                    style={"display": "inline-block", "marginRight": "24px"},
                                ),
                                html.Div(
                                    [
                                        html.Label("maxMenuHeight: ", style={"fontWeight": "bold"}),
                                        dcc.Input(
                                            id="opt-maxMenuHeight",
                                            type="number",
                                            value=300,
                                            min=50,
                                            max=500,
                                            style={"width": "80px"},
                                            debounce=True,
                                        ),
                                        html.Span(" px"),
                                    ],
                                    style={"display": "inline-block", "marginRight": "24px"},
                                ),
                                html.Div(
                                    [
                                        html.Label("menuPlacement: ", style={"fontWeight": "bold"}),
                                        dcc.Dropdown(
                                            id="opt-menuPlacement",
                                            options=[
                                                {"label": "auto", "value": "auto"},
                                                {"label": "top", "value": "top"},
                                                {"label": "bottom", "value": "bottom"},
                                            ],
                                            value="auto",
                                            style={"width": "120px"},
                                            clearable=False,
                                        ),
                                    ],
                                    style={"display": "inline-block"},
                                ),
                            ],
                        ),
                    ],
                    id="options-panel",
                    style={
                        "backgroundColor": "#f5f5f5",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "marginBottom": "20px",
                    },
                ),
            ]
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=get_initial_data({}),
            height=300,
            rowMarkers="number",
            theme=LIGHT_THEME,
        ),
        html.Div(
            [
                html.H3("Instructions:"),
                html.Ul(
                    [
                        html.Li("Click on a Tags cell to open the multi-select editor"),
                        html.Li("Toggle options above to see changes immediately"),
                        html.Li("Try selectionIndicator to change how selected options are shown"),
                        html.Li("Try typing to filter options (if isSearchable is enabled)"),
                        html.Li("Try pressing backspace to remove values (if backspaceRemovesValue is enabled)"),
                    ]
                ),
            ],
            id="instructions",
            style={"marginTop": "20px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("grid", "data"),
    Input("boolean-options", "value"),
    Input("opt-placeholder", "value"),
    Input("opt-maxMenuHeight", "value"),
    Input("opt-menuPlacement", "value"),
    Input("opt-selectionIndicator", "value"),
)
def update_grid(boolean_options, placeholder, maxMenuHeight, menuPlacement, selectionIndicator):
    """Update grid when any option changes."""
    boolean_options = boolean_options or []
    options = {}

    # Handle boolean options
    if "closeMenuOnSelect" in boolean_options:
        options["closeMenuOnSelect"] = True
    if "isClearable" not in boolean_options:
        options["isClearable"] = False
    if "isSearchable" not in boolean_options:
        options["isSearchable"] = False
    if "backspaceRemovesValue" not in boolean_options:
        options["backspaceRemovesValue"] = False
    if "hideSelectedOptions" in boolean_options:
        options["hideSelectedOptions"] = True
    if "showOverflowCount" in boolean_options:
        options["showOverflowCount"] = True

    # Handle other options
    if placeholder:
        options["placeholder"] = placeholder
    if maxMenuHeight and maxMenuHeight != 300:
        options["maxMenuHeight"] = maxMenuHeight
    if menuPlacement and menuPlacement != "auto":
        options["menuPlacement"] = menuPlacement
    if selectionIndicator and selectionIndicator != "checkmark":
        options["selectionIndicator"] = selectionIndicator

    return get_initial_data(options)


@callback(
    Output("grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("options-panel", "style"),
    Output("instructions", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

    if is_dark:
        return (
            DARK_THEME,
            {"margin": "40px", "fontFamily": "Arial, sans-serif", "backgroundColor": "#111827", "minHeight": "100vh", "color": "#f3f4f6"},
            {"color": "#f3f4f6"},
            {"color": "#9ca3af"},
            {"backgroundColor": "#374151", "padding": "20px", "borderRadius": "8px", "marginBottom": "20px"},
            {"marginTop": "20px", "color": "#f3f4f6"},
            {"marginBottom": "15px", "padding": "8px 16px", "cursor": "pointer", "borderRadius": "6px", "border": "1px solid #4b5563", "backgroundColor": "#4b5563", "color": "#f3f4f6"},
            "Toggle Light Mode",
        )
    else:
        return (
            LIGHT_THEME,
            {"margin": "40px", "fontFamily": "Arial, sans-serif"},
            {"color": "#111827"},
            {"color": "#6b7280"},
            {"backgroundColor": "#f5f5f5", "padding": "20px", "borderRadius": "8px", "marginBottom": "20px"},
            {"marginTop": "20px"},
            {"marginBottom": "15px", "padding": "8px 16px", "cursor": "pointer", "borderRadius": "6px", "border": "1px solid #d1d5db", "backgroundColor": "#f3f4f6"},
            "Toggle Dark Mode",
        )


if __name__ == "__main__":
    app.run(debug=True, port=8058)
