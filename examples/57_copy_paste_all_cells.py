"""
Example: Copy/Paste Test for All Cell Types

Tests copy (Ctrl+C) and paste (Ctrl+V) functionality across all cell types.

Instructions:
1. Select a cell and press Ctrl+C to copy
2. Check the "Last Copy Data" output to see what was copied
3. Select another cell and press Ctrl+V to paste
4. Check the "Last Paste Action" output to see the result

Copy behavior (what goes to clipboard):
- dropdown-cell: the selected value
- multi-select-cell: comma-separated values
- tags-cell: comma-separated tag names
- star-cell: rating number
- date-picker-cell: display date or ISO date
- range-cell: label or value
- links-cell: markdown format [title](url), preserves both title and URL
- sparkline-cell: comma-separated values
- tree-view-cell: text|depth|canOpen|isOpen (preserves tree structure)
- user-profile-cell: name
- button-cell: title
- spinner-cell: empty

Paste behavior (how pasted data is transformed):
- dropdown-cell: only accepts values in allowedValues
- multi-select-cell: comma-separated, filtered to valid options
- tags-cell: comma-separated, filtered to possibleTags
- star-cell: parsed as integer, clamped to 0-maxStars
- date-picker-cell: parses various date formats
- range-cell: parsed as float, clamped to min/max
- sparkline-cell: parsed as comma-separated numbers
- etc.
"""

from dash import Dash, html, callback, Input, Output
import dash_glide_grid as dgg
import json

app = Dash(__name__)

# Status options for dropdowns
STATUS_OPTIONS = ["active", "pending", "completed", "archived"]

# Tag definitions
TAG_DEFS = [
    {"tag": "Bug", "color": "#ef4444"},
    {"tag": "Feature", "color": "#8b5cf6"},
    {"tag": "Critical", "color": "#f97316"},
]

# Skill options
SKILL_OPTIONS = [
    {"value": "python", "label": "Python"},
    {"value": "javascript", "label": "JavaScript"},
    {"value": "rust", "label": "Rust"},
]

DATA = [
    {
        "id": {"kind": "number", "data": 1},
        "text": {"kind": "text", "data": "Hello World"},
        "number": {"kind": "number", "data": 42},
        "boolean": {"kind": "boolean", "data": True},
        "dropdown": {
            "kind": "dropdown-cell",
            "value": "active",
            "allowedValues": STATUS_OPTIONS,
        },
        "multiselect": {
            "kind": "multi-select-cell",
            "values": ["python", "rust"],
            "options": SKILL_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Bug", "Feature"],
            "possibleTags": TAG_DEFS,
        },
        "stars": {"kind": "star-cell", "rating": 4, "maxStars": 5},
        "date": {
            "kind": "date-picker-cell",
            "date": "2024-03-15",
            "displayDate": "Mar 15, 2024",
        },
        "range": {
            "kind": "range-cell",
            "value": 75,
            "min": 0,
            "max": 100,
            "label": "75%",
        },
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "Google", "href": "https://google.com"},
                {"title": "GitHub", "href": "https://github.com"},
            ],
        },
        "sparkline": {
            "kind": "sparkline-cell",
            "values": [10, 25, 15, 40, 30],
            "yAxis": [0, 50],
        },
        "tree": {
            "kind": "tree-view-cell",
            "text": "Parent Node",
            "depth": 0,
            "canOpen": True,
        },
        "profile": {
            "kind": "user-profile-cell",
            "name": "Alice Johnson",
            "initial": "A",
            "tint": "#3b82f6",
        },
        "button": {"kind": "button-cell", "title": "Click Me"},
        "spinner": {"kind": "spinner-cell"},
    },
    {
        "id": {"kind": "number", "data": 2},
        "text": {"kind": "text", "data": "Test Row"},
        "number": {"kind": "number", "data": 100},
        "boolean": {"kind": "boolean", "data": False},
        "dropdown": {
            "kind": "dropdown-cell",
            "value": "pending",
            "allowedValues": STATUS_OPTIONS,
        },
        "multiselect": {
            "kind": "multi-select-cell",
            "values": ["javascript"],
            "options": SKILL_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Critical"],
            "possibleTags": TAG_DEFS,
        },
        "stars": {"kind": "star-cell", "rating": 2, "maxStars": 5},
        "date": {
            "kind": "date-picker-cell",
            "date": "2024-01-01",
            "displayDate": "Jan 1, 2024",
        },
        "range": {
            "kind": "range-cell",
            "value": 25,
            "min": 0,
            "max": 100,
            "label": "25%",
        },
        "links": {
            "kind": "links-cell",
            "links": [{"title": "Example", "href": "https://example.com"}],
        },
        "sparkline": {
            "kind": "sparkline-cell",
            "values": [5, 10, 15, 20, 25],
            "yAxis": [0, 30],
        },
        "tree": {
            "kind": "tree-view-cell",
            "text": "Child Node",
            "depth": 1,
            "canOpen": False,
        },
        "profile": {
            "kind": "user-profile-cell",
            "name": "Bob Smith",
            "initial": "B",
            "tint": "#10b981",
        },
        "button": {"kind": "button-cell", "title": "Action"},
        "spinner": {"kind": "spinner-cell"},
    },
]

