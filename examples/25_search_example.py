"""
Example 25: Search Functionality
Demonstrates the built-in search interface and programmatic search control
"""
import dash
from dash import html, Input, Output, State, callback, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {'title': 'Product', 'id': 'product', 'width': 200},
    {'title': 'Category', 'id': 'category', 'width': 120},
    {'title': 'Brand', 'id': 'brand', 'width': 120},
    {'title': 'Price', 'id': 'price', 'width': 100},
    {'title': 'In Stock', 'id': 'in_stock', 'width': 80},
    {'title': 'SKU', 'id': 'sku', 'width': 120},
]

DATA = [
    {'product': 'Laptop Pro 15"', 'category': 'Electronics', 'brand': 'TechCorp', 'price': 1299.99, 'in_stock': True, 'sku': 'TECH-LP15'},
    {'product': 'Wireless Mouse', 'category': 'Accessories', 'brand': 'ClickMaster', 'price': 29.99, 'in_stock': True, 'sku': 'ACC-WM01'},
    {'product': 'USB-C Hub', 'category': 'Accessories', 'brand': 'TechCorp', 'price': 49.99, 'in_stock': True, 'sku': 'ACC-HUB7'},
    {'product': '4K Monitor 27"', 'category': 'Electronics', 'brand': 'ViewMax', 'price': 449.99, 'in_stock': False, 'sku': 'TECH-MON27'},
    {'product': 'Mechanical Keyboard', 'category': 'Accessories', 'brand': 'KeyPro', 'price': 89.99, 'in_stock': True, 'sku': 'ACC-KB01'},
    {'product': 'Laptop Stand', 'category': 'Accessories', 'brand': 'DeskMate', 'price': 39.99, 'in_stock': True, 'sku': 'ACC-LS01'},
    {'product': 'Webcam HD', 'category': 'Electronics', 'brand': 'ViewMax', 'price': 79.99, 'in_stock': True, 'sku': 'TECH-WC01'},
    {'product': 'Desk Lamp LED', 'category': 'Office', 'brand': 'BrightLight', 'price': 34.99, 'in_stock': True, 'sku': 'OFF-DL01'},
    {'product': 'Notebook Set', 'category': 'Office', 'brand': 'PaperCo', 'price': 12.99, 'in_stock': True, 'sku': 'OFF-NB05'},
    {'product': 'Ergonomic Chair', 'category': 'Furniture', 'brand': 'ComfortPlus', 'price': 299.99, 'in_stock': True, 'sku': 'FURN-CH01'},
    {'product': 'Standing Desk', 'category': 'Furniture', 'brand': 'DeskMate', 'price': 549.99, 'in_stock': False, 'sku': 'FURN-SD01'},
    {'product': 'Monitor Arm', 'category': 'Accessories', 'brand': 'DeskMate', 'price': 79.99, 'in_stock': True, 'sku': 'ACC-MA01'},
    {'product': 'Wireless Charger', 'category': 'Electronics', 'brand': 'TechCorp', 'price': 24.99, 'in_stock': True, 'sku': 'TECH-WC02'},
    {'product': 'Headphones Pro', 'category': 'Electronics', 'brand': 'AudioMax', 'price': 199.99, 'in_stock': True, 'sku': 'TECH-HP01'},
    {'product': 'Mouse Pad XL', 'category': 'Accessories', 'brand': 'ClickMaster', 'price': 19.99, 'in_stock': True, 'sku': 'ACC-MP01'},
]

app.layout = html.Div([
    html.H1('Product Search Demo'),
    html.P('Use the built-in search or the controls below to search the grid.'),

    # Search Controls
    html.Div([
        html.Label('Programmatic Search:', style={'fontWeight': 'bold'}),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Type to search...',
            style={
                'padding': '8px 12px',
                'fontSize': '14px',
                'border': '1px solid #ccc',
                'borderRadius': '4px',
                'width': '250px',
                'marginRight': '10px'
            }
        ),
        html.Button(
            'Toggle Search UI',
            id='toggle-search-btn',
            style={
                'padding': '8px 16px',
                'backgroundColor': '#007bff',
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer',
                'marginRight': '10px'
            }
        ),
        html.Button(
            'Clear Search',
            id='clear-search-btn',
            style={
                'padding': '8px 16px',
                'backgroundColor': '#6c757d',
                'color': 'white',
                'border': 'none',
                'borderRadius': '4px',
                'cursor': 'pointer'
            }
        ),
    ], style={'marginBottom': '20px'}),

    # Grid
    dgg.GlideGrid(
        id='search-grid',
        columns=COLUMNS,
        data=DATA,
        height=400,
        readonly=True,
        rowMarkers='number',
        showSearch=False,
        searchValue='',
        smoothScrollX=True,
        smoothScrollY=True,
    ),

    # Search Status
    html.Div([
        html.H3('Search Status:'),
        html.Div(id='search-status', style={
            'padding': '15px',
            'backgroundColor': '#f8f9fa',
            'border': '1px solid #dee2e6',
            'borderRadius': '4px',
        })
    ], style={'marginTop': '20px'}),

    # Instructions
    html.Div([
        html.H3('How to Use:'),
        html.Ul([
            html.Li('Type in the "Programmatic Search" input to search the grid'),
            html.Li('Click "Toggle Search UI" to show/hide the built-in search overlay'),
            html.Li('When the search UI is open, press Ctrl+F (Cmd+F on Mac) to focus it'),
            html.Li('The grid highlights matching cells as you type'),
            html.Li('Use arrow keys to navigate between search results'),
        ])
    ], style={
        'marginTop': '20px',
        'padding': '15px',
        'backgroundColor': '#e7f3ff',
        'borderRadius': '4px',
    })
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('search-grid', 'showSearch'),
    Input('toggle-search-btn', 'n_clicks'),
    State('search-grid', 'showSearch'),
    prevent_initial_call=True
)
def toggle_search(n_clicks, current_show):
    return not current_show


@callback(
    Output('search-grid', 'searchValue'),
    Input('search-input', 'value'),
    Input('clear-search-btn', 'n_clicks'),
    prevent_initial_call=True
)
def update_search_value(search_text, clear_clicks):
    from dash import ctx
    if ctx.triggered_id == 'clear-search-btn':
        return ''
    return search_text or ''


@callback(
    Output('search-input', 'value'),
    Input('clear-search-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_search_input(n_clicks):
    return ''


@callback(
    Output('search-status', 'children'),
    Input('search-grid', 'searchValue'),
    Input('search-grid', 'showSearch'),
)
def update_search_status(search_value, show_search):
    return html.Div([
        html.Div([
            html.Strong('Search UI: '),
            html.Span(
                'Visible' if show_search else 'Hidden',
                style={'color': '#28a745' if show_search else '#6c757d'}
            )
        ]),
        html.Div([
            html.Strong('Search Query: '),
            html.Code(f'"{search_value}"' if search_value else '(empty)')
        ], style={'marginTop': '5px'}),
    ])


if __name__ == '__main__':
    app.run(debug=True, port=8050)