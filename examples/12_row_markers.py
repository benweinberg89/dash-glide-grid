"""
Example: Row Marker Options

Demonstrates the different rowMarkers styles and configuration options:
- rowMarkers: 'none', 'number', 'checkbox', 'both', 'checkbox-visible', 'clickable-number'
- rowMarkerStartIndex: Starting number for row numbering
- rowMarkerWidth: Custom width for the marker column
"""

import dash
from dash import html, Input, Output, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Role", "id": "role", "width": 120},
    {"title": "Department", "id": "department", "width": 120},
    {"title": "Status", "id": "status", "width": 100},
]

DATA = [
    {"name": "Alice Johnson", "role": "Engineer", "department": "Engineering", "status": "Active"},
    {"name": "Bob Smith", "role": "Manager", "department": "Sales", "status": "Active"},
    {"name": "Charlie Brown", "role": "Designer", "department": "Marketing", "status": "On Leave"},
    {"name": "Diana Prince", "role": "Engineer", "department": "Engineering", "status": "Active"},
    {"name": "Eve Wilson", "role": "Director", "department": "Sales", "status": "Active"},
    {"name": "Frank Miller", "role": "Analyst", "department": "Finance", "status": "Active"},
    {"name": "Grace Lee", "role": "Engineer", "department": "Engineering", "status": "Active"},
    {"name": "Henry Chen", "role": "Manager", "department": "Support", "status": "Inactive"},
]

app.layout = html.Div([
    html.H1("Row Markers Example"),
    html.P("Explore different row marker styles and configurations."),

    html.Div([
        html.Div([
            html.Label("Row Marker Style:"),
            dcc.Dropdown(
                id="marker-style",
                options=[
                    {"label": "None", "value": "none"},
                    {"label": "Number", "value": "number"},
                    {"label": "Checkbox (on hover)", "value": "checkbox"},
                    {"label": "Both (number + checkbox)", "value": "both"},
                    {"label": "Checkbox (always visible)", "value": "checkbox-visible"},
                    {"label": "Clickable Number", "value": "clickable-number"},
                ],
                value="both",
                style={"width": "250px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Start Index:"),
            dcc.Input(
                id="start-index",
                type="number",
                value=1,
                min=0,
                max=100,
                style={"width": "80px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),

        html.Div([
            html.Label("Marker Width (px):"),
            dcc.Input(
                id="marker-width",
                type="number",
                value=50,
                min=30,
                max=100,
                style={"width": "80px"}
            ),
        ], style={"display": "inline-block", "margin": "10px", "verticalAlign": "top"}),
    ], style={"marginBottom": "20px"}),

    html.Div([
        dgg.GlideGrid(
            id="markers-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=36,

            # Row marker configuration
            rowMarkers="both",
            rowMarkerStartIndex=1,
            rowMarkerWidth=50,

            # Enable row selection to see checkboxes work
            rowSelect="multi",
            rowSelectionMode="multi",
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Row Marker Styles:"),
        html.Ul([
            html.Li([html.Strong("none"), " - No row markers"]),
            html.Li([html.Strong("number"), " - Show row numbers only"]),
            html.Li([html.Strong("checkbox"), " - Show checkboxes on hover"]),
            html.Li([html.Strong("both"), " - Show both numbers and checkboxes"]),
            html.Li([html.Strong("checkbox-visible"), " - Always show checkboxes (not just on hover)"]),
            html.Li([html.Strong("clickable-number"), " - Row numbers act as selection buttons"]),
        ]),
        html.H4("Configuration:"),
        html.Ul([
            html.Li([html.Strong("rowMarkerStartIndex"), " - First row number (default: 1)"]),
            html.Li([html.Strong("rowMarkerWidth"), " - Width of marker column in pixels"]),
        ]),
        html.Div(id="selection-output", style={"marginTop": "10px", "fontWeight": "bold"}),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@app.callback(
    Output("markers-grid", "rowMarkers"),
    Input("marker-style", "value"),
)
def update_marker_style(style):
    return style


@app.callback(
    Output("markers-grid", "rowMarkerStartIndex"),
    Input("start-index", "value"),
)
def update_start_index(index):
    return index or 1


@app.callback(
    Output("markers-grid", "rowMarkerWidth"),
    Input("marker-width", "value"),
)
def update_marker_width(width):
    return width or 50


@app.callback(
    Output("selection-output", "children"),
    Input("markers-grid", "selectedRows"),
)
def show_selection(rows):
    if rows:
        return f"Selected rows: {rows}"
    return "No rows selected. Click checkboxes or row markers to select."


if __name__ == "__main__":
    app.run(debug=True, port=8050)
