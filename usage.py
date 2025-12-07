"""
Dash Glide Grid - Comprehensive Usage Example

This example demonstrates many key features of the GlideGrid component:
- Records-based data format (compatible with df.to_dict('records'))
- Column sorting and filtering
- Custom theming
- Row markers and selection
- Fill handle for Excel-like data entry
- Undo/redo support
- Search functionality
- Event callbacks
"""

import dash
from dash import html, dcc, Input, Output, callback, ctx
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions with sorting and filtering enabled
COLUMNS = [
    {"title": "Name", "id": "name", "width": 180, "sortable": True},
    {"title": "Department", "id": "department", "width": 140, "sortable": True, "filterable": True, "hasMenu": True},
    {"title": "Role", "id": "role", "width": 160, "sortable": True, "filterable": True, "hasMenu": True},
    {"title": "Salary", "id": "salary", "width": 120, "sortable": True},
    {"title": "Start Date", "id": "start_date", "width": 120, "sortable": True},
    {"title": "Active", "id": "active", "width": 80},
    {"title": "Rating", "id": "rating", "width": 80, "sortable": True},
]

# Sample employee data using records format (like pandas df.to_dict('records'))
DATA = [
    {"name": "Alice Chen", "department": "Engineering", "role": "Senior Developer", "salary": 125000, "start_date": "2020-03-15", "active": True, "rating": 4.8},
    {"name": "Bob Martinez", "department": "Engineering", "role": "Tech Lead", "salary": 145000, "start_date": "2018-07-01", "active": True, "rating": 4.9},
    {"name": "Carol Williams", "department": "Design", "role": "UX Designer", "salary": 95000, "start_date": "2021-01-10", "active": True, "rating": 4.5},
    {"name": "David Kim", "department": "Engineering", "role": "Junior Developer", "salary": 75000, "start_date": "2023-06-01", "active": True, "rating": 4.2},
    {"name": "Eva Johnson", "department": "Marketing", "role": "Marketing Manager", "salary": 110000, "start_date": "2019-11-20", "active": True, "rating": 4.7},
    {"name": "Frank Brown", "department": "Sales", "role": "Sales Director", "salary": 130000, "start_date": "2017-04-05", "active": True, "rating": 4.6},
    {"name": "Grace Lee", "department": "Design", "role": "Creative Director", "salary": 135000, "start_date": "2016-09-12", "active": True, "rating": 4.9},
    {"name": "Henry Wilson", "department": "Engineering", "role": "DevOps Engineer", "salary": 115000, "start_date": "2020-08-25", "active": False, "rating": 4.4},
    {"name": "Iris Taylor", "department": "HR", "role": "HR Manager", "salary": 90000, "start_date": "2019-02-14", "active": True, "rating": 4.3},
    {"name": "Jack Anderson", "department": "Sales", "role": "Account Executive", "salary": 85000, "start_date": "2022-03-01", "active": True, "rating": 4.1},
    {"name": "Karen White", "department": "Engineering", "role": "QA Engineer", "salary": 95000, "start_date": "2021-05-15", "active": True, "rating": 4.5},
    {"name": "Leo Garcia", "department": "Marketing", "role": "Content Strategist", "salary": 80000, "start_date": "2022-09-10", "active": True, "rating": 4.0},
]

# Custom theme
THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "#dbeafe",
    "bgCell": "#ffffff",
    "bgHeader": "#f8fafc",
    "bgHeaderHovered": "#f1f5f9",
    "textDark": "#1e293b",
    "textHeader": "#475569",
    "borderColor": "#e2e8f0",
    "fontFamily": "system-ui, -apple-system, sans-serif",
}

