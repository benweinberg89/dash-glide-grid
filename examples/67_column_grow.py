"""
Example: Column Grow and Fit-Content Width

Demonstrates two ways to control how a grid fills horizontal space:

1. `grow` column property - columns expand proportionally to fill the grid width
2. `width="fit-content"` - the grid itself shrinks to exactly fit its columns
"""

import dash
from dash import html, dcc, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

DATA = [
    {"name": "Alice Johnson", "role": "Engineer", "department": "Platform", "email": "alice@example.com", "status": "Active"},
    {"name": "Bob Smith", "role": "Designer", "department": "Product", "email": "bob@example.com", "status": "Active"},
    {"name": "Charlie Brown", "role": "Manager", "department": "Engineering", "email": "charlie@example.com", "status": "On Leave"},
    {"name": "Diana Prince", "role": "Engineer", "department": "Infrastructure", "email": "diana@example.com", "status": "Active"},
    {"name": "Eve Wilson", "role": "Analyst", "department": "Data", "email": "eve@example.com", "status": "Active"},
    {"name": "Frank Miller", "role": "Engineer", "department": "Platform", "email": "frank@example.com", "status": "Remote"},
    {"name": "Grace Lee", "role": "Designer", "department": "Product", "email": "grace@example.com", "status": "Active"},
    {"name": "Henry Chen", "role": "Manager", "department": "Engineering", "email": "henry@example.com", "status": "Active"},
]

COLUMNS = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Role", "id": "role", "width": 120},
    {"title": "Department", "id": "department", "width": 130},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Status", "id": "status", "width": 100},
]

COLUMNS_UNIFORM_GROW = [
    {"title": "Name", "id": "name", "width": 150, "grow": 1},
    {"title": "Role", "id": "role", "width": 120, "grow": 1},
    {"title": "Department", "id": "department", "width": 130, "grow": 1},
    {"title": "Email", "id": "email", "width": 200, "grow": 1},
    {"title": "Status", "id": "status", "width": 100, "grow": 1},
]

COLUMNS_WEIGHTED_GROW = [
    {"title": "Name", "id": "name", "width": 150, "grow": 2},
    {"title": "Role", "id": "role", "width": 120, "grow": 1},
    {"title": "Department", "id": "department", "width": 130, "grow": 1},
    {"title": "Email", "id": "email", "width": 200, "grow": 3},
    {"title": "Status", "id": "status", "width": 100},
]

COLUMNS_SINGLE_GROW = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Role", "id": "role", "width": 120},
    {"title": "Department", "id": "department", "width": 130},
    {"title": "Email", "id": "email", "width": 200, "grow": 1},
    {"title": "Status", "id": "status", "width": 100},
]

MODE_CONFIG = {
    "fit-content": {"columns": COLUMNS, "width": "fit-content"},
    "uniform": {"columns": COLUMNS_UNIFORM_GROW, "width": "100%"},
    "weighted": {"columns": COLUMNS_WEIGHTED_GROW, "width": "100%"},
    "single": {"columns": COLUMNS_SINGLE_GROW, "width": "100%"},
    "none": {"columns": COLUMNS, "width": "100%"},
}

app.layout = html.Div([
    html.H1("Column Grow and Fit-Content Width"),
    html.P("Two approaches to eliminate blank space to the right of your columns."),

    html.Div([
        html.Label("Mode:", style={"fontWeight": "bold", "marginRight": "10px"}),
        dcc.RadioItems(
            id="grow-mode",
            options=[
                {"label": 'width="fit-content" - grid shrinks to fit columns exactly', "value": "fit-content"},
                {"label": "Uniform grow (all grow=1) - columns stretch equally to fill width", "value": "uniform"},
                {"label": "Weighted grow - Name(2), Role(1), Dept(1), Email(3), Status(0)", "value": "weighted"},
                {"label": "Single column grow - only Email stretches", "value": "single"},
                {"label": "No grow, full width (default) - blank space on the right", "value": "none"},
            ],
            value="fit-content",
        ),
    ], style={"margin": "20px 0"}),

    html.Div([
        dgg.GlideGrid(
            id="grow-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=36,
            width="fit-content",
        ),
    ], style={"margin": "20px 0"}),

    html.Div(id="grow-info", style={
        "margin": "20px 0", "padding": "15px",
        "backgroundColor": "#f5f5f5", "borderRadius": "4px",
    }),
], style={"padding": "20px", "maxWidth": "1200px", "margin": "0 auto"})


@app.callback(
    [Output("grow-grid", "columns"), Output("grow-grid", "width")],
    Input("grow-mode", "value"),
)
def update_grid(mode):
    config = MODE_CONFIG[mode]
    return config["columns"], config["width"]


@app.callback(
    Output("grow-info", "children"),
    Input("grow-mode", "value"),
)
def update_info(mode):
    descriptions = {
        "fit-content": 'width="fit-content" sizes the grid to exactly fit its columns. No blank space, no stretching.',
        "uniform": "All columns have grow=1, so they share extra space equally to fill the full width.",
        "weighted": "Name gets 2 shares, Email gets 3 shares, Role and Dept get 1 each, Status doesn't grow.",
        "single": "Only Email has grow=1, so it absorbs all the extra space.",
        "none": "No grow, width=100%. Columns use fixed widths and blank space appears to the right.",
    }
    return html.P(descriptions[mode])


if __name__ == "__main__":
    app.run(debug=True, port=8050)
