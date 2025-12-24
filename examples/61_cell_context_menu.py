"""
Example: Built-in Cell Context Menu

Demonstrates the built-in cell context menu feature with functional actions.
Right-click on any cell to see the context menu.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

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

# Column definitions
COLUMNS = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Product", "id": "product", "width": 150},
    {"title": "Category", "id": "category", "width": 120},
    {"title": "Price", "id": "price", "width": 100},
    {"title": "Stock", "id": "stock", "width": 80},
]

# Initial sample data
INITIAL_DATA = [
    {"id": 1, "product": "Laptop Pro", "category": "Electronics", "price": 1299.99, "stock": 45},
    {"id": 2, "product": "Wireless Mouse", "category": "Accessories", "price": 49.99, "stock": 200},
    {"id": 3, "product": "USB-C Hub", "category": "Accessories", "price": 79.99, "stock": 150},
    {"id": 4, "product": 'Monitor 27"', "category": "Electronics", "price": 449.99, "stock": 30},
    {"id": 5, "product": "Keyboard RGB", "category": "Accessories", "price": 129.99, "stock": 85},
    {"id": 6, "product": "Webcam HD", "category": "Electronics", "price": 89.99, "stock": 120},
    {"id": 7, "product": "Desk Lamp", "category": "Office", "price": 39.99, "stock": 75},
    {"id": 8, "product": "Chair Ergonomic", "category": "Furniture", "price": 299.99, "stock": 20},
    {"id": 9, "product": "Standing Desk", "category": "Furniture", "price": 599.99, "stock": 15},
    {"id": 10, "product": "Headphones Pro", "category": "Electronics", "price": 249.99, "stock": 60},
    {"id": 11, "product": "Mouse Pad XL", "category": "Accessories", "price": 29.99, "stock": 300},
    {"id": 12, "product": "Monitor Arm", "category": "Accessories", "price": 89.99, "stock": 45},
    {"id": 13, "product": "Cable Management", "category": "Office", "price": 19.99, "stock": 500},
    {"id": 14, "product": "Desk Organizer", "category": "Office", "price": 34.99, "stock": 180},
    {"id": 15, "product": "Laptop Stand", "category": "Accessories", "price": 59.99, "stock": 95},
    {"id": 16, "product": "USB Microphone", "category": "Electronics", "price": 129.99, "stock": 70},
    {"id": 17, "product": "Ring Light", "category": "Electronics", "price": 49.99, "stock": 110},
    {"id": 18, "product": "Whiteboard", "category": "Office", "price": 79.99, "stock": 40},
    {"id": 19, "product": "Footrest", "category": "Furniture", "price": 44.99, "stock": 55},
    {"id": 20, "product": "Filing Cabinet", "category": "Furniture", "price": 149.99, "stock": 25},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Cell Context Menu Example", id="title"),
        html.P(
            "Right-click on any cell to see the context menu with working actions.",
            id="subtitle",
        ),
        html.Div(
            [
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
                html.Label(" Scroll Behavior: ", style={"marginLeft": "20px"}),
                dcc.Dropdown(
                    id="scroll-behavior-dropdown",
                    options=[
                        {"label": "default", "value": "default"},
                        {"label": "close-overlay-on-scroll", "value": "close-overlay-on-scroll"},
                        {"label": "lock-scroll", "value": "lock-scroll"},
                    ],
                    value="default",
                    clearable=False,
                    style={"width": "220px", "display": "inline-block", "verticalAlign": "middle"},
                ),
            ],
            style={"display": "flex", "alignItems": "center", "marginBottom": "15px"},
        ),
        html.Div(
            [
                dgg.GlideGrid(
                    id="context-menu-grid",
                    columns=COLUMNS,
                    data=INITIAL_DATA,
                    height=350,
                    rowHeight=34,
                    headerHeight=40,
                    rowMarkers="number",
                    rangeSelect="rect",
                    theme=LIGHT_THEME,
                    contextMenuConfig={
                        "maxHeight": "150px",  # Enable scrolling with fixed height
                        "items": [
                            # Built-in copy actions using 'action' property
                            # Using monochrome Unicode symbols
                            {
                                "id": "copy",
                                "label": "Copy Cell",
                                "icon": "⧉",
                                "action": "copyClickedCell",
                            },
                            {
                                "id": "copy-selection",
                                "label": "Copy Selection",
                                "icon": "⧉",
                                "action": "copySelection",
                            },
                            {
                                "id": "paste-cell",
                                "label": "Paste at Cell",
                                "icon": "⎘",
                                "iconSize": "19px",
                                "action": "pasteAtClickedCell",
                            },
                            {
                                "id": "paste-selection",
                                "label": "Paste at Selection",
                                "icon": "⎘",
                                "iconSize": "19px",
                                "action": "pasteAtSelection",
                                "dividerAfter": True,
                            },
                            # Custom actions handled by Python callback
                            {
                                "id": "delete",
                                "label": "Delete Row",
                                "icon": "✕",
                                "iconWeight": "800",
                                "color": "#dc2626",  # red label
                                # "fontWeight": "600",  # semi-bold label
                                "iconColor": "#dc2626",  # red icon
                            },
                            {
                                "id": "details",
                                "label": "View Details",
                                "color": "#4762BC",  # blue label
                                "icon": "\u24d8",
                                "iconSize": "11px",
                                "iconWeight": "800",
                                "iconColor": "#4762BC",  # blue icon
                            },
                        ]
                    },
                ),
            ],
            style={"margin": "20px 0"},
        ),
        # Action feedback area
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Last Action:", id="action-label"),
                        html.Div(
                            id="action-output",
                            style={
                                "fontFamily": "monospace",
                                "padding": "15px",
                                "backgroundColor": "#e8f4e8",
                                "borderRadius": "5px",
                                "minHeight": "40px",
                                "whiteSpace": "pre-wrap",
                            },
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={"display": "flex", "margin": "20px 0"},
        ),
        # Details modal
        html.Div(id="details-modal", style={"display": "none"}),
        html.Div(
            id="info-box",
            children=[
                html.H4("Context Menu Items:"),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Strong("Copy Cell"),
                                " - Copies the clicked cell value (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Copy Selection"),
                                " - Copies all cells in the current range selection as TSV (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Paste at Cell"),
                                " - Pastes clipboard content at the right-clicked cell (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Paste at Selection"),
                                " - Pastes clipboard content at top-left of selection (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Delete Row"),
                                " - Removes the row from the grid (Python callback)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("View Details"),
                                " - Shows detailed information about the row (Python callback)",
                            ]
                        ),
                    ]
                ),
                html.P(
                    [
                        "Tip: Native actions (copy/paste) work directly in the browser without a server round-trip. ",
                        "Custom actions trigger Python callbacks for more complex logic.",
                    ],
                    style={"fontStyle": "italic", "marginTop": "10px"},
                ),
            ],
            style={
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#f5f5f5",
                "borderRadius": "6px",
            },
        ),
        # Store for theme state
        dcc.Store(id="theme-store", data="light"),
    ],
    style={
        "padding": "20px",
        "maxWidth": "800px",
        "fontFamily": "system-ui, sans-serif",
    },
)


@callback(
    Output("context-menu-grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Output("action-output", "style"),
    Output("action-label", "style"),
    Output("info-box", "style"),
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

    if is_dark:
        return (
            DARK_THEME,
            {
                "padding": "20px",
                "maxWidth": "800px",
                "fontFamily": "system-ui, sans-serif",
                "backgroundColor": "#111827",
                "minHeight": "100vh",
            },
            {"color": "#f3f4f6"},
            {"color": "#9ca3af"},
            btn_style_dark,
            "Toggle Light Mode",
            {
                "fontFamily": "monospace",
                "padding": "15px",
                "backgroundColor": "#374151",
                "borderRadius": "5px",
                "minHeight": "40px",
                "whiteSpace": "pre-wrap",
                "color": "#f3f4f6",
            },
            {"color": "#f3f4f6"},
            {
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#374151",
                "borderRadius": "6px",
                "color": "#f3f4f6",
            },
        )
    else:
        return (
            LIGHT_THEME,
            {
                "padding": "20px",
                "maxWidth": "800px",
                "fontFamily": "system-ui, sans-serif",
            },
            {"color": "#111827"},
            {"color": "#6b7280"},
            btn_style_light,
            "Toggle Dark Mode",
            {
                "fontFamily": "monospace",
                "padding": "15px",
                "backgroundColor": "#e8f4e8",
                "borderRadius": "5px",
                "minHeight": "40px",
                "whiteSpace": "pre-wrap",
            },
            {"color": "#111827"},
            {
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#f5f5f5",
                "borderRadius": "6px",
            },
        )


@callback(
    Output("context-menu-grid", "data"),
    Output("action-output", "children"),
    Output("details-modal", "children"),
    Output("details-modal", "style"),
    Input("context-menu-grid", "contextMenuItemClicked"),
    State("context-menu-grid", "data"),
    prevent_initial_call=True,
)
def handle_context_menu(item, current_data):
    """Handle context menu actions."""
    if not item:
        return no_update, no_update, no_update, no_update

    col = item.get("col", 0)
    row = item.get("row", 0)
    item_id = item.get("itemId", "")

    # Get column info
    col_id = COLUMNS[col]["id"] if col < len(COLUMNS) else None

    # Get row data
    row_data = current_data[row] if row < len(current_data) else {}
    cell_value = row_data.get(col_id, "") if col_id else ""

    # Default outputs (no change)
    new_data = no_update
    action_msg = no_update
    modal_content = no_update
    modal_style = {"display": "none"}

    # Native actions just show a message - the actual copy/paste is handled by the component
    if item_id == "copy":
        action_msg = f"Copied cell value: {cell_value}"

    elif item_id == "copy-selection":
        action_msg = "Copied selection to clipboard"

    elif item_id == "paste":
        action_msg = "Pasted from clipboard"

    elif item_id == "delete":
        # Delete action - remove the row
        if row < len(current_data):
            new_data = [r for i, r in enumerate(current_data) if i != row]
            deleted_product = row_data.get("product", f"Row {row + 1}")
            action_msg = f"Deleted: {deleted_product}"

    elif item_id == "details":
        # Details action - show modal with row info
        action_msg = f"Viewing details for Row {row + 1}"
        modal_content = html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            f"Row Details: {row_data.get('product', 'Unknown')}",
                            style={"marginTop": 0},
                        ),
                        html.Table(
                            [
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td(
                                                    html.Strong(
                                                        f"{COLUMNS[i]['title']}:"
                                                    ),
                                                    style={
                                                        "padding": "8px",
                                                        "textAlign": "right",
                                                    },
                                                ),
                                                html.Td(
                                                    str(
                                                        row_data.get(
                                                            COLUMNS[i]["id"], "N/A"
                                                        )
                                                    ),
                                                    style={"padding": "8px"},
                                                ),
                                            ]
                                        )
                                        for i in range(len(COLUMNS))
                                    ]
                                )
                            ],
                            style={"width": "100%"},
                        ),
                        html.Button(
                            "Close",
                            id="close-modal",
                            n_clicks=0,
                            style={"marginTop": "15px", "padding": "8px 20px"},
                        ),
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.3)",
                        "maxWidth": "400px",
                        "margin": "auto",
                    },
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "backgroundColor": "rgba(0,0,0,0.5)",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "zIndex": 1000,
            },
        )
        modal_style = {"display": "block"}

    return new_data, action_msg, modal_content, modal_style


# Close modal callback
@callback(
    Output("details-modal", "style", allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    prevent_initial_call=True,
)
def close_modal(n_clicks):
    if n_clicks:
        return {"display": "none"}
    return no_update


@callback(
    Output("context-menu-grid", "contextMenuScrollBehavior"),
    Input("scroll-behavior-dropdown", "value"),
)
def update_scroll_behavior(value):
    return value


if __name__ == "__main__":
    app.run(debug=True, port=8061)
