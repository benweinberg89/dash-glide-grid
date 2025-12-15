"""
Example: All Cell Types - Sorting & Filtering Test

Comprehensive test of sorting and filtering for ALL cell types:

Built-in types:
- text, number, boolean, markdown, uri, image, bubble, drilldown, loading, rowid, protected

Custom types:
- dropdown, multi-select, button, tags, user-profile, spinner,
  star, date-picker, range, links, sparkline, tree-view

Click column headers to sort. Use the column menu (▼ on right side of header) to filter.
"""

from dash import Dash, html, callback, Input, Output
import dash_glide_grid as dgg

app = Dash(__name__)

# Theme configurations
DARK_THEME = {
    "accentColor": "#8b5cf6",
    "accentLight": "rgba(139, 92, 246, 0.2)",
    "bgCell": "#1f2937",
    "bgCellMedium": "#374151",
    "bgHeader": "#111827",
    "bgHeaderHasFocus": "#374151",
    "bgHeaderHovered": "#374151",
    "bgBubble": "#4b5563",
    "textDark": "#f3f4f6",
    "textMedium": "#9ca3af",
    "textLight": "#6b7280",
    "textHeader": "#f3f4f6",
    "textBubble": "#f3f4f6",
    "borderColor": "rgba(255, 255, 255, 0.1)",
    "horizontalBorderColor": "rgba(255, 255, 255, 0.1)",
}

LIGHT_THEME = {
    "accentColor": "#8b5cf6",
    "accentLight": "rgba(139, 92, 246, 0.1)",
    "bgCell": "#ffffff",
    "bgCellMedium": "#f9fafb",
    "bgHeader": "#f3f4f6",
    "bgHeaderHasFocus": "#e5e7eb",
    "bgHeaderHovered": "#e5e7eb",
    "bgBubble": "#e5e7eb",
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "textLight": "#9ca3af",
    "textHeader": "#111827",
    "textBubble": "#374151",
    "borderColor": "#e5e7eb",
    "horizontalBorderColor": "#e5e7eb",
}

# Status options for dropdowns
STATUS_OPTIONS = ["active", "pending", "completed", "archived"]

# Tag definitions
TAG_DEFS = [
    {"tag": "Bug", "color": "#ef4444"},
    {"tag": "Feature", "color": "#8b5cf6"},
    {"tag": "Critical", "color": "#f97316"},
    {"tag": "Low", "color": "#22c55e"},
    {"tag": "Documentation", "color": "#3b82f6"},
]

# Skill options
SKILL_OPTIONS = [
    {"value": "python", "label": "Python"},
    {"value": "javascript", "label": "JavaScript"},
    {"value": "rust", "label": "Rust"},
    {"value": "go", "label": "Go"},
    {"value": "sql", "label": "SQL"},
]

