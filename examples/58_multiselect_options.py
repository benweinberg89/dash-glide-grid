"""
Example 58: MultiSelect Cell Options
Demonstrates all configurable options for multi-select cells.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_glide_grid as dgg
import json

app = dash.Dash(__name__)

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
    {"title": "Tags", "id": "tags", "width": 200},  # Narrower to demonstrate overflow
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
        {
            "project": "Frontend App",
            "tags": make_multiselect_cell(["react", "typescript"], **options),
        },
        {
            "project": "Backend API",
            "tags": make_multiselect_cell(["python", "rust"], **options),
        },
        {
            "project": "CLI Tool",
            "tags": make_multiselect_cell(["go"], **options),
        },
        {
            "project": "Full Stack",
            "tags": make_multiselect_cell(["react", "python", "javascript"], **options),
        },
    ]


app.layout = html.Div(
    [
        html.H1("MultiSelect Cell Options"),
        html.P("Toggle the options below and click 'Apply' to see how they affect the multi-select cells."),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Options"),
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
                                html.Label("placeholder: ", style={"fontWeight": "bold"}),
                                dcc.Input(
                                    id="opt-placeholder",
                                    type="text",
                                    placeholder="Custom placeholder...",
                                    style={"width": "200px"},
                                ),
                            ],
                            style={"marginBottom": "12px"},
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
                                ),
                                html.Span(" px"),
                            ],
                            style={"marginBottom": "12px"},
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
                                    style={"width": "150px"},
                                    clearable=False,
                                ),
                            ],
                            style={"marginBottom": "16px"},
                        ),
                        html.Button(
                            "Apply Options",
                            id="apply-btn",
                            n_clicks=0,
                            style={
                                "backgroundColor": "#4CAF50",
                                "color": "white",
                                "padding": "10px 20px",
                                "border": "none",
                                "borderRadius": "4px",
                                "cursor": "pointer",
                            },
                        ),
                    ],
                    style={
                        "backgroundColor": "#f5f5f5",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "marginBottom": "20px",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.H3("Current Options:"),
                html.Pre(
                    id="options-display",
                    style={
                        "backgroundColor": "#2d2d2d",
                        "color": "#f8f8f2",
                        "padding": "15px",
                        "borderRadius": "4px",
                        "fontFamily": "monospace",
                    },
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=get_initial_data({}),
            height=300,
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Instructions:"),
                html.Ul(
                    [
                        html.Li("Click on a Tags cell to open the multi-select editor"),
                        html.Li("Toggle options above and click 'Apply' to see the effect"),
                        html.Li("Try selecting multiple tags to see closeMenuOnSelect behavior"),
                        html.Li("Try typing to filter options (if isSearchable is enabled)"),
                        html.Li("Try pressing backspace to remove values (if backspaceRemovesValue is enabled)"),
                    ]
                ),
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("grid", "data"),
    Output("options-display", "children"),
    Input("apply-btn", "n_clicks"),
    State("boolean-options", "value"),
    State("opt-placeholder", "value"),
    State("opt-maxMenuHeight", "value"),
    State("opt-menuPlacement", "value"),
    prevent_initial_call=False,
)
def update_grid(n_clicks, boolean_options, placeholder, maxMenuHeight, menuPlacement):
    boolean_options = boolean_options or []
    options = {}

    # Handle boolean options (check which are enabled vs disabled from defaults)
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

    options_str = json.dumps(options, indent=2) if options else "{}"

    return get_initial_data(options), options_str


if __name__ == "__main__":
    app.run(debug=True, port=8058)
