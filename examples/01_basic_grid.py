"""
Example 1: Basic Read-Only Grid
Simple grid displaying data without editing
"""
import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Simple product catalog data
COLUMNS = [
    {'title': 'Product', 'id': 'product', 'width': 250},
    {'title': 'Category', 'id': 'category', 'width': 150},
    {'title': 'Price', 'id': 'price', 'width': 100},
    {'title': 'In Stock', 'id': 'in_stock', 'width': 100},
    {'title': 'Units', 'id': 'units', 'width': 100}
]

DATA = [
    {'product': 'Laptop Pro 15"', 'category': 'Electronics', 'price': 1299.99, 'in_stock': True, 'units': 45},
    {'product': 'Wireless Mouse', 'category': 'Accessories', 'price': 29.99, 'in_stock': True, 'units': 120},
    {'product': 'USB-C Cable', 'category': 'Accessories', 'price': 12.99, 'in_stock': True, 'units': 200},
    {'product': '4K Monitor', 'category': 'Electronics', 'price': 449.99, 'in_stock': False, 'units': 0},
    {'product': 'Mechanical Keyboard', 'category': 'Accessories', 'price': 89.99, 'in_stock': True, 'units': 67},
    {'product': 'Laptop Stand', 'category': 'Accessories', 'price': 39.99, 'in_stock': True, 'units': 88},
    {'product': 'Webcam HD', 'category': 'Electronics', 'price': 79.99, 'in_stock': True, 'units': 34},
    {'product': 'Desk Lamp', 'category': 'Office', 'price': 34.99, 'in_stock': True, 'units': 55},
]

app.layout = html.Div([
    html.H1('Product Catalog - Read-Only Grid'),
    html.P('This grid displays product data without allowing edits'),

    dgg.GlideGrid(
        id='product-grid',
        columns=COLUMNS,
        data=DATA,
        height=350,
        readonly=True,  # Make grid read-only
        rowMarkers='number',  # Show row numbers
        smoothScrollX=True,
        smoothScrollY=True
    ),
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})

if __name__ == '__main__':
    app.run(debug=True, port=8050)
