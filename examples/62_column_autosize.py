"""
Example: Column Auto-sizing

Demonstrates columns that automatically size to fit their content.
- Columns without a fixed width will auto-size to fit content
- Use remeasureColumns to trigger re-measurement after data changes
- maxColumnAutoWidth limits how wide auto-sized columns can grow
"""

import dash
from dash import html, Input, Output, State, callback
import dash_glide_grid as dgg
import time

app = dash.Dash(__name__)

# Mix of fixed-width and auto-sized columns
COLUMNS = [
    {"title": "ID", "id": "id", "width": 60},  # Fixed width
    {"title": "Name", "id": "name"},  # Auto-sized
    {"title": "Email", "id": "email"},  # Auto-sized
    {"title": "Department", "id": "department"},  # Auto-sized
    {"title": "Notes", "id": "notes"},  # Auto-sized (longer content)
]

DATA = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "department": "Eng", "notes": "Team lead"},
    {"id": 2, "name": "Bob", "email": "bob@example.com", "department": "Sales", "notes": "New hire"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com", "department": "Marketing", "notes": "Remote"},
    {"id": 4, "name": "Diana", "email": "diana@example.com", "department": "Eng", "notes": "Senior"},
    {"id": 5, "name": "Eve", "email": "eve@example.com", "department": "HR", "notes": "Manager"},
]

# Data with longer content to demonstrate auto-sizing difference
DATA_LONG = [
    {"id": 1, "name": "Alexandria Johnson-Smith", "email": "alexandria.johnson.smith@longcompanyname.com", "department": "Engineering & Research", "notes": "Lead software architect, 10+ years experience"},
    {"id": 2, "name": "Robert Williams III", "email": "robert.williams.iii@corporate.org", "department": "Sales & Business Development", "notes": "Top performer Q4 2024"},
    {"id": 3, "name": "Charlotte Brown-Davis", "email": "charlotte.bd@enterprise.io", "department": "Marketing Communications", "notes": "Brand strategy specialist"},
    {"id": 4, "name": "Diana Prince-Wayne", "email": "diana.pw@startup.co", "department": "Product Engineering", "notes": "Full-stack developer, React expert"},
    {"id": 5, "name": "Evangeline Wilson", "email": "evangeline.w@company.net", "department": "Human Resources", "notes": "Handles recruitment and onboarding"},
]

app.layout = html.Div([
    html.H1("Column Auto-sizing Example"),
    html.P("Columns without a 'width' property automatically size to fit their content."),

    html.Div([
        html.Button("Load Short Data", id="btn-short", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Load Long Data", id="btn-long", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Remeasure All Columns", id="btn-remeasure-all", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Remeasure Name Column Only", id="btn-remeasure-name", n_clicks=0),
    ], style={"margin": "20px 0"}),

    html.Div([
        dgg.GlideGrid(
            id="autosize-grid",
            columns=COLUMNS,
            data=DATA,
            height=300,
            rowHeight=36,

            # Auto-size constraints
            maxColumnAutoWidth=400,  # Limit auto-sized columns to 400px max

            # Enable column resize so users can adjust
            columnResize=True,

            # Row markers
            rowMarkers="number",
            rowMarkerStartIndex=1,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props demonstrated:"),
        html.Ul([
            html.Li([
                html.Strong("columns without width"),
                " - Columns auto-size to fit their content"
            ]),
            html.Li([
                html.Strong("maxColumnAutoWidth"),
                " - Maximum width for auto-sized columns (400px in this example)"
            ]),
            html.Li([
                html.Strong("remeasureColumns"),
                " - Trigger re-measurement after data changes. Format: {'columns': [...], 'timestamp': ...}"
            ]),
        ]),
        html.H4("How it works:"),
        html.Ul([
            html.Li("The 'ID' column has a fixed width of 60px"),
            html.Li("Other columns have no width specified, so they auto-size"),
            html.Li("Click 'Load Long Data' to see columns expand for longer content"),
            html.Li("Use 'Remeasure' buttons to trigger column width recalculation"),
        ]),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("autosize-grid", "data"),
    Input("btn-short", "n_clicks"),
    Input("btn-long", "n_clicks"),
    prevent_initial_call=True,
)
def update_data(short_clicks, long_clicks):
    from dash import ctx
    if ctx.triggered_id == "btn-long":
        return DATA_LONG
    return DATA


@callback(
    Output("autosize-grid", "remeasureColumns"),
    Input("btn-remeasure-all", "n_clicks"),
    Input("btn-remeasure-name", "n_clicks"),
    prevent_initial_call=True,
)
def remeasure_columns(all_clicks, name_clicks):
    from dash import ctx
    if ctx.triggered_id == "btn-remeasure-name":
        # Remeasure only the Name column (index 1)
        return {"columns": [1], "timestamp": time.time() * 1000}
    # Remeasure all columns (empty array = all)
    return {"columns": [], "timestamp": time.time() * 1000}


if __name__ == "__main__":
    app.run(debug=True, port=8062)