# Comprehensive data - varied values for interesting sorting/filtering
DATA = [
    {
        "id": 1,
        # Built-in types
        "name": "Alice Johnson",
        "age": 32,
        "active": True,
        "description": {"kind": "markdown", "data": "**Senior** developer"},
        "website": {"kind": "uri", "data": "https://alice.dev", "displayData": "alice.dev"},
        "avatar": {"kind": "image", "data": ["https://i.pravatar.cc/40?u=alice"]},
        "skills_bubble": {"kind": "bubble", "data": ["Python", "Rust"]},
        "details": {"kind": "drilldown", "data": [{"text": "Engineering"}]},
        "row_id": {"kind": "rowid", "data": "ROW-001"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        # Custom types
        "status": {
            "kind": "dropdown-cell",
            "value": "active",
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Feature", "Critical"],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": 5, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-03-15",
            "displayDate": "Mar 15, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": 85,
            "min": 0,
            "max": 100,
            "label": "85%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": "Alice Johnson",
            "initial": "A",
            "tint": "#3b82f6",
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": ["python", "rust"],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "Docs", "href": "https://docs.example.com"},
                {"title": "API", "href": "https://api.example.com"},
            ],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [10, 25, 15, 40, 30],
            "yAxis": [0, 50],
            "graphKind": "line",
        },
        "category": {
            "kind": "tree-view-cell",
            "text": "Engineering",
            "depth": 0,
            "canOpen": True,
            "isOpen": False,
        },
        "action": {"kind": "button-cell", "title": "Edit"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "age": 28,
        "active": False,
        "description": {"kind": "markdown", "data": "*Junior* developer"},
        "website": {"kind": "uri", "data": "https://bobsmith.io", "displayData": "bobsmith.io"},
        "avatar": {"kind": "image", "data": ["https://i.pravatar.cc/40?u=bob"]},
        "skills_bubble": {"kind": "bubble", "data": ["JavaScript"]},
        "details": {"kind": "drilldown", "data": [{"text": "Design"}]},
        "row_id": {"kind": "rowid", "data": "ROW-002"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        "status": {
            "kind": "dropdown-cell",
            "value": "pending",
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Bug"],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": 2, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-01-10",
            "displayDate": "Jan 10, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": 25,
            "min": 0,
            "max": 100,
            "label": "25%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": "Bob Smith",
            "initial": "B",
            "tint": "#10b981",
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": ["javascript"],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [{"title": "GitHub", "href": "https://github.com"}],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [5, 8, 12, 9, 15],
            "yAxis": [0, 20],
            "graphKind": "area",
        },
        "category": {
            "kind": "tree-view-cell",
            "text": "Design",
            "depth": 0,
            "canOpen": False,
            "isOpen": False,
        },
        "action": {"kind": "button-cell", "title": "View"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
    {
        "id": 3,
        "name": "Carol Williams",
        "age": 45,
        "active": True,
        "description": {"kind": "markdown", "data": "# Lead\n\nTeam lead"},
        "website": {"kind": "uri", "data": "https://carol.tech", "displayData": "carol.tech"},
        "avatar": {"kind": "image", "data": ["https://i.pravatar.cc/40?u=carol"]},
        "skills_bubble": {"kind": "bubble", "data": ["Python", "JS", "SQL"]},
        "details": {"kind": "drilldown", "data": [{"text": "Backend"}, {"text": "API"}]},
        "row_id": {"kind": "rowid", "data": "ROW-003"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        "status": {
            "kind": "dropdown-cell",
            "value": "completed",
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Bug", "Feature", "Documentation"],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": 4, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-06-20",
            "displayDate": "Jun 20, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": 100,
            "min": 0,
            "max": 100,
            "label": "100%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": "Carol Williams",
            "initial": "C",
            "tint": "#f59e0b",
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": ["python", "javascript", "sql"],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [50, 45, 60, 55, 70],
            "yAxis": [0, 100],
            "graphKind": "bar",
        },
        "category": {
            "kind": "tree-view-cell",
            "text": "Backend",
            "depth": 1,
            "canOpen": True,
            "isOpen": True,
        },
        "action": {"kind": "button-cell", "title": "Delete"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
    {
        "id": 4,
        "name": "David Lee",
        "age": 38,
        "active": True,
        "description": {"kind": "markdown", "data": "DevOps engineer\n- CI/CD\n- K8s"},
        "website": {"kind": "uri", "data": "https://davidlee.com", "displayData": "davidlee.com"},
        "avatar": {"kind": "image", "data": ["https://i.pravatar.cc/40?u=david"]},
        "skills_bubble": {"kind": "bubble", "data": ["Go", "Rust"]},
        "details": {"kind": "drilldown", "data": [{"text": "Frontend"}]},
        "row_id": {"kind": "rowid", "data": "ROW-004"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        "status": {
            "kind": "dropdown-cell",
            "value": "archived",
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Low"],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": 3, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-02-28",
            "displayDate": "Feb 28, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": 50,
            "min": 0,
            "max": 100,
            "label": "50%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": "David Lee",
            "initial": "D",
            "tint": "#ec4899",
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": ["go", "rust"],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "Portfolio", "href": "https://portfolio.dev"},
                {"title": "Blog", "href": "https://blog.dev"},
                {"title": "LinkedIn", "href": "https://linkedin.com"},
            ],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [20, 18, 22, 25, 20],
            "yAxis": [0, 30],
            "graphKind": "line",
        },
        "category": {
            "kind": "tree-view-cell",
            "text": "Frontend",
            "depth": 1,
            "canOpen": False,
            "isOpen": False,
        },
        "action": {"kind": "button-cell", "title": "Archive"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
    {
        "id": 5,
        "name": "Eve Martinez",
        "age": 29,
        "active": False,
        "description": {"kind": "markdown", "data": "Data analyst"},
        "website": {"kind": "uri", "data": "https://eve.codes", "displayData": "eve.codes"},
        "avatar": {"kind": "image", "data": ["https://i.pravatar.cc/40?u=eve"]},
        "skills_bubble": {"kind": "bubble", "data": ["SQL"]},
        "details": {"kind": "drilldown", "data": [{"text": "Analytics"}]},
        "row_id": {"kind": "rowid", "data": "ROW-005"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        "status": {
            "kind": "dropdown-cell",
            "value": "active",
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Feature"],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": 1, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-12-01",
            "displayDate": "Dec 1, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": 10,
            "min": 0,
            "max": 100,
            "label": "10%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": "Eve Martinez",
            "initial": "E",
            "tint": "#6366f1",
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": ["sql"],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [{"title": "Twitter", "href": "https://twitter.com"}],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [2, 5, 3, 8, 6],
            "yAxis": [0, 10],
            "graphKind": "area",
        },
        "category": {
            "kind": "tree-view-cell",
            "text": "Analytics",
            "depth": 0,
            "canOpen": True,
            "isOpen": False,
        },
        "action": {"kind": "button-cell", "title": "Edit"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
]

# Column definitions - all marked as filterable
COLUMNS = [
    # ID
    {"id": "id", "title": "ID", "width": 50, "filterable": True},
    # Built-in types
    {"id": "name", "title": "Name (text)", "width": 130, "filterable": True},
    {"id": "age", "title": "Age (num)", "width": 70, "filterable": True},
    {"id": "active", "title": "Active (bool)", "width": 90, "filterable": True},
    {"id": "description", "title": "Desc (markdown)", "width": 140, "filterable": True},
    {"id": "website", "title": "Site (uri)", "width": 100, "filterable": True},
    {"id": "avatar", "title": "Avatar (image)", "width": 80, "filterable": True},
    {"id": "skills_bubble", "title": "Skills (bubble)", "width": 120, "filterable": True},
    {"id": "details", "title": "Info (drilldown)", "width": 110, "filterable": True},
    {"id": "row_id", "title": "RowID", "width": 80, "filterable": True},
    {"id": "secret", "title": "Secret (protected)", "width": 100, "filterable": True},
    {"id": "pending_data", "title": "Pending (loading)", "width": 100, "filterable": True},
    # Custom types
    {"id": "status", "title": "Status (dropdown)", "width": 110, "filterable": True},
    {"id": "tags", "title": "Tags", "width": 160, "filterable": True},
    {"id": "rating", "title": "Rating (stars)", "width": 100, "filterable": True},
    {"id": "due_date", "title": "Due Date", "width": 110, "filterable": True},
    {"id": "progress", "title": "Progress (range)", "width": 110, "filterable": True},
    {"id": "assignee", "title": "Assignee (profile)", "width": 140, "filterable": True},
    {"id": "multi_skills", "title": "Skills (multi)", "width": 140, "filterable": True},
    {"id": "links", "title": "Links", "width": 130, "filterable": True},
    {"id": "trend", "title": "Trend (sparkline)", "width": 110, "filterable": True},
    {"id": "category", "title": "Category (tree)", "width": 120, "filterable": True},
    {"id": "action", "title": "Action (button)", "width": 90, "filterable": True},
    {"id": "loading_indicator", "title": "Loading (spinner)", "width": 100, "filterable": True},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            [
                html.H1("All Cell Types - Sorting & Filtering Test", id="title"),
                html.P(
                    "Click column headers to sort. Click the menu icon (▼) to filter.",
                    id="subtitle",
                ),
                html.Button(
                    "Toggle Dark Mode",
                    id="theme-toggle",
                    style={
                        "marginBottom": "15px",
                        "padding": "8px 16px",
                        "cursor": "pointer",
                        "borderRadius": "6px",
                        "border": "1px solid #d1d5db",
                        "backgroundColor": "#f3f4f6",
                    },
                ),
            ]
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=400,
            theme=LIGHT_THEME,
            sortable=True,
            columnResize=True,
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Sort/Filter State:", id="state-title"),
                html.Pre(id="state-output"),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            [
                html.H3("Expected Sort Orders (ascending):", id="expected-title"),
                html.Ul(
                    [
                        html.Li("Name: Alice, Bob, Carol, David, Eve"),
                        html.Li("Age: 28, 29, 32, 38, 45"),
                        html.Li("Active: false (2), true (3)"),
                        html.Li("Status: active, active, archived, completed, pending"),
                        html.Li("Rating (stars): 1, 2, 3, 4, 5"),
                        html.Li("Due Date: Jan, Feb, Mar, Jun, Dec"),
                        html.Li("Progress: 10%, 25%, 50%, 85%, 100%"),
                        html.Li("Trend (sparkline by avg): 4.8, 9.8, 21, 24, 56"),
                        html.Li("Button/Spinner: Should NOT sort (unsortable)"),
                    ],
                    id="expected-list",
                ),
            ],
            style={"marginTop": "20px"},
        ),
    ],
    style={"padding": "20px", "fontFamily": "system-ui, sans-serif"},
)


@callback(
    Output("grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Output("state-title", "style"),
    Output("expected-title", "style"),
    Output("expected-list", "style"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1
    text_style = {"color": "#f3f4f6" if is_dark else "#111827"}

    if is_dark:
        return (
            DARK_THEME,
            {
                "padding": "20px",
                "fontFamily": "system-ui, sans-serif",
                "backgroundColor": "#111827",
                "minHeight": "100vh",
            },
            text_style,
            {"color": "#9ca3af"},
            {
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #4b5563",
                "backgroundColor": "#374151",
                "color": "#f3f4f6",
            },
            "Toggle Light Mode",
            text_style,
            text_style,
            text_style,
        )
    else:
        return (
            LIGHT_THEME,
            {"padding": "20px", "fontFamily": "system-ui, sans-serif"},
            text_style,
            {"color": "#6b7280"},
            {
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
                "color": "#111827",
            },
            "Toggle Dark Mode",
            text_style,
            text_style,
            text_style,
        )


@callback(
    Output("state-output", "children"),
    Output("state-output", "style"),
    Input("grid", "sortColumns"),
    Input("grid", "columnFilters"),
    Input("grid", "theme"),
)
def show_state(sort_columns, column_filters, theme):
    is_dark = theme and theme.get("bgCell") == "#1f2937"
    text_color = "#f3f4f6" if is_dark else "#111827"

    import json

    state = {
        "sortColumns": sort_columns or [],
        "columnFilters": column_filters or {},
    }
    return json.dumps(state, indent=2), {"color": text_color}


if __name__ == "__main__":
    app.run(debug=True, port=8054)
