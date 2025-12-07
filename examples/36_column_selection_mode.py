"""
Example 37: Column Selection Mode
Demonstrates the columnSelectionMode prop which controls how multi-column
selection works with modifier keys.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Sample data
COLUMNS = [
    {'title': 'A', 'id': 'a', 'width': 100},
    {'title': 'B', 'id': 'b', 'width': 100},
    {'title': 'C', 'id': 'c', 'width': 100},
    {'title': 'D', 'id': 'd', 'width': 100},
    {'title': 'E', 'id': 'e', 'width': 100},
]

DATA = [{'a': f'A{i}', 'b': f'B{i}', 'c': f'C{i}', 'd': f'D{i}', 'e': f'E{i}'}
        for i in range(10)]

app.layout = html.Div([
    html.H1('Column Selection Mode'),
    html.P('Control how multi-column selection works with modifier keys.'),

    # Controls
    html.Div([
        html.Label('columnSelectionMode:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='col-mode-toggle',
            options=[
                {'label': ' "auto" (default) - Ctrl/Cmd required for multi-select', 'value': 'auto'},
                {'label': ' "multi" - No modifier needed for multi-select', 'value': 'multi'},
            ],
            value='auto',
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
        html.P('Click on column headers to select columns. This prop controls whether you need modifier keys for multi-selection.'),
        html.Ul([
            html.Li([
                html.Strong('columnSelectionMode="auto" (default)'),
                ': Click a column header to select it. Hold Ctrl (Windows/Linux) or Cmd (Mac) ',
                'and click additional headers to add to selection. Standard behavior.'
            ]),
            html.Li([
                html.Strong('columnSelectionMode="multi"'),
                ': Each click on a column header toggles its selection without needing modifier keys. ',
                'Great for touch interfaces or simplified multi-select.'
            ]),
        ]),
        html.H4('Try it:'),
        html.Ol([
            html.Li('With "auto" mode: Click column A, then Ctrl+click column C - both selected'),
            html.Li('With "auto" mode: Click column A, then click column C (no Ctrl) - only C selected'),
            html.Li('With "multi" mode: Click column A, then click column C - both selected'),
        ]),
        html.H4('Note:'),
        html.P('columnSelect must be set to "multi" (the default) for multi-column selection to work. '
               'If columnSelect="single", only one column can be selected regardless of this mode.')
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('col-mode-toggle', 'value'),
)
def update_grid(col_mode):
    return dgg.GlideGrid(
        id='col-mode-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        columnSelect='multi',
        columnSelectionMode=col_mode,
    )


@callback(
    Output('selection-display', 'children'),
    Input('col-mode-grid', 'selectedColumns'),
    prevent_initial_call=True
)
def display_selection(selected_cols):
    if selected_cols:
        col_names = [COLUMNS[i]['title'] for i in selected_cols]
        return f"Selected columns: {', '.join(col_names)} (indices: {selected_cols})"
    return "No columns selected"


if __name__ == '__main__':
    app.run(debug=True, port=8050)
