"""
Example 53: Tree View Cell

This example demonstrates the tree view cell type for hierarchical data:
- Expandable/collapsible nodes with chevron icons
- Indentation based on depth level
- Callback fires when a node is toggled
- Supports dark/light mode themes

Tree view cell data structure:
{
    "kind": "tree-view-cell",
    "text": "Node Name",
    "depth": 0,           # Indentation level (0 = root)
    "isOpen": True,       # Whether node is expanded
    "canOpen": True       # Whether node has children (shows chevron)
}

Note: The tree structure is "flattened" into rows. When a parent is collapsed,
the Dash callback should filter out child rows from the data.
"""

import dash
from dash import html, dcc, callback, Input, Output, State
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__)

# Theme configurations
DARK_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.2)",
    "bgCell": "#1f2937",
    "bgCellMedium": "#374151",
    "bgHeader": "#111827",
    "bgHeaderHasFocus": "#374151",
    "bgHeaderHovered": "#374151",
    "textDark": "#f3f4f6",
    "textMedium": "#9ca3af",
    "textLight": "#6b7280",
    "textHeader": "#f3f4f6",
    "borderColor": "rgba(255, 255, 255, 0.1)",
    "horizontalBorderColor": "rgba(255, 255, 255, 0.1)",
}

LIGHT_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.1)",
    "bgCell": "#ffffff",
    "bgCellMedium": "#f9fafb",
    "bgHeader": "#f3f4f6",
    "bgHeaderHasFocus": "#e5e7eb",
    "bgHeaderHovered": "#e5e7eb",
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "textLight": "#9ca3af",
    "textHeader": "#111827",
    "borderColor": "#e5e7eb",
    "horizontalBorderColor": "#e5e7eb",
}

# Hierarchical data structure (stored in a Store, not directly in grid)
# Each node has: id, parent_id, name, type, size
TREE_DATA = [
    {"id": "root", "parent_id": None, "name": "Project Root", "type": "folder", "size": "-"},
    {"id": "src", "parent_id": "root", "name": "src", "type": "folder", "size": "-"},
    {"id": "src_components", "parent_id": "src", "name": "components", "type": "folder", "size": "-"},
    {"id": "src_components_button", "parent_id": "src_components", "name": "Button.tsx", "type": "file", "size": "2.4 KB"},
    {"id": "src_components_input", "parent_id": "src_components", "name": "Input.tsx", "type": "file", "size": "3.1 KB"},
    {"id": "src_components_modal", "parent_id": "src_components", "name": "Modal.tsx", "type": "file", "size": "4.8 KB"},
    {"id": "src_utils", "parent_id": "src", "name": "utils", "type": "folder", "size": "-"},
    {"id": "src_utils_api", "parent_id": "src_utils", "name": "api.ts", "type": "file", "size": "1.2 KB"},
    {"id": "src_utils_helpers", "parent_id": "src_utils", "name": "helpers.ts", "type": "file", "size": "0.8 KB"},
    {"id": "src_app", "parent_id": "src", "name": "App.tsx", "type": "file", "size": "5.6 KB"},
    {"id": "src_index", "parent_id": "src", "name": "index.tsx", "type": "file", "size": "0.5 KB"},
    {"id": "public", "parent_id": "root", "name": "public", "type": "folder", "size": "-"},
    {"id": "public_index", "parent_id": "public", "name": "index.html", "type": "file", "size": "1.1 KB"},
    {"id": "public_favicon", "parent_id": "public", "name": "favicon.ico", "type": "file", "size": "4.2 KB"},
    {"id": "package", "parent_id": "root", "name": "package.json", "type": "file", "size": "1.8 KB"},
    {"id": "readme", "parent_id": "root", "name": "README.md", "type": "file", "size": "2.3 KB"},
]


def get_node_depth(node_id, tree_data):
    """Calculate depth by counting parent levels"""
    depth = 0
    node = next((n for n in tree_data if n["id"] == node_id), None)
    while node and node["parent_id"]:
        depth += 1
        node = next((n for n in tree_data if n["id"] == node["parent_id"]), None)
    return depth


def has_children(node_id, tree_data):
    """Check if node has any children"""
    return any(n["parent_id"] == node_id for n in tree_data)


def build_visible_rows(tree_data, expanded_nodes):
    """Build the flattened list of visible rows based on expanded state"""
    visible = []

    def add_children(parent_id):
        children = [n for n in tree_data if n["parent_id"] == parent_id]
        # Sort: folders first, then alphabetically
        children.sort(key=lambda x: (0 if x["type"] == "folder" else 1, x["name"]))

        for node in children:
            depth = get_node_depth(node["id"], tree_data)
            can_open = has_children(node["id"], tree_data)
            is_open = node["id"] in expanded_nodes

            visible.append({
                "id": node["id"],
                "name": {
                    "kind": "tree-view-cell",
                    "text": node["name"],
                    "depth": depth,
                    "isOpen": is_open,
                    "canOpen": can_open,
                },
                "type": node["type"].capitalize(),
                "size": node["size"],
            })

            # If expanded, add children recursively
            if is_open and can_open:
                add_children(node["id"])

    # Only show root's children if root is expanded
    if "root" in expanded_nodes:
        add_children("root")

    # Also add root itself at the top
    root = next((n for n in tree_data if n["id"] == "root"), None)
    if root:
        root_row = {
            "id": "root",
            "name": {
                "kind": "tree-view-cell",
                "text": root["name"],
                "depth": 0,
                "isOpen": "root" in expanded_nodes,
                "canOpen": has_children("root", tree_data),
            },
            "type": root["type"].capitalize(),
            "size": root["size"],
        }
        visible.insert(0, root_row)

    return visible


