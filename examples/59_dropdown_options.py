"""
Example 59: Dropdown Cell Options
Demonstrates all configurable options for dropdown cells.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

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


# Boolean option definitions
BOOLEAN_OPTIONS = [
    {"value": "isClearable", "label": "isClearable", "description": "Show X button to clear selection"},
    {"value": "isSearchable", "label": "isSearchable", "description": "Enable typing to filter options", "default": True},
    {"value": "hideSelectedOptions", "label": "hideSelectedOptions", "description": "Hide selected option from dropdown"},
]

app.layout = html.Div(
    [
        html.H1("Dropdown Cell Options"),
        html.P("Toggle the options below to see how they affect the dropdown cells. Changes apply immediately."),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Options", style={"marginTop": 0}),
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
                                    style={"marginBottom": "16px"},
                                ),
                            ],
                        ),
                        html.Div(
                            [
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
        ),
        html.Div(
            [
                html.H3("Instructions:"),
                html.Ul(
                    [
                        html.Li("Click on a Status or Priority cell to open the dropdown editor"),
                        html.Li("The checkmark indicator shows which option is currently selected"),
                        html.Li("Toggle options above to see changes immediately"),
                        html.Li("Try isClearable to enable clearing the selection with X"),
                        html.Li("Try hideSelectedOptions to remove the selected item from the list"),
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
    Input("opt-isClearable", "value"),
    Input("opt-isSearchable", "value"),
    Input("opt-hideSelectedOptions", "value"),
    Input("opt-placeholder", "value"),
    Input("opt-maxMenuHeight", "value"),
    Input("opt-menuPlacement", "value"),
)
def update_grid(is_clearable, is_searchable, hide_selected, placeholder, max_height, menu_placement):
    """Update grid when any option changes."""
    options = {}

    # Boolean options
    if is_clearable and "on" in is_clearable:
        options["isClearable"] = True
    if not is_searchable or "on" not in is_searchable:
        options["isSearchable"] = False
    if hide_selected and "on" in hide_selected:
        options["hideSelectedOptions"] = True

    # Other options
    if placeholder:
        options["placeholder"] = placeholder
    if max_height and max_height != 300:
        options["maxMenuHeight"] = max_height
    if menu_placement and menu_placement != "auto":
        options["menuPlacement"] = menu_placement

    return get_data(**options)


if __name__ == "__main__":
    app.run(debug=True, port=8059)
