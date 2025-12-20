"""
Example 6: Custom Cell Editors (Dropdown & MultiSelect)
Demonstrates dropdown and multi-select custom cell editors from @glideapps/glide-data-grid-cells
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg
import json

app = dash.Dash(__name__)

# Column definitions
COLUMNS = [
    {"title": "Product", "id": "product", "width": 200},
    {"title": "Status", "id": "status", "width": 150},
    {"title": "Priority", "id": "priority", "width": 120},
    {"title": "Tags (stays open)", "id": "tags", "width": 200},
    {"title": "Tags (closes)", "id": "tags_close", "width": 200},
    {"title": "Categories", "id": "categories", "width": 200},
]

TAG_OPTIONS = [
    {"value": "frontend", "color": "#ffc38a", "label": "Frontend"},
    {"value": "backend", "color": "#ebfdea", "label": "Backend"},
    {"value": "design", "color": "#a8dadc", "label": "Design"},
    {"value": "testing", "color": "#e63946", "label": "Testing"},
]

# Initial data with custom cell types
# Dropdown cells: kind='dropdown-cell' with allowedValues and value
# MultiSelect cells: kind='multi-select-cell' with values and options
DATA = [
    {
        "product": "Website Redesign",
        "status": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Not Started", "In Progress", "Review", "Complete"],
                "value": "In Progress",
            },
            "copyData": "In Progress",
        },
        "priority": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Low", "Medium", "High", "Urgent"],
                "value": "High",
            },
            "copyData": "High",
        },
        "tags": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["frontend", "design"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "frontend,design",
        },
        "tags_close": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["frontend", "design"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
                "closeMenuOnSelect": True,
            },
            "copyData": "frontend,design",
        },
        "categories": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["web", "mobile"],
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "web,mobile",
        },
    },
    {
        "product": "API Development",
        "status": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Not Started", "In Progress", "Review", "Complete"],
                "value": "Review",
            },
            "copyData": "Review",
        },
        "priority": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Low", "Medium", "High", "Urgent"],
                "value": "Urgent",
            },
            "copyData": "Urgent",
        },
        "tags": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "backend,testing",
        },
        "tags_close": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
                "closeMenuOnSelect": True,
            },
            "copyData": "backend,testing",
        },
        "categories": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["api", "microservices"],
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "api,microservices",
        },
    },
    {
        "product": "Database Migration",
        "status": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Not Started", "In Progress", "Review", "Complete"],
                "value": "Not Started",
            },
            "copyData": "Not Started",
        },
        "priority": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Low", "Medium", "High", "Urgent"],
                "value": "Medium",
            },
            "copyData": "Medium",
        },
        "tags": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "backend",
        },
        "tags_close": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
                "closeMenuOnSelect": True,
            },
            "copyData": "backend",
        },
        "categories": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["database"],
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "database",
        },
    },
    {
        "product": "Mobile App Release",
        "status": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Not Started", "In Progress", "Review", "Complete"],
                "value": "Complete",
            },
            "copyData": "Complete",
        },
        "priority": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Low", "Medium", "High", "Urgent"],
                "value": "High",
            },
            "copyData": "High",
        },
        "tags": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["frontend", "design", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "frontend,design,testing",
        },
        "tags_close": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["frontend", "design", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
                "closeMenuOnSelect": True,
            },
            "copyData": "frontend,design,testing",
        },
        "categories": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["ios", "android"],
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "ios,android",
        },
    },
    {
        "product": "Security Audit",
        "status": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Not Started", "In Progress", "Review", "Complete"],
                "value": "In Progress",
            },
            "copyData": "In Progress",
        },
        "priority": {
            "kind": "dropdown-cell",
            "data": {
                "allowedValues": ["Low", "Medium", "High", "Urgent"],
                "value": "Urgent",
            },
            "copyData": "Urgent",
        },
        "tags": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "backend,testing",
        },
        "tags_close": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["backend", "testing"],
                "options": TAG_OPTIONS,
                "allowDuplicates": False,
                "allowCreation": True,
                "closeMenuOnSelect": True,
            },
            "copyData": "backend,testing",
        },
        "categories": {
            "kind": "multi-select-cell",
            "data": {
                "values": ["security", "compliance"],
                "allowDuplicates": False,
                "allowCreation": True,
            },
            "copyData": "security,compliance",
        },
    },
]

app.layout = html.Div(
    [
        html.H1("Custom Cell Editors: Dropdown & MultiSelect"),
        html.Div(
            [
                html.H3("Features Demonstrated:"),
                html.Ul(
                    [
                        html.Li(
                            "Dropdown cells: Click to select from predefined options (Status, Priority columns)"
                        ),
                        html.Li(
                            "MultiSelect with options: Select multiple items with color-coded badges (Tags columns)"
                        ),
                        html.Li(
                            "MultiSelect without options: Create custom tags on-the-fly (Categories column)"
                        ),
                        html.Li(
                            "closeMenuOnSelect: 'Tags (stays open)' keeps dropdown open, 'Tags (closes)' closes after each selection"
                        ),
                        html.Li("All cells support copy/paste and editing"),
                    ]
                ),
            ],
            style={"marginBottom": "20px"},
        ),
        dgg.GlideGrid(
            id="custom-cells-grid",
            columns=COLUMNS,
            data=DATA,
            height=400,
            rowMarkers="number",
            enableCopyPaste=True,
            smoothScrollX=True,
            smoothScrollY=True,
        ),
        html.Div(
            [
                html.H3("Last Edited Cell:", style={"marginTop": "30px"}),
                html.Pre(
                    id="edit-output",
                    style={
                        "backgroundColor": "#f5f5f5",
                        "padding": "15px",
                        "borderRadius": "4px",
                        "fontFamily": "monospace",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.H3("Full Grid Data:", style={"marginTop": "30px"}),
                html.Details(
                    [
                        html.Summary("Click to expand/collapse data"),
                        html.Pre(
                            id="data-output",
                            style={
                                "backgroundColor": "#f5f5f5",
                                "padding": "15px",
                                "borderRadius": "4px",
                                "fontFamily": "monospace",
                                "maxHeight": "400px",
                                "overflow": "auto",
                            },
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)


@callback(Output("edit-output", "children"), Input("custom-cells-grid", "cellEdited"))
def display_edited_cell(cell_edited):
    if not cell_edited:
        return "No edits yet. Try clicking on a dropdown or multi-select cell!"

    return json.dumps(cell_edited, indent=2)


@callback(Output("data-output", "children"), Input("custom-cells-grid", "data"))
def display_full_data(data):
    if not data:
        return "No data"

    return json.dumps(data, indent=2)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
