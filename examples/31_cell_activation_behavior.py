"""
Example 32: Cell Activation Behavior
Demonstrates the cellActivationBehavior prop which controls when cells open for editing.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Sample data
COLUMNS = [
    {'title': 'Name', 'id': 'name', 'width': 150},
    {'title': 'Value', 'id': 'value', 'width': 100},
    {'title': 'Notes', 'id': 'notes', 'width': 250},
]

DATA = [
    {'name': 'Item A', 'value': 100, 'notes': 'Click to edit this cell'},
    {'name': 'Item B', 'value': 200, 'notes': 'Try different activation modes'},
    {'name': 'Item C', 'value': 300, 'notes': 'Single-click is fastest'},
    {'name': 'Item D', 'value': 400, 'notes': 'Double-click is most deliberate'},
    {'name': 'Item E', 'value': 500, 'notes': 'Second-click is the default'},
]

app.layout = html.Div([
    html.H1('Cell Activation Behavior'),
    html.P('Control when cells open for editing with the cellActivationBehavior prop.'),

    # Controls
    html.Div([
        html.Label('Activation Mode:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='activation-mode',
            options=[
                {'label': ' single-click - Edit immediately on click', 'value': 'single-click'},
                {'label': ' second-click - Click selected cell again to edit (default)', 'value': 'second-click'},
                {'label': ' double-click - Double-click to edit', 'value': 'double-click'},
            ],
            value='second-click',
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
                html.Strong('single-click'),
                ': Cell opens for editing immediately when clicked. Best for rapid data entry.'
            ]),
            html.Li([
                html.Strong('second-click'),
                ': First click selects the cell, clicking again opens it for editing. This is the default behavior.'
            ]),
            html.Li([
                html.Strong('double-click'),
                ': Must double-click to open cell for editing. Most deliberate, prevents accidental edits.'
            ]),
        ]),
        html.H4('Use cases:'),
        html.Ul([
            html.Li('Use single-click for forms or data entry grids where users need to edit many cells quickly'),
            html.Li('Use second-click (default) for general purpose grids where selection and editing are both common'),
            html.Li('Use double-click for read-heavy grids where editing should be deliberate'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('activation-mode', 'value'),
)
def update_grid(activation_mode):
    return dgg.GlideGrid(
        id='activation-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        cellActivationBehavior=activation_mode,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)
