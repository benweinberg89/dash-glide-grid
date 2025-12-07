"""
Example: Row and Column Reordering

Demonstrates drag-and-drop reordering of rows and columns.
- Drag column headers to reorder columns
- Drag row markers to reorder rows (requires rowMarkers to be set)
"""

import dash
from dash import html, callback, Input, Output, State
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions
INITIAL_COLUMNS = [
    {"title": "ID", "width": 60, "id": "id"},
    {"title": "Name", "width": 150, "id": "name"},
    {"title": "Department", "width": 130, "id": "dept"},
    {"title": "Role", "width": 130, "id": "role"},
    {"title": "Salary", "width": 100, "id": "salary"},
]

# Sample data
INITIAL_DATA = [
    {"id": 1, "name": "Alice Smith", "dept": "Engineering", "role": "Senior Developer", "salary": 95000},
    {"id": 2, "name": "Bob Johnson", "dept": "Marketing", "role": "Marketing Manager", "salary": 75000},
    {"id": 3, "name": "Carol Williams", "dept": "Engineering", "role": "Tech Lead", "salary": 105000},
    {"id": 4, "name": "David Brown", "dept": "Sales", "role": "Sales Rep", "salary": 82000},
    {"id": 5, "name": "Eve Davis", "dept": "Engineering", "role": "Developer", "salary": 98000},
    {"id": 6, "name": "Frank Miller", "dept": "Marketing", "role": "Content Writer", "salary": 71000},
    {"id": 7, "name": "Grace Wilson", "dept": "Sales", "role": "Account Executive", "salary": 88000},
    {"id": 8, "name": "Henry Taylor", "dept": "Engineering", "role": "Principal Engineer", "salary": 115000},
]

app.layout = html.Div([
    html.H1("Row & Column Reordering Example"),
    html.P([
        html.Strong("Column reordering: "),
        "Drag column headers left/right to reorder columns.",
        html.Br(),
        html.Strong("Row reordering: "),
        "Drag the row number markers up/down to reorder rows.",
    ]),

    html.Div([
        dgg.GlideGrid(
            id="reorder-grid",
            columns=INITIAL_COLUMNS,
            data=INITIAL_DATA,
            height=350,
            rowHeight=34,
            headerHeight=40,
            # Row markers are required for row reordering
            rowMarkers="number",
            rowMarkerStartIndex=1,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Event Log:"),
        html.Div(id="reorder-log", style={
            "fontFamily": "monospace",
            "padding": "10px",
            "backgroundColor": "#f0f0f0",
            "minHeight": "100px",
            "maxHeight": "200px",
            "overflow": "auto",
            "whiteSpace": "pre-wrap"
        }),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Current Column Order:"),
        html.Div(id="column-order", style={
            "fontFamily": "monospace",
            "padding": "10px",
            "backgroundColor": "#e8f4e8",
        }),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props used:"),
        html.Code("columnMoved"),
        html.P("Fires when a column is dragged to a new position. Returns {startIndex, endIndex, timestamp}."),
        html.Code("rowMoved"),
        html.P("Fires when a row is dragged to a new position. Requires rowMarkers to be set. Returns {startIndex, endIndex, timestamp}."),
        html.Hr(),
        html.P([
            html.Strong("Note: "),
            "You must update the columns/data props in your callback to effect the reorder. ",
            "The grid only reports the move event - it doesn't automatically reorder the data."
        ]),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("reorder-grid", "columns"),
    Output("reorder-log", "children", allow_duplicate=True),
    Output("column-order", "children", allow_duplicate=True),
    Input("reorder-grid", "columnMoved"),
    State("reorder-grid", "columns"),
    State("reorder-log", "children"),
    prevent_initial_call=True
)
def handle_column_moved(column_moved, current_columns, current_log):
    """Handle column reorder events."""
    if not column_moved:
        return current_columns, current_log, ""

    start_idx = column_moved.get("startIndex", 0)
    end_idx = column_moved.get("endIndex", 0)

    # Get the column being moved
    moved_col = current_columns[start_idx]

    # Create new column order
    new_columns = current_columns.copy()
    new_columns.pop(start_idx)
    new_columns.insert(end_idx, moved_col)

    # Update log
    log_entries = current_log if current_log else ""
    log_entries = f"Column Moved: '{moved_col['title']}' from index {start_idx} to {end_idx}\n" + log_entries

    # Limit log size
    log_lines = log_entries.split("\n")[:20]
    log_entries = "\n".join(log_lines)

    # Current column order display
    col_order = " → ".join([c["title"] for c in new_columns])

    return new_columns, log_entries, col_order


@callback(
    Output("reorder-grid", "data"),
    Output("reorder-log", "children", allow_duplicate=True),
    Input("reorder-grid", "rowMoved"),
    State("reorder-grid", "data"),
    State("reorder-log", "children"),
    prevent_initial_call=True
)
def handle_row_moved(row_moved, current_data, current_log):
    """Handle row reorder events."""
    if not row_moved:
        return current_data, current_log

    start_idx = row_moved.get("startIndex", 0)
    end_idx = row_moved.get("endIndex", 0)

    # Get the row being moved
    moved_row = current_data[start_idx]

    # Create new data order
    new_data = current_data.copy()
    new_data.pop(start_idx)
    new_data.insert(end_idx, moved_row)

    # Update log
    log_entries = current_log if current_log else ""
    row_name = moved_row.get("name", f"Row {start_idx}")
    log_entries = f"Row Moved: '{row_name}' from index {start_idx} to {end_idx}\n" + log_entries

    # Limit log size
    log_lines = log_entries.split("\n")[:20]
    log_entries = "\n".join(log_lines)

    return new_data, log_entries


@callback(
    Output("column-order", "children"),
    Input("reorder-grid", "columns"),
)
def update_column_order_display(columns):
    """Update the column order display."""
    if not columns:
        return ""
    return " → ".join([c["title"] for c in columns])


if __name__ == "__main__":
    app.run(debug=True, port=8050)
