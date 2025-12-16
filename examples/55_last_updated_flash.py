"""
Example: Cell Flash Effect (lastUpdated)

Demonstrates the lastUpdated feature that highlights cells when they change:
- Cells flash when edited, undo/redo, or pasted
- The flash effect fades out over 500ms
- Flash color can be customized via theme.bgSearchResult
- Can control which operations trigger flash:
  - showCellFlash=True  (all operations)
  - showCellFlash=["paste", "undo", "redo"]  (only specific operations)
"""

import dash
from dash import html, callback, Input, Output
import dash_glide_grid as dgg
import time

app = dash.Dash(__name__)

# Sample data
initial_data = [
    {"product": "Laptop", "category": "Electronics", "price": 999, "stock": 50},
    {"product": "Headphones", "category": "Electronics", "price": 149, "stock": 200},
    {"product": "Desk Chair", "category": "Furniture", "price": 299, "stock": 75},
    {"product": "Monitor", "category": "Electronics", "price": 349, "stock": 120},
    {"product": "Keyboard", "category": "Electronics", "price": 79, "stock": 300},
    {"product": "Mouse", "category": "Electronics", "price": 49, "stock": 400},
    {"product": "Standing Desk", "category": "Furniture", "price": 599, "stock": 30},
    {"product": "Webcam", "category": "Electronics", "price": 89, "stock": 150},
]

columns = [
    {"title": "Product", "id": "product", "width": 150},
    {"title": "Category", "id": "category", "width": 120},
    {"title": "Price ($)", "id": "price", "width": 100},
    {"title": "Stock", "id": "stock", "width": 100},
]

app.layout = html.Div([
    html.H1("Cell Flash Effect Demo"),
    html.P("Cells flash to show they were updated. This example only flashes on paste/undo/redo (not regular edits)."),
    html.Ul([
        html.Li("Double-click a cell to edit it - NO flash (edit not in list)"),
        html.Li("Use Cmd+Z / Cmd+Shift+Z to undo/redo - cells WILL flash"),
        html.Li("Copy cells (Cmd+C) and paste (Cmd+V) - cells WILL flash"),
    ]),
    html.P([
        "Config: ",
        html.Code("showCellFlash=['paste', 'undo', 'redo']"),
        " | Color: ",
        html.Code("theme={'bgSearchResult': '#00ff0055'}")
    ], style={"fontSize": "14px", "color": "#666"}),

    html.Div([
        html.Button("Undo", id="undo-btn", disabled=True, style={"marginRight": "10px"}),
        html.Button("Redo", id="redo-btn", disabled=True),
        html.Span(id="status", style={"marginLeft": "20px", "color": "#666"})
    ], style={"marginBottom": "10px"}),

    dgg.GlideGrid(
        id="grid",
        columns=columns,
        data=initial_data,
        height=350,
        enableUndoRedo=True,
        enableCopyPaste=True,
        showCellFlash=["paste", "undo", "redo"],  # Only flash on these operations
        theme={
            "bgSearchResult": "#00ff0055"  # Green flash color (with alpha)
        }
    ),

    html.Div(id="log", style={"marginTop": "20px", "fontFamily": "monospace", "color": "#666"})
])


@callback(
    Output("undo-btn", "disabled"),
    Output("redo-btn", "disabled"),
    Output("status", "children"),
    Input("grid", "canUndo"),
    Input("grid", "canRedo"),
)
def update_button_states(can_undo, can_redo):
    status = []
    if can_undo:
        status.append("Can undo")
    if can_redo:
        status.append("Can redo")
    return not can_undo, not can_redo, " | ".join(status) if status else "No edits yet"


@callback(
    Output("grid", "undoRedoAction", allow_duplicate=True),
    Input("undo-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_undo(n_clicks):
    if n_clicks:
        return {"action": "undo", "timestamp": int(time.time() * 1000)}
    return dash.no_update


@callback(
    Output("grid", "undoRedoAction", allow_duplicate=True),
    Input("redo-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_redo(n_clicks):
    if n_clicks:
        return {"action": "redo", "timestamp": int(time.time() * 1000)}
    return dash.no_update


@callback(
    Output("log", "children"),
    Input("grid", "cellEdited"),
    Input("grid", "undoRedoPerformed"),
)
def log_events(cell_edited, undo_redo):
    ctx = dash.callback_context
    if not ctx.triggered:
        return "Waiting for edits..."

    trigger_id = ctx.triggered[0]["prop_id"]

    if "cellEdited" in trigger_id and cell_edited:
        return f"Cell edited at row {cell_edited['row']}, col {cell_edited['col']} - watch it flash!"
    elif "undoRedoPerformed" in trigger_id and undo_redo:
        return f"{undo_redo['action'].upper()} performed - watch the affected cells flash!"

    return "Waiting for edits..."


if __name__ == "__main__":
    app.run(debug=True, port=8055)
