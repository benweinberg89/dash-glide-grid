"""
Example 65: Hidden Rows with Tree View Cells

Demonstrates using hiddenRows with tree-view-cell for collapse/expand that:
- Preserves original row numbers (unlike filtering/rebuilding data)
- Maintains selection state on hidden rows (reappears when unhidden)
- Provides instant visual collapse without data manipulation

Compare to example 53 which rebuilds the data array on each toggle.
This approach is more efficient and preserves row identity.

Also includes testing for hidden row edge cases:
- Tab/Arrow navigation should skip hidden rows
- Fill handle should not fill hidden cells
- Delete should not clear hidden cells
- Copy should not include hidden rows
- Paste should skip hidden rows
- Context menu should not appear on hidden rows

The hiddenRowsConfig prop allows toggling each of these behaviors on/off.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
import json
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__)

# Flat tree data - all rows always present, visibility controlled by hiddenRows
# Each row knows its parent so we can compute which rows to hide
TREE_DATA = [
    {"id": "root", "parent_id": None, "name": "Project Root", "type": "folder", "size": "-"},
    {"id": "src", "parent_id": "root", "name": "src", "type": "folder", "size": "-"},
    {"id": "components", "parent_id": "src", "name": "components", "type": "folder", "size": "-"},
    {"id": "button", "parent_id": "components", "name": "Button.tsx", "type": "file", "size": "2.4 KB"},
    {"id": "input", "parent_id": "components", "name": "Input.tsx", "type": "file", "size": "3.1 KB"},
    {"id": "modal", "parent_id": "components", "name": "Modal.tsx", "type": "file", "size": "4.8 KB"},
    {"id": "utils", "parent_id": "src", "name": "utils", "type": "folder", "size": "-"},
    {"id": "api", "parent_id": "utils", "name": "api.ts", "type": "file", "size": "1.2 KB"},
    {"id": "helpers", "parent_id": "utils", "name": "helpers.ts", "type": "file", "size": "0.8 KB"},
    {"id": "app", "parent_id": "src", "name": "App.tsx", "type": "file", "size": "5.6 KB"},
    {"id": "index", "parent_id": "src", "name": "index.tsx", "type": "file", "size": "0.5 KB"},
    {"id": "public", "parent_id": "root", "name": "public", "type": "folder", "size": "-"},
    {"id": "html", "parent_id": "public", "name": "index.html", "type": "file", "size": "1.1 KB"},
    {"id": "favicon", "parent_id": "public", "name": "favicon.ico", "type": "file", "size": "4.2 KB"},
    {"id": "package", "parent_id": "root", "name": "package.json", "type": "file", "size": "1.8 KB"},
    {"id": "readme", "parent_id": "root", "name": "README.md", "type": "file", "size": "2.3 KB"},
]

# Build lookup tables
ID_TO_ROW = {node["id"]: i for i, node in enumerate(TREE_DATA)}
ROW_TO_ID = {i: node["id"] for i, node in enumerate(TREE_DATA)}

# Folder row indices (for unselectableRows)
FOLDER_ROWS = [i for i, node in enumerate(TREE_DATA) if node["type"] == "folder"]


def get_depth(node_id):
    """Calculate depth by counting parent levels"""
    depth = 0
    node = TREE_DATA[ID_TO_ROW[node_id]]
    while node["parent_id"]:
        depth += 1
        node = TREE_DATA[ID_TO_ROW[node["parent_id"]]]
    return depth


def has_children(node_id):
    """Check if node has any children"""
    return any(n["parent_id"] == node_id for n in TREE_DATA)


def get_all_descendants(node_id):
    """Get all descendant row indices (children, grandchildren, etc.)"""
    descendants = []
    for i, node in enumerate(TREE_DATA):
        if is_descendant_of(node["id"], node_id):
            descendants.append(i)
    return descendants


def is_descendant_of(node_id, ancestor_id):
    """Check if node_id is a descendant of ancestor_id"""
    node = TREE_DATA[ID_TO_ROW[node_id]]
    while node["parent_id"]:
        if node["parent_id"] == ancestor_id:
            return True
        node = TREE_DATA[ID_TO_ROW[node["parent_id"]]]
    return False


def compute_hidden_rows(collapsed_nodes):
    """Compute which rows should be hidden based on collapsed nodes"""
    hidden = set()
    for node_id in collapsed_nodes:
        # Hide all descendants of collapsed nodes
        for desc_row in get_all_descendants(node_id):
            hidden.add(desc_row)
    return sorted(hidden)


def build_grid_data(collapsed_nodes):
    """Build grid data with tree-view-cell for the name column"""
    collapsed_set = set(collapsed_nodes)
    data = []
    for i, node in enumerate(TREE_DATA):
        node_id = node["id"]
        can_open = has_children(node_id)
        # isOpen = node is NOT in collapsed set (and can open)
        is_open = can_open and (node_id not in collapsed_set)

        data.append({
            "name": {
                "kind": "tree-view-cell",
                "text": node["name"],
                "depth": get_depth(node_id),
                "isOpen": is_open,
                "canOpen": can_open,
            },
            "type": node["type"].capitalize(),
            "size": node["size"],
            # Test cells for hidden rows rendering
            "rating": {"kind": "star-cell", "rating": (i % 5) + 1, "maxStars": 5},
            "trend": {"kind": "sparkline-cell", "values": [10, 20, 15, 25, 30, 20], "graphKind": "line"},
            "progress": {"kind": "range-cell", "value": (i * 7) % 100, "min": 0, "max": 100},
            "action": {"kind": "button-cell", "title": "Edit", "backgroundColor": "#3b82f6"},
            "tags": {"kind": "tags-cell", "tags": ["alpha", "beta"][:((i % 3) + 1)], "possibleTags": [
                {"tag": "alpha", "color": "#ef4444"},
                {"tag": "beta", "color": "#22c55e"},
            ]},
            "owner": {"kind": "user-profile-cell", "name": f"User {i}", "initial": chr(65 + (i % 26))},
            "links": {"kind": "links-cell", "links": [{"title": "View", "href": "#"}]},
            "status": {
                "kind": "dropdown-cell",
                "data": {
                    "value": ["active", "pending", "done"][i % 3],
                    "allowedValues": [
                        {"value": "active", "label": "Active"},
                        {"value": "pending", "label": "Pending"},
                        {"value": "done", "label": "Done"},
                    ],
                },
            },
            "labels": {
                "kind": "multi-select-cell",
                "data": {
                    "values": ["bug", "feature"][:((i % 2) + 1)],
                    "options": [
                        {"value": "bug", "label": "Bug", "color": "#ef4444"},
                        {"value": "feature", "label": "Feature", "color": "#3b82f6"},
                    ],
                },
            },
            "date": {"kind": "date-picker-cell", "date": "2024-01-15", "displayDate": "Jan 15, 2024"},
            "loading": {"kind": "spinner-cell"} if i % 4 == 0 else node["type"].capitalize(),
        })
    return data


def update_tree_cells_only(current_data, collapsed_nodes):
    """Update only the tree-view-cell properties, preserving other column edits"""
    if not current_data:
        return build_grid_data(collapsed_nodes)

    collapsed_set = set(collapsed_nodes)
    updated_data = []

    for i, row in enumerate(current_data):
        if i >= len(TREE_DATA):
            break

        node = TREE_DATA[i]
        node_id = node["id"]
        can_open = has_children(node_id)
        is_open = can_open and (node_id not in collapsed_set)

        # Copy existing row but update only the name column's tree properties
        new_row = dict(row)  # Preserve all existing values (including edits)
        new_row["name"] = {
            "kind": "tree-view-cell",
            "text": node["name"],
            "depth": get_depth(node_id),
            "isOpen": is_open,
            "canOpen": can_open,
        }
        updated_data.append(new_row)

    return updated_data


# Initial state: all nodes expanded (nothing collapsed)
INITIAL_COLLAPSED = []

COLUMNS = [
    {"title": "Name", "id": "name", "width": 200, "readonly": True},
    {"title": "Type", "id": "type", "width": 70},
    {"title": "Size", "id": "size", "width": 70},
    {"title": "Rating", "id": "rating", "width": 90},
    {"title": "Trend", "id": "trend", "width": 100},
    {"title": "Progress", "id": "progress", "width": 90},
    {"title": "Action", "id": "action", "width": 80},
    {"title": "Tags", "id": "tags", "width": 120},
    {"title": "Owner", "id": "owner", "width": 120},
    {"title": "Links", "id": "links", "width": 100},
    {"title": "Status", "id": "status", "width": 100},
    {"title": "Labels", "id": "labels", "width": 120},
    {"title": "Date", "id": "date", "width": 100},
    {"title": "Loading", "id": "loading", "width": 60},
]

THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.15)",
    "bgCell": "#ffffff",
    "bgCellMedium": "#f9fafb",
    "bgHeader": "#f3f4f6",
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "borderColor": "#e5e7eb",
}

app.layout = html.Div([
    html.H3("Hidden Rows + Tree View Cells"),
    html.P([
        "Click chevrons to expand/collapse. ",
        html.Strong("Row numbers are preserved"),
        " - notice how collapsing doesn't renumber rows."
    ]),

    html.Div([
        html.Button("Expand All", id="expand-all", style={"marginRight": "8px"}),
        html.Button("Collapse All", id="collapse-all", style={"marginRight": "8px"}),
        html.Span(" | ", style={"color": "#999"}),
        html.Button("Hide Rows 3-5", id="hide-simple", style={"marginRight": "8px"}),
        html.Button("Show All", id="show-all", style={"marginRight": "8px"}),
        html.Span("(simple mode - no data reset)", style={"fontSize": "11px", "color": "#666"}),
    ], style={"marginBottom": "10px"}),

    html.Div([
        dcc.Checklist(
            id="options",
            options=[
                {"label": " Folders unselectable", "value": "folders-unselectable"},
                {"label": " Row select on cell click", "value": "row-select-on-click"},
                {"label": " Draw focus ring", "value": "draw-focus-ring"},
                {"label": " Fill handle", "value": "fill-handle"},
                {"label": " Tab wrapping", "value": "tab-wrapping"},
            ],
            value=["draw-focus-ring", "fill-handle", "tab-wrapping"],
            inline=True,
            style={"marginBottom": "10px"},
            inputStyle={"marginRight": "4px"},
            labelStyle={"marginRight": "16px"},
        ),
    ]),

    html.Div([
        html.Strong("Hidden Rows Config: ", style={"fontSize": "12px"}),
        dcc.Checklist(
            id="hidden-rows-config",
            options=[
                {"label": " Skip on Copy", "value": "skipOnCopy"},
                {"label": " Skip on Paste", "value": "skipOnPaste"},
                {"label": " Skip on Fill", "value": "skipOnFill"},
                {"label": " Skip on Delete", "value": "skipOnDelete"},
                {"label": " Skip on Navigation", "value": "skipOnNavigation"},
            ],
            value=["skipOnCopy", "skipOnPaste", "skipOnFill", "skipOnDelete", "skipOnNavigation"],
            inline=True,
            style={"marginBottom": "10px"},
            inputStyle={"marginRight": "4px"},
            labelStyle={"marginRight": "12px", "fontSize": "12px"},
        ),
    ]),

    html.Div(id="status", style={"marginBottom": "10px", "fontFamily": "monospace", "fontSize": "12px"}),

    html.Div([
        html.Div([
            GlideGrid(
                id="grid",
                columns=COLUMNS,
                data=build_grid_data(INITIAL_COLLAPSED),
                height=450,
                width=1500,
                theme=THEME,
                rowMarkers="both",
                rowSelect="multi",
                hiddenRows=compute_hidden_rows(INITIAL_COLLAPSED),
                hiddenRowsConfig={
                    "skipOnCopy": True,
                    "skipOnPaste": True,
                    "skipOnFill": True,
                    "skipOnDelete": True,
                    "skipOnNavigation": True,
                },
                unselectableRows=[],
                rowSelectOnCellClick=False,
                fillHandle=True,
                tabWrapping=True,
                enableCopyPaste=True,
            ),
        ], style={"display": "inline-block", "verticalAlign": "top"}),

        html.Div([
            html.H4("Edge Case Testing", style={"marginTop": "0"}),
            html.P("Collapse a folder or hide rows 3-5, then test:", style={"fontSize": "13px", "marginBottom": "8px"}),
            html.Ul([
                html.Li("Tab/Arrow: Navigate - should skip hidden rows"),
                html.Li("Fill handle: Drag across hidden rows"),
                html.Li("Delete: Select range spanning hidden, press Delete"),
                html.Li("Copy: Select range spanning hidden, Cmd+C"),
                html.Li("Paste: Copy visible rows, paste into range with hidden"),
                html.Li("Right-click: Should not work on hidden cells"),
            ], style={"fontSize": "12px", "marginBottom": "12px", "paddingLeft": "20px"}),
            html.P("Toggle config checkboxes above to change skip behavior.", style={"fontSize": "11px", "color": "#666", "marginBottom": "8px"}),

            html.Div([
                html.Strong("Selected Cell: ", style={"fontSize": "12px"}),
                html.Span(id="selected-cell", style={"fontFamily": "monospace", "fontSize": "12px"}),
            ], style={"marginBottom": "4px"}),

            html.Div([
                html.Strong("Selected Range: ", style={"fontSize": "12px"}),
                html.Span(id="selected-range", style={"fontFamily": "monospace", "fontSize": "12px"}),
            ], style={"marginBottom": "4px"}),

            html.Div([
                html.Strong("Hidden Rows: ", style={"fontSize": "12px"}),
                html.Span(id="hidden-rows-display", style={"fontFamily": "monospace", "fontSize": "12px"}),
            ], style={"marginBottom": "8px"}),

            html.Div([
                html.Strong("Last Event:", style={"fontSize": "12px"}),
                html.Pre(id="last-event", style={
                    "fontFamily": "monospace",
                    "fontSize": "11px",
                    "backgroundColor": "#f5f5f5",
                    "padding": "8px",
                    "borderRadius": "4px",
                    "maxHeight": "150px",
                    "overflow": "auto",
                    "margin": "4px 0",
                    "whiteSpace": "pre-wrap",
                }),
            ]),
        ], style={"display": "inline-block", "verticalAlign": "top", "marginLeft": "20px", "width": "300px"}),
    ]),

    dcc.Store(id="collapsed-store", data=INITIAL_COLLAPSED),
    dcc.Store(id="hidden-rows-store", data=compute_hidden_rows(INITIAL_COLLAPSED)),
], style={"padding": "20px", "fontFamily": "system-ui, sans-serif"})


@callback(
    Output("grid", "unselectableRows"),
    Output("grid", "rowSelectOnCellClick"),
    Output("grid", "drawFocusRing"),
    Output("grid", "fillHandle"),
    Output("grid", "tabWrapping"),
    Input("options", "value"),
)
def update_options(options):
    options = options or []
    unselectable = FOLDER_ROWS if "folders-unselectable" in options else []
    row_select_on_click = "row-select-on-click" in options
    draw_focus_ring = "draw-focus-ring" in options
    fill_handle = "fill-handle" in options
    tab_wrapping = "tab-wrapping" in options
    return unselectable, row_select_on_click, draw_focus_ring, fill_handle, tab_wrapping


@callback(
    Output("grid", "hiddenRowsConfig"),
    Input("hidden-rows-config", "value"),
)
def update_hidden_rows_config(config_values):
    """Update hiddenRowsConfig based on checklist selection"""
    config_values = config_values or []
    return {
        "skipOnCopy": "skipOnCopy" in config_values,
        "skipOnPaste": "skipOnPaste" in config_values,
        "skipOnFill": "skipOnFill" in config_values,
        "skipOnDelete": "skipOnDelete" in config_values,
        "skipOnNavigation": "skipOnNavigation" in config_values,
    }


@callback(
    Output("grid", "data"),
    Output("grid", "hiddenRows"),
    Output("collapsed-store", "data"),
    Output("hidden-rows-store", "data"),
    Output("status", "children"),
    Input("grid", "treeNodeToggled"),
    Input("expand-all", "n_clicks"),
    Input("collapse-all", "n_clicks"),
    State("collapsed-store", "data"),
    State("grid", "data"),
    prevent_initial_call=True,
)
def handle_toggle(toggle_info, expand_clicks, collapse_clicks, collapsed, current_data):
    from dash import ctx

    collapsed = collapsed or []
    collapsed_set = set(collapsed)

    trigger = ctx.triggered_id

    if trigger == "expand-all":
        collapsed_set = set()
        status = "All nodes expanded (edits preserved)"

    elif trigger == "collapse-all":
        # Collapse all nodes that have children
        collapsed_set = {node["id"] for node in TREE_DATA if has_children(node["id"])}
        status = "All nodes collapsed (edits preserved)"

    elif trigger == "grid" and toggle_info:
        row_idx = toggle_info["row"]
        node_id = ROW_TO_ID.get(row_idx)
        if node_id:
            if toggle_info["isOpen"]:
                # Opening: remove from collapsed set
                collapsed_set.discard(node_id)
                status = f"Expanded '{node_id}' (row {row_idx})"
            else:
                # Closing: add to collapsed set
                collapsed_set.add(node_id)
                status = f"Collapsed '{node_id}' (row {row_idx})"
        else:
            status = f"Unknown row {row_idx}"
    else:
        status = "Ready"

    collapsed_list = list(collapsed_set)
    hidden_rows = compute_hidden_rows(collapsed_list)

    # Use update_tree_cells_only to preserve edits in other columns
    updated_data = update_tree_cells_only(current_data, collapsed_list)

    return (
        updated_data,
        hidden_rows,
        collapsed_list,
        hidden_rows,
        f"{status} | Hidden: {hidden_rows if hidden_rows else 'none'} | Folders: {FOLDER_ROWS}",
    )


@callback(
    Output("grid", "hiddenRows", allow_duplicate=True),
    Output("hidden-rows-store", "data", allow_duplicate=True),
    Output("status", "children", allow_duplicate=True),
    Input("hide-simple", "n_clicks"),
    Input("show-all", "n_clicks"),
    prevent_initial_call=True,
)
def handle_simple_hide(hide_clicks, show_clicks):
    """Simple hide/show that doesn't reset data - useful for testing fill/delete"""
    from dash import ctx

    trigger = ctx.triggered_id
    if trigger == "hide-simple":
        hidden = [3, 4, 5]
        status = "Simple mode: Hidden rows 3-5 (data NOT reset - edits preserved)"
    else:
        hidden = []
        status = "Simple mode: All rows visible (data NOT reset - edits preserved)"

    return hidden, hidden, status