COLUMNS = [
    {"id": "id", "title": "ID", "width": 50},
    {"id": "text", "title": "Text", "width": 100},
    {"id": "number", "title": "Number", "width": 80},
    {"id": "boolean", "title": "Boolean", "width": 80},
    {"id": "dropdown", "title": "Dropdown", "width": 100},
    {"id": "multiselect", "title": "Multi-Select", "width": 130},
    {"id": "tags", "title": "Tags", "width": 140},
    {"id": "stars", "title": "Stars", "width": 100},
    {"id": "date", "title": "Date", "width": 110},
    {"id": "range", "title": "Range", "width": 110},
    {"id": "links", "title": "Links", "width": 140},
    {"id": "sparkline", "title": "Sparkline", "width": 100},
    {"id": "tree", "title": "Tree", "width": 110},
    {"id": "profile", "title": "Profile", "width": 130},
    {"id": "button", "title": "Button", "width": 90},
    {"id": "spinner", "title": "Spinner", "width": 80},
]

app.layout = html.Div(
    [
        html.H1("Copy/Paste Test - All Cell Types"),
        html.P(
            [
                "Select a cell and press ",
                html.Code("Ctrl+C"),
                " to copy, then select another cell and press ",
                html.Code("Ctrl+V"),
                " to paste.",
            ]
        ),
        html.P(
            "Try copying from row 1 and pasting into row 2 to test paste validation.",
            style={"color": "#6b7280", "fontSize": "14px"},
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=200,
            enableCopyPaste=True,
            fillHandle=True,
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Cell Edit Events:"),
                html.Pre(
                    id="edit-output",
                    style={
                        "backgroundColor": "#f3f4f6",
                        "padding": "10px",
                        "borderRadius": "6px",
                        "maxHeight": "200px",
                        "overflow": "auto",
                    },
                ),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            [
                html.H3("Expected Copy Values:"),
                html.Table(
                    [
                        html.Tr(
                            [html.Th("Cell Type"), html.Th("Row 1 Copy Value")]
                        ),
                        html.Tr([html.Td("Text"), html.Td("Hello World")]),
                        html.Tr([html.Td("Number"), html.Td("42")]),
                        html.Tr([html.Td("Boolean"), html.Td("true")]),
                        html.Tr([html.Td("Dropdown"), html.Td("active")]),
                        html.Tr([html.Td("Multi-Select"), html.Td("python, rust")]),
                        html.Tr([html.Td("Tags"), html.Td("Bug, Feature")]),
                        html.Tr([html.Td("Stars"), html.Td("4")]),
                        html.Tr([html.Td("Date"), html.Td("Mar 15, 2024")]),
                        html.Tr([html.Td("Range"), html.Td("75%")]),
                        html.Tr(
                            [
                                html.Td("Links"),
                                html.Td("[Google](https://google.com), [GitHub](https://github.com)"),
                            ]
                        ),
                        html.Tr([html.Td("Sparkline"), html.Td("10, 25, 15, 40, 30")]),
                        html.Tr([html.Td("Tree"), html.Td("Parent Node|0|true|false")]),
                        html.Tr([html.Td("Profile"), html.Td("Alice Johnson")]),
                        html.Tr([html.Td("Button"), html.Td("Click Me")]),
                        html.Tr([html.Td("Spinner"), html.Td("(empty)")]),
                    ],
                    style={
                        "borderCollapse": "collapse",
                        "width": "100%",
                        "maxWidth": "500px",
                    },
                ),
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"padding": "20px", "fontFamily": "system-ui, sans-serif"},
)


# Add CSS for table
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            table th, table td {
                border: 1px solid #d1d5db;
                padding: 8px 12px;
                text-align: left;
            }
            table th {
                background-color: #f3f4f6;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""


@callback(
    Output("edit-output", "children"),
    Input("grid", "cellEdited"),
    Input("grid", "data"),
)
def show_edit(cell_edited, data):
    if cell_edited:
        return json.dumps(cell_edited, indent=2, default=str)
    return "No edits yet. Try copying and pasting between cells."


if __name__ == "__main__":
    app.run(debug=True, port=8057)
