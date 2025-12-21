"""
Example 59: Dropdown Cell Options
Demonstrates all configurable options for dropdown cells.
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

STATUS_OPTIONS = [
    {"value": "not_started", "label": "Not Started"},
    {"value": "in_progress", "label": "In Progress"},
    {"value": "review", "label": "Review"},
    {"value": "blocked", "label": "Blocked"},
    {"value": "complete", "label": "Complete"},
]

PRIORITY_OPTIONS = ["Low", "Medium", "High", "Urgent", "Critical"]

COLUMNS = [
    {"title": "Task", "id": "task", "width": 180},
    {"title": "Status", "id": "status", "width": 160},
    {"title": "Priority", "id": "priority", "width": 140},
]


def make_dropdown_cell(value, allowed_values, **options):
    """Helper to create a dropdown cell with custom options."""
    return {
        "kind": "dropdown-cell",
        "data": {
            "allowedValues": allowed_values,
            "value": value,
            **options,
        },
        "copyData": value or "",
    }


def get_data(**options):
    """Generate data with the given options applied."""
    return [
        {
            "task": "Design mockups",
            "status": make_dropdown_cell("complete", STATUS_OPTIONS, **options),
            "priority": make_dropdown_cell("High", PRIORITY_OPTIONS, **options),
        },
        {
            "task": "API integration",
            "status": make_dropdown_cell("in_progress", STATUS_OPTIONS, **options),
            "priority": make_dropdown_cell("Urgent", PRIORITY_OPTIONS, **options),
        },
        {
            "task": "Write tests",
            "status": make_dropdown_cell("not_started", STATUS_OPTIONS, **options),
            "priority": make_dropdown_cell("Medium", PRIORITY_OPTIONS, **options),
        },
        {
            "task": "Documentation",
            "status": make_dropdown_cell("review", STATUS_OPTIONS, **options),
            "priority": make_dropdown_cell("Low", PRIORITY_OPTIONS, **options),
        },
        {
            "task": "Performance audit",
            "status": make_dropdown_cell("blocked", STATUS_OPTIONS, **options),
            "priority": make_dropdown_cell("Critical", PRIORITY_OPTIONS, **options),
        },
    ]


app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Dropdown Cell Options", id="title"),
        html.P("Toggle the options below to see how they affect the dropdown cells. Changes apply immediately.", id="subtitle"),
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
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="opt-isClearable",
                                            options=[{"label": " isClearable - Show X button to clear selection", "value": "on"}],
                                            value=[],
                                        ),
                                    ],
                                    style={"marginBottom": "8px"},
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="opt-isSearchable",
                                            options=[{"label": " isSearchable - Enable typing to filter options (default: on)", "value": "on"}],
                                            value=["on"],
                                        ),
                                    ],
                                    style={"marginBottom": "8px"},
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="opt-hideSelectedOptions",
                                            options=[{"label": " hideSelectedOptions - Hide selected option from dropdown", "value": "on"}],
                                            value=[],
                                        ),
                                    ],
                                    style={"marginBottom": "8px"},
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="opt-allowCreation",
                                            options=[{"label": " allowCreation - Allow typing custom values not in the list", "value": "on"}],
                                            value=[],
                                        ),
                                    ],
                                    style={"marginBottom": "8px"},
                                ),
                                html.Div(
                                    [
                                        dcc.Checklist(
                                            id="opt-prefillSearch",
                                            options=[{"label": " prefillSearch - Pre-fill search with current value (auto-selected)", "value": "on"}],
                                            value=[],
                                        ),
                                    ],
                                    style={"marginBottom": "16px"},
                                ),
                            ],
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
                                            style={"width": "180px", "display": "inline-block"},
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
                                            style={"width": "120px", "display": "inline-block"},
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
            data=get_data(),
            height=280,
            rowMarkers="number",
            theme=LIGHT_THEME,
            enableCopyPaste=True,
            enableUndoRedo=True,
        ),
        html.Div(
            [
                html.H3("Instructions:"),
                html.Ul(
                    [
                        html.Li("Click on a Status or Priority cell to open the dropdown editor"),
                        html.Li("Toggle options above to see changes immediately"),
                        html.Li("Try selectionIndicator to change how selected options are shown (checkmark, highlight, or both)"),
                        html.Li("Try isClearable to enable clearing the selection with X"),
                        html.Li("Try hideSelectedOptions to remove the selected item from the list"),
                        html.Li("Try allowCreation to type custom values that aren't in the dropdown list"),
                        html.Li("Try prefillSearch to pre-fill the search box with the current value (useful for editing similar options)"),
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
    Input("opt-isClearable", "value"),
    Input("opt-isSearchable", "value"),
    Input("opt-hideSelectedOptions", "value"),
    Input("opt-allowCreation", "value"),
    Input("opt-prefillSearch", "value"),
    Input("opt-placeholder", "value"),
    Input("opt-maxMenuHeight", "value"),
    Input("opt-menuPlacement", "value"),
    Input("opt-selectionIndicator", "value"),
)
def update_grid(is_clearable, is_searchable, hide_selected, allow_creation, prefill_search, placeholder, max_height, menu_placement, selection_indicator):
    """Update grid when any option changes."""
    options = {}

    # Boolean options
    if is_clearable and "on" in is_clearable:
        options["isClearable"] = True
    if not is_searchable or "on" not in is_searchable:
        options["isSearchable"] = False
    if hide_selected and "on" in hide_selected:
        options["hideSelectedOptions"] = True
    if allow_creation and "on" in allow_creation:
        options["allowCreation"] = True
    if prefill_search and "on" in prefill_search:
        options["prefillSearch"] = True

    # Other options
    if placeholder:
        options["placeholder"] = placeholder
    if max_height and max_height != 300:
        options["maxMenuHeight"] = max_height
    if menu_placement and menu_placement != "auto":
        options["menuPlacement"] = menu_placement
    if selection_indicator and selection_indicator != "checkmark":
        options["selectionIndicator"] = selection_indicator

    return get_data(**options)


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
    app.run(debug=True, port=8059)
