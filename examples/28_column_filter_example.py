"""
Example 28: Column Filter Menu
Demonstrates the built-in column filter feature with unique value checkboxes
"""

import dash
from dash import html, callback, Input, Output, State
import dash_glide_grid as dgg
import json

app = dash.Dash(__name__)

# Light theme (default)
LIGHT_THEME = {
    "bgHeader": "#f7f7f8",
    "bgHeaderHovered": "#efeff1",
    "bgHeaderHasFocus": "#e8e8eb",
    "bgCell": "#ffffff",
    "textDark": "#313139",
    "textHeader": "#313139",
    "accentColor": "#4F5DFF",
    "borderColor": "#e1e1e1",
}

# Dark theme
DARK_THEME = {
    "bgHeader": "#1e1e2e",
    "bgHeaderHovered": "#2a2a3e",
    "bgHeaderHasFocus": "#3a3a4e",
    "bgCell": "#181825",
    "textDark": "#cdd6f4",
    "textHeader": "#cdd6f4",
    "accentColor": "#89b4fa",
    "borderColor": "#45475a",
}

# Column definitions - filterable columns show a dropdown menu
COLUMNS = [
    {"title": "Name", "width": 180, "id": "name"},
    {"title": "Department", "width": 130, "id": "department", "filterable": True},
    {"title": "Role", "width": 150, "id": "role", "filterable": True},
    {"title": "Salary", "width": 110, "id": "salary"},
    {"title": "Experience", "width": 100, "id": "experience"},
    {"title": "Status", "width": 100, "id": "status", "filterable": True},
]

# Sample data with repeated values for filtering
DATA = [
    {"name": "Alice Johnson", "department": "Engineering", "role": "Senior Developer", "salary": 95000, "experience": 8, "status": "Active"},
    {"name": "Bob Smith", "department": "Marketing", "role": "Marketing Manager", "salary": 82000, "experience": 6, "status": "Active"},
    {"name": "Carol White", "department": "Engineering", "role": "Tech Lead", "salary": 115000, "experience": 10, "status": "Active"},
    {"name": "David Brown", "department": "Sales", "role": "Sales Representative", "salary": 55000, "experience": 3, "status": "On Leave"},
    {"name": "Emma Davis", "department": "Engineering", "role": "Junior Developer", "salary": 65000, "experience": 2, "status": "Active"},
    {"name": "Frank Miller", "department": "HR", "role": "HR Specialist", "salary": 58000, "experience": 4, "status": "Active"},
    {"name": "Grace Lee", "department": "Marketing", "role": "Content Writer", "salary": 52000, "experience": 2, "status": "Inactive"},
    {"name": "Henry Wilson", "department": "Sales", "role": "Sales Manager", "salary": 78000, "experience": 7, "status": "Active"},
    {"name": "Ivy Chen", "department": "Engineering", "role": "DevOps Engineer", "salary": 88000, "experience": 5, "status": "Active"},
    {"name": "Jack Taylor", "department": "Finance", "role": "Financial Analyst", "salary": 72000, "experience": 4, "status": "On Leave"},
    {"name": "Kate Anderson", "department": "Engineering", "role": "QA Engineer", "salary": 70000, "experience": 3, "status": "Active"},
    {"name": "Liam Thomas", "department": "Marketing", "role": "SEO Specialist", "salary": 60000, "experience": 3, "status": "Active"},
    {"name": "Mia Jackson", "department": "Sales", "role": "Account Executive", "salary": 68000, "experience": 4, "status": "Inactive"},
    {"name": "Noah Garcia", "department": "HR", "role": "Recruiter", "salary": 55000, "experience": 2, "status": "Active"},
    {"name": "Olivia Martinez", "department": "Finance", "role": "Accountant", "salary": 65000, "experience": 5, "status": "Active"},
    {"name": "Peter Robinson", "department": "Engineering", "role": "Senior Developer", "salary": 92000, "experience": 7, "status": "Active"},
    {"name": "Quinn Foster", "department": "Marketing", "role": "Marketing Manager", "salary": 85000, "experience": 8, "status": "On Leave"},
    {"name": "Rachel Kim", "department": "Sales", "role": "Sales Representative", "salary": 58000, "experience": 2, "status": "Active"},
    {"name": "Sam Wright", "department": "HR", "role": "HR Manager", "salary": 75000, "experience": 9, "status": "Active"},
    {"name": "Tina Lopez", "department": "Finance", "role": "Senior Accountant", "salary": 78000, "experience": 6, "status": "Inactive"},
]

