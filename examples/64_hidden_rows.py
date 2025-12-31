"""
Example 64: Hidden Rows Test

Test if getRowThemeOverride + rowHeight=0 can hide rows while preserving row numbers.

SETUP REQUIRED:
---------------
This example requires custom JavaScript functions.
Add the following to assets/dashGlideGridFunctions.js:

var dggfuncs = window.dashGlideGridFunctions = window.dashGlideGridFunctions || {};

// Hidden rows - set in Python and read by JavaScript
dggfuncs._hiddenRows = [];

dggfuncs.setHiddenRows = function(rows) {
    dggfuncs._hiddenRows = rows || [];
};

dggfuncs.getHiddenRowHeight = function(rowIndex) {
    if (dggfuncs._hiddenRows.includes(rowIndex)) {
        return 0;
    }
    return 34;  // Default row height
};

dggfuncs.getHiddenRowTheme = function(row, rowData) {
    if (dggfuncs._hiddenRows.includes(row)) {
        return {
            textDark: "transparent",
            textMedium: "transparent",
            textLight: "transparent",
            bgCell: "transparent",
        };
    }
    return undefined;
};
"""
import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {'title': 'Row', 'id': 'row', 'width': 60},
    {'title': 'Name', 'id': 'name', 'width': 150},
    {'title': 'Department', 'id': 'department', 'width': 120},
    {'title': 'Status', 'id': 'status', 'width': 100},
]

DATA = [
    {'row': 0, 'name': 'Row 0 - Alice', 'department': 'Engineering', 'status': 'Active'},
    {'row': 1, 'name': 'Row 1 - Bob', 'department': 'Marketing', 'status': 'Active'},
    {'row': 2, 'name': 'Row 2 - Carol (HIDDEN)', 'department': 'Engineering', 'status': 'Hidden'},
    {'row': 3, 'name': 'Row 3 - David', 'department': 'Sales', 'status': 'Active'},
    {'row': 4, 'name': 'Row 4 - Eve', 'department': 'HR', 'status': 'Active'},
    {'row': 5, 'name': 'Row 5 - Frank (HIDDEN)', 'department': 'Engineering', 'status': 'Hidden'},
    {'row': 6, 'name': 'Row 6 - Grace', 'department': 'Design', 'status': 'Active'},
    {'row': 7, 'name': 'Row 7 - Henry', 'department': 'Finance', 'status': 'Active'},
    {'row': 8, 'name': 'Row 8 - Ivy (HIDDEN)', 'department': 'Engineering', 'status': 'Hidden'},
    {'row': 9, 'name': 'Row 9 - Jack', 'department': 'Marketing', 'status': 'Active'},
    {'row': 10, 'name': 'Row 10 - Kate', 'department': 'Engineering', 'status': 'Active'},
    {'row': 11, 'name': 'Row 11 - Leo', 'department': 'Sales', 'status': 'Active'},
    {'row': 12, 'name': 'Row 12 - Mary', 'department': 'HR', 'status': 'Active'},
    {'row': 13, 'name': 'Row 13 - Nick', 'department': 'Design', 'status': 'Active'},
    {'row': 14, 'name': 'Row 14 - Olivia', 'department': 'Finance', 'status': 'Active'},
    {'row': 15, 'name': 'Row 15 - Paul', 'department': 'Marketing', 'status': 'Active'},
    {'row': 16, 'name': 'Row 16 - Quinn', 'department': 'Engineering', 'status': 'Active'},
    {'row': 17, 'name': 'Row 17 - Rachel', 'department': 'Sales', 'status': 'Active'},
    {'row': 18, 'name': 'Row 18 - Steve', 'department': 'HR', 'status': 'Active'},
    {'row': 19, 'name': 'Row 19 - Tina', 'department': 'Design', 'status': 'Active'},
]

# Default hidden rows
HIDDEN_ROWS = [2, 5, 8]

app.layout = html.Div([
    html.H1('Hidden Rows Test'),
    html.P('Testing if getRowThemeOverride + rowHeight=0 can hide rows while preserving row numbers.'),

    # Store for hidden rows
    dcc.Store(id='hidden-rows-store', data=HIDDEN_ROWS),

    # Controls
    html.Div([
        html.Label('Hidden Rows (comma-separated indices): '),
        dcc.Input(
            id='hidden-rows-input',
            type='text',
            value=','.join(map(str, HIDDEN_ROWS)),
            style={'width': '200px', 'marginRight': '10px'}
        ),
        html.Button('Update Hidden Rows', id='update-btn', n_clicks=0),
    ], style={'marginBottom': '20px'}),

    # Grid - rendered directly in layout
    dgg.GlideGrid(
        id='test-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='both',
        rowMarkerStartIndex=0,
        rowSelect='multi',
        rowSelectOnCellClick=True,
        rowHeight={'function': 'getHiddenRowHeight(rowIndex)'},
        getRowThemeOverride={'function': 'getHiddenRowTheme(row, rowData)'},
        drawCell={'function': 'drawHiddenRowCell(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent)'},
    ),

    # Results
    html.Div([
        html.H3('Expected Behavior:'),
        html.Ul([
            html.Li('Rows 2, 5, 8 should be hidden (0 height)'),
            html.Li('Row markers should show: 0, 1, 3, 4, 6, 7, 9 (original indices preserved)'),
            html.Li('Hidden row content should be invisible (transparent)'),
        ]),
        html.H3('Actual Behavior:'),
        html.P(id='result-text', style={'color': 'blue', 'fontWeight': 'bold'}),
    ], style={'marginTop': '20px', 'padding': '20px', 'backgroundColor': '#f5f5f5'}),
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


# Clientside callback to update hidden rows in JavaScript and trigger redraw
clientside_callback(
    """
    function(hiddenRows, currentTrigger) {
        if (window.dashGlideGridFunctions && window.dashGlideGridFunctions.setHiddenRows) {
            window.dashGlideGridFunctions.setHiddenRows(hiddenRows);
        }
        // Increment trigger to force grid redraw
        return (currentTrigger || 0) + 1;
    }
    """,
    Output('test-grid', 'redrawTrigger'),
    Input('hidden-rows-store', 'data'),
    State('test-grid', 'redrawTrigger'),
    prevent_initial_call=True  # Don't run on page load
)


@callback(
    Output('hidden-rows-store', 'data', allow_duplicate=True),
    Input('update-btn', 'n_clicks'),
    State('hidden-rows-input', 'value'),
    prevent_initial_call=True
)
def update_hidden_rows(n_clicks, input_value):
    if not input_value:
        return []
    try:
        rows = [int(x.strip()) for x in input_value.split(',') if x.strip()]
        return rows
    except ValueError:
        return HIDDEN_ROWS


if __name__ == '__main__':
    app.run(debug=True, port=8064)
