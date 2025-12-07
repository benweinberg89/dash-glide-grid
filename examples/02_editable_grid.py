"""
Example 2: Editable Grid with Callbacks
Demonstrates cell editing and event handling
"""
import dash
from dash import html, Input, Output, State, callback
import dash_glide_grid as dgg
import json

app = dash.Dash(__name__)

COLUMNS = [
    {'title': 'Employee', 'id': 'employee', 'width': 200},
    {'title': 'Department', 'id': 'department', 'width': 150},
    {'title': 'Salary', 'id': 'salary', 'width': 120},
    {'title': 'Active', 'id': 'active', 'width': 100},
    {'title': 'Rating', 'id': 'rating', 'width': 100}
]

DATA = [
    {'employee': 'John Doe', 'department': 'Engineering', 'salary': 85000, 'active': True, 'rating': 4.5},
    {'employee': 'Jane Smith', 'department': 'Marketing', 'salary': 72000, 'active': True, 'rating': 4.8},
    {'employee': 'Bob Johnson', 'department': 'Sales', 'salary': 68000, 'active': True, 'rating': 4.2},
    {'employee': 'Alice Williams', 'department': 'Engineering', 'salary': 92000, 'active': True, 'rating': 4.9},
    {'employee': 'Charlie Brown', 'department': 'HR', 'salary': 65000, 'active': False, 'rating': 3.8},
]

app.layout = html.Div([
    html.H1('Employee Database - Editable Grid'),
    html.P('Click cells to edit. Changes are tracked below.'),

    dgg.GlideGrid(
        id='employee-grid',
        columns=COLUMNS,
        data=DATA,
        height=300,
        rowMarkers='number',
        columnResize=True
    ),

    html.Div([
        html.H3('Event Log:'),
        html.Div(id='event-log', style={
            'marginTop': '20px',
            'padding': '15px',
            'backgroundColor': '#f5f5f5',
            'border': '1px solid #ddd',
            'borderRadius': '4px',
            'maxHeight': '200px',
            'overflowY': 'auto'
        })
    ], style={'marginTop': '30px'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})

@callback(
    Output('employee-grid', 'data'),
    Output('event-log', 'children'),
    Input('employee-grid', 'cellEdited'),
    Input('employee-grid', 'cellClicked'),
    State('employee-grid', 'data'),
    prevent_initial_call=True
)
def update_event_log(cell_edited, cell_clicked, current_data):
    events = []

    if cell_edited:
        row, col = cell_edited['row'], cell_edited['col']
        col_id = COLUMNS[col]['id']
        new_value = current_data[row][col_id]
        events.append(html.Div([
            html.Strong('EDIT: '),
            f"Row {row}, Col {col} ({col_id}) → ",
            html.Code(str(new_value))
        ], style={'marginBottom': '5px', 'color': '#d9534f'}))

    if cell_clicked:
        events.append(html.Div([
            html.Strong('CLICK: '),
            f"Row {cell_clicked['row']}, Col {cell_clicked['col']}"
        ], style={'marginBottom': '5px', 'color': '#5bc0de'}))

    return current_data, events if events else 'No events yet'

if __name__ == '__main__':
    app.run(debug=True, port=8050)
