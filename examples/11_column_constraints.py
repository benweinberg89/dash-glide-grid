"""
Example: Column Width Constraints

Demonstrates minColumnWidth and maxColumnWidth to control how users can resize columns.
Also shows selection blending modes.
"""

import dash
from dash import html, Input, Output, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Department", "id": "department", "width": 120},
    {"title": "Location", "id": "location", "width": 120},
    {"title": "Salary", "id": "salary", "width": 100},
]

DATA = [
    {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "department": "Engineering", "location": "New York", "salary": 95000},
    {"id": 2, "name": "Bob Smith", "email": "bob@example.com", "department": "Sales", "location": "Chicago", "salary": 85000},
    {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "department": "Marketing", "location": "Seattle", "salary": 78000},
    {"id": 4, "name": "Diana Prince", "email": "diana@example.com", "department": "Engineering", "location": "Austin", "salary": 102000},
    {"id": 5, "name": "Eve Wilson", "email": "eve@example.com", "department": "HR", "location": "Boston", "salary": 72000},
    {"id": 6, "name": "Frank Miller", "email": "frank@example.com", "department": "Sales", "location": "Denver", "salary": 88000},
    {"id": 7, "name": "Grace Lee", "email": "grace@example.com", "department": "Engineering", "location": "Portland", "salary": 98000},
    {"id": 8, "name": "Henry Chen", "email": "henry@example.com", "department": "Finance", "location": "Miami", "salary": 92000},
]

app.layout = html.Div([
    html.H1("Column Width Constraints Example"),
    html.P("Try resizing columns by dragging the column edges. Width is constrained!"),

    html.Div([
        html.Div([
            html.Label("Min Column Width:"),
            dcc.Slider(
                id="min-width-slider",
                min=30,
                max=150,
                value=80,
                marks={30: "30", 50: "50", 80: "80", 100: "100", 150: "150"},
            ),
        ], style={"width": "300px", "display": "inline-block", "margin": "20px"}),

        html.Div([
            html.Label("Max Column Width:"),
            dcc.Slider(
                id="max-width-slider",
                min=150,
                max=500,
                value=250,
                marks={150: "150", 250: "250", 350: "350", 500: "500"},
            ),
        ], style={"width": "300px", "display": "inline-block", "margin": "20px"}),
    ]),

    html.Div([
        html.Label("Selection Blending Mode: ", style={"marginRight": "10px"}),
        dcc.RadioItems(
            id="blending-mode",
            options=[
                {"label": "Exclusive (selections replace each other)", "value": "exclusive"},
                {"label": "Mixed (selections can combine)", "value": "mixed"},
            ],
            value="exclusive",
            inline=True,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        dgg.GlideGrid(
            id="constrained-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=36,

            # Column constraints
            minColumnWidth=80,
            maxColumnWidth=250,

            # Enable column resize
            columnResize=True,

            # Selection with blending
            rowSelect="multi",
            columnSelect="multi",
            rangeSelect="multi-rect",
            rowSelectionBlending="exclusive",
            columnSelectionBlending="exclusive",
            rangeSelectionBlending="exclusive",

            # Row markers
            rowMarkers="both",
            rowMarkerStartIndex=1,

            # Visual feedback
            drawFocusRing=True,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props demonstrated:"),
        html.Ul([
            html.Li([
                html.Strong("minColumnWidth / maxColumnWidth"),
                " - Columns can only be resized within this range"
            ]),
            html.Li([
                html.Strong("rowSelectionBlending / columnSelectionBlending / rangeSelectionBlending"),
                " - Control how different selection types interact"
            ]),
        ]),
        html.H4("Selection Blending Explained:"),
        html.Ul([
            html.Li([
                html.Strong("Exclusive: "),
                "Selecting rows clears column selection and vice versa"
            ]),
            html.Li([
                html.Strong("Mixed: "),
                "You can have row, column, and range selections simultaneously"
            ]),
        ]),
        html.P("Try: Select some rows, then select a column. In 'exclusive' mode, the row selection clears."),
        html.Div(id="constraint-info"),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@app.callback(
    [
        Output("constrained-grid", "minColumnWidth"),
        Output("constrained-grid", "maxColumnWidth"),
    ],
    [
        Input("min-width-slider", "value"),
        Input("max-width-slider", "value"),
    ],
)
def update_constraints(min_width, max_width):
    return min_width, max_width


@app.callback(
    [
        Output("constrained-grid", "rowSelectionBlending"),
        Output("constrained-grid", "columnSelectionBlending"),
        Output("constrained-grid", "rangeSelectionBlending"),
    ],
    Input("blending-mode", "value"),
)
def update_blending(mode):
    return mode, mode, mode


@app.callback(
    Output("constraint-info", "children"),
    [
        Input("min-width-slider", "value"),
        Input("max-width-slider", "value"),
    ],
)
def show_constraints(min_w, max_w):
    return html.P(f"Current constraints: {min_w}px - {max_w}px")


if __name__ == "__main__":
    app.run(debug=True, port=8050)
