"""
Example: Freeform Cell Selection

Demonstrates the rangeSelect="freeform" mode for non-rectangular cell selection:
- Click/drag to start a new selection (clears previous)
- Cmd/Ctrl+click/drag to toggle cells (add unselected, remove selected)
- Escape to clear the selection
- Unselectable cells are automatically excluded when dragging across them

This mode maintains a single unified set of selected cells (not multiple
overlapping ranges like multi-rect mode).
"""

from dash import Dash, html, callback, Output, Input
import dash_glide_grid as dgg
import json

app = Dash(__name__)

# Sample data
DATA = [
    {"id": 1, "name": "Alice", "department": "Engineering", "salary": 95000, "active": True},
    {"id": 2, "name": "Bob", "department": "Marketing", "salary": 75000, "active": True},
    {"id": 3, "name": "Carol", "department": "Sales", "salary": 85000, "active": False},
    {"id": 4, "name": "David", "department": "Engineering", "salary": 105000, "active": True},
    {"id": 5, "name": "Eve", "department": "HR", "salary": 65000, "active": True},
    {"id": 6, "name": "Frank", "department": "Sales", "salary": 72000, "active": False},
    {"id": 7, "name": "Grace", "department": "Engineering", "salary": 115000, "active": True},
    {"id": 8, "name": "Henry", "department": "Marketing", "salary": 68000, "active": True},
]

COLUMNS = [
    {"id": "id", "title": "ID", "width": 60},
    {"id": "name", "title": "Name", "width": 120},
    {"id": "department", "title": "Department", "width": 130},
    {"id": "salary", "title": "Salary", "width": 100},
    {"id": "active", "title": "Active", "width": 80},
]

app.layout = html.Div(
    [
        html.H1("Freeform Cell Selection"),
        html.P(
            [
                "Select cells freely without being limited to rectangular shapes. ",
                "Use ",
                html.Strong("Cmd/Ctrl+click"),
                " to toggle cells on/off.",
            ]
        ),
        html.H3("Instructions:"),
        html.Ul(
            [
                html.Li("Click and drag to select a range of cells"),
                html.Li("Cmd/Ctrl+click on unselected cells to ADD them to the selection"),
                html.Li("Cmd/Ctrl+click on selected cells to REMOVE them from the selection"),
                html.Li("Cmd/Ctrl+drag to toggle an entire range"),
                html.Li("Press Escape to clear the selection"),
                html.Li("Click without Cmd/Ctrl to start a fresh selection"),
            ]
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rangeSelect="freeform",  # Enable freeform selection
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Selected Cells:"),
                html.Pre(
                    id="selected-cells-output",
                    style={
                        "backgroundColor": "#f5f5f5",
                        "padding": "10px",
                        "borderRadius": "4px",
                        "maxHeight": "200px",
                        "overflow": "auto",
                    },
                ),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            [
                html.H3("With Unselectable Columns"),
                html.P(
                    "The ID column (column 0) is unselectable. "
                    "Dragging across it will exclude those cells from the selection."
                ),
                dgg.GlideGrid(
                    id="grid-unselectable",
                    columns=COLUMNS,
                    data=DATA,
                    height=350,
                    rangeSelect="freeform",
                    unselectableColumns=[0],  # ID column is unselectable
                    rowMarkers="number",
                ),
            ],
            style={"marginTop": "40px"},
        ),
    ],
    style={"padding": "20px", "fontFamily": "system-ui, sans-serif"},
)


@callback(
    Output("selected-cells-output", "children"),
    Input("grid", "selectedCells"),
)
def display_selected_cells(selected_cells):
    if not selected_cells:
        return "No cells selected"
    return json.dumps(selected_cells, indent=2)


if __name__ == "__main__":
    app.run(debug=True, port=8062)
