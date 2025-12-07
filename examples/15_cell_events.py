"""
Example: Cell Events (Context Menu, Activation, Hover)

Demonstrates cellContextMenu, cellActivated, and itemHovered events.
"""

import dash
from dash import html, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions
COLUMNS = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Product", "id": "product", "width": 150},
    {"title": "Category", "id": "category", "width": 120},
    {"title": "Price", "id": "price", "width": 100},
    {"title": "Stock", "id": "stock", "width": 80},
]

# Sample data
DATA = [
    {"id": 1, "product": "Laptop Pro", "category": "Electronics", "price": 1299.99, "stock": 45},
    {"id": 2, "product": "Wireless Mouse", "category": "Accessories", "price": 49.99, "stock": 200},
    {"id": 3, "product": "USB-C Hub", "category": "Accessories", "price": 79.99, "stock": 150},
    {"id": 4, "product": "Monitor 27\"", "category": "Electronics", "price": 449.99, "stock": 30},
    {"id": 5, "product": "Keyboard RGB", "category": "Accessories", "price": 129.99, "stock": 85},
    {"id": 6, "product": "Webcam HD", "category": "Electronics", "price": 89.99, "stock": 120},
    {"id": 7, "product": "Desk Lamp", "category": "Office", "price": 39.99, "stock": 75},
    {"id": 8, "product": "Chair Ergonomic", "category": "Furniture", "price": 299.99, "stock": 20},
    {"id": 9, "product": "Standing Desk", "category": "Furniture", "price": 599.99, "stock": 15},
    {"id": 10, "product": "Cable Organizer", "category": "Office", "price": 19.99, "stock": 300},
]

app.layout = html.Div([
    html.H1("Cell Events Example"),
    html.P([
        "Try: ",
        html.Strong("Double-click"), " a cell (cellActivated), ",
        html.Strong("Right-click"), " a cell (cellContextMenu), ",
        html.Strong("Hover"), " over cells (itemHovered)"
    ]),

    html.Div([
        dgg.GlideGrid(
            id="cell-events-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=34,
            headerHeight=40,
            rowMarkers="number",
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.Div([
            html.H4("Currently Hovered:"),
            html.Div(id="hover-info", style={
                "fontFamily": "monospace",
                "padding": "10px",
                "backgroundColor": "#e8f4e8",
                "minHeight": "40px"
            }),
        ], style={"flex": "1", "marginRight": "10px"}),

        html.Div([
            html.H4("Last Cell Activated (Double-click/Enter):"),
            html.Div(id="activated-info", style={
                "fontFamily": "monospace",
                "padding": "10px",
                "backgroundColor": "#e8e8f4",
                "minHeight": "40px"
            }),
        ], style={"flex": "1", "marginRight": "10px"}),

        html.Div([
            html.H4("Last Context Menu (Right-click):"),
            html.Div(id="context-info", style={
                "fontFamily": "monospace",
                "padding": "10px",
                "backgroundColor": "#f4e8e8",
                "minHeight": "40px"
            }),
        ], style={"flex": "1"}),
    ], style={"display": "flex", "margin": "20px"}),

    html.Div([
        html.H4("Cell Details:"),
        html.Div(id="cell-details", style={
            "fontFamily": "monospace",
            "padding": "15px",
            "backgroundColor": "#f8f8f8",
            "borderRadius": "5px",
            "minHeight": "60px"
        }),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props used:"),
        html.Code("cellActivated"),
        html.P("Fires when a cell is activated (Enter, Space, or double-click). Use for drill-down actions."),
        html.Code("cellContextMenu"),
        html.P("Fires when a cell is right-clicked. Use for custom context menus."),
        html.Code("itemHovered"),
        html.P("Fires when the mouse moves over different grid items. Returns kind: 'cell', 'header', etc."),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("hover-info", "children"),
    Input("cell-events-grid", "itemHovered"),
    prevent_initial_call=True
)
def handle_hover(item_hovered):
    """Update hover display."""
    if not item_hovered:
        return "Nothing hovered"

    kind = item_hovered.get("kind", "unknown")
    col = item_hovered.get("col")
    row = item_hovered.get("row")

    if kind == "cell" and col is not None and row is not None:
        col_name = COLUMNS[col]["title"] if col < len(COLUMNS) else f"Col {col}"
        return f"Cell: Row {row}, Column '{col_name}'"
    elif kind == "header":
        col_name = COLUMNS[col]["title"] if col is not None and col < len(COLUMNS) else f"Col {col}"
        return f"Header: '{col_name}'"
    elif kind == "out-of-bounds":
        return "Outside grid area"
    else:
        return f"Kind: {kind}"


@callback(
    Output("activated-info", "children"),
    Output("cell-details", "children"),
    Input("cell-events-grid", "cellActivated"),
    prevent_initial_call=True
)
def handle_activation(cell_activated):
    """Handle cell activation (double-click, Enter, or Space)."""
    if not cell_activated:
        return "No cell activated yet", ""

    col = cell_activated.get("col", 0)
    row = cell_activated.get("row", 0)

    col_name = COLUMNS[col]["title"] if col < len(COLUMNS) else f"Col {col}"
    col_id = COLUMNS[col]["id"] if col < len(COLUMNS) else None

    # Get cell value
    cell_value = DATA[row].get(col_id, "N/A") if row < len(DATA) and col_id else "N/A"

    activated_text = f"Row {row}, Column '{col_name}'"

    # Build detail view
    if row < len(DATA):
        row_data = DATA[row]
        details = f"""
Activated Cell Details:
-----------------------
Row: {row}
Column: {col} ({col_name})
Value: {cell_value}

Full Row Data:
  ID: {row_data.get('id', 'N/A')}
  Product: {row_data.get('product', 'N/A')}
  Category: {row_data.get('category', 'N/A')}
  Price: ${row_data.get('price', 0):.2f}
  Stock: {row_data.get('stock', 'N/A')} units

💡 In a real app, you might open a detail modal or navigate to a detail page!
        """.strip()
    else:
        details = "Row data not available"

    return activated_text, details


@callback(
    Output("context-info", "children"),
    Input("cell-events-grid", "cellContextMenu"),
    prevent_initial_call=True
)
def handle_context_menu(cell_context):
    """Handle cell right-click."""
    if not cell_context:
        return "No context menu yet"

    col = cell_context.get("col", 0)
    row = cell_context.get("row", 0)

    col_name = COLUMNS[col]["title"] if col < len(COLUMNS) else f"Col {col}"

    return f"Row {row}, Column '{col_name}' - You could show a custom menu!"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