@callback(
    Output("selected-cell", "children"),
    Output("selected-range", "children"),
    Input("grid", "selectedCell"),
    Input("grid", "selectedRange"),
)
def update_selection_display(cell, range_):
    cell_str = f"col={cell['col']}, row={cell['row']}" if cell else "None"
    if range_:
        range_str = f"rows {range_['startRow']}-{range_['endRow']}, cols {range_['startCol']}-{range_['endCol']}"
    else:
        range_str = "None"
    return cell_str, range_str


@callback(
    Output("hidden-rows-display", "children"),
    Input("hidden-rows-store", "data"),
)
def update_hidden_display(hidden):
    if not hidden:
        return "None"
    return str(hidden)


@callback(
    Output("last-event", "children"),
    Input("grid", "cellEdited"),
    Input("grid", "cellsEdited"),
    Input("grid", "deletePressed"),
    Input("grid", "contextMenu"),
    prevent_initial_call=True,
)
def update_last_event(cell_edited, cells_edited, delete_pressed, context_menu):
    from dash import ctx

    trigger = ctx.triggered_id
    if not trigger:
        return "None"

    prop = ctx.triggered[0]["prop_id"].split(".")[-1]
    value = ctx.triggered[0]["value"]

    if prop == "cellEdited" and value:
        return f"cellEdited:\n  row={value.get('row')}, col={value.get('col')}\n  value={value.get('value')}"
    elif prop == "cellsEdited" and value:
        edits = value.get("edits", [])
        rows = sorted(set(e.get("row") for e in edits))
        return f"cellsEdited:\n  count={value.get('count')}\n  rows affected: {rows}"
    elif prop == "deletePressed" and value:
        cells = value.get("cells", [])
        rows = sorted(set(c.get("row") for c in cells))
        return f"deletePressed:\n  cells={len(cells)}\n  rows affected: {rows}"
    elif prop == "contextMenu" and value:
        return f"contextMenu:\n  row={value.get('row')}, col={value.get('col')}"

    return f"{prop}: {json.dumps(value, indent=2)[:200]}"


if __name__ == "__main__":
    app.run(debug=True, port=8065)