# Initial expanded nodes (root and src expanded)
INITIAL_EXPANDED = {"root", "src"}

COLUMNS = [
    {"title": "Name", "id": "name", "width": 250},
    {"title": "Type", "id": "type", "width": 80},
    {"title": "Size", "id": "size", "width": 80},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Tree View Cell Example", id="title"),
        html.P("Click the chevron icons to expand/collapse folders.", id="subtitle"),
        html.Button(
            "Toggle Dark Mode",
            id="theme-toggle",
            style={
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
            },
        ),
        html.Button(
            "Expand All",
            id="expand-all",
            style={
                "marginBottom": "15px",
                "marginLeft": "8px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
            },
        ),
        html.Button(
            "Collapse All",
            id="collapse-all",
            style={
                "marginBottom": "15px",
                "marginLeft": "8px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
            },
        ),
        GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=build_visible_rows(TREE_DATA, INITIAL_EXPANDED),
            height=400,
            width="100%",
            theme=LIGHT_THEME,
        ),
        # Store for expanded nodes
        dcc.Store(id="expanded-nodes", data=list(INITIAL_EXPANDED)),
        # Store for tree data
        dcc.Store(id="tree-data", data=TREE_DATA),
        html.Div(
            id="toggle-output",
            style={
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#f3f4f6",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
            },
            children="Click a chevron to see toggle callback data..."
        ),
    ],
    style={"padding": "20px", "maxWidth": "600px", "fontFamily": "system-ui, sans-serif"},
)


@callback(
    Output("grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("expand-all", "style"),
    Output("collapse-all", "style"),
    Output("theme-toggle", "children"),
    Output("toggle-output", "style"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

    btn_style_light = {
        "marginBottom": "15px",
        "padding": "8px 16px",
        "cursor": "pointer",
        "borderRadius": "6px",
        "border": "1px solid #d1d5db",
        "backgroundColor": "#f3f4f6",
        "color": "#111827",
    }
    btn_style_dark = {
        "marginBottom": "15px",
        "padding": "8px 16px",
        "cursor": "pointer",
        "borderRadius": "6px",
        "border": "1px solid #4b5563",
        "backgroundColor": "#374151",
        "color": "#f3f4f6",
    }
    btn_style_light_ml = {**btn_style_light, "marginLeft": "8px"}
    btn_style_dark_ml = {**btn_style_dark, "marginLeft": "8px"}

    if is_dark:
        return (
            DARK_THEME,
            {
                "padding": "20px",
                "maxWidth": "600px",
                "fontFamily": "system-ui, sans-serif",
                "backgroundColor": "#111827",
                "minHeight": "100vh",
            },
            {"color": "#f3f4f6"},
            {"color": "#9ca3af"},
            btn_style_dark,
            btn_style_dark_ml,
            btn_style_dark_ml,
            "Toggle Light Mode",
            {
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#374151",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
                "color": "#f3f4f6",
            },
        )
    else:
        return (
            LIGHT_THEME,
            {
                "padding": "20px",
                "maxWidth": "600px",
                "fontFamily": "system-ui, sans-serif",
            },
            {"color": "#111827"},
            {"color": "#6b7280"},
            btn_style_light,
            btn_style_light_ml,
            btn_style_light_ml,
            "Toggle Dark Mode",
            {
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#f3f4f6",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
                "color": "#111827",
            },
        )


@callback(
    Output("grid", "data"),
    Output("expanded-nodes", "data"),
    Output("toggle-output", "children"),
    Input("grid", "treeNodeToggled"),
    Input("expand-all", "n_clicks"),
    Input("collapse-all", "n_clicks"),
    State("expanded-nodes", "data"),
    State("tree-data", "data"),
    prevent_initial_call=True,
)
def handle_tree_toggle(toggle_info, expand_clicks, collapse_clicks, expanded_nodes, tree_data):
    from dash import ctx

    expanded_set = set(expanded_nodes or [])
    output_text = "Click a chevron to see toggle callback data..."

    if ctx.triggered_id == "expand-all":
        # Expand all nodes that can be opened
        expanded_set = {n["id"] for n in tree_data if has_children(n["id"], tree_data)}
        output_text = "Expanded all nodes"
    elif ctx.triggered_id == "collapse-all":
        # Collapse all nodes
        expanded_set = set()
        output_text = "Collapsed all nodes"
    elif toggle_info:
        # Get the node ID from the grid data
        row_idx = toggle_info["row"]
        visible_rows = build_visible_rows(tree_data, expanded_set)
        if 0 <= row_idx < len(visible_rows):
            node_id = visible_rows[row_idx]["id"]
            if toggle_info["isOpen"]:
                expanded_set.add(node_id)
            else:
                expanded_set.discard(node_id)
            output_text = f"Toggle: {toggle_info}"

    new_data = build_visible_rows(tree_data, expanded_set)
    return new_data, list(expanded_set), output_text


if __name__ == "__main__":
    app.run(debug=True, port=8053)
