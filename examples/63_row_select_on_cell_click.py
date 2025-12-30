"""
Example: Row Select on Cell Click

Demonstrates the rowSelectOnCellClick feature that allows selecting rows
by clicking on any cell, not just the row marker column.

Features demonstrated:
- rowSelectOnCellClick: Enable row selection on any cell click
- rowSelect: 'single' or 'multi' selection modes
- rowSelectionMode: 'auto' (requires modifiers) or 'multi' (toggle mode)
- Modifier keys: Ctrl/Cmd to toggle, Shift for range selection
"""

import dash
from dash import html, Input, Output, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Role", "id": "role", "width": 120},
    {"title": "Department", "id": "department", "width": 130},
    {"title": "Location", "id": "location", "width": 120},
    {"title": "Status", "id": "status", "width": 100},
]

DATA = [
    {"name": "Alice Johnson", "role": "Engineer", "department": "Engineering", "location": "New York", "status": "Active"},
    {"name": "Bob Smith", "role": "Manager", "department": "Sales", "location": "Los Angeles", "status": "Active"},
    {"name": "Charlie Brown", "role": "Designer", "department": "Marketing", "location": "Chicago", "status": "On Leave"},
    {"name": "Diana Prince", "role": "Engineer", "department": "Engineering", "location": "Houston", "status": "Active"},
    {"name": "Eve Wilson", "role": "Director", "department": "Sales", "location": "Phoenix", "status": "Active"},
    {"name": "Frank Miller", "role": "Analyst", "department": "Finance", "location": "Seattle", "status": "Active"},
    {"name": "Grace Lee", "role": "Engineer", "department": "Engineering", "location": "Boston", "status": "Active"},
    {"name": "Henry Chen", "role": "Manager", "department": "Support", "location": "Denver", "status": "Inactive"},
    {"name": "Ivy Martinez", "role": "Designer", "department": "Marketing", "location": "Austin", "status": "Active"},
    {"name": "Jack Thompson", "role": "Analyst", "department": "Finance", "location": "Miami", "status": "Active"},
]

