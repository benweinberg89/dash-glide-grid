"""
Example 20: Scroll Control

This example demonstrates the scrollToCell prop for programmatically scrolling
the grid to a specific cell position. This is useful for:
- Navigating to search results
- Jumping to specific data points
- Creating "Go to row" functionality
- Syncing scroll position with external controls

Port: 8070
"""

from dash import Dash, html, dcc, callback, Input, Output, State
from dash_glide_grid import GlideGrid

# Create a large dataset to demonstrate scrolling
NUM_ROWS = 1000
NUM_COLS = 20

columns = [{"title": f"Column {i}", "width": 120, "id": f"col_{i}"} for i in range(NUM_COLS)]

# Generate sample data
data = [
    {f"col_{col}": f"R{row}C{col}" for col in range(NUM_COLS)}
    for row in range(NUM_ROWS)
]

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Scroll Control Example"),
    html.P("Use the controls below to programmatically scroll the grid to specific cells."),

    # Navigation controls
    html.Div([
        html.Div([
            html.Label("Row:"),
            dcc.Input(
                id="row-input",
                type="number",
                min=0,
                max=NUM_ROWS - 1,
                value=0,
                style={"width": "80px", "marginLeft": "10px"}
            ),
        ], style={"display": "inline-block", "marginRight": "20px"}),

        html.Div([
            html.Label("Column:"),
            dcc.Input(
                id="col-input",
                type="number",
                min=0,
                max=NUM_COLS - 1,
                value=0,
                style={"width": "80px", "marginLeft": "10px"}
            ),
        ], style={"display": "inline-block", "marginRight": "20px"}),

        html.Div([
            html.Label("Alignment:"),
            dcc.Dropdown(
                id="align-select",
                options=[
                    {"label": "Start", "value": "start"},
                    {"label": "Center", "value": "center"},
                    {"label": "End", "value": "end"},
                ],
                value="start",
                style={"width": "120px", "display": "inline-block", "marginLeft": "10px"},
                clearable=False
            ),
        ], style={"display": "inline-block", "marginRight": "20px", "verticalAlign": "middle"}),

        html.Button("Go to Cell", id="goto-btn", n_clicks=0),
    ], style={"marginBottom": "20px", "padding": "10px", "backgroundColor": "#f5f5f5", "borderRadius": "5px"}),

    # Quick navigation buttons
    html.Div([
        html.Button("Top-Left (0,0)", id="btn-top-left", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Center (500, 10)", id="btn-center", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Bottom-Right", id="btn-bottom-right", n_clicks=0, style={"marginRight": "10px"}),
        html.Button("Random Cell", id="btn-random", n_clicks=0),
    ], style={"marginBottom": "20px"}),

    # Current visible region display
    html.Div(id="visible-region-display", style={"marginBottom": "10px", "fontFamily": "monospace"}),

    # The grid
    GlideGrid(
        id="grid",
        columns=columns,
        data=data,
        height=500,
        width="100%",
        rowMarkers="number",
        rowMarkerStartIndex=0,
    ),

    # Hidden div to store the scrollToCell value
    html.Div(id="scroll-target", style={"display": "none"})
], style={"padding": "20px", "maxWidth": "1200px", "margin": "0 auto"})


@callback(
    Output("grid", "scrollToCell"),
    Input("goto-btn", "n_clicks"),
    Input("btn-top-left", "n_clicks"),
    Input("btn-center", "n_clicks"),
    Input("btn-bottom-right", "n_clicks"),
    Input("btn-random", "n_clicks"),
    State("row-input", "value"),
    State("col-input", "value"),
    State("align-select", "value"),
    prevent_initial_call=True
)
def scroll_to_cell(goto_clicks, top_left, center, bottom_right, random_click,
                   row, col, align):
    """Handle scroll navigation based on which button was clicked."""
    from dash import ctx
    import random

    triggered = ctx.triggered_id

    if triggered == "goto-btn":
        return {
            "col": int(col) if col is not None else 0,
            "row": int(row) if row is not None else 0,
            "hAlign": align,
            "vAlign": align
        }
    elif triggered == "btn-top-left":
        return {"col": 0, "row": 0, "hAlign": "start", "vAlign": "start"}
    elif triggered == "btn-center":
        return {"col": 10, "row": 500, "hAlign": "center", "vAlign": "center"}
    elif triggered == "btn-bottom-right":
        return {"col": NUM_COLS - 1, "row": NUM_ROWS - 1, "hAlign": "end", "vAlign": "end"}
    elif triggered == "btn-random":
        return {
            "col": random.randint(0, NUM_COLS - 1),
            "row": random.randint(0, NUM_ROWS - 1),
            "hAlign": "center",
            "vAlign": "center"
        }

    return None


@callback(
    Output("visible-region-display", "children"),
    Input("grid", "visibleRegion")
)
def update_visible_region(region):
    """Display the currently visible region."""
    if region:
        return f"Visible region: Rows {region['y']} - {region['y'] + region['height'] - 1}, Columns {region['x']} - {region['x'] + region['width'] - 1}"
    return "Visible region: Loading..."


if __name__ == "__main__":
    app.run(debug=True, port=8050)
