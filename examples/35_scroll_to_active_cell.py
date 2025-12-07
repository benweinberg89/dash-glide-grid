"""
Example 36: Scroll To Active Cell
Demonstrates the scrollToActiveCell prop which controls automatic scrolling
when navigating with keyboard.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Large dataset to require scrolling
COLUMNS = [
    {'title': 'Row', 'id': 'row', 'width': 80},
    {'title': 'A', 'id': 'a', 'width': 100},
    {'title': 'B', 'id': 'b', 'width': 100},
    {'title': 'C', 'id': 'c', 'width': 100},
    {'title': 'D', 'id': 'd', 'width': 100},
    {'title': 'E', 'id': 'e', 'width': 100},
]

DATA = [{'row': i, 'a': f'A{i}', 'b': f'B{i}', 'c': f'C{i}', 'd': f'D{i}', 'e': f'E{i}'}
        for i in range(50)]

app.layout = html.Div([
    html.H1('Scroll To Active Cell'),
    html.P('Control whether the grid auto-scrolls to keep the active cell visible.'),

    # Controls
    html.Div([
        html.Label('scrollToActiveCell:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='scroll-toggle',
            options=[
                {'label': ' True (default) - Grid scrolls to keep active cell visible', 'value': True},
                {'label': ' False - Active cell can scroll out of view', 'value': False},
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
                html.Strong('scrollToActiveCell=True (default)'),
                ': When you navigate with arrow keys, the grid automatically scrolls ',
                'to keep the selected cell in view. Standard spreadsheet behavior.'
            ]),
            html.Li([
                html.Strong('scrollToActiveCell=False'),
                ': The grid does not auto-scroll when navigating. The active cell can ',
                'move outside the visible area while still receiving keyboard input.'
            ]),
        ]),
        html.H4('Try it:'),
        html.Ol([
            html.Li('Click on a cell in the middle of the grid'),
            html.Li('Press the Down arrow key repeatedly'),
            html.Li('With scrollToActiveCell=True: Grid scrolls to follow your selection'),
            html.Li('With scrollToActiveCell=False: Selection moves but grid stays put'),
        ]),
        html.H4('Use cases for disabling auto-scroll:'),
        html.Ul([
            html.Li('Keeping a specific view while making edits elsewhere'),
            html.Li('Custom scroll behavior controlled by application logic'),
            html.Li('Performance optimization in very large grids'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('scroll-toggle', 'value'),
)
def update_grid(scroll_to_active):
    return dgg.GlideGrid(
        id='scroll-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        scrollToActiveCell=scroll_to_active,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)