app.layout = html.Div(
    [
        html.H1("Column Filter Menu"),
        html.P(
            "Click the dropdown arrow (▼) on filterable columns to open the filter menu. "
            "Select/deselect values to filter rows."
        ),
        html.P(
            [html.Strong("Filterable columns: "), "Department, Role, Status"],
            style={"marginBottom": "15px", "color": "#555"},
        ),
        # Dark mode toggle and anchor toggle
        html.Div(
            [
                html.Button(
                    "Toggle Dark Mode",
                    id="dark-mode-btn",
                    style={
                        "padding": "8px 16px",
                        "backgroundColor": "#333",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                        "marginRight": "15px",
                    },
                ),
                html.Span(id="theme-status", children="Light Mode"),
                html.Button(
                    "Toggle Menu Anchor",
                    id="anchor-toggle-btn",
                    style={
                        "padding": "8px 16px",
                        "backgroundColor": "#0066cc",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "4px",
                        "cursor": "pointer",
                        "marginLeft": "15px",
                        "marginRight": "15px",
                    },
                ),
                html.Span(id="anchor-status", children="Menu anchored to header"),
            ],
            style={"marginBottom": "15px"},
        ),
        # Filter status display
        html.Div(
            [
                html.Span("Active Filters: ", style={"fontWeight": "bold"}),
                html.Span(id="filter-display", children="None"),
                html.Button(
                    "Clear All Filters",
                    id="clear-filters-btn",
                    style={
                        "marginLeft": "20px",
                        "padding": "5px 12px",
                        "backgroundColor": "#dc3545",
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
        # Visible row count
        html.Div(
            [
                html.Span("Showing ", style={"fontWeight": "bold"}),
                html.Span(id="row-count", children=str(len(DATA))),
                html.Span(f" of {len(DATA)} rows"),
            ],
            style={
                "marginBottom": "15px",
                "padding": "8px 15px",
                "backgroundColor": "#d4edda",
                "borderRadius": "4px",
            },
        ),
        # Grid with filterable columns
        dgg.GlideGrid(
            id="filterable-grid",
            columns=COLUMNS,
            data=DATA,
            height=450,
            rowHeight=36,
            headerHeight=42,
            rowMarkers="number",
            smoothScrollY=True,
            # Enable sorting too (filters + sorting work together)
            sortable=True,
            sortColumns=[],
            # Column filters (starts empty)
            columnFilters={},
            headerMenuConfig={"menuIcon": "hamburger"},
            # Theme (controlled by dark mode toggle)
            theme=LIGHT_THEME,
        ),
        # Instructions
        html.Div(
            [
                html.H3("How Column Filtering Works:"),
                html.Ul(
                    [
                        html.Li(
                            "Columns with filterable=True show a dropdown arrow (▼) in the header"
                        ),
                        html.Li("Click the dropdown to open the filter menu"),
                        html.Li("Use the search box to find specific values"),
                        html.Li("Check/uncheck values to include/exclude them"),
                        html.Li(
                            "Use 'Select All' to quickly select or deselect all values"
                        ),
                        html.Li(
                            "When a filter is active, the column header text turns blue"
                        ),
                        html.Li(
                            "Filtering works together with sorting - filter first, then sort"
                        ),
                        html.Li(
                            "By default, the menu stays anchored to the header when scrolling the page"
                        ),
                        html.Li(
                            "Set anchorToHeader=False in headerMenuConfig to keep menu fixed to viewport"
                        ),
                    ]
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
                html.H4("columnFilters prop value:"),
                html.Pre(
                    id="filter-debug",
                    style={
                        "backgroundColor": "#f0f0f0",
                        "padding": "10px",
                        "borderRadius": "4px",
                        "maxHeight": "150px",
                        "overflow": "auto",
                    },
                ),
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)


@callback(
    Output("filter-display", "children"),
    Output("filter-debug", "children"),
    Output("row-count", "children"),
    Input("filterable-grid", "columnFilters"),
    Input("filterable-grid", "visibleRowIndices"),
)
def update_filter_display(column_filters, visible_indices):
    """Display current filter state."""
    if not column_filters:
        return "None", "{}", str(len(DATA))

    # Build display text
    parts = []
    for col_idx_str, values in column_filters.items():
        col_idx = int(col_idx_str)
        col_name = COLUMNS[col_idx]["title"]
        if len(values) <= 2:
            val_str = ", ".join(str(v) for v in values)
        else:
            val_str = f"{len(values)} values"
        parts.append(f"{col_name}: [{val_str}]")

    display = " | ".join(parts) if parts else "None"
    debug = json.dumps(column_filters, indent=2)

    # Calculate visible row count (use 'is not None' since empty list [] is valid)
    row_count = len(visible_indices) if visible_indices is not None else len(DATA)

    return display, debug, str(row_count)


@callback(
    Output("filterable-grid", "columnFilters"),
    Input("clear-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_filters(n_clicks):
    """Clear all column filters."""
    return {}


@callback(
    Output("filterable-grid", "theme"),
    Output("theme-status", "children"),
    Input("dark-mode-btn", "n_clicks"),
    State("filterable-grid", "theme"),
    prevent_initial_call=True,
)
def toggle_dark_mode(n_clicks, current_theme):
    """Toggle between light and dark mode."""
    # Check if currently in dark mode by comparing bgCell
    is_dark = current_theme and current_theme.get("bgCell") == DARK_THEME["bgCell"]

    if is_dark:
        return LIGHT_THEME, "Light Mode"
    else:
        return DARK_THEME, "Dark Mode"


@callback(
    Output("filterable-grid", "headerMenuConfig"),
    Output("anchor-status", "children"),
    Input("anchor-toggle-btn", "n_clicks"),
    State("filterable-grid", "headerMenuConfig"),
    prevent_initial_call=True,
)
def toggle_anchor_mode(n_clicks, current_config):
    """Toggle between anchored (follows header on scroll) and fixed (stays in viewport) menu."""
    current_config = current_config or {}
    is_anchored = current_config.get("anchorToHeader", True)

    if is_anchored:
        return {**current_config, "anchorToHeader": False}, "Menu fixed to viewport"
    else:
        return {**current_config, "anchorToHeader": True}, "Menu anchored to header"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
