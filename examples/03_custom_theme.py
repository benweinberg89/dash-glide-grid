"""
Example 3: Custom Theme and Styling
Demonstrates theme customization
"""
import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {'title': 'Task', 'id': 'task', 'width': 250},
    {'title': 'Priority', 'id': 'priority', 'width': 100},
    {'title': 'Status', 'id': 'status', 'width': 120},
    {'title': 'Assigned', 'id': 'assigned', 'width': 150},
    {'title': 'Due Date', 'id': 'due_date', 'width': 120}
]

DATA = [
    {'task': 'Implement authentication', 'priority': 'High', 'status': 'In Progress', 'assigned': 'Alice', 'due_date': '2024-01-15'},
    {'task': 'Fix bug #1234', 'priority': 'Critical', 'status': 'Open', 'assigned': 'Bob', 'due_date': '2024-01-10'},
    {'task': 'Update documentation', 'priority': 'Low', 'status': 'Completed', 'assigned': 'Charlie', 'due_date': '2024-01-05'},
    {'task': 'Code review PR #567', 'priority': 'Medium', 'status': 'In Progress', 'assigned': 'Diana', 'due_date': '2024-01-12'},
    {'task': 'Database optimization', 'priority': 'High', 'status': 'Open', 'assigned': 'Eve', 'due_date': '2024-01-20'},
    {'task': 'UI redesign', 'priority': 'Medium', 'status': 'Planning', 'assigned': 'Frank', 'due_date': '2024-02-01'},
    {'task': 'API integration', 'priority': 'High', 'status': 'In Progress', 'assigned': 'Grace', 'due_date': '2024-01-18'},
]

# Dark theme configuration - matches Dash Mantine Components dark theme
DARK_THEME = {
    'accentColor': '#D6336C',  # Mantine pink
    'accentLight': 'rgba(214, 51, 108, 0.2)',
    'bgCell': '#292929',  # rgb(41,41,41)
    'bgCellMedium': '#2D2D2D',  # rgb(45,45,45) - for alternating rows
    'bgHeader': '#323232',  # rgb(50,50,50)
    'bgHeaderHasFocus': '#3D3D3D',
    'bgHeaderHovered': '#3D3D3D',
    'textDark': '#BEBEBE',  # rgb(190,190,190)
    'textMedium': '#BEBEBE',
    'textLight': '#808080',
    'textHeader': '#BEBEBE',
    'borderColor': 'rgba(255, 255, 255, 0.2)',
    'horizontalBorderColor': 'rgba(255, 255, 255, 0.2)',
}

# Light theme - matches Dash Mantine Components light theme
LIGHT_THEME = {
    'accentColor': '#D6336C',  # Mantine pink
    'accentLight': 'rgba(214, 51, 108, 0.1)',
    'bgCell': '#FFFFFF',
    'bgCellMedium': '#F5F5F5',  # Subtle alternating row
    'bgHeader': '#F5F5F5',
    'bgHeaderHasFocus': 'rgba(125, 125, 125, 0.1)',
    'bgHeaderHovered': 'rgba(125, 125, 125, 0.1)',
    'textDark': '#212121',
    'textMedium': '#424242',
    'textLight': '#757575',
    'textHeader': '#212121',
    'borderColor': '#E0E0E0',
    'horizontalBorderColor': '#E0E0E0',
}

app.layout = html.Div([
    html.H1('Task Manager - Custom Themes'),

    html.Div([
        html.H3('Dark Theme', style={'color': '#FFFFFF'}),
        dgg.GlideGrid(
            id='dark-grid',
            columns=COLUMNS,
            data=DATA,
            height=300,
            theme=DARK_THEME,
            rowMarkers='checkbox',
            columnResize=True
        ),
    ], style={'marginBottom': '40px', 'padding': '20px', 'backgroundColor': '#121212'}),

    html.Div([
        html.H3('Light Theme'),
        dgg.GlideGrid(
            id='light-grid',
            columns=COLUMNS,
            data=DATA,
            height=300,
            theme=LIGHT_THEME,
            rowMarkers='number',
            columnResize=True
        ),
    ], style={'marginBottom': '40px', 'padding': '20px', 'backgroundColor': '#F5F5F5'}),

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})

if __name__ == '__main__':
    app.run(debug=True, port=8050)
