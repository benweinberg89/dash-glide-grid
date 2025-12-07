"""
Example 35: Trap Focus
Demonstrates the trapFocus prop which prevents keyboard focus from leaving the grid.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Sample data
COLUMNS = [
    {'title': 'Name', 'id': 'name', 'width': 150},
    {'title': 'Value', 'id': 'value', 'width': 100},
    {'title': 'Notes', 'id': 'notes', 'width': 250},
]

DATA = [
    {'name': 'Item A', 'value': 100, 'notes': 'Try pressing Tab to leave the grid'},
    {'name': 'Item B', 'value': 200, 'notes': 'With trapFocus=True, Tab stays in grid'},
    {'name': 'Item C', 'value': 300, 'notes': 'Arrow keys also stay within grid'},
    {'name': 'Item D', 'value': 400, 'notes': 'Useful for modal-like experiences'},
    {'name': 'Item E', 'value': 500, 'notes': 'Click outside to release focus'},
]

app.layout = html.Div([
    html.H1('Trap Focus'),
    html.P('Control whether keyboard focus can leave the grid.'),

    # Controls
    html.Div([
        html.Label('trapFocus:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='trap-focus-toggle',
            options=[
                {'label': ' False (default) - Tab/arrows can leave grid', 'value': False},
                {'label': ' True - Focus stays trapped in grid', 'value': True},
            ],
            value=False,
            labelStyle={'display': 'block', 'marginBottom': '8px'}
        ),
    ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

    # Grid
    html.Div(id='grid-container'),

    # Extra focusable element to demonstrate Tab behavior
    html.Div([
        html.Label('Extra input (to test Tab navigation):', style={'display': 'block', 'marginBottom': '5px'}),
        dcc.Input(id='extra-input', placeholder='Tab here from grid...', style={'width': '300px', 'padding': '8px'}),
    ], style={'marginTop': '20px', 'padding': '15px', 'backgroundColor': '#f0f0f0', 'borderRadius': '8px'}),

    # Info
    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li([
                html.Strong('trapFocus=False (default)'),
                ': Pressing Tab moves focus to the next focusable element outside the grid. ',
                'Arrow keys at grid edges allow focus to leave.'
            ]),
            html.Li([
                html.Strong('trapFocus=True'),
                ': Tab key cycles within the grid (or does nothing). ',
                'Arrow keys wrap around at edges. Focus only leaves when clicking outside.'
            ]),
        ]),
        html.H4('Try it:'),
        html.Ol([
            html.Li('Click a cell in the grid to focus it'),
            html.Li('With trapFocus=False: Press Tab - focus moves to the input below'),
            html.Li('With trapFocus=True: Press Tab - focus stays in the grid'),
        ]),
        html.H4('Use cases:'),
        html.Ul([
            html.Li('Modal dialogs containing a grid as the primary content'),
            html.Li('Full-screen grid applications'),
            html.Li('Data entry forms where accidental focus loss is problematic'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('trap-focus-toggle', 'value'),
)
def update_grid(trap_focus):
    return dgg.GlideGrid(
        id='trap-grid',
        columns=COLUMNS,
        data=DATA,
        height=250,
        rowMarkers='number',
        trapFocus=trap_focus,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)
