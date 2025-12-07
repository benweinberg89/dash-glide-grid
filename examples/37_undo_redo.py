"""
Example: Undo/Redo Support

Demonstrates the undo/redo functionality for cell edits:
- Keyboard shortcuts: Cmd+Z (undo), Cmd+Shift+Z or Ctrl+Y (redo)
- Programmatic undo/redo via buttons
- canUndo/canRedo state tracking
"""

import dash
from dash import html, callback, Input, Output, State
import dash_glide_grid as dgg
import time

app = dash.Dash(__name__)

# Sample data
initial_data = [
    {"name": "Alice", "department": "Engineering", "salary": 95000},
    {"name": "Bob", "department": "Marketing", "salary": 75000},
    {"name": "Charlie", "department": "Sales", "salary": 82000},
    {"name": "Diana", "department": "Engineering", "salary": 105000},
    {"name": "Eve", "department": "HR", "salary": 68000},
]

columns = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Department", "id": "department", "width": 150},
    {"title": "Salary", "id": "salary", "width": 120},
]

app.layout = html.Div([
    html.H1("Undo/Redo Demo"),
    html.P("Edit cells and use Cmd+Z / Cmd+Shift+Z to undo/redo, or use the buttons below."),

    html.Div([
        html.Button("Undo", id="undo-btn", disabled=True, style={"marginRight": "10px"}),
        html.Button("Redo", id="redo-btn", disabled=True),
        html.Span(id="status", style={"marginLeft": "20px", "color": "#666"})
    ], style={"marginBottom": "10px"}),

    dgg.GlideGrid(
        id="grid",
        columns=columns,
        data=initial_data,
        height=300,
        enableUndoRedo=True,
        maxUndoSteps=20,  # Keep last 20 edit batches
    ),

    html.Div(id="edit-log", style={"marginTop": "20px", "fontFamily": "monospace"})
])


# Update button states based on canUndo/canRedo
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
    return not can_undo, not can_redo, " | ".join(status) if status else "No history"


# Handle Undo button click
@callback(
    Output("grid", "undoRedoAction", allow_duplicate=True),
    Input("undo-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_undo(n_clicks):
    if n_clicks:
        return {"action": "undo", "timestamp": int(time.time() * 1000)}
    return dash.no_update


# Handle Redo button click
@callback(
    Output("grid", "undoRedoAction", allow_duplicate=True),
    Input("redo-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_redo(n_clicks):
    if n_clicks:
        return {"action": "redo", "timestamp": int(time.time() * 1000)}
    return dash.no_update


# Log edits and undo/redo events
@callback(
    Output("edit-log", "children"),
    Input("grid", "cellEdited"),
    Input("grid", "undoRedoPerformed"),
    State("edit-log", "children"),
)
def log_events(cell_edited, undo_redo, current_log):
    ctx = dash.callback_context
    if not ctx.triggered:
        return current_log or []

    logs = current_log or []
    if isinstance(logs, str):
        logs = [logs]

    trigger_id = ctx.triggered[0]["prop_id"]

    if "cellEdited" in trigger_id and cell_edited:
        logs.append(f"Edit: row={cell_edited['row']}, col={cell_edited['col']}, value={cell_edited['value']}")
    elif "undoRedoPerformed" in trigger_id and undo_redo:
        logs.append(f">>> {undo_redo['action'].upper()} performed")

    # Keep last 10 entries
    logs = logs[-10:]

    return [html.Div(log) for log in logs]


if __name__ == "__main__":
    app.run(debug=True, port=8050)
