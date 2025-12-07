"""
Example 26: Data Filtering
Demonstrates client-side filtering with dropdown and text filters
"""
import dash
from dash import html, Input, Output, callback, dcc
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {'title': 'Employee', 'id': 'employee', 'width': 180},
    {'title': 'Department', 'id': 'department', 'width': 130},
    {'title': 'Role', 'id': 'role', 'width': 150},
    {'title': 'Salary', 'id': 'salary', 'width': 100},
    {'title': 'Experience', 'id': 'experience', 'width': 100},
    {'title': 'Status', 'id': 'status', 'width': 100},
]

# Full dataset
FULL_DATA = [
    {'employee': 'Alice Johnson', 'department': 'Engineering', 'role': 'Senior Developer', 'salary': 95000, 'experience': 8, 'status': 'Active'},
    {'employee': 'Bob Smith', 'department': 'Engineering', 'role': 'Junior Developer', 'salary': 65000, 'experience': 2, 'status': 'Active'},
    {'employee': 'Carol White', 'department': 'Marketing', 'role': 'Marketing Manager', 'salary': 82000, 'experience': 6, 'status': 'Active'},
    {'employee': 'David Brown', 'department': 'Sales', 'role': 'Sales Representative', 'salary': 55000, 'experience': 3, 'status': 'Active'},
    {'employee': 'Emma Davis', 'department': 'Engineering', 'role': 'Tech Lead', 'salary': 115000, 'experience': 10, 'status': 'Active'},
    {'employee': 'Frank Miller', 'department': 'HR', 'role': 'HR Specialist', 'salary': 58000, 'experience': 4, 'status': 'Active'},
    {'employee': 'Grace Lee', 'department': 'Marketing', 'role': 'Content Writer', 'salary': 52000, 'experience': 2, 'status': 'Active'},
    {'employee': 'Henry Wilson', 'department': 'Sales', 'role': 'Sales Manager', 'salary': 78000, 'experience': 7, 'status': 'Active'},
    {'employee': 'Ivy Chen', 'department': 'Engineering', 'role': 'DevOps Engineer', 'salary': 88000, 'experience': 5, 'status': 'Active'},
    {'employee': 'Jack Taylor', 'department': 'Finance', 'role': 'Financial Analyst', 'salary': 72000, 'experience': 4, 'status': 'Active'},
    {'employee': 'Kate Anderson', 'department': 'Engineering', 'role': 'QA Engineer', 'salary': 70000, 'experience': 3, 'status': 'Inactive'},
    {'employee': 'Liam Thomas', 'department': 'Marketing', 'role': 'SEO Specialist', 'salary': 60000, 'experience': 3, 'status': 'Active'},
    {'employee': 'Mia Jackson', 'department': 'Sales', 'role': 'Account Executive', 'salary': 68000, 'experience': 4, 'status': 'Active'},
    {'employee': 'Noah Garcia', 'department': 'HR', 'role': 'Recruiter', 'salary': 55000, 'experience': 2, 'status': 'Active'},
    {'employee': 'Olivia Martinez', 'department': 'Finance', 'role': 'Accountant', 'salary': 65000, 'experience': 5, 'status': 'Inactive'},
    {'employee': 'Peter Robinson', 'department': 'Engineering', 'role': 'Software Architect', 'salary': 125000, 'experience': 12, 'status': 'Active'},
    {'employee': 'Quinn Clark', 'department': 'Marketing', 'role': 'Brand Manager', 'salary': 75000, 'experience': 5, 'status': 'Active'},
    {'employee': 'Rachel Lewis', 'department': 'Sales', 'role': 'Business Developer', 'salary': 72000, 'experience': 6, 'status': 'Active'},
    {'employee': 'Sam Walker', 'department': 'Engineering', 'role': 'Frontend Developer', 'salary': 78000, 'experience': 4, 'status': 'Active'},
    {'employee': 'Tina Hall', 'department': 'HR', 'role': 'HR Manager', 'salary': 85000, 'experience': 8, 'status': 'Active'},
]

# Extract unique values for filters
DEPARTMENTS = sorted(set(row['department'] for row in FULL_DATA))
STATUSES = sorted(set(row['status'] for row in FULL_DATA))

app.layout = html.Div([
    html.H1('Employee Directory with Filters'),
    html.P('Use the filters below to narrow down the employee list.'),

    # Filter Controls
    html.Div([
        # Text search filter
        html.Div([
            html.Label('Search Name:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            dcc.Input(
                id='name-filter',
                type='text',
                placeholder='Type to filter by name...',
                style={
                    'padding': '8px 12px',
                    'fontSize': '14px',
                    'border': '1px solid #ccc',
                    'borderRadius': '4px',
                    'width': '200px',
                }
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px', 'verticalAlign': 'top'}),

        # Department dropdown filter
        html.Div([
            html.Label('Department:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='department-filter',
                options=[{'label': 'All Departments', 'value': 'all'}] +
                        [{'label': d, 'value': d} for d in DEPARTMENTS],
                value='all',
                clearable=False,
                style={'width': '180px'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px', 'verticalAlign': 'top'}),

        # Status dropdown filter
        html.Div([
            html.Label('Status:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            dcc.Dropdown(
                id='status-filter',
                options=[{'label': 'All Statuses', 'value': 'all'}] +
                        [{'label': s, 'value': s} for s in STATUSES],
                value='all',
                clearable=False,
                style={'width': '150px'}
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px', 'verticalAlign': 'top'}),

        # Salary range filter
        html.Div([
            html.Label('Min Salary:', style={'fontWeight': 'bold', 'display': 'block', 'marginBottom': '5px'}),
            dcc.Input(
                id='salary-filter',
                type='number',
                placeholder='e.g., 70000',
                min=0,
                step=5000,
                style={
                    'padding': '8px 12px',
                    'fontSize': '14px',
                    'border': '1px solid #ccc',
                    'borderRadius': '4px',
                    'width': '120px',
                }
            ),
        ], style={'display': 'inline-block', 'marginRight': '20px', 'verticalAlign': 'top'}),

        # Clear filters button
        html.Div([
            html.Label('\u00A0', style={'display': 'block', 'marginBottom': '5px'}),  # Spacer
            html.Button(
                'Clear All Filters',
                id='clear-filters-btn',
                style={
                    'padding': '8px 16px',
                    'backgroundColor': '#dc3545',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer',
                }
            ),
        ], style={'display': 'inline-block', 'verticalAlign': 'top'}),
    ], style={
        'marginBottom': '20px',
        'padding': '15px',
        'backgroundColor': '#f8f9fa',
        'borderRadius': '4px',
    }),

    # Results count
    html.Div(id='results-count', style={
        'marginBottom': '10px',
        'fontSize': '14px',
        'color': '#666',
    }),

    # Grid
    dgg.GlideGrid(
        id='filter-grid',
        columns=COLUMNS,
        data=FULL_DATA,
        height=450,
        readonly=True,
        rowMarkers='number',
        smoothScrollX=True,
        smoothScrollY=True,
    ),

    # Active filters display
    html.Div([
        html.H3('Active Filters:'),
        html.Div(id='active-filters', style={
            'padding': '10px',
            'backgroundColor': '#fff3cd',
            'border': '1px solid #ffc107',
            'borderRadius': '4px',
        })
    ], style={'marginTop': '20px'}),

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('filter-grid', 'data'),
    Output('results-count', 'children'),
    Output('active-filters', 'children'),
    Input('name-filter', 'value'),
    Input('department-filter', 'value'),
    Input('status-filter', 'value'),
    Input('salary-filter', 'value'),
)
def filter_data(name_filter, department, status, min_salary):
    filtered = FULL_DATA.copy()
    active_filters = []

    # Apply name filter (case-insensitive)
    if name_filter:
        filtered = [row for row in filtered if name_filter.lower() in row['employee'].lower()]
        active_filters.append(f'Name contains "{name_filter}"')

    # Apply department filter
    if department and department != 'all':
        filtered = [row for row in filtered if row['department'] == department]
        active_filters.append(f'Department = {department}')

    # Apply status filter
    if status and status != 'all':
        filtered = [row for row in filtered if row['status'] == status]
        active_filters.append(f'Status = {status}')

    # Apply salary filter
    if min_salary is not None and min_salary > 0:
        filtered = [row for row in filtered if row['salary'] >= min_salary]
        active_filters.append(f'Salary >= ${min_salary:,}')

    # Build results count message
    count_msg = f'Showing {len(filtered)} of {len(FULL_DATA)} employees'

    # Build active filters display
    if active_filters:
        filter_display = html.Ul([html.Li(f) for f in active_filters])
    else:
        filter_display = html.Em('No filters applied - showing all data')

    return filtered, count_msg, filter_display


@callback(
    Output('name-filter', 'value'),
    Output('department-filter', 'value'),
    Output('status-filter', 'value'),
    Output('salary-filter', 'value'),
    Input('clear-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_filters(n_clicks):
    return '', 'all', 'all', None


if __name__ == '__main__':
    app.run(debug=True, port=8050)