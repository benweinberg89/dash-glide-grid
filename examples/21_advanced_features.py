"""
Example 21: Advanced Features

This example demonstrates the advanced props:
- keybindings: Customize keyboard shortcuts
- isDraggable: Make the grid draggable for external drag-and-drop
- experimental: Performance and rendering options
- scrollOffsetX/scrollOffsetY: Initial scroll position

Port: 8071
"""

from dash import Dash, html, dcc, callback, Input, Output
from dash_glide_grid import GlideGrid

# Sample data
columns = [
    {"title": "ID", "width": 80, "id": "id"},
    {"title": "Name", "width": 150, "id": "name"},
    {"title": "Department", "width": 150, "id": "dept"},
    {"title": "Salary", "width": 120, "id": "salary"},
    {"title": "Status", "width": 100, "id": "status"},
]

data = [
    {
        "id": i,
        "name": f"Employee {i}",
        "dept": ["Engineering", "Sales", "Marketing", "HR"][i % 4],
        "salary": 50000 + (i * 1000),
        "status": ["Active", "On Leave", "Remote"][i % 3]
    }
    for i in range(100)
]

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Advanced Features Example"),

    # Keybindings section
    html.Div([
        html.H3("1. Keybindings"),
        html.P("This grid has custom keybindings:"),
        html.Ul([
            html.Li("Ctrl+F (search) is DISABLED"),
            html.Li("Ctrl+A (select all) is ENABLED"),
            html.Li("Fill operations are DISABLED"),
        ]),
    ], style={"marginBottom": "20px"}),

    GlideGrid(
        id="grid-keybindings",
        columns=columns,
        data=data[:20],
        height=300,
        keybindings={
            "search": False,  # Disable Ctrl+F
            "selectAll": True,  # Keep Ctrl+A
            "downFill": False,  # Disable Ctrl+D
            "rightFill": False,  # Disable Ctrl+R
        },
    ),

    html.Hr(),

    # Draggable section
    html.Div([
        html.H3("2. Draggable Grid"),
        html.P("This grid has isDraggable='cell' - try dragging a cell!"),
        html.Div(id="drag-info", style={"fontFamily": "monospace", "marginBottom": "10px"}),
    ], style={"marginBottom": "20px"}),

    GlideGrid(
        id="grid-draggable",
        columns=columns,
        data=data[:10],
        height=250,
        isDraggable="cell",
    ),

    html.Hr(),

    # Experimental section
    html.Div([
        html.H3("3. Experimental Options"),
        html.P("This grid uses experimental performance options:"),
        html.Ul([
            html.Li("kineticScrollPerfHack: Performance optimization for scrolling"),
            html.Li("paddingBottom: 50px extra padding at bottom"),
            html.Li("renderStrategy: 'direct' for faster rendering"),
        ]),
    ], style={"marginBottom": "20px"}),

    GlideGrid(
        id="grid-experimental",
        columns=columns,
        data=data,
        height=350,
        experimental={
            "kineticScrollPerfHack": True,
            "paddingBottom": 50,
            "renderStrategy": "direct",
        },
    ),

    html.Hr(),

    # Initial scroll offset section
    html.Div([
        html.H3("4. Initial Scroll Offset"),
        html.P("This grid starts scrolled to position (200px, 500px):"),
    ], style={"marginBottom": "20px"}),

    GlideGrid(
        id="grid-scroll-offset",
        columns=columns,
        data=data,
        height=300,
        scrollOffsetX=200,
        scrollOffsetY=500,
        rowMarkers="number",
    ),

], style={"padding": "20px", "maxWidth": "1000px", "margin": "0 auto"})


@callback(
    Output("drag-info", "children"),
    Input("grid-draggable", "dragStarted"),
    prevent_initial_call=True
)
def show_drag_info(drag_started):
    if drag_started:
        return f"Drag started at cell: col={drag_started.get('col')}, row={drag_started.get('row')}"
    return "No drag event yet"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
