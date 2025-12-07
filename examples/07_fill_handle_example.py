"""
Example demonstrating the fill handle feature in GlideGrid

The fill handle allows users to drag a small square at the bottom-right corner
of a selection to fill adjacent cells with the selected pattern, just like in Excel.
"""
import dash
from dash import html, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Sample data with numbers and text
COLUMNS = [
    {'title': 'Item', 'id': 'item', 'width': 150},
    {'title': 'Q1', 'id': 'q1', 'width': 100},
    {'title': 'Q2', 'id': 'q2', 'width': 100},
    {'title': 'Q3', 'id': 'q3', 'width': 100},
    {'title': 'Q4', 'id': 'q4', 'width': 100},
]

DATA = [
    {'item': 'Product A', 'q1': 100, 'q2': 110, 'q3': 120, 'q4': 130},
    {'item': 'Product B', 'q1': 200, 'q2': 220, 'q3': 240, 'q4': 260},
    {'item': 'Product C', 'q1': 150, 'q2': 165, 'q3': 180, 'q4': 195},
    {'item': 'Product D', 'q1': 300, 'q2': 330, 'q3': 360, 'q4': 390},
    {'item': 'Product E', 'q1': 250, 'q2': 275, 'q3': 300, 'q4': 325},
    {'item': 'Product F', 'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0},
    {'item': 'Product G', 'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0},
    {'item': 'Product H', 'q1': 0, 'q2': 0, 'q3': 0, 'q4': 0},
]

app.layout = html.Div([
    html.H1('GlideGrid - Fill Handle Demo'),

    html.Div([
        html.H3('Try the Fill Handle:'),
        html.Ul([
            html.Li('Click on a cell or select a range of cells'),
            html.Li('Look for the small square at the bottom-right corner of your selection'),
            html.Li('Click and drag that square to fill adjacent cells with the pattern'),
            html.Li('Works both horizontally and vertically!'),
        ]),
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#f0f0f0', 'borderRadius': '5px'}),

    html.Div([
        dgg.GlideGrid(
            id='fill-handle-grid',
            columns=COLUMNS,
            data=DATA,
            height=400,
            rowMarkers='number',
            columnResize=True,
            fillHandle=True,  # Enable the fill handle feature
            rangeSelect='rect',  # Allow range selection for better UX
        ),
    ], style={'margin': '20px'}),

    html.Div([
        html.H4('Grid Events:'),
        html.Div(id='fill-output', style={'margin': '10px'}),
    ], style={'margin': '20px', 'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px'})
])

@app.callback(
    Output('fill-output', 'children'),
    Input('fill-handle-grid', 'cellEdited')
)
def display_fill_event(cell_edited):
    if cell_edited and cell_edited.get('value'):
        value = cell_edited['value']
        # Check if this was a fill operation
        if isinstance(value, str) and 'Filled' in value:
            return html.Div([
                html.Strong(f"Fill operation: ", style={'color': 'green'}),
                html.Span(value)
            ])
        else:
            return f"Cell edited: Row {cell_edited['row']}, Column {cell_edited['col']} → {value}"
    return 'No fill operations yet - try dragging the fill handle!'

if __name__ == '__main__':
    app.run(debug=True, port=8050)
