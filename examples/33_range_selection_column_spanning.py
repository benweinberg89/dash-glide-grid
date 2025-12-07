"""
Example 34: Range Selection Column Spanning
Demonstrates the rangeSelectionColumnSpanning prop which controls whether range
selections can span across multiple columns.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Sample data - multiple columns to demonstrate spanning
COLUMNS = [
    {'title': 'A', 'id': 'a', 'width': 80},
    {'title': 'B', 'id': 'b', 'width': 80},
    {'title': 'C', 'id': 'c', 'width': 80},
    {'title': 'D', 'id': 'd', 'width': 80},
    {'title': 'E', 'id': 'e', 'width': 80},
    {'title': 'F', 'id': 'f', 'width': 80},
]

DATA = [
    {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6},
    {'a': 7, 'b': 8, 'c': 9, 'd': 10, 'e': 11, 'f': 12},
    {'a': 13, 'b': 14, 'c': 15, 'd': 16, 'e': 17, 'f': 18},
    {'a': 19, 'b': 20, 'c': 21, 'd': 22, 'e': 23, 'f': 24},
    {'a': 25, 'b': 26, 'c': 27, 'd': 28, 'e': 29, 'f': 30},
    {'a': 31, 'b': 32, 'c': 33, 'd': 34, 'e': 35, 'f': 36},
    {'a': 37, 'b': 38, 'c': 39, 'd': 40, 'e': 41, 'f': 42},
    {'a': 43, 'b': 44, 'c': 45, 'd': 46, 'e': 47, 'f': 48},
]

app.layout = html.Div([
    html.H1('Range Selection Column Spanning'),
    html.P('Control whether range selections can span across multiple columns.'),

    # Controls
    html.Div([
        html.Label('rangeSelectionColumnSpanning:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='column-spanning-toggle',
            options=[
                {'label': ' True (default) - Select across multiple columns', 'value': True},
                {'label': ' False - Restrict selection to single column', 'value': False},
            ],
            value=True,
            labelStyle={'display': 'block', 'marginBottom': '8px'}
        ),
    ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

    # Grid
    html.Div(id='grid-container'),

    # Selection display
    html.Div(id='selection-display', style={'marginTop': '15px', 'padding': '10px', 'backgroundColor': '#e8f4f8', 'borderRadius': '4px'}),

    # Info
    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li([
                html.Strong('rangeSelectionColumnSpanning=True (default)'),
                ': Click and drag to select any rectangular region across multiple columns. ',
                'This is standard spreadsheet behavior.'
            ]),
            html.Li([
                html.Strong('rangeSelectionColumnSpanning=False'),
                ': Range selections are restricted to a single column. When you try to drag across columns, ',
                'the selection stays within the starting column.'
            ]),
        ]),
        html.H4('Try it:'),
        html.Ol([
            html.Li('With spanning enabled: Click on cell A1 and drag to C3 - you get a 3x3 selection'),
            html.Li('With spanning disabled: Click on cell A1 and drag to C3 - selection stays in column A only'),
        ]),
        html.H4('Use cases for disabling column spanning:'),
        html.Ul([
            html.Li('Column-oriented data where cross-column selections don\'t make sense'),
            html.Li('Preventing accidental multi-column selections'),
            html.Li('Interfaces that treat each column as an independent data series'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('column-spanning-toggle', 'value'),
)
def update_grid(column_spanning):
    return dgg.GlideGrid(
        id='spanning-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        rangeSelectionColumnSpanning=column_spanning,
    )


@callback(
    Output('selection-display', 'children'),
    Input('spanning-grid', 'selectedRange'),
    prevent_initial_call=True
)
def display_selection(selected_range):
    if selected_range:
        cols = selected_range['endCol'] - selected_range['startCol'] + 1
        rows = selected_range['endRow'] - selected_range['startRow'] + 1
        return f"Selected range: {cols} column(s) x {rows} row(s) - from ({selected_range['startCol']}, {selected_range['startRow']}) to ({selected_range['endCol']}, {selected_range['endRow']})"
    return "No range selected"


if __name__ == '__main__':
    app.run(debug=True, port=8050)
