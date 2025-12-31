"""
Example 65: Hidden Rows with Tree View Cells

Demonstrates using hiddenRows with tree-view-cell for collapse/expand that:
- Preserves original row numbers (unlike filtering/rebuilding data)
- Maintains selection state on hidden rows (reappears when unhidden)
- Provides instant visual collapse without data manipulation

Compare to example 53 which rebuilds the data array on each toggle.
This approach is more efficient and preserves row identity.
"""

import dash
from dash import html, callback, Input, Output, State
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
    for node in TREE_DATA:
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
        })
    return data


# Initial state: all nodes expanded (nothing collapsed)
INITIAL_COLLAPSED = []

COLUMNS = [
    {"title": "Name", "id": "name", "width": 250},
    {"title": "Type", "id": "type", "width": 80},
    {"title": "Size", "id": "size", "width": 80},
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
        " - notice how collapsing doesn't renumber rows. ",
        "Selection state is also preserved on hidden rows."
    ]),

    html.Div([
        html.Button("Expand All", id="expand-all", style={"marginRight": "8px"}),
        html.Button("Collapse All", id="collapse-all", style={"marginRight": "8px"}),
        html.Button("Select Rows 3-5", id="select-rows", style={"marginRight": "8px"}),
    ], style={"marginBottom": "10px"}),

    html.Div(id="status", style={"marginBottom": "10px", "fontFamily": "monospace"}),

    GlideGrid(
        id="grid",
        columns=COLUMNS,
        data=build_grid_data(INITIAL_COLLAPSED),
        height=450,
        width=500,
        theme=THEME,
        rowMarkers="number",
        rowSelect="multi",
        hiddenRows=compute_hidden_rows(INITIAL_COLLAPSED),
    ),

    html.Div(id="collapsed-store", style={"display": "none"}, children=str(INITIAL_COLLAPSED)),
], style={"padding": "20px", "fontFamily": "system-ui, sans-serif"})


@callback(
    Output("grid", "data"),
    Output("grid", "hiddenRows"),
    Output("collapsed-store", "children"),
    Output("status", "children"),
    Input("grid", "treeNodeToggled"),
    Input("expand-all", "n_clicks"),
    Input("collapse-all", "n_clicks"),
    State("collapsed-store", "children"),
    prevent_initial_call=True,
)
def handle_toggle(toggle_info, expand_clicks, collapse_clicks, collapsed_str):
    from dash import ctx
    import ast

    # Parse collapsed nodes from store
    try:
        collapsed = ast.literal_eval(collapsed_str) if collapsed_str else []
    except (ValueError, SyntaxError):
        collapsed = []
    collapsed_set = set(collapsed)

    trigger = ctx.triggered_id

    if trigger == "expand-all":
        collapsed_set = set()
        status = "All nodes expanded"

    elif trigger == "collapse-all":
        # Collapse all nodes that have children
        collapsed_set = {node["id"] for node in TREE_DATA if has_children(node["id"])}
        status = f"All nodes collapsed"

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

    return (
        build_grid_data(collapsed_list),
        hidden_rows,
        str(collapsed_list),
        f"{status} | Hidden rows: {hidden_rows if hidden_rows else 'none'}",
    )


@callback(
    Output("grid", "selectedRows"),
    Input("select-rows", "n_clicks"),
    prevent_initial_call=True,
)
def select_rows(n_clicks):
    # Select rows 3, 4, 5 to demonstrate selection persistence
    return [3, 4, 5]


if __name__ == "__main__":
    app.run(debug=True, port=8065)
