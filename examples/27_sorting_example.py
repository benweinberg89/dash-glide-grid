"""
Example 27: Built-in Column Sorting
Demonstrates the built-in sortable feature with single and multi-column sorting
"""

import dash
from dash import html, callback, Input, Output, dcc
import dash_glide_grid as dgg
import json

app = dash.Dash(__name__)

# Column definitions
COLUMNS = [
    {"title": "Name", "width": 180, "id": "name"},
    {"title": "Department", "width": 130, "id": "department"},
    {"title": "Role", "width": 150, "id": "role"},
    {"title": "Salary", "width": 110, "id": "salary"},
    {"title": "Experience", "width": 100, "id": "experience"},
    {"title": "Rating", "width": 90, "id": "rating"},
]

# Sample data
DATA = [
    {"name": "Alice Johnson", "department": "Engineering", "role": "Senior Developer", "salary": 95000, "experience": 8, "rating": 4.8},
    {"name": "Bob Smith", "department": "Marketing", "role": "Marketing Manager", "salary": 82000, "experience": 6, "rating": 4.5},
    {"name": "Carol White", "department": "Engineering", "role": "Tech Lead", "salary": 115000, "experience": 10, "rating": 4.9},
    {"name": "David Brown", "department": "Sales", "role": "Sales Representative", "salary": 55000, "experience": 3, "rating": 4.2},
    {"name": "Emma Davis", "department": "Engineering", "role": "Junior Developer", "salary": 65000, "experience": 2, "rating": 4.0},
    {"name": "Frank Miller", "department": "HR", "role": "HR Specialist", "salary": 58000, "experience": 4, "rating": 4.3},
    {"name": "Grace Lee", "department": "Marketing", "role": "Content Writer", "salary": 52000, "experience": 2, "rating": 3.9},
    {"name": "Henry Wilson", "department": "Sales", "role": "Sales Manager", "salary": 78000, "experience": 7, "rating": 4.6},
    {"name": "Ivy Chen", "department": "Engineering", "role": "DevOps Engineer", "salary": 88000, "experience": 5, "rating": 4.7},
    {"name": "Jack Taylor", "department": "Finance", "role": "Financial Analyst", "salary": 72000, "experience": 4, "rating": 4.4},
    {"name": "Kate Anderson", "department": "Engineering", "role": "QA Engineer", "salary": 70000, "experience": 3, "rating": 4.1},
    {"name": "Liam Thomas", "department": "Marketing", "role": "SEO Specialist", "salary": 60000, "experience": 3, "rating": 4.2},
    {"name": "Mia Jackson", "department": "Sales", "role": "Account Executive", "salary": 68000, "experience": 4, "rating": 4.5},
    {"name": "Noah Garcia", "department": "HR", "role": "Recruiter", "salary": 55000, "experience": 2, "rating": 3.8},
    {"name": "Olivia Martinez", "department": "Finance", "role": "Accountant", "salary": 65000, "experience": 5, "rating": 4.3},
]

app.layout = html.Div(
    [
        html.H1("Built-in Sortable Data Grid"),
        html.P(
            "Click column headers to sort. Shift+click to add multi-column sorting."
        ),
        # Sort status display
        html.Div(
            [
                html.Span("Current Sort: ", style={"fontWeight": "bold"}),
                html.Span(id="sort-display", children="None"),
                html.Button(
                    "Clear Sort",
                    id="clear-sort-btn",
                    style={
                        "marginLeft": "20px",
                        "padding": "5px 12px",
                        "backgroundColor": "#6c757d",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                    },
                ),
            ],
            style={
                "marginBottom": "15px",
                "padding": "10px 15px",
                "backgroundColor": "#e9ecef",
                "borderRadius": "4px",
            },
        ),
        # Grid with built-in sorting enabled
        dgg.GlideGrid(
            id="sortable-grid",
            columns=COLUMNS,
            data=DATA,
            height=450,
            rowHeight=36,
            headerHeight=42,
            rowMarkers="number",
            smoothScrollY=True,
            # Enable built-in sorting!
            sortable=True,
            sortColumns=[],
        ),
        # Instructions
        html.Div(
            [
                html.H3("How Sorting Works:"),
                html.Ul(
                    [
                        html.Li(
                            "Click a column header to sort by that column (ascending)"
                        ),
                        html.Li("Click the same column again to toggle to descending"),
                        html.Li("Click a third time to clear the sort"),
                        html.Li(
                            [
                                html.Strong("Shift+click"),
                                " to add secondary sort columns",
                            ]
                        ),
                        html.Li(
                            "The ▲/▼ indicators show sort direction and priority (for multi-sort)"
                        ),
                    ]
                ),
                html.H3("Data Editing:"),
                html.P(
                    "You can edit cells even when sorted - edits are applied to the correct row in the underlying data."
                ),
            ],
            style={
                "marginTop": "20px",
                "padding": "15px",
                "backgroundColor": "#f8f9fa",
                "borderRadius": "4px",
            },
        ),
        # Debug output
        html.Div(
            [
                html.H4("sortColumns prop value:"),
                html.Pre(
                    id="sort-debug",
                    style={
                        "backgroundColor": "#f0f0f0",
                        "padding": "10px",
                        "borderRadius": "4px",
                    },
                ),
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("sort-display", "children"),
    Output("sort-debug", "children"),
    Input("sortable-grid", "sortColumns"),
)
def update_sort_display(sort_columns):
    """Display current sort state."""
    if not sort_columns:
        return "None", "[]"

    # Build display text
    parts = []
    for i, sc in enumerate(sort_columns):
        col_name = COLUMNS[sc["columnIndex"]]["title"]
        direction = "Asc" if sc["direction"] == "asc" else "Desc"
        parts.append(f"{col_name} ({direction})")

    display = " → ".join(parts)
    debug = json.dumps(sort_columns, indent=2)

    return display, debug


@callback(
    Output("sortable-grid", "sortColumns"),
    Input("clear-sort-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_sort(n_clicks):
    """Clear all sorting."""
    return []


if __name__ == "__main__":
    app.run(debug=True, port=8050)
