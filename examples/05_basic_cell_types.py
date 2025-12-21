"""
Example 5: All Cell Types
Demonstrates all supported cell types: text, number, boolean, markdown, uri, etc.
"""

import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "Text", "id": "text", "width": 150},
    {"title": "Number", "id": "number", "width": 100},
    {"title": "Boolean", "id": "boolean", "width": 100},
    {"title": "Markdown", "id": "markdown", "width": 200},
    {"title": "URI", "id": "uri", "width": 200},
    {"title": "Image", "id": "image", "width": 120},
    {"title": "Bubble", "id": "bubble", "width": 150},
    {"title": "Drilldown", "id": "drilldown", "width": 180},
    {"title": "Row ID", "id": "rowid", "width": 100},
    {"title": "Protected", "id": "protected", "width": 100},
    {"title": "Loading", "id": "loading", "width": 100},
]

# Mix of simple values and cell objects
DATA = [
    {
        # Simple text
        "text": "Simple text",
        # Simple number
        "number": 42,
        # Simple boolean
        "boolean": True,
        # Markdown cell object
        "markdown": {
            "kind": "markdown",
            "data": "**Bold** and *italic*",
            "allowOverlay": True,
        },
        # URI cell object
        "uri": {
            "kind": "uri",
            "data": "https://plotly.com/dash/",
            "displayData": "Dash Docs",
        },
        # Image cell
        "image": {
            "kind": "image",
            "data": ["https://picsum.photos/100/100?random=1"],
            "allowOverlay": True,
        },
        # Bubble cell - displays tags/labels
        "bubble": {"kind": "bubble", "data": ["Python", "Dash", "React"]},
        # Drilldown cell - text with optional images
        "drilldown": {
            "kind": "drilldown",
            "data": [
                {"text": "Item A", "img": "https://picsum.photos/20/20?random=10"},
                {"text": "Item B"},
            ],
        },
        # Row ID cell - for primary keys
        "rowid": {"kind": "rowid", "data": "ROW-001"},
        # Protected cell - shows hidden data as stars
        "protected": {"kind": "protected"},
        # Loading cell - shows loading spinner
        "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20},
    },
    {
        "text": "Another row",
        "number": 123.45,
        "boolean": False,
        "markdown": {"kind": "markdown", "data": "# Heading 1\n\nWith paragraph"},
        "uri": {"kind": "uri", "data": "https://github.com", "displayData": "GitHub"},
        "image": {"kind": "image", "data": ["https://picsum.photos/100/100?random=2"]},
        "bubble": {"kind": "bubble", "data": ["JavaScript", "TypeScript"]},
        "drilldown": {"kind": "drilldown", "data": [{"text": "Category X"}]},
        "rowid": {"kind": "rowid", "data": "ROW-002"},
        "protected": {"kind": "protected"},
        "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20},
    },
    {
        # Text cell object with custom settings
        "text": {"kind": "text", "data": "Custom text cell", "allowOverlay": True},
        # Number with display override
        "number": {"kind": "number", "data": 1000000, "displayData": "1.0M"},
        "boolean": True,
        "markdown": {"kind": "markdown", "data": "- Item 1\n- Item 2\n- Item 3"},
        "uri": {
            "kind": "uri",
            "data": "https://python.org",
            "displayData": "Python.org",
        },
        # Multiple images in one cell
        "image": {
            "kind": "image",
            "data": [
                "https://picsum.photos/100/100?random=3",
                "https://picsum.photos/100/100?random=4",
            ],
        },
        "bubble": {"kind": "bubble", "data": ["Data", "Science", "ML", "AI"]},
        "drilldown": {
            "kind": "drilldown",
            "data": [
                {"text": "View 1", "img": "https://picsum.photos/20/20?random=11"},
                {"text": "View 2", "img": "https://picsum.photos/20/20?random=12"},
            ],
        },
        "rowid": {"kind": "rowid", "data": "ROW-003"},
        "protected": {"kind": "protected"},
        "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20},
    },
    {
        "text": "Read-only cell",
        "number": 999,
        "boolean": False,
        "markdown": {
            "kind": "markdown",
            "data": "`code snippet`",
            "allowOverlay": False,
        },
        "uri": {"kind": "uri", "data": "https://react.dev"},
        "image": {"kind": "image", "data": ["https://picsum.photos/100/100?random=5"]},
        "bubble": {"kind": "bubble", "data": ["Web", "Dev"]},
        "drilldown": {"kind": "drilldown", "data": [{"text": "Details"}]},
        "rowid": {"kind": "rowid", "data": "ROW-004"},
        "protected": {"kind": "protected"},
        "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20},
    },
    {
        # Number cell with formatting options
        "text": "Formatted number",
        "number": {
            "kind": "number",
            "data": 1234567.89,
            "displayData": "1,234,567.89",
            "fixedDecimals": 2,
            "allowNegative": False,
            "thousandSeparator": True,
        },
        # Boolean with custom maxSize
        "boolean": {"kind": "boolean", "data": True, "maxSize": 24},
        "markdown": {"kind": "markdown", "data": "Number & Boolean props demo"},
        "uri": {"kind": "uri", "data": "https://example.com"},
        "image": {"kind": "image", "data": ["https://picsum.photos/100/100?random=6"]},
        "bubble": {"kind": "bubble", "data": ["Formatting"]},
        "drilldown": {"kind": "drilldown", "data": [{"text": "Props"}]},
        "rowid": {"kind": "rowid", "data": "ROW-005"},
        "protected": {"kind": "protected"},
        "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20},
    },
]

