"""
Example: Built-in Cell Context Menu

Demonstrates the built-in cell context menu feature with functional actions.
Right-click on any cell to see the context menu.
"""

import dash
from dash import html, callback, Input, Output, State, no_update
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

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
    {"id": 4, "product": "Monitor 27\"", "category": "Electronics", "price": 449.99, "stock": 30},
    {"id": 5, "product": "Keyboard RGB", "category": "Accessories", "price": 129.99, "stock": 85},
    {"id": 6, "product": "Webcam HD", "category": "Electronics", "price": 89.99, "stock": 120},
    {"id": 7, "product": "Desk Lamp", "category": "Office", "price": 39.99, "stock": 75},
    {"id": 8, "product": "Chair Ergonomic", "category": "Furniture", "price": 299.99, "stock": 20},
]

app.layout = html.Div([
    html.H1("Cell Context Menu Example"),
    html.P("Right-click on any cell to see the context menu with working actions."),

    html.Div([
        dgg.GlideGrid(
            id="context-menu-grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=350,
            rowHeight=34,
            headerHeight=40,
            rowMarkers="number",
            rangeSelect="rect",
            cellContextMenuConfig={
                "items": [
                    # Built-in copy actions using 'action' property
                    {"id": "copy", "label": "Copy Cell", "action": "copyCell"},
                    {"id": "copy-selection", "label": "Copy Selection", "action": "copySelection"},
                    {"id": "paste", "label": "Paste", "action": "paste", "dividerAfter": True},
                    # Custom actions handled by Python callback
                    {"id": "delete", "label": "Delete Row"},
                    {"id": "details", "label": "View Details"},
                ]
            }
        ),
    ], style={"margin": "20px"}),

    # Action feedback area
    html.Div([
        html.Div([
            html.H4("Last Action:"),
            html.Div(id="action-output", style={
                "fontFamily": "monospace",
                "padding": "15px",
                "backgroundColor": "#e8f4e8",
                "borderRadius": "5px",
                "minHeight": "40px",
                "whiteSpace": "pre-wrap"
            }),
        ], style={"flex": "1"}),
    ], style={"display": "flex", "margin": "20px"}),

    # Details modal
    html.Div(id="details-modal", style={"display": "none"}),

    html.Div([
        html.H4("Context Menu Items:"),
        html.Ul([
            html.Li([html.Strong("Copy Cell"), " - Copies the clicked cell value (native action)"]),
            html.Li([html.Strong("Copy Selection"), " - Copies all cells in the current range selection as TSV (native action)"]),
            html.Li([html.Strong("Paste"), " - Pastes clipboard content starting at clicked cell (native action)"]),
            html.Li([html.Strong("Delete Row"), " - Removes the row from the grid (Python callback)"]),
            html.Li([html.Strong("View Details"), " - Shows detailed information about the row (Python callback)"]),
        ]),
        html.P([
            "Tip: Native actions (copy/paste) work directly in the browser without a server round-trip. ",
            "Custom actions trigger Python callbacks for more complex logic."
        ], style={"fontStyle": "italic", "marginTop": "10px"}),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("context-menu-grid", "data"),
    Output("action-output", "children"),
    Output("details-modal", "children"),
    Output("details-modal", "style"),
    Input("context-menu-grid", "cellContextMenuItemClicked"),
    State("context-menu-grid", "data"),
    prevent_initial_call=True
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
        modal_content = html.Div([
            html.Div([
                html.H3(f"Row Details: {row_data.get('product', 'Unknown')}",
                       style={"marginTop": 0}),
                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td(html.Strong(f"{COLUMNS[i]['title']}:"),
                                   style={"padding": "8px", "textAlign": "right"}),
                            html.Td(str(row_data.get(COLUMNS[i]["id"], "N/A")),
                                   style={"padding": "8px"})
                        ]) for i in range(len(COLUMNS))
                    ])
                ], style={"width": "100%"}),
                html.Button("Close", id="close-modal", n_clicks=0,
                           style={"marginTop": "15px", "padding": "8px 20px"})
            ], style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "8px",
                "boxShadow": "0 4px 20px rgba(0,0,0,0.3)",
                "maxWidth": "400px",
                "margin": "auto"
            })
        ], style={
            "position": "fixed",
            "top": 0, "left": 0, "right": 0, "bottom": 0,
            "backgroundColor": "rgba(0,0,0,0.5)",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "zIndex": 1000
        })
        modal_style = {"display": "block"}

    return new_data, action_msg, modal_content, modal_style


# Close modal callback
@callback(
    Output("details-modal", "style", allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(n_clicks):
    if n_clicks:
        return {"display": "none"}
    return no_update


if __name__ == "__main__":
    app.run(debug=True, port=8050)
