"""
Example 38: Editor Scroll Behavior
Demonstrates the editorScrollBehavior prop which controls how the grid behaves
when the user scrolls while a cell editor is open.
"""
import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Sample data with various cell types to demonstrate editing
COLUMNS = [
    {'title': 'ID', 'id': 'id', 'width': 60},
    {'title': 'Name', 'id': 'name', 'width': 150},
    {'title': 'Status', 'id': 'status', 'width': 140},
    {'title': 'Tags', 'id': 'tags', 'width': 200},
    {'title': 'Notes', 'id': 'notes', 'width': 250},
    {'title': 'Amount', 'id': 'amount', 'width': 100},
]

# Status dropdown options
STATUS_OPTIONS = [
    {'value': 'active', 'label': 'Active', 'color': '#10b981'},
    {'value': 'pending', 'label': 'Pending', 'color': '#f59e0b'},
    {'value': 'inactive', 'label': 'Inactive', 'color': '#ef4444'},
    {'value': 'review', 'label': 'Under Review', 'color': '#6366f1'},
]

# Tags multiselect options
TAG_OPTIONS = [
    {'value': 'urgent', 'label': 'Urgent', 'color': '#ef4444'},
    {'value': 'important', 'label': 'Important', 'color': '#f59e0b'},
    {'value': 'low', 'label': 'Low Priority', 'color': '#22c55e'},
    {'value': 'followup', 'label': 'Follow Up', 'color': '#3b82f6'},
    {'value': 'archived', 'label': 'Archived', 'color': '#6b7280'},
]

# Generate sample data with custom cell types
DATA = []
for i in range(30):
    status_idx = i % 4
    DATA.append({
        'id': i + 1,
        'name': f'Project {chr(65 + (i % 26))}',
        'status': {
            'kind': 'dropdown-cell',
            'data': {
                'value': STATUS_OPTIONS[status_idx]['value'],
                'allowedValues': STATUS_OPTIONS,
            },
            'allowOverlay': True,
        },
        'tags': {
            'kind': 'multi-select-cell',
            'data': {
                'values': ['urgent', 'important'] if i % 3 == 0 else ['low'],
                'options': TAG_OPTIONS,
                'allowCreation': False,
            },
            'allowOverlay': True,
        },
        'notes': f'Notes for project {i + 1}. Click to edit this text field.',
        'amount': (i + 1) * 100,
    })

app.layout = html.Div([
    html.H1('Editor Scroll Behavior'),
    html.P([
        'This example demonstrates the ',
        html.Code('editorScrollBehavior'),
        ' prop which controls what happens when you scroll while editing a cell.'
    ]),

    # Controls
    html.Div([
        html.Label('Scroll Behavior Mode:', style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='scroll-behavior-mode',
            options=[
                {'label': ' default - Editor stays at original position (standard behavior)', 'value': 'default'},
                {'label': ' close-dropdown-on-scroll - Only dropdown menu closes, overlay stays open', 'value': 'close-dropdown-on-scroll'},
                {'label': ' close-overlay-on-scroll - Entire editor overlay closes on scroll', 'value': 'close-overlay-on-scroll'},
                {'label': ' lock-scroll - Scrolling is prevented while editor is open', 'value': 'lock-scroll'},
            ],
            value='default',
            labelStyle={'display': 'block', 'marginBottom': '8px'}
        ),
    ], style={'marginBottom': '20px', 'padding': '15px', 'backgroundColor': '#f5f5f5', 'borderRadius': '8px'}),

    # Instructions
    html.Div([
        html.Strong('Try this: '),
        'Click on a cell to open the editor (especially a Dropdown or Tags cell), then try scrolling the page.',
    ], style={'marginBottom': '15px', 'padding': '10px', 'backgroundColor': '#e0f2fe', 'borderRadius': '4px'}),

    # Grid container
    html.Div(id='grid-container'),

    # Spacer to enable page scrolling
    html.Div([
        html.P('Scroll down to see more content and test the scroll behavior...',
               style={'color': '#666', 'fontStyle': 'italic'}),
    ], style={'marginTop': '20px'}),

    # Info section
    html.Div([
        html.H3('How it works:'),
        html.Ul([
            html.Li([
                html.Strong('default'),
                ': The editor overlay stays at its original position when you scroll. ',
                'This is the standard Glide Data Grid behavior. The editor may appear disconnected ',
                'from its cell after scrolling.'
            ]),
            html.Li([
                html.Strong('close-dropdown-on-scroll'),
                ': Only the dropdown menu closes on scroll, but the overlay editor (text input) stays open. ',
                'Good for dropdown/multiselect cells where you want to close the menu but continue typing.'
            ]),
            html.Li([
                html.Strong('close-overlay-on-scroll'),
                ': The entire editor overlay closes when any scroll is detected. ',
                'This prevents orphaned editors completely.'
            ]),
            html.Li([
                html.Strong('lock-scroll'),
                ': Scrolling is completely disabled while the editor is open (similar to a modal). ',
                'The editor stays perfectly aligned with its cell. Close the editor to scroll again.'
            ]),
        ]),
        html.H4('Cell Types in this example:'),
        html.Ul([
            html.Li([html.Strong('Status'), ': Dropdown cell with colored options']),
            html.Li([html.Strong('Tags'), ': Multi-select cell with colored tags']),
            html.Li([html.Strong('Notes'), ': Standard text editor']),
            html.Li([html.Strong('Amount'), ': Number editor']),
        ]),
        html.H4('Use cases:'),
        html.Ul([
            html.Li([html.Strong('default'), ': Best when users may need to reference other data while editing']),
            html.Li([html.Strong('close-dropdown-on-scroll'), ': Good for dropdown cells where scrolling should close the menu but not the input']),
            html.Li([html.Strong('close-overlay-on-scroll'), ': Good for preventing confusion from misaligned editors']),
            html.Li([html.Strong('lock-scroll'), ': Best for focused data entry where scroll during edit is not needed']),
        ])
    ], style={'marginTop': '30px', 'color': '#666'}),

    # Extra content to enable scrolling
    html.Div([
        html.H3('Additional Content (to enable page scrolling)'),
        html.P('This extra content allows you to test page scrolling behavior. '
               'Open an editor in the grid above, then try to scroll down here.'),
        html.Div([
            html.P(f'Paragraph {i+1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. '
                   'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.')
            for i in range(5)
        ], style={'color': '#888'}),
    ], style={'marginTop': '40px', 'paddingTop': '20px', 'borderTop': '1px solid #ddd'}),

], style={'margin': '40px', 'fontFamily': 'Arial, sans-serif'})


@callback(
    Output('grid-container', 'children'),
    Input('scroll-behavior-mode', 'value'),
)
def update_grid(scroll_mode):
    return dgg.GlideGrid(
        id='scroll-behavior-grid',
        columns=COLUMNS,
        data=DATA,
        height=400,
        rowMarkers='number',
        cellActivationBehavior='second-click',
        editorScrollBehavior=scroll_mode,
    )


if __name__ == '__main__':
    app.run(debug=True, port=8050)
