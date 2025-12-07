"""
Example 33: Edit On Type
Demonstrates the editOnType prop which controls whether typing on a selected cell
immediately starts editing.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Sample data
COLUMNS = [
    {'title': 'Product', 'id': 'product', 'width': 150},
    {'title': 'Price', 'id': 'price', 'width': 100},
    {'title': 'Quantity', 'id': 'quantity', 'width': 100},
    {'title': 'Notes', 'id': 'notes', 'width': 250},
]

DATA = [
    {'product': 'Laptop', 'price': 999.99, 'quantity': 5, 'notes': 'Select a cell and start typing'},
    {'product': 'Mouse', 'price': 29.99, 'quantity': 50, 'notes': 'Try with editOnType on and off'},
    {'product': 'Keyboard', 'price': 79.99, 'quantity': 30, 'notes': 'When enabled, typing starts editing'},
    {'product': 'Monitor', 'price': 299.99, 'quantity': 10, 'notes': 'When disabled, you must click to edit'},
    {'product': 'Headphones', 'price': 149.99, 'quantity': 25, 'notes': 'Great for rapid data entry'},
]

app.layout = html.Div([
    html.H1('Edit On Type'),
    html.P('Control whether typing immediately starts editing a selected cell.'),

    # Controls
    html.Div([
        html.Label('editOnType:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='edit-on-type-toggle',
            options=[
                {'label': ' True (default) - Typing immediately starts editing', 'value': True},
                {'label': ' False - Must activate cell first (double-click/Enter)', 'value': False},
            ],
            value=True,
            labelStyle={'display': 'block', 'marginBottom': '8px'}
        ),
    ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

    # Grid
    html.Div(id='grid-container'),

    # Info
    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li([
                html.Strong('editOnType=True (default)'),
                ': Select any cell and start typing. The cell immediately enters edit mode ',
                'and your keystrokes are captured. This is the standard spreadsheet behavior.'
            ]),
            html.Li([
                html.Strong('editOnType=False'),
                ': Select a cell and start typing - nothing happens. You must first activate ',
                'the cell by double-clicking, pressing Enter, or pressing F2. Only then can you type to edit.'
            ]),
        ]),
        html.H4('Use cases:'),
        html.Ul([
            html.Li([
                html.Strong('editOnType=True'),
                ': Data entry forms, spreadsheet-like interfaces, rapid editing workflows'
            ]),
            html.Li([
                html.Strong('editOnType=False'),
                ': Read-heavy grids where accidental edits should be prevented, ',
                'grids with keyboard navigation where arrow keys should always navigate'
            ]),
        ]),
        html.H4('Try it:'),
        html.Ol([
            html.Li('With editOnType=True: Click a cell, then type "hello" - the cell starts editing'),
            html.Li('With editOnType=False: Click a cell, then type "hello" - nothing happens'),
            html.Li('With editOnType=False: Double-click a cell, then type - now editing works'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('edit-on-type-toggle', 'value'),
)
def update_grid(edit_on_type):
    return dgg.GlideGrid(
        id='edit-on-type-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        editOnType=edit_on_type,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)