app.layout = html.Div([
    html.H1("Row Select on Cell Click"),
    html.P("Click any cell to select its entire row - no need to click the row marker!"),

    html.Div([
        html.Div([
            html.Label("Row Select on Click:"),
            dcc.Dropdown(
                id="row-select-on-click",
                options=[
                    {"label": "On", "value": True},
                    {"label": "Off", "value": False},
                ],
                value=True,
                style={"width": "100px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Row Select Mode:"),
            dcc.Dropdown(
                id="row-select-mode",
                options=[
                    {"label": "Single", "value": "single"},
                    {"label": "Multi", "value": "multi"},
                ],
                value="multi",
                style={"width": "150px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Selection Mode:"),
            dcc.Dropdown(
                id="selection-mode",
                options=[
                    {"label": "Auto (use modifiers)", "value": "auto"},
                    {"label": "Multi (always toggle)", "value": "multi"},
                ],
                value="auto",
                style={"width": "200px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Row Markers:"),
            dcc.Dropdown(
                id="row-markers",
                options=[
                    {"label": "None", "value": "none"},
                    {"label": "Checkbox", "value": "checkbox"},
                    {"label": "Both", "value": "both"},
                ],
                value="checkbox",
                style={"width": "150px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Focus Ring:"),
            dcc.Dropdown(
                id="focus-ring",
                options=[
                    {"label": "On", "value": True},
                    {"label": "Off", "value": False},
                ],
                value=False,
                style={"width": "100px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Range Select:"),
            dcc.Dropdown(
                id="range-select",
                options=[
                    {"label": "Cell", "value": "cell"},
                    {"label": "Rect", "value": "rect"},
                    {"label": "Multi-Cell", "value": "multi-cell"},
                    {"label": "Multi-Rect", "value": "multi-rect"},
                    {"label": "None", "value": "none"},
                ],
                value="cell",
                style={"width": "130px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Row Blending:"),
            dcc.Dropdown(
                id="row-blending",
                options=[
                    {"label": "Exclusive", "value": "exclusive"},
                    {"label": "Mixed", "value": "mixed"},
                ],
                value="exclusive",
                style={"width": "120px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Column Blending:"),
            dcc.Dropdown(
                id="column-blending",
                options=[
                    {"label": "Exclusive", "value": "exclusive"},
                    {"label": "Mixed", "value": "mixed"},
                ],
                value="exclusive",
                style={"width": "120px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Range Blending:"),
            dcc.Dropdown(
                id="range-blending",
                options=[
                    {"label": "Exclusive", "value": "exclusive"},
                    {"label": "Mixed", "value": "mixed"},
                ],
                value="exclusive",
                style={"width": "120px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),
    ], style={"marginBottom": "10px"}),

    dgg.GlideGrid(
        id="grid",
        columns=COLUMNS,
        data=DATA,
        height=400,
        rowHeight=36,

        # Enable row selection on cell click
        rowSelectOnCellClick=True,

        # Row selection configuration
        rowSelect="multi",
        rowSelectionMode="auto",
        rowMarkers="checkbox",

        # Column selection (click header to select column)
        columnSelect="multi",

        # Hide focus ring border but keep row/column highlighting
        drawFocusRing=False,
        rangeSelect="cell",
    ),

    html.Div([
        html.H4("Selected Rows:"),
        html.Div(id="selection-output", style={"fontSize": "16px", "fontWeight": "bold"}),
    ], style={"margin": "20px 0"}),

    html.Div([
        html.H4("How it works:"),
        html.Ul([
            html.Li([html.Strong("Single mode: "), "Clicking any cell selects only that row"]),
            html.Li([html.Strong("Multi mode + Auto: ")]),
            html.Ul([
                html.Li("Plain click: Select only that row"),
                html.Li("Ctrl/Cmd + click: Toggle row in selection"),
                html.Li("Shift + click: Select range from last clicked row"),
            ]),
            html.Li([html.Strong("Multi mode + Multi: "), "Every click toggles the row (no modifiers needed)"]),
        ]),
        html.P([
            html.Strong("Note: "),
            "This works even with rowMarkers='none' - you don't need visible row markers!"
        ], style={"marginTop": "10px", "color": "#666"}),
    ], style={"padding": "20px", "backgroundColor": "#f5f5f5", "borderRadius": "8px"}),
])


@app.callback(
    Output("grid", "rowSelectOnCellClick"),
    Input("row-select-on-click", "value"),
)
def update_row_select_on_click(value):
    return value


@app.callback(
    Output("grid", "rowSelect"),
    Input("row-select-mode", "value"),
)
def update_row_select(value):
    return value


@app.callback(
    Output("grid", "rowSelectionMode"),
    Input("selection-mode", "value"),
)
def update_selection_mode(value):
    return value


@app.callback(
    Output("grid", "rowMarkers"),
    Input("row-markers", "value"),
)
def update_row_markers(value):
    return value


@app.callback(
    Output("grid", "drawFocusRing"),
    Input("focus-ring", "value"),
)
def update_focus_ring(value):
    return value


@app.callback(
    Output("grid", "rangeSelect"),
    Input("range-select", "value"),
)
def update_range_select(value):
    return value


@app.callback(
    Output("grid", "rowSelectionBlending"),
    Input("row-blending", "value"),
)
def update_row_blending(value):
    return value


@app.callback(
    Output("grid", "columnSelectionBlending"),
    Input("column-blending", "value"),
)
def update_column_blending(value):
    return value


@app.callback(
    Output("grid", "rangeSelectionBlending"),
    Input("range-blending", "value"),
)
def update_range_blending(value):
    return value


@app.callback(
    Output("selection-output", "children"),
    Input("grid", "selectedRows"),
)
def show_selection(rows):
    if not rows:
        return "No rows selected. Click any cell to select its row!"

    # Show selected names
    names = [DATA[i]["name"] for i in rows if i < len(DATA)]
    return f"Rows {rows}: {', '.join(names)}"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