app.layout = html.Div([
    html.H1("Dash Glide Grid", style={"color": "#1e293b", "marginBottom": "8px"}),
    html.P("A high-performance data grid for Dash applications",
           style={"color": "#64748b", "marginBottom": "24px"}),

    # Toolbar
    html.Div([
        html.Button("Undo", id="undo-btn", n_clicks=0,
                    style={"marginRight": "8px", "padding": "8px 16px"}),
        html.Button("Redo", id="redo-btn", n_clicks=0,
                    style={"marginRight": "16px", "padding": "8px 16px"}),
        html.Button("Clear Filters", id="clear-filters-btn", n_clicks=0,
                    style={"padding": "8px 16px"}),
    ], style={"marginBottom": "16px"}),

    # The Grid
    html.Div([
        dgg.GlideGrid(
            id="main-grid",
            columns=COLUMNS,
            data=DATA,
            height=500,

            # Appearance
            theme=THEME,
            rowHeight=40,
            headerHeight=44,

            # Row markers and selection
            rowMarkers="clickable-number",
            rowSelect="multi",
            columnSelect="multi",
            rangeSelect="multi-rect",

            # Editing features
            fillHandle=True,
            enableCopyPaste=True,

            # Column features
            freezeColumns=1,
            columnResize=True,
            minColumnWidth=60,
            maxColumnWidth=400,

            # Sorting
            sortable=True,
            sortColumns=[],

            # Filtering (via column menus)
            columnFilters={},

            # Search
            showSearch=True,
            searchValue="",

            # Visual enhancements
            hoverRow=True,
            drawFocusRing=True,
            smoothScrollX=True,
            smoothScrollY=True,

            # Undo/redo
            enableUndoRedo=True,
            maxUndoSteps=50,
        ),
    ], style={"border": "1px solid #e2e8f0", "borderRadius": "8px", "overflow": "hidden"}),

    # Status panel
    html.Div([
        html.Div([
            html.Strong("Selection: "),
            html.Span(id="selection-display", children="None"),
        ], style={"marginBottom": "8px"}),
        html.Div([
            html.Strong("Last Edit: "),
            html.Span(id="edit-display", children="None"),
        ], style={"marginBottom": "8px"}),
        html.Div([
            html.Strong("Sort: "),
            html.Span(id="sort-display", children="None"),
        ], style={"marginBottom": "8px"}),
        html.Div([
            html.Strong("Filters: "),
            html.Span(id="filter-display", children="None"),
        ]),
    ], style={
        "marginTop": "16px",
        "padding": "16px",
        "backgroundColor": "#f8fafc",
        "borderRadius": "8px",
        "fontFamily": "monospace",
        "fontSize": "13px",
    }),

    # Hidden div for undo/redo trigger
    dcc.Store(id="undo-redo-trigger"),

], style={"maxWidth": "1200px", "margin": "40px auto", "padding": "0 20px"})


@callback(
    Output("selection-display", "children"),
    Input("main-grid", "selectedCell"),
    Input("main-grid", "selectedRows"),
    Input("main-grid", "selectedRange"),
)
def update_selection(cell, rows, range_sel):
    parts = []
    if cell:
        parts.append(f"Cell({cell['row']}, {cell['col']})")
    if rows:
        parts.append(f"Rows{rows}")
    if range_sel:
        parts.append(f"Range({range_sel['startRow']}:{range_sel['endRow']}, {range_sel['startCol']}:{range_sel['endCol']})")
    return " | ".join(parts) if parts else "None"


@callback(
    Output("edit-display", "children"),
    Input("main-grid", "cellEdited"),
)
def update_edit(edit):
    if edit:
        return f"Row {edit['row']}, Col {edit['col']} = {edit['value']}"
    return "None"


@callback(
    Output("sort-display", "children"),
    Input("main-grid", "sortColumns"),
)
def update_sort(sort_cols):
    if sort_cols:
        parts = [f"{COLUMNS[s['columnIndex']]['id']} ({s['direction']})" for s in sort_cols]
        return ", ".join(parts)
    return "None"


@callback(
    Output("filter-display", "children"),
    Input("main-grid", "columnFilters"),
)
def update_filters(filters):
    if filters:
        parts = [f"{COLUMNS[int(k)]['id']}: {v}" for k, v in filters.items()]
        return " | ".join(parts)
    return "None"


@callback(
    Output("main-grid", "columnFilters"),
    Input("clear-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_filters(_):
    return {}


@callback(
    Output("main-grid", "undoRedoAction"),
    Input("undo-btn", "n_clicks"),
    Input("redo-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_undo_redo(_undo, _redo):
    import time
    triggered = ctx.triggered_id
    if triggered == "undo-btn":
        return {"action": "undo", "timestamp": int(time.time() * 1000)}
    elif triggered == "redo-btn":
        return {"action": "redo", "timestamp": int(time.time() * 1000)}
    return dash.no_update


if __name__ == "__main__":
    app.run(debug=True)