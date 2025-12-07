"""
Example 9: Grouped Columns
Demonstrates how to use column groups to organize related columns under group headers.
"""
import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Define columns with groups
# Columns with the same 'group' value will be grouped together under a header
COLUMNS = [
    # Personal Information group
    {'title': 'First Name', 'width': 120, 'id': 'first_name', 'group': 'Personal Info'},
    {'title': 'Last Name', 'width': 120, 'id': 'last_name', 'group': 'Personal Info'},
    {'title': 'Age', 'width': 80, 'id': 'age', 'group': 'Personal Info'},

    # Contact Details group
    {'title': 'Email', 'width': 200, 'id': 'email', 'group': 'Contact Details'},
    {'title': 'Phone', 'width': 130, 'id': 'phone', 'group': 'Contact Details'},
    {'title': 'City', 'width': 120, 'id': 'city', 'group': 'Contact Details'},

    # Employment group
    {'title': 'Department', 'width': 140, 'id': 'department', 'group': 'Employment'},
    {'title': 'Position', 'width': 150, 'id': 'position', 'group': 'Employment'},
    {'title': 'Salary', 'width': 100, 'id': 'salary', 'group': 'Employment'},

    # Performance group
    {'title': 'Rating', 'width': 80, 'id': 'rating', 'group': 'Performance'},
    {'title': 'Projects', 'width': 90, 'id': 'projects', 'group': 'Performance'},
]

# Sample employee data
DATA = [
    {
        'first_name': 'Alice', 'last_name': 'Johnson', 'age': 32,
        'email': 'alice.j@company.com', 'phone': '555-0101', 'city': 'New York',
        'department': 'Engineering', 'position': 'Senior Developer', 'salary': 125000,
        'rating': 4.8, 'projects': 12
    },
    {
        'first_name': 'Bob', 'last_name': 'Smith', 'age': 28,
        'email': 'bob.smith@company.com', 'phone': '555-0102', 'city': 'San Francisco',
        'department': 'Engineering', 'position': 'Developer', 'salary': 95000,
        'rating': 4.5, 'projects': 8
    },
    {
        'first_name': 'Carol', 'last_name': 'Williams', 'age': 35,
        'email': 'carol.w@company.com', 'phone': '555-0103', 'city': 'Boston',
        'department': 'Product', 'position': 'Product Manager', 'salary': 110000,
        'rating': 4.7, 'projects': 15
    },
    {
        'first_name': 'David', 'last_name': 'Brown', 'age': 29,
        'email': 'david.b@company.com', 'phone': '555-0104', 'city': 'Seattle',
        'department': 'Design', 'position': 'UX Designer', 'salary': 90000,
        'rating': 4.6, 'projects': 10
    },
    {
        'first_name': 'Eve', 'last_name': 'Davis', 'age': 41,
        'email': 'eve.davis@company.com', 'phone': '555-0105', 'city': 'Austin',
        'department': 'Engineering', 'position': 'Engineering Manager', 'salary': 145000,
        'rating': 4.9, 'projects': 20
    },
    {
        'first_name': 'Frank', 'last_name': 'Miller', 'age': 26,
        'email': 'frank.m@company.com', 'phone': '555-0106', 'city': 'Chicago',
        'department': 'Marketing', 'position': 'Marketing Specialist', 'salary': 75000,
        'rating': 4.3, 'projects': 6
    },
    {
        'first_name': 'Grace', 'last_name': 'Wilson', 'age': 33,
        'email': 'grace.w@company.com', 'phone': '555-0107', 'city': 'Denver',
        'department': 'Sales', 'position': 'Sales Manager', 'salary': 105000,
        'rating': 4.8, 'projects': 18
    },
    {
        'first_name': 'Henry', 'last_name': 'Taylor', 'age': 30,
        'email': 'henry.t@company.com', 'phone': '555-0108', 'city': 'Miami',
        'department': 'Engineering', 'position': 'DevOps Engineer', 'salary': 100000,
        'rating': 4.4, 'projects': 9
    },
]

app.layout = html.Div([
    html.H1('Grouped Columns Demo'),

    html.Div([
        html.H3('About Column Groups:'),
        html.P([
            'Column groups help organize related columns under a common header. ',
            'This makes it easier to navigate large datasets with many columns. ',
            'In this example, employee data is organized into four logical groups:'
        ]),
        html.Ul([
            html.Li([html.Strong('Personal Info: '), 'Basic personal details (name, age)']),
            html.Li([html.Strong('Contact Details: '), 'Communication information (email, phone, location)']),
            html.Li([html.Strong('Employment: '), 'Work-related data (department, position, salary)']),
            html.Li([html.Strong('Performance: '), 'Performance metrics (rating, project count)']),
        ])
    ], style={
        'marginBottom': '20px',
        'backgroundColor': '#f9f9f9',
        'padding': '15px',
        'borderRadius': '4px'
    }),

    html.Div([
        dgg.GlideGrid(
            id='grouped-columns-grid',
            columns=COLUMNS,
            data=DATA,
            height=500,
            rowMarkers='number',
            columnResize=True,
            verticalBorder=True,
            headerHeight=36,
        ),
    ], style={'marginBottom': '20px'}),

    html.Div([
        html.H4('How to Define Column Groups:'),
        html.Pre('''
# Add the 'group' property to columns:
COLUMNS = [
    {'title': 'First Name', 'width': 120, 'group': 'Personal Info'},
    {'title': 'Last Name', 'width': 120, 'group': 'Personal Info'},
    {'title': 'Email', 'width': 200, 'group': 'Contact Details'},
    {'title': 'Phone', 'width': 130, 'group': 'Contact Details'},
    # ... more columns
]

# Columns with the same group name will appear under that group header
        ''', style={
            'backgroundColor': '#282c34',
            'color': '#abb2bf',
            'padding': '15px',
            'borderRadius': '4px',
            'overflowX': 'auto'
        })
    ], style={'marginTop': '20px'})

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})

if __name__ == '__main__':
    app.run(debug=True, port=8050)