app.layout = html.Div(
    [
        html.H1("All Cell Types Demo"),
        html.Div(
            [
                html.H3("Cell Type Descriptions:"),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Strong("Text: "),
                                "Simple string values or text cell objects",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Number: "),
                                "Numeric values with optional display formatting",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Boolean: "),
                                "True/False values displayed as checkboxes",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Markdown: "),
                                "Rich text with markdown formatting (bold, italic, lists, etc.)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("URI: "),
                                "Clickable links with custom display text",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Image: "),
                                "Display images with optional overlay for editing",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Bubble: "),
                                "Display tags/labels in bubble format",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Drilldown: "),
                                "Display items with text and optional images",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Row ID: "),
                                "Display primary keys or identifiers",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Protected: "),
                                "Display hidden data as stars (e.g., passwords)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Loading: "),
                                "Display loading indicator for async data",
                            ]
                        ),
                    ]
                ),
            ],
            style={
                "marginBottom": "20px",
                "backgroundColor": "#f9f9f9",
                "padding": "15px",
                "borderRadius": "4px",
            },
        ),
        dgg.GlideGrid(
            id="cell-types-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            rowHeight=50,
            rowMarkers="number",
            columnResize=True,
        ),
        html.Div(
            [
                html.H4("How to use cell objects:"),
                html.Pre(
                    """
# Simple values (auto-detected):
data = [{"text": "text", "number": 123, "boolean": True}]

# Full cell objects:
data = [{
    "text": {"kind": "text", "data": "Hello"},
    "number": {"kind": "number", "data": 42, "displayData": "42 items"},
    "markdown": {"kind": "markdown", "data": "**Bold**"},
    "uri": {"kind": "uri", "data": "https://example.com", "displayData": "Example"},
    "boolean": {"kind": "boolean", "data": True},
    "image": {"kind": "image", "data": ["https://example.com/img.png"]},
    "bubble": {"kind": "bubble", "data": ["tag1", "tag2"]},
    "drilldown": {"kind": "drilldown", "data": [{"text": "Item", "img": "url"}]},
    "rowid": {"kind": "rowid", "data": "ID-001"},
    "protected": {"kind": "protected"},
    "loading": {"kind": "loading", "skeletonWidth": 80, "skeletonHeight": 20}
}]

# Number cell with formatting options:
"number": {
    "kind": "number",
    "data": 1234.56,
    "fixedDecimals": 2,        # Fixed decimal places in editor
    "allowNegative": False,     # Disable negative numbers
    "thousandSeparator": True,  # Add thousand separators
    "decimalSeparator": ".",    # Custom decimal separator
}

# Boolean cell with custom size:
"boolean": {"kind": "boolean", "data": True, "maxSize": 24}
        """,
                    style={
                        "backgroundColor": "#282c34",
                        "color": "#abb2bf",
                        "padding": "15px",
                        "borderRadius": "4px",
                    },
                ),
            ],
            style={"marginTop": "30px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
