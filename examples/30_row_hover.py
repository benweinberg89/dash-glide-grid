"""
Example 31: Row Hover Effect
Demonstrates the hoverRow prop
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Sample data
COLUMNS = [
    {'title': 'Name', 'id': 'name', 'width': 150},
    {'title': 'Department', 'id': 'department', 'width': 120},
    {'title': 'Role', 'id': 'role', 'width': 150},
    {'title': 'Email', 'id': 'email', 'width': 200},
    {'title': 'Location', 'id': 'location', 'width': 120},
    {'title': 'Years', 'id': 'years', 'width': 80},
]

DATA = [
    {'name': 'Alice Johnson', 'department': 'Engineering', 'role': 'Senior Developer', 'email': 'alice@example.com', 'location': 'New York', 'years': 5},
    {'name': 'Bob Smith', 'department': 'Marketing', 'role': 'Marketing Manager', 'email': 'bob@example.com', 'location': 'Chicago', 'years': 3},
    {'name': 'Carol Williams', 'department': 'Engineering', 'role': 'Tech Lead', 'email': 'carol@example.com', 'location': 'San Francisco', 'years': 8},
    {'name': 'David Brown', 'department': 'Sales', 'role': 'Sales Rep', 'email': 'david@example.com', 'location': 'Boston', 'years': 2},
    {'name': 'Eve Davis', 'department': 'HR', 'role': 'HR Director', 'email': 'eve@example.com', 'location': 'New York', 'years': 6},
    {'name': 'Frank Miller', 'department': 'Engineering', 'role': 'Junior Developer', 'email': 'frank@example.com', 'location': 'Austin', 'years': 1},
    {'name': 'Grace Lee', 'department': 'Design', 'role': 'UX Designer', 'email': 'grace@example.com', 'location': 'Seattle', 'years': 4},
    {'name': 'Henry Wilson', 'department': 'Finance', 'role': 'Accountant', 'email': 'henry@example.com', 'location': 'Chicago', 'years': 7},
    {'name': 'Ivy Chen', 'department': 'Engineering', 'role': 'DevOps Engineer', 'email': 'ivy@example.com', 'location': 'San Francisco', 'years': 3},
    {'name': 'Jack Taylor', 'department': 'Marketing', 'role': 'Content Writer', 'email': 'jack@example.com', 'location': 'Remote', 'years': 2},
]

app.layout = html.Div([
    html.H1('Row Hover Effect'),
    html.P('Hover over any cell to highlight the entire row.'),

    # Controls
    html.Div([
        html.Div([
            dcc.Checklist(
                id='hover-options',
                options=[
                    {'label': ' Enable Row Hover', 'value': 'row'},
                ],
                value=['row'],
                inline=True,
                style={'marginBottom': '10px'}
            ),
        ]),
        html.Div([
            html.Label('Row Highlight Color: ', style={'marginRight': '10px'}),
            dcc.Input(
                id='row-color',
                type='text',
                value='rgba(66, 135, 245, 0.15)',
                style={'width': '180px'}
            ),
        ], style={'marginBottom': '15px'}),
    ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

    # Grid
    html.Div(id='grid-container'),

    # Info
    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li('hoverRow: When enabled, highlights the entire row when hovering over any cell'),
            html.Li('Uses getRowThemeOverride internally for clean row hover effect'),
            html.Li('Customize the color via theme.bgRowHovered'),
        ])
    ], style={'marginTop': '20px', 'color': '#666'})
], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('hover-options', 'value'),
    Input('row-color', 'value'),
)
def update_grid(hover_options, row_color):
    enable_hover = 'row' in (hover_options or [])

    return dgg.GlideGrid(
        id='hover-grid',
        columns=COLUMNS,
        data=DATA,
        height=400,
        readonly=True,
        rowMarkers='number',
        smoothScrollX=True,
        smoothScrollY=True,
        hoverRow=enable_hover,
        theme={
            'bgRowHovered': row_color or 'rgba(0, 0, 0, 0.04)',
        }
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)