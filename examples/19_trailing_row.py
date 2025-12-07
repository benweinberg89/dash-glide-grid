"""
Example: Trailing Row (Add New Row)

Demonstrates the trailing row feature for adding new rows to the grid.
- Click on the trailing row to add a new row
- Configure appearance with hint text, sticky position, and tint color
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions
COLUMNS = [
    {"title": "ID", "width": 60, "id": "id"},
    {"title": "Name", "width": 180, "id": "name"},
    {"title": "Email", "width": 220, "id": "email"},
    {"title": "Department", "width": 130, "id": "dept"},
    {"title": "Status", "width": 100, "id": "status"},
]

# Initial sample data
INITIAL_DATA = [
    {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "dept": "Engineering", "status": "Active"},
    {"id": 2, "name": "Bob Johnson", "email": "bob@example.com", "dept": "Marketing", "status": "Active"},
    {"id": 3, "name": "Carol Williams", "email": "carol@example.com", "dept": "Sales", "status": "Active"},
]

app.layout = html.Div([
    html.H1("Trailing Row Example (Add New Row)"),
    html.P([
        "Click on the trailing row at the bottom of the grid to add a new row. ",
        "The trailing row shows hint text and can be configured to be sticky (always visible) ",
        "or have a tinted background."
    ]),

    html.Div([
        html.H4("Configuration:"),
        html.Div([
            dcc.Checklist(
                id="options-checklist",
                options=[
                    {"label": " Sticky (trailing row stays visible at bottom)", "value": "sticky"},
                    {"label": " Tint (apply background color to trailing row)", "value": "tint"},
                ],
                value=["sticky", "tint"],
                inline=True,
                style={"marginBottom": "10px"}
            ),
        ]),
        html.Div([
            html.Label("Hint text: "),
            dcc.Input(
                id="hint-input",
                type="text",
                value="Click to add new row...",
                style={"width": "200px", "marginLeft": "5px"}
            ),
        ]),
    ], style={"margin": "20px", "padding": "15px", "backgroundColor": "#f0f0f0", "borderRadius": "5px"}),

    html.Div([
        dgg.GlideGrid(
            id="trailing-row-grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=350,
            rowHeight=34,
            headerHeight=40,
            rowMarkers="number",
            # Trailing row configuration
            trailingRowOptions={
                "hint": "Click to add new row...",
                "sticky": True,
                "tint": True,
            },
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Event Log:"),
        html.Div(id="trailing-row-log", style={
            "fontFamily": "monospace",
            "padding": "10px",
            "backgroundColor": "#f0f0f0",
            "minHeight": "80px",
            "maxHeight": "150px",
            "overflow": "auto",
            "whiteSpace": "pre-wrap"
        }),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Current Data:"),
        html.Div(id="data-display", style={
            "fontFamily": "monospace",
            "padding": "10px",
            "backgroundColor": "#e8f4e8",
            "maxHeight": "200px",
            "overflow": "auto"
        }),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props used:"),
        html.Code("trailingRowOptions"),
        html.P("Configuration for the trailing row: {hint, sticky, tint, addIcon, targetColumn}"),
        html.Code("rowAppended"),
        html.P("Output prop fired when the trailing row is clicked. Returns {timestamp}."),
        html.Hr(),
        html.P([
            html.Strong("Note: "),
            "You must handle adding the new row to your data in your callback. ",
            "The grid only reports the append event - it doesn't automatically add rows."
        ]),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("trailing-row-grid", "trailingRowOptions"),
    Input("options-checklist", "value"),
    Input("hint-input", "value"),
)
def update_trailing_options(options, hint):
    """Update trailing row options based on user configuration."""
    return {
        "hint": hint or "Add new...",
        "sticky": "sticky" in (options or []),
        "tint": "tint" in (options or []),
    }


@callback(
    Output("trailing-row-grid", "data"),
    Output("trailing-row-log", "children"),
    Input("trailing-row-grid", "rowAppended"),
    State("trailing-row-grid", "data"),
    State("trailing-row-log", "children"),
    prevent_initial_call=True
)
def handle_row_appended(row_appended, current_data, current_log):
    """Handle row append events - add a new row to the data."""
    if not row_appended:
        return current_data, current_log

    # Calculate the new ID (max ID + 1)
    max_id = max(row["id"] for row in current_data) if current_data else 0
    new_id = max_id + 1

    # Create a new row with default values
    new_row = {
        "id": new_id,
        "name": f"New User {new_id}",
        "email": f"user{new_id}@example.com",
        "dept": "Unassigned",
        "status": "Pending"
    }

    # Add the new row to the data
    new_data = current_data + [new_row]

    # Update log
    timestamp = row_appended.get("timestamp", 0)
    log_entries = current_log if current_log else ""
    log_entries = f"Row Appended: ID={new_id}, timestamp={timestamp}\n" + log_entries

    # Limit log size
    log_lines = log_entries.split("\n")[:15]
    log_entries = "\n".join(log_lines)

    return new_data, log_entries


@callback(
    Output("data-display", "children"),
    Input("trailing-row-grid", "data"),
)
def update_data_display(data):
    """Display the current data in the grid."""
    if not data:
        return "No data"

    lines = []
    for i, row in enumerate(data):
        lines.append(f"Row {i}: {row}")

    return "\n".join(lines)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
