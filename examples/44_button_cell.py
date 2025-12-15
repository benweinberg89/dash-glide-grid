"""
Example 44: Button Cell

This example demonstrates the button cell type, which renders clickable buttons
in grid cells. When clicked, buttons fire a `buttonClicked` callback with
information about which button was clicked.

Button cells support:
- Custom colors (backgroundColor, color, borderColor)
- Custom border radius
- Click callbacks with row/column information
"""

import dash
from dash import html, callback, Input, Output, State
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__)

# Sample data with button cells
initial_data = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "status": "Active",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "status": "Pending",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 3,
        "name": "Carol White",
        "email": "carol@example.com",
        "status": "Active",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 4,
        "name": "David Brown",
        "email": "david@example.com",
        "status": "Inactive",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
]

columns = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Status", "id": "status", "width": 100},
    {"title": "Action", "id": "action", "width": 80},
    {"title": "Delete", "id": "delete", "width": 80},
]

app.layout = html.Div([
    html.H1("Button Cell Example"),
    html.P("Click the buttons in the grid to see the callback fire."),

    GlideGrid(
        id="grid",
        columns=columns,
        data=initial_data,
        height=300,
        width="100%",
    ),

    html.Div([
        html.H3("Last Button Clicked:"),
        html.Pre(id="click-output", style={
            "backgroundColor": "#f5f5f5",
            "padding": "10px",
            "borderRadius": "4px",
            "minHeight": "60px"
        })
    ], style={"marginTop": "20px"}),

    html.Div([
        html.H3("Action Log:"),
        html.Div(id="action-log", style={
            "backgroundColor": "#f5f5f5",
            "padding": "10px",
            "borderRadius": "4px",
            "minHeight": "100px",
            "maxHeight": "200px",
            "overflowY": "auto"
        })
    ], style={"marginTop": "20px"})
], style={"padding": "20px", "maxWidth": "900px"})


@callback(
    Output("click-output", "children"),
    Input("grid", "buttonClicked"),
    prevent_initial_call=True
)
def handle_button_click(click_info):
    if not click_info:
        return "No button clicked yet"

    return f"""Button: "{click_info['title']}"
Column: {click_info['col']}
Row: {click_info['row']}
Timestamp: {click_info['timestamp']}"""


@callback(
    Output("action-log", "children"),
    Input("grid", "buttonClicked"),
    State("action-log", "children"),
    State("grid", "data"),
    prevent_initial_call=True
)
def log_action(click_info, current_log, data):
    if not click_info:
        return current_log or []

    row_data = data[click_info['row']]
    name = row_data.get('name', 'Unknown')
    button = click_info['title']

    message = f"{button} clicked for {name} (row {click_info['row']})"

    new_entry = html.Div(message, style={
        "padding": "5px",
        "borderBottom": "1px solid #ddd"
    })

    if current_log:
        if isinstance(current_log, list):
            return [new_entry] + current_log[:9]  # Keep last 10 entries
        return [new_entry, current_log]

    return [new_entry]


if __name__ == "__main__":
    app.run(debug=True, port=8044)
