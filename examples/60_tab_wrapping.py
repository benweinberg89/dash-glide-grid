"""
Example: Tab Wrapping Navigation

Demonstrates the tabWrapping prop for spreadsheet-like Tab navigation:
- Tab at end of row wraps to first cell of next row
- Shift+Tab at start of row wraps to last cell of previous row
- Works in both selection mode and edit mode
- At grid boundaries (first/last cell), stays put

Try it:
1. Click any cell to select it
2. Press Tab repeatedly to navigate through cells
3. Watch Tab wrap to the next row at row boundaries
4. Press Shift+Tab to navigate backwards with wrapping
5. Double-click to edit a cell, then Tab to move to next cell and continue editing
"""

from dash import Dash, html
import dash_glide_grid as dgg

app = Dash(__name__)

# Sample editable data - all text columns for easy Tab editing test
DATA = [
    {"name": "Alice", "department": "Engineering", "role": "Senior Dev", "location": "NYC"},
    {"name": "Bob", "department": "Marketing", "role": "Manager", "location": "LA"},
    {"name": "Carol", "department": "Sales", "role": "Lead", "location": "Chicago"},
    {"name": "David", "department": "Engineering", "role": "Junior Dev", "location": "Seattle"},
    {"name": "Eve", "department": "HR", "role": "Coordinator", "location": "Boston"},
]

COLUMNS = [
    {"id": "name", "title": "Name", "width": 150},
    {"id": "department", "title": "Department", "width": 150},
    {"id": "role", "title": "Role", "width": 120},
    {"id": "location", "title": "Location", "width": 120},
]

app.layout = html.Div(
    [
        html.H1("Tab Wrapping Navigation"),
        html.P(
            [
                "Tab key navigation wraps at row boundaries. ",
                html.Strong("Tab"),
                " at end of row → first cell of next row. ",
                html.Strong("Shift+Tab"),
                " at start of row → last cell of previous row.",
            ]
        ),
        html.H3("Instructions:"),
        html.Ul(
            [
                html.Li("Click any cell to select it"),
                html.Li("Press Tab repeatedly - watch it wrap to next row at row end"),
                html.Li("Press Shift+Tab - watch it wrap to previous row at row start"),
                html.Li("Double-click to edit, then Tab to move and continue editing"),
                html.Li("At grid boundaries (first/last cell), Tab stays put"),
            ]
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=300,
            tabWrapping=True,  # Enable Tab wrapping
            editOnType=True,   # Typing immediately starts editing
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Comparison Grid (tabWrapping=False)"),
                html.P("This grid has default Tab behavior - no wrapping at row boundaries."),
                dgg.GlideGrid(
                    id="grid-no-wrap",
                    columns=COLUMNS,
                    data=DATA,
                    height=300,
                    tabWrapping=False,  # Default behavior
                    editOnType=True,
                    rowMarkers="number",
                ),
            ],
            style={"marginTop": "40px"},
        ),
    ],
    style={"padding": "20px", "fontFamily": "system-ui, sans-serif"},
)

if __name__ == "__main__":
    app.run(debug=True, port=8060)
