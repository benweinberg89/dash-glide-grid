"""
Example: Header Click Events (Sorting Pattern)

Demonstrates using headerClicked to implement column sorting.
Also shows headerMenuClicked for dropdown menus on columns.
"""

import dash
from dash import html, callback, Input, Output, State
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions with hasMenu for some columns
COLUMNS = [
    {"title": "Name", "width": 150, "id": "name"},
    {"title": "Department", "width": 130, "id": "dept", "hasMenu": True},
    {"title": "Salary", "width": 100, "id": "salary", "hasMenu": True},
    {"title": "Start Date", "width": 110, "id": "start_date"},
    {"title": "Status", "width": 100, "id": "status"},
]

# Sample data
INITIAL_DATA = [
    {"name": "Alice Smith", "dept": "Engineering", "salary": 95000, "start_date": "2020-03-15", "status": "Active"},
    {"name": "Bob Johnson", "dept": "Marketing", "salary": 75000, "start_date": "2019-07-22", "status": "Active"},
    {"name": "Carol Williams", "dept": "Engineering", "salary": 105000, "start_date": "2018-11-01", "status": "Active"},
    {"name": "David Brown", "dept": "Sales", "salary": 82000, "start_date": "2021-02-14", "status": "Active"},
    {"name": "Eve Davis", "dept": "Engineering", "salary": 98000, "start_date": "2020-08-30", "status": "On Leave"},
    {"name": "Frank Miller", "dept": "Marketing", "salary": 71000, "start_date": "2022-01-10", "status": "Active"},
    {"name": "Grace Wilson", "dept": "Sales", "salary": 88000, "start_date": "2019-04-05", "status": "Active"},
    {"name": "Henry Taylor", "dept": "Engineering", "salary": 115000, "start_date": "2017-06-20", "status": "Active"},
]

app.layout = html.Div([
    html.H1("Header Events Example"),
    html.P("Click column headers to sort. Columns with dropdown arrows (hasMenu) will show menu click events."),

    # Store for sort state
    html.Div(id="sort-state", children="", style={"display": "none"}),

    html.Div([
        dgg.GlideGrid(
            id="header-events-grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=350,
            rowHeight=34,
            headerHeight=40,
            rowMarkers="number",
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Event Log:"),
        html.Div(id="event-log", style={
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
        html.H4("Props used:"),
        html.Code("headerClicked"),
        html.P("Fires when a column header is clicked. Use for sorting."),
        html.Code("headerMenuClicked"),
        html.P("Fires when the menu icon on a column (hasMenu=True) is clicked."),
        html.Code("headerContextMenu"),
        html.P("Fires when a column header is right-clicked. Use for custom context menus."),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("event-log", "children"),
    Output("header-events-grid", "data"),
    Input("header-events-grid", "headerClicked"),
    Input("header-events-grid", "headerMenuClicked"),
    Input("header-events-grid", "headerContextMenu"),
    State("header-events-grid", "data"),
    State("event-log", "children"),
    prevent_initial_call=True
)
def handle_header_events(header_clicked, header_menu, header_context, current_data, current_log):
    """Handle header click events and implement sorting."""
    from dash import ctx

    log_entries = current_log if current_log else ""
    sorted_data = current_data

    triggered_id = ctx.triggered_id

    if triggered_id == "header-events-grid":
        prop_triggered = ctx.triggered[0]["prop_id"].split(".")[-1]

        if prop_triggered == "headerClicked" and header_clicked:
            col_idx = header_clicked.get("col", 0)
            col_name = COLUMNS[col_idx]["title"]
            log_entries = f"Header Clicked: Column {col_idx} ({col_name})\n" + log_entries

            # Sort data by clicked column
            try:
                col_id = COLUMNS[col_idx]["id"]
                sorted_data = sorted(current_data, key=lambda row: row.get(col_id, "") if row.get(col_id) is not None else "")
                log_entries = f"  → Sorted by {col_name} (ascending)\n" + log_entries
            except Exception as e:
                log_entries = f"  → Sort failed: {e}\n" + log_entries

        elif prop_triggered == "headerMenuClicked" and header_menu:
            col_idx = header_menu.get("col", 0)
            screen_x = header_menu.get("screenX", 0)
            screen_y = header_menu.get("screenY", 0)
            col_name = COLUMNS[col_idx]["title"]
            log_entries = f"Header Menu Clicked: Column {col_idx} ({col_name}) at ({screen_x}, {screen_y})\n" + log_entries
            log_entries = f"  → You could show a dropdown menu here!\n" + log_entries

        elif prop_triggered == "headerContextMenu" and header_context:
            col_idx = header_context.get("col", 0)
            col_name = COLUMNS[col_idx]["title"]
            log_entries = f"Header Right-Click: Column {col_idx} ({col_name})\n" + log_entries
            log_entries = f"  → You could show a context menu here!\n" + log_entries

    # Limit log size
    log_lines = log_entries.split("\n")[:30]
    log_entries = "\n".join(log_lines)

    return log_entries, sorted_data


if __name__ == "__main__":
    app.run(debug=True, port=8050)
