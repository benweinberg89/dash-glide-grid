"""
Example: Fill Handle Directions

Demonstrates the allowedFillDirections prop which controls how users can drag
the fill handle to copy cell values.
"""

import dash
from dash import html, Input, Output, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "A", "id": "a", "width": 80},
    {"title": "B", "id": "b", "width": 80},
    {"title": "C", "id": "c", "width": 80},
    {"title": "D", "id": "d", "width": 80},
    {"title": "E", "id": "e", "width": 80},
]

# Simple numeric data for easy fill demonstration
DATA = [
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
    {"a": 10, "b": 20, "c": 30, "d": 40, "e": 50},
    {"a": 100, "b": 200, "c": 300, "d": 400, "e": 500},
    {"a": "", "b": "", "c": "", "d": "", "e": ""},
    {"a": "", "b": "", "c": "", "d": "", "e": ""},
    {"a": "", "b": "", "c": "", "d": "", "e": ""},
    {"a": "", "b": "", "c": "", "d": "", "e": ""},
    {"a": "", "b": "", "c": "", "d": "", "e": ""},
]

app.layout = html.Div([
    html.H1("Fill Handle Directions Example"),
    html.P("Select a cell or range, then drag the fill handle (small square at bottom-right corner)."),

    html.Div([
        html.Label("Allowed Fill Directions: ", style={"marginRight": "10px"}),
        dcc.RadioItems(
            id="fill-direction",
            options=[
                {"label": "Horizontal only", "value": "horizontal"},
                {"label": "Vertical only", "value": "vertical"},
                {"label": "Orthogonal (H or V)", "value": "orthogonal"},
                {"label": "Any direction", "value": "any"},
            ],
            value="orthogonal",
            inline=True,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        dgg.GlideGrid(
            id="fill-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=36,

            # Fill handle configuration
            fillHandle=True,
            allowedFillDirections="orthogonal",

            # Visual settings
            drawFocusRing=True,
            rowMarkers="number",
            rowMarkerStartIndex=1,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("How to use:"),
        html.Ol([
            html.Li("Click on a cell with data (rows 1-3)"),
            html.Li("Look for the small blue square at the bottom-right corner of the selection"),
            html.Li("Drag it to fill adjacent cells"),
        ]),
        html.H4("Fill Directions:"),
        html.Ul([
            html.Li([html.Strong("horizontal"), " - Can only drag left/right"]),
            html.Li([html.Strong("vertical"), " - Can only drag up/down"]),
            html.Li([html.Strong("orthogonal"), " - Can drag horizontally OR vertically (default)"]),
            html.Li([html.Strong("any"), " - Can drag in any direction including diagonal"]),
        ]),
        html.Div(id="fill-info"),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@app.callback(
    Output("fill-grid", "allowedFillDirections"),
    Input("fill-direction", "value"),
)
def update_fill_direction(direction):
    return direction


@app.callback(
    Output("fill-info", "children"),
    Input("fill-grid", "cellEdited"),
)
def show_fill_info(edited):
    if edited:
        return html.P(f"Last edit: Row {edited['row']}, Col {edited['col']}",
                     style={"color": "green"})
    return html.P("Drag the fill handle to copy values to adjacent cells.")


if __name__ == "__main__":
    app.run(debug=True, port=8050)
