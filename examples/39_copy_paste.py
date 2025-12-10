"""
Example demonstrating copy/paste functionality in GlideGrid

GlideGrid supports full clipboard operations:
- Copy cells with Ctrl+C (Cmd+C on Mac)
- Paste with Ctrl+V (Cmd+V on Mac)
- Paste from Excel, Google Sheets, or other sources
- Custom paste coercion via JavaScript functions

Note: This example uses coercePasteValue with a JS function from
assets/dashGlideGridFunctions.js to properly handle pasting text
values like "yes", "no", "true", "false" into boolean cells.
"""
import dash
from dash import html, Input, Output, callback
import dash_glide_grid as dgg

app = dash.Dash(__name__, assets_folder='assets')

# Sample data - a mix of types to demonstrate copy/paste behavior
COLUMNS = [
    {'title': 'Name', 'id': 'name', 'width': 150, 'type': 'text'},
    {'title': 'Department', 'id': 'department', 'width': 120, 'type': 'text'},
    {'title': 'Salary', 'id': 'salary', 'width': 100, 'type': 'number'},
    {'title': 'Start Date', 'id': 'start_date', 'width': 120, 'type': 'text'},
    {'title': 'Active', 'id': 'active', 'width': 80, 'type': 'boolean'},
]

DATA = [
    {'name': 'Alice Johnson', 'department': 'Engineering', 'salary': 95000, 'start_date': '2021-03-15', 'active': True},
    {'name': 'Bob Smith', 'department': 'Marketing', 'salary': 75000, 'start_date': '2020-07-01', 'active': True},
    {'name': 'Carol Williams', 'department': 'Engineering', 'salary': 105000, 'start_date': '2019-11-20', 'active': True},
    {'name': 'David Brown', 'department': 'Sales', 'salary': 85000, 'start_date': '2022-01-10', 'active': False},
    {'name': 'Eva Martinez', 'department': 'HR', 'salary': 70000, 'start_date': '2021-06-01', 'active': True},
    {'name': '', 'department': '', 'salary': 0, 'start_date': '', 'active': False},
    {'name': '', 'department': '', 'salary': 0, 'start_date': '', 'active': False},
    {'name': '', 'department': '', 'salary': 0, 'start_date': '', 'active': False},
]

app.layout = html.Div([
    html.H1('GlideGrid - Copy/Paste Demo'),

    html.Div([
        html.H3('Clipboard Operations:'),
        html.Ul([
            html.Li([html.Strong('Copy: '), 'Select cells and press Ctrl+C (Cmd+C on Mac)']),
            html.Li([html.Strong('Paste: '), 'Select target cell and press Ctrl+V (Cmd+V on Mac)']),
            html.Li([html.Strong('Multi-cell: '), 'Select a range, copy, then paste to fill multiple cells']),
            html.Li([html.Strong('From Excel: '), 'Copy cells from Excel or Google Sheets and paste directly']),
        ]),
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#e8f4e8', 'borderRadius': '5px'}),

    html.Div([
        html.H3('Try These:'),
        html.Ol([
            html.Li('Select "Alice Johnson" and copy (Ctrl+C), then paste into an empty row'),
            html.Li('Select multiple cells (e.g., the first 3 names), copy, and paste below'),
            html.Li('Copy data from Excel or a text file and paste into the grid'),
            html.Li('Copy a number like "95000" and paste it into another Salary cell'),
        ]),
    ], style={'margin': '20px', 'padding': '20px', 'backgroundColor': '#e8e8f4', 'borderRadius': '5px'}),

    html.Div([
        dgg.GlideGrid(
            id='copy-paste-grid',
            columns=COLUMNS,
            data=DATA,
            height=400,
            rowMarkers='number',
            rangeSelect='rect',  # Enable range selection for multi-cell copy/paste
            columnResize=True,
            # Use smartPaste to properly coerce pasted values (e.g., "yes" -> True)
            coercePasteValue={"function": "smartPaste(val, cell)"},
        ),
    ], style={'margin': '20px'}),

    html.Div([
        html.H4('Last Cell Edit:'),
        html.Div(id='paste-output', style={
            'fontFamily': 'monospace',
            'padding': '15px',
            'backgroundColor': '#f8f8f8',
            'borderRadius': '5px',
            'minHeight': '60px'
        }),
    ], style={'margin': '20px'}),

    html.Div([
        html.H4('Paste Coercion:'),
        html.P([
            'This example uses ',
            html.Code('coercePasteValue={"function": "smartPaste(val, cell)"}'),
            ' to convert pasted text to the correct cell type:'
        ]),
        html.Ul([
            html.Li('Boolean cells: "true", "false", "yes", "no", "1", "0" → True/False'),
            html.Li('Number cells: numeric strings are parsed automatically'),
            html.Li('Tab-separated data fills multiple columns'),
            html.Li('Newline-separated data fills multiple rows'),
        ]),
        html.P([
            'See ',
            html.Code('assets/dashGlideGridFunctions.js'),
            ' for the smartPaste implementation.'
        ], style={'marginTop': '10px', 'fontSize': '0.9em', 'color': '#666'}),
    ], style={'margin': '20px', 'padding': '15px', 'backgroundColor': '#fff3e0', 'borderRadius': '5px'}),
])


@callback(
    Output('paste-output', 'children'),
    Input('copy-paste-grid', 'cellEdited'),
    prevent_initial_call=True
)
def display_paste_event(cell_edited):
    if not cell_edited:
        return 'No edits yet'

    col = cell_edited.get('col', 0)
    row = cell_edited.get('row', 0)
    value = cell_edited.get('value')
    col_name = COLUMNS[col]['title'] if col < len(COLUMNS) else f'Col {col}'

    return html.Div([
        html.Div(f'Row: {row}, Column: {col_name}'),
        html.Div(f'New Value: {value}', style={'fontWeight': 'bold'}),
        html.Div(f'Type: {type(value).__name__}', style={'color': '#666'}),
    ])


if __name__ == '__main__':
    app.run(debug=True, port=8050)
