"""
Example 4: Large Dataset Performance
Demonstrates handling of large datasets with 10,000+ rows
"""
import dash
from dash import html
import dash_glide_grid as dgg
import random

app = dash.Dash(__name__)

# Generate large dataset
def generate_large_dataset(num_rows=10000):
    """Generate a large dataset for performance testing"""
    first_names = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Operations']

    data = []
    for i in range(num_rows):
        row = {
            'name': f"{random.choice(first_names)} {random.choice(last_names)}",
            'department': random.choice(departments),
            'city': random.choice(cities),
            'age': random.randint(22, 65),
            'salary': random.randint(40000, 150000),
            'active': random.choice([True, False]),
            'rating': round(random.uniform(1.0, 5.0), 1)
        }
        data.append(row)

    return data

COLUMNS = [
    {'title': 'Name', 'id': 'name', 'width': 180},
    {'title': 'Department', 'id': 'department', 'width': 130},
    {'title': 'City', 'id': 'city', 'width': 130},
    {'title': 'Age', 'id': 'age', 'width': 80},
    {'title': 'Salary', 'id': 'salary', 'width': 100},
    {'title': 'Active', 'id': 'active', 'width': 80},
    {'title': 'Rating', 'id': 'rating', 'width': 80}
]

# Generate 10,000 rows
LARGE_DATA = generate_large_dataset(10000)

app.layout = html.Div([
    html.H1('Large Dataset Performance Test'),
    html.P(f'Grid with {len(LARGE_DATA):,} rows - scroll smoothly with virtualization'),

    html.Div([
        html.Strong('Performance Stats: '),
        f'{len(LARGE_DATA):,} rows × {len(COLUMNS)} columns = {len(LARGE_DATA) * len(COLUMNS):,} cells'
    ], style={
        'padding': '10px',
        'backgroundColor': '#e7f3ff',
        'border': '1px solid #2196F3',
        'borderRadius': '4px',
        'marginBottom': '20px'
    }),

    dgg.GlideGrid(
        id='large-grid',
        columns=COLUMNS,
        data=LARGE_DATA,
        height=600,
        rowMarkers='number',
        freezeColumns=1,  # Freeze the Name column
        columnResize=True,
        smoothScrollX=True,
        smoothScrollY=True
    ),

    html.Div([
        html.P('Note: The grid uses virtualization to render only visible cells, '
               'ensuring smooth performance even with millions of rows.'),
        html.P('Try scrolling, resizing columns, and selecting cells - all remain fast!')
    ], style={'marginTop': '20px', 'color': '#666'})

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})

if __name__ == '__main__':
    app.run(debug=True, port=8050)
