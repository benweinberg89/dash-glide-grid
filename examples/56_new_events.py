"""
Example demonstrating new event props:
- mouseMove: Raw mouse movement over grid
- cellsEdited: Batch edits from paste/fill operations
- deletePressed: Delete key events with allowDelete control
"""

import dash
from dash import html, Input, Output, callback
import dash_glide_grid as dgg

app = dash.Dash(__name__)

columns = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Value", "id": "value", "width": 100},
    {"title": "Status", "id": "status", "width": 120},
]

data = [
    {"name": "Item A", "value": 100, "status": "Active"},
    {"name": "Item B", "value": 200, "status": "Pending"},
    {"name": "Item C", "value": 300, "status": "Active"},
    {"name": "Item D", "value": 400, "status": "Inactive"},
    {"name": "Item E", "value": 500, "status": "Active"},
]

app.layout = html.Div([
    html.H2("New Event Props Demo"),

    html.Div([
        html.Label("Allow Delete: "),
        html.Button("Toggle", id="toggle-delete", n_clicks=0),
        html.Span(id="delete-status", style={"marginLeft": "10px", "fontWeight": "bold"}),
    ], style={"marginBottom": "10px"}),

    dgg.GlideGrid(
        id="grid",
        columns=columns,
        data=data,
        height=300,
        width="100%",
        enableCopyPaste=True,
        fillHandle=True,
        allowDelete=True,
    ),

    html.Div([
        html.H4("Mouse Move (last position)"),
        html.Pre(id="mouse-output", style={"backgroundColor": "#f0f0f0", "padding": "10px"}),
    ], style={"marginTop": "20px"}),

    html.Div([
        html.H4("Cells Edited (batch - from paste/fill)"),
        html.Pre(id="cells-edited-output", style={"backgroundColor": "#f0f0f0", "padding": "10px"}),
    ]),

    html.Div([
        html.H4("Delete Pressed"),
        html.Pre(id="delete-output", style={"backgroundColor": "#f0f0f0", "padding": "10px"}),
    ]),
])


@callback(
    Output("grid", "allowDelete"),
    Output("delete-status", "children"),
    Input("toggle-delete", "n_clicks"),
)
def toggle_delete(n_clicks):
    allow = n_clicks % 2 == 0
    return allow, f"Delete {'Enabled' if allow else 'Disabled'}"


@callback(
    Output("mouse-output", "children"),
    Input("grid", "mouseMove"),
)
def update_mouse(mouse_move):
    if not mouse_move:
        return "Move mouse over grid..."
    return f"Col: {mouse_move.get('col')}, Row: {mouse_move.get('row')}, Kind: {mouse_move.get('kind')}\nX: {mouse_move.get('localEventX')}, Y: {mouse_move.get('localEventY')}"


@callback(
    Output("cells-edited-output", "children"),
    Input("grid", "cellsEdited"),
)
def update_cells_edited(cells_edited):
    if not cells_edited:
        return "Paste data or use fill handle to see batch edits..."
    edits = cells_edited.get("edits", [])
    count = cells_edited.get("count", 0)
    output = f"Count: {count} cells edited\n\nEdits:\n"
    for edit in edits[:10]:  # Show first 10
        output += f"  [{edit.get('col')}, {edit.get('row')}] = {edit.get('value')}\n"
    if len(edits) > 10:
        output += f"  ... and {len(edits) - 10} more"
    return output


@callback(
    Output("delete-output", "children"),
    Input("grid", "deletePressed"),
)
def update_delete(delete_pressed):
    if not delete_pressed:
        return "Select cells and press Delete..."
    cells = delete_pressed.get("cells", [])
    rows = delete_pressed.get("rows", [])
    cols = delete_pressed.get("columns", [])
    return f"Cells: {cells}\nRows: {rows}\nColumns: {cols}"


if __name__ == "__main__":
    app.run(debug=True, port=8056)
