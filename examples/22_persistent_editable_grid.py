"""
Example 22: Persistent Editable Grid
Demonstrates an editable grid that persists data using browser session storage.
When you refresh the page, your edits are preserved. Data clears when browser is closed.
"""
import dash
from dash import html, dcc, Input, Output, State, callback, ctx
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Default data used when no saved data exists
DEFAULT_COLUMNS = [
    {'title': 'Product', 'id': 'product', 'width': 200},
    {'title': 'Category', 'id': 'category', 'width': 150},
    {'title': 'Price', 'id': 'price', 'width': 100},
    {'title': 'In Stock', 'id': 'in_stock', 'width': 100},
    {'title': 'Rating', 'id': 'rating', 'width': 100}
]

DEFAULT_DATA = [
    {'product': 'Laptop Pro', 'category': 'Electronics', 'price': 1299.99, 'in_stock': True, 'rating': 4.8},
    {'product': 'Wireless Mouse', 'category': 'Electronics', 'price': 29.99, 'in_stock': True, 'rating': 4.5},
    {'product': 'Standing Desk', 'category': 'Furniture', 'price': 449.00, 'in_stock': True, 'rating': 4.7},
    {'product': 'Ergonomic Chair', 'category': 'Furniture', 'price': 299.00, 'in_stock': False, 'rating': 4.2},
    {'product': 'USB-C Hub', 'category': 'Electronics', 'price': 49.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Desk Lamp', 'category': 'Accessories', 'price': 34.99, 'in_stock': True, 'rating': 4.6},
    {'product': 'Keyboard', 'category': 'Electronics', 'price': 89.99, 'in_stock': True, 'rating': 4.4},
    {'product': 'Monitor Stand', 'category': 'Furniture', 'price': 79.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Webcam HD', 'category': 'Electronics', 'price': 79.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Notebook Set', 'category': 'Office', 'price': 12.99, 'in_stock': True, 'rating': 4.0},
    {'product': 'Pen Holder', 'category': 'Office', 'price': 8.99, 'in_stock': True, 'rating': 3.9},
    {'product': 'Filing Cabinet', 'category': 'Furniture', 'price': 189.00, 'in_stock': False, 'rating': 4.1},
    {'product': 'Whiteboard', 'category': 'Office', 'price': 45.99, 'in_stock': True, 'rating': 4.4},
    {'product': 'Desk Organizer', 'category': 'Accessories', 'price': 24.99, 'in_stock': True, 'rating': 4.2},
    {'product': 'Cable Management Kit', 'category': 'Accessories', 'price': 19.99, 'in_stock': True, 'rating': 4.5},
    {'product': 'External SSD 1TB', 'category': 'Electronics', 'price': 109.99, 'in_stock': True, 'rating': 4.7},
    {'product': 'Wireless Charger', 'category': 'Electronics', 'price': 34.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Headphone Stand', 'category': 'Accessories', 'price': 29.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Desk Mat XL', 'category': 'Accessories', 'price': 39.99, 'in_stock': True, 'rating': 4.6},
    {'product': 'Monitor Light Bar', 'category': 'Electronics', 'price': 54.99, 'in_stock': True, 'rating': 4.5},
    {'product': 'Footrest', 'category': 'Furniture', 'price': 49.99, 'in_stock': True, 'rating': 4.0},
    {'product': 'Laptop Stand', 'category': 'Accessories', 'price': 44.99, 'in_stock': True, 'rating': 4.4},
    {'product': 'Bluetooth Speaker', 'category': 'Electronics', 'price': 59.99, 'in_stock': True, 'rating': 4.2},
    {'product': 'Desk Clock', 'category': 'Accessories', 'price': 22.99, 'in_stock': True, 'rating': 3.8},
    {'product': 'Plant Pot', 'category': 'Decor', 'price': 15.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Wall Calendar', 'category': 'Office', 'price': 9.99, 'in_stock': True, 'rating': 3.7},
    {'product': 'Sticky Notes Pack', 'category': 'Office', 'price': 6.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Highlighter Set', 'category': 'Office', 'price': 7.99, 'in_stock': True, 'rating': 4.2},
    {'product': 'Bookends', 'category': 'Accessories', 'price': 18.99, 'in_stock': True, 'rating': 4.0},
    {'product': 'Desk Fan', 'category': 'Electronics', 'price': 32.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Paper Shredder', 'category': 'Office', 'price': 89.99, 'in_stock': False, 'rating': 4.0},
    {'product': 'Label Maker', 'category': 'Office', 'price': 39.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Stapler', 'category': 'Office', 'price': 11.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Tape Dispenser', 'category': 'Office', 'price': 8.99, 'in_stock': True, 'rating': 3.9},
    {'product': 'Scissors Set', 'category': 'Office', 'price': 14.99, 'in_stock': True, 'rating': 4.2},
    {'product': 'Drawer Organizer', 'category': 'Accessories', 'price': 21.99, 'in_stock': True, 'rating': 4.0},
    {'product': 'Mouse Pad', 'category': 'Accessories', 'price': 12.99, 'in_stock': True, 'rating': 4.4},
    {'product': 'Wrist Rest', 'category': 'Accessories', 'price': 16.99, 'in_stock': True, 'rating': 4.3},
    {'product': 'Screen Cleaner', 'category': 'Accessories', 'price': 9.99, 'in_stock': True, 'rating': 4.1},
    {'product': 'Surge Protector', 'category': 'Electronics', 'price': 29.99, 'in_stock': True, 'rating': 4.5},
]


app.layout = html.Div([
    # Session storage persists across page refreshes but clears when browser closes
    dcc.Store(id='data-store', storage_type='session'),

    html.H1('Persistent Product Inventory'),
    html.P([
        'Edit any cell by clicking on it. Your changes persist across page refreshes. ',
        html.Strong('Close the browser to clear the data.')
    ]),

    dgg.GlideGrid(
        id='persistent-grid',
        columns=DEFAULT_COLUMNS,
        data=DEFAULT_DATA,
        height=350,
        rowMarkers='number',
        columnResize=True
    ),

    html.Div([
        html.Button('Reset to Default Data', id='reset-button', style={
            'marginTop': '20px',
            'padding': '10px 20px',
            'backgroundColor': '#dc3545',
            'color': 'white',
            'border': 'none',
            'borderRadius': '4px',
            'cursor': 'pointer'
        }),
    ]),

    html.Div([
        html.H3('Last Edit:'),
        html.Div(id='edit-status', children='No edits yet', style={
            'marginTop': '10px',
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'border': '1px solid #dee2e6',
            'borderRadius': '4px',
        })
    ], style={'marginTop': '30px'}),

    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li('Data is stored in browser session storage (dcc.Store)'),
            html.Li('Every edit triggers a callback that saves the updated data'),
            html.Li('Refresh the page - your edits persist!'),
            html.Li('Close the browser to clear the data'),
            html.Li('Click "Reset to Default Data" to restore the original values'),
        ])
    ], style={'marginTop': '30px', 'color': '#6c757d'})

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


# Load persisted data from session storage on page load
@callback(
    Output('persistent-grid', 'data'),
    Input('data-store', 'data'),
)
def load_from_store(stored_data):
    if stored_data:
        return stored_data
    return DEFAULT_DATA


# Save edits to session storage and update status
@callback(
    Output('data-store', 'data'),
    Output('edit-status', 'children'),
    Input('persistent-grid', 'cellEdited'),
    Input('reset-button', 'n_clicks'),
    State('persistent-grid', 'data'),
    State('persistent-grid', 'columns'),
    prevent_initial_call=True
)
def handle_edits(cell_edited, reset_clicks, current_data, columns):
    triggered = ctx.triggered_id

    if triggered == 'reset-button':
        # Reset to default data (clear storage by setting to None)
        return None, html.Div([
            html.Strong('Data reset! '),
            'All values restored to defaults.'
        ], style={'color': '#dc3545'})

    if triggered == 'persistent-grid' and cell_edited:
        row = cell_edited['row']
        col_idx = cell_edited['col']
        col_id = columns[col_idx]['id']
        col_title = columns[col_idx]['title']
        new_value = current_data[row][col_id]

        # Save current data to session storage
        return current_data, html.Div([
            html.Strong('Saved! '),
            f'Row {row + 1}, "{col_title}" → ',
            html.Code(str(new_value)),
            ' (persisted to session)'
        ], style={'color': '#28a745'})

    return current_data, 'No edits yet'


if __name__ == '__main__':
    app.run(debug=True, port=8050)