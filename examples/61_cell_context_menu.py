"""
Example: Built-in Cell Context Menu - All Cell Types

Demonstrates the built-in cell context menu feature with ALL cell types:
- Built-in: text, number, boolean, markdown, uri, image, bubble, drilldown, loading, rowid, protected
- Custom: dropdown, multi-select, button, tags, user-profile, spinner, star, date-picker, range, links, sparkline, tree-view

Right-click on any cell to see the context menu with copy/paste, clear, and custom actions.
"""

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Theme configurations
DARK_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.2)",
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
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.1)",
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

# Skill options for multi-select
SKILL_OPTIONS = [
    {"value": "python", "label": "Python"},
    {"value": "javascript", "label": "JavaScript"},
    {"value": "rust", "label": "Rust"},
    {"value": "go", "label": "Go"},
    {"value": "sql", "label": "SQL"},
]

# Column definitions with ALL cell types
COLUMNS = [
    # ID
    {"id": "id", "title": "ID", "width": 50},
    # Built-in types
    {"id": "name", "title": "Name (text)", "width": 130},
    {"id": "age", "title": "Age (num)", "width": 70},
    {"id": "active", "title": "Active (bool)", "width": 90},
    {"id": "description", "title": "Desc (markdown)", "width": 140},
    {"id": "website", "title": "Site (uri)", "width": 100},
    {"id": "avatar", "title": "Avatar (image)", "width": 80},
    {"id": "skills_bubble", "title": "Skills (bubble)", "width": 120},
    {"id": "details", "title": "Info (drilldown)", "width": 110},
    {"id": "row_id", "title": "RowID", "width": 80},
    {"id": "secret", "title": "Secret (protected)", "width": 100},
    {"id": "pending_data", "title": "Pending (loading)", "width": 100},
    # Custom types
    {"id": "status", "title": "Status (dropdown)", "width": 110},
    {"id": "tags", "title": "Tags", "width": 160},
    {"id": "rating", "title": "Rating (stars)", "width": 100},
    {"id": "due_date", "title": "Due Date", "width": 110},
    {"id": "progress", "title": "Progress (range)", "width": 110},
    {"id": "assignee", "title": "Assignee (profile)", "width": 140},
    {"id": "multi_skills", "title": "Skills (multi)", "width": 140},
    {"id": "links", "title": "Links", "width": 130},
    {"id": "trend", "title": "Trend (sparkline)", "width": 110},
    {"id": "category", "title": "Category (tree)", "width": 120},
    {"id": "action", "title": "Action (button)", "width": 90},
    {"id": "loading_indicator", "title": "Loading (spinner)", "width": 100},
]

# Comprehensive data with ALL cell types
INITIAL_DATA = [
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
        "status": {"kind": "dropdown-cell", "data": {"value": "active", "allowedValues": STATUS_OPTIONS}},
        "tags": {"kind": "tags-cell", "tags": ["Feature", "Critical"], "possibleTags": TAG_DEFS},
        "rating": {"kind": "star-cell", "rating": 5, "maxStars": 5},
        "due_date": {"kind": "date-picker-cell", "date": "2024-03-15", "displayDate": "Mar 15, 2024"},
        "progress": {"kind": "range-cell", "value": 85, "min": 0, "max": 100, "label": "85%"},
        "assignee": {"kind": "user-profile-cell", "name": "Alice Johnson", "initial": "A", "tint": "#3b82f6"},
        "multi_skills": {"kind": "multi-select-cell", "data": {"values": ["python", "rust"], "options": SKILL_OPTIONS}},
        "links": {"kind": "links-cell", "links": [{"title": "Docs", "href": "https://docs.example.com"}, {"title": "API", "href": "https://api.example.com"}]},
        "trend": {"kind": "sparkline-cell", "values": [10, 25, 15, 40, 30], "yAxis": [0, 50], "graphKind": "line"},
        "category": {"kind": "tree-view-cell", "text": "Engineering", "depth": 0, "canOpen": True, "isOpen": False},
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
        "status": {"kind": "dropdown-cell", "data": {"value": "pending", "allowedValues": STATUS_OPTIONS}},
        "tags": {"kind": "tags-cell", "tags": ["Bug"], "possibleTags": TAG_DEFS},
        "rating": {"kind": "star-cell", "rating": 2, "maxStars": 5},
        "due_date": {"kind": "date-picker-cell", "date": "2024-01-10", "displayDate": "Jan 10, 2024"},
        "progress": {"kind": "range-cell", "value": 25, "min": 0, "max": 100, "label": "25%"},
        "assignee": {"kind": "user-profile-cell", "name": "Bob Smith", "initial": "B", "tint": "#10b981"},
        "multi_skills": {"kind": "multi-select-cell", "data": {"values": ["javascript"], "options": SKILL_OPTIONS}},
        "links": {"kind": "links-cell", "links": [{"title": "GitHub", "href": "https://github.com"}]},
        "trend": {"kind": "sparkline-cell", "values": [5, 8, 12, 9, 15], "yAxis": [0, 20], "graphKind": "area"},
        "category": {"kind": "tree-view-cell", "text": "Design", "depth": 0, "canOpen": False, "isOpen": False},
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
        "status": {"kind": "dropdown-cell", "data": {"value": "completed", "allowedValues": STATUS_OPTIONS}},
        "tags": {"kind": "tags-cell", "tags": ["Bug", "Feature", "Documentation"], "possibleTags": TAG_DEFS},
        "rating": {"kind": "star-cell", "rating": 4, "maxStars": 5},
        "due_date": {"kind": "date-picker-cell", "date": "2024-06-20", "displayDate": "Jun 20, 2024"},
        "progress": {"kind": "range-cell", "value": 100, "min": 0, "max": 100, "label": "100%"},
        "assignee": {"kind": "user-profile-cell", "name": "Carol Williams", "initial": "C", "tint": "#f59e0b"},
        "multi_skills": {"kind": "multi-select-cell", "data": {"values": ["python", "javascript", "sql"], "options": SKILL_OPTIONS}},
        "links": {"kind": "links-cell", "links": []},
        "trend": {"kind": "sparkline-cell", "values": [50, 45, 60, 55, 70], "yAxis": [0, 100], "graphKind": "bar"},
        "category": {"kind": "tree-view-cell", "text": "Backend", "depth": 1, "canOpen": True, "isOpen": True},
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
        "status": {"kind": "dropdown-cell", "data": {"value": "archived", "allowedValues": STATUS_OPTIONS}},
        "tags": {"kind": "tags-cell", "tags": ["Low"], "possibleTags": TAG_DEFS},
        "rating": {"kind": "star-cell", "rating": 3, "maxStars": 5},
        "due_date": {"kind": "date-picker-cell", "date": "2024-02-28", "displayDate": "Feb 28, 2024"},
        "progress": {"kind": "range-cell", "value": 50, "min": 0, "max": 100, "label": "50%"},
        "assignee": {"kind": "user-profile-cell", "name": "David Lee", "initial": "D", "tint": "#ec4899"},
        "multi_skills": {"kind": "multi-select-cell", "data": {"values": ["go", "rust"], "options": SKILL_OPTIONS}},
        "links": {"kind": "links-cell", "links": [{"title": "Portfolio", "href": "https://portfolio.dev"}, {"title": "Blog", "href": "https://blog.dev"}, {"title": "LinkedIn", "href": "https://linkedin.com"}]},
        "trend": {"kind": "sparkline-cell", "values": [20, 18, 22, 25, 20], "yAxis": [0, 30], "graphKind": "line"},
        "category": {"kind": "tree-view-cell", "text": "Frontend", "depth": 1, "canOpen": False, "isOpen": False},
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
        "status": {"kind": "dropdown-cell", "data": {"value": "active", "allowedValues": STATUS_OPTIONS}},
        "tags": {"kind": "tags-cell", "tags": ["Feature"], "possibleTags": TAG_DEFS},
        "rating": {"kind": "star-cell", "rating": 1, "maxStars": 5},
        "due_date": {"kind": "date-picker-cell", "date": "2024-12-01", "displayDate": "Dec 1, 2024"},
        "progress": {"kind": "range-cell", "value": 10, "min": 0, "max": 100, "label": "10%"},
        "assignee": {"kind": "user-profile-cell", "name": "Eve Martinez", "initial": "E", "tint": "#6366f1"},
        "multi_skills": {"kind": "multi-select-cell", "data": {"values": ["sql"], "options": SKILL_OPTIONS}},
        "links": {"kind": "links-cell", "links": [{"title": "Twitter", "href": "https://twitter.com"}]},
        "trend": {"kind": "sparkline-cell", "values": [2, 5, 3, 8, 6], "yAxis": [0, 10], "graphKind": "area"},
        "category": {"kind": "tree-view-cell", "text": "Analytics", "depth": 0, "canOpen": True, "isOpen": False},
        "action": {"kind": "button-cell", "title": "Edit"},
        "loading_indicator": {"kind": "spinner-cell"},
    },
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Cell Context Menu - All Cell Types", id="title"),
        html.P(
            "Right-click on any cell to see the context menu. Demonstrates all cell types.",
            id="subtitle",
        ),
        html.Div(
            [
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
                html.Label(" Scroll Behavior: ", style={"marginLeft": "20px"}),
                dcc.Dropdown(
                    id="scroll-behavior-dropdown",
                    options=[
                        {"label": "default", "value": "default"},
                        {"label": "close-overlay-on-scroll", "value": "close-overlay-on-scroll"},
                        {"label": "lock-scroll", "value": "lock-scroll"},
                    ],
                    value="default",
                    clearable=False,
                    style={"width": "220px", "display": "inline-block", "verticalAlign": "middle"},
                ),
                html.Label(" Menu Max Height: ", style={"marginLeft": "20px"}),
                dcc.Dropdown(
                    id="max-height-dropdown",
                    options=[
                        {"label": "No limit", "value": "none"},
                        {"label": "100px", "value": "100px"},
                        {"label": "150px", "value": "150px"},
                        {"label": "200px", "value": "200px"},
                        {"label": "300px", "value": "300px"},
                    ],
                    value="none",
                    clearable=False,
                    style={"width": "120px", "display": "inline-block", "verticalAlign": "middle"},
                ),
            ],
            style={"display": "flex", "alignItems": "center", "marginBottom": "15px"},
        ),
        html.Div(
            [
                dgg.GlideGrid(
                    id="context-menu-grid",
                    columns=COLUMNS,
                    data=INITIAL_DATA,
                    height=350,
                    rowHeight=34,
                    headerHeight=40,
                    rowMarkers="number",
                    rangeSelect="rect",
                    theme=LIGHT_THEME,
                    contextMenuConfig={
                        "items": [
                            # Built-in copy actions using 'action' property
                            # Using monochrome Unicode symbols
                            {
                                "id": "copy",
                                "label": "Copy Cell",
                                "icon": "⧉",
                                "action": "copyClickedCell",
                            },
                            {
                                "id": "copy-selection",
                                "label": "Copy Selection",
                                "icon": "⧉",
                                "action": "copySelection",
                            },
                            {
                                "id": "paste-cell",
                                "label": "Paste at Cell",
                                "icon": "⎘",
                                "iconSize": "19px",
                                "action": "pasteAtClickedCell",
                            },
                            {
                                "id": "paste-selection",
                                "label": "Paste at Selection",
                                "icon": "⎘",
                                "iconSize": "19px",
                                "action": "pasteAtSelection",
                                "dividerAfter": True,
                            },
                            # Built-in clear actions
                            {
                                "id": "clear",
                                "label": "Clear Cell",
                                "icon": "⌀",
                                "action": "clearClickedCell",
                            },
                            {
                                "id": "uppercase",
                                "label": "Uppercase",
                                "icon": "Aa",
                                "iconSize": "11px",
                                "action": {"function": "uppercaseCell(col, row, columnId, cellData, utils)"},
                            },
                            {
                                "id": "paste-upper",
                                "label": "Paste Uppercase",
                                "icon": "⎘",
                                "iconSize": "19px",
                                "action": {"function": "pasteUppercase(col, row, utils)"},
                                "dividerAfter": True,
                            },
                            # Selection-based clientside actions
                            {
                                "id": "uppercase-sel",
                                "label": "Uppercase Selection",
                                "icon": "AA",
                                "iconSize": "10px",
                                "action": {"function": "uppercaseSelection(selection, columns, data, utils)"},
                            },
                            {
                                "id": "lowercase-sel",
                                "label": "Lowercase Selection",
                                "icon": "aa",
                                "iconSize": "10px",
                                "action": {"function": "lowercaseSelection(selection, columns, data, utils)"},
                            },
                            {
                                "id": "clear-sel",
                                "label": "Clear Selection",
                                "icon": "⌀",
                                "action": "clearSelection",
                                "dividerAfter": True,
                            },
                            # Custom actions handled by Python callback
                            {
                                "id": "delete",
                                "label": "Delete Row",
                                "icon": "✕",
                                "iconWeight": "800",
                                "color": "#dc2626",  # red label
                                # "fontWeight": "600",  # semi-bold label
                                "iconColor": "#dc2626",  # red icon
                            },
                            {
                                "id": "details",
                                "label": "View Details",
                                "color": "#4762BC",  # blue label
                                "icon": "\u24d8",
                                "iconSize": "11px",
                                "iconWeight": "800",
                                "iconColor": "#4762BC",  # blue icon
                            },
                        ]
                    },
                ),
            ],
            style={"margin": "20px 0"},
        ),
        # Action feedback area
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Last Action:", id="action-label"),
                        html.Div(
                            id="action-output",
                            style={
                                "fontFamily": "monospace",
                                "padding": "15px",
                                "backgroundColor": "#e8f4e8",
                                "borderRadius": "5px",
                                "minHeight": "40px",
                                "whiteSpace": "pre-wrap",
                            },
                        ),
                    ],
                    style={"flex": "1", "marginRight": "10px"},
                ),
                html.Div(
                    [
                        html.H4("cellsEdited (for server sync):"),
                        html.Div(
                            id="cells-edited-output",
                            children="No edits yet",
                            style={
                                "fontFamily": "monospace",
                                "padding": "15px",
                                "backgroundColor": "#e8e8f4",
                                "borderRadius": "5px",
                                "minHeight": "40px",
                                "whiteSpace": "pre-wrap",
                                "fontSize": "12px",
                            },
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={"display": "flex", "margin": "20px 0"},
        ),
        # Details modal
        html.Div(id="details-modal", style={"display": "none"}),
        html.Div(
            id="info-box",
            children=[
                html.H4("Context Menu Items:"),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Strong("Copy Cell"),
                                " - Copies the clicked cell value (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Copy Selection"),
                                " - Copies all cells in the current range selection as TSV (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Paste at Cell"),
                                " - Pastes clipboard content at the right-clicked cell (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Paste at Selection"),
                                " - Pastes clipboard content at top-left of selection (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Clear Cell"),
                                " - Clears the cell value (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Uppercase"),
                                " - Converts cell text to uppercase (clientside function)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Paste Uppercase"),
                                " - Pastes clipboard as uppercase (async clientside function)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Uppercase/Lowercase Selection"),
                                " - Operates on all text cells in selection (clientside)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Clear Selection"),
                                " - Clears all cells in selection (native action)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Delete Row"),
                                " - Removes the row from the grid (Python callback)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("View Details"),
                                " - Shows detailed information about the row (Python callback)",
                            ]
                        ),
                    ]
                ),
                html.P(
                    [
                        "Actions can be: (1) built-in strings like 'copyClickedCell', ",
                        "(2) clientside functions via {\"function\": \"myFunc(...)\"}, or ",
                        "(3) Python callbacks for complex logic.",
                    ],
                    style={"fontStyle": "italic", "marginTop": "10px"},
                ),
            ],
            style={
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#f5f5f5",
                "borderRadius": "6px",
            },
        ),
        # Store for theme state
        dcc.Store(id="theme-store", data="light"),
    ],
    style={
        "padding": "20px",
        "fontFamily": "system-ui, sans-serif",
    },
)


@callback(
    Output("context-menu-grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Output("action-output", "style"),
    Output("action-label", "style"),
    Output("info-box", "style"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

    btn_style_light = {
        "marginBottom": "15px",
        "padding": "8px 16px",
        "cursor": "pointer",
        "borderRadius": "6px",
        "border": "1px solid #d1d5db",
        "backgroundColor": "#f3f4f6",
        "color": "#111827",
    }
    btn_style_dark = {
        "marginBottom": "15px",
        "padding": "8px 16px",
        "cursor": "pointer",
        "borderRadius": "6px",
        "border": "1px solid #4b5563",
        "backgroundColor": "#374151",
        "color": "#f3f4f6",
    }

    if is_dark:
        return (
            DARK_THEME,
            {
                "padding": "20px",
                "fontFamily": "system-ui, sans-serif",
                "backgroundColor": "#111827",
                "minHeight": "100vh",
            },
            {"color": "#f3f4f6"},
            {"color": "#9ca3af"},
            btn_style_dark,
            "Toggle Light Mode",
            {
                "fontFamily": "monospace",
                "padding": "15px",
                "backgroundColor": "#374151",
                "borderRadius": "5px",
                "minHeight": "40px",
                "whiteSpace": "pre-wrap",
                "color": "#f3f4f6",
            },
            {"color": "#f3f4f6"},
            {
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#374151",
                "borderRadius": "6px",
                "color": "#f3f4f6",
            },
        )
    else:
        return (
            LIGHT_THEME,
            {
                "padding": "20px",
                "fontFamily": "system-ui, sans-serif",
            },
            {"color": "#111827"},
            {"color": "#6b7280"},
            btn_style_light,
            "Toggle Dark Mode",
            {
                "fontFamily": "monospace",
                "padding": "15px",
                "backgroundColor": "#e8f4e8",
                "borderRadius": "5px",
                "minHeight": "40px",
                "whiteSpace": "pre-wrap",
            },
            {"color": "#111827"},
            {
                "margin": "20px 0",
                "padding": "20px",
                "backgroundColor": "#f5f5f5",
                "borderRadius": "6px",
            },
        )


@callback(
    Output("context-menu-grid", "data"),
    Output("action-output", "children"),
    Output("details-modal", "children"),
    Output("details-modal", "style"),
    Input("context-menu-grid", "contextMenuItemClicked"),
    State("context-menu-grid", "data"),
    prevent_initial_call=True,
)
def handle_context_menu(item, current_data):
    """Handle context menu actions."""
    if not item:
        return no_update, no_update, no_update, no_update

    col = item.get("col", 0)
    row = item.get("row", 0)
    item_id = item.get("itemId", "")

    # Get column info
    col_id = COLUMNS[col]["id"] if col < len(COLUMNS) else None

    # Get row data
    row_data = current_data[row] if row < len(current_data) else {}
    cell_value = row_data.get(col_id, "") if col_id else ""

    # Default outputs (no change)
    new_data = no_update
    action_msg = no_update
    modal_content = no_update
    modal_style = {"display": "none"}

    # Native actions just show a message - the actual copy/paste is handled by the component
    if item_id == "copy":
        action_msg = f"Copied cell value: {cell_value}"

    elif item_id == "copy-selection":
        action_msg = "Copied selection to clipboard"

    elif item_id == "paste":
        action_msg = "Pasted from clipboard"

    # Clientside function actions - just show a message (action already executed in browser)
    elif item_id == "clear":
        action_msg = f"Cleared cell at row {row + 1}, column '{col_id}'"

    elif item_id == "uppercase":
        action_msg = f"Uppercased cell at row {row + 1}, column '{col_id}'"

    elif item_id == "paste-upper":
        action_msg = f"Pasted uppercase at row {row + 1}, column '{col_id}'"

    # Selection-based clientside actions
    elif item_id == "uppercase-sel":
        action_msg = "Uppercased all text cells in selection"

    elif item_id == "lowercase-sel":
        action_msg = "Lowercased all text cells in selection"

    elif item_id == "clear-sel":
        action_msg = "Cleared all cells in selection"

    elif item_id == "delete":
        # Delete action - remove the row
        if row < len(current_data):
            new_data = [r for i, r in enumerate(current_data) if i != row]
            deleted_product = row_data.get("product", f"Row {row + 1}")
            action_msg = f"Deleted: {deleted_product}"

    elif item_id == "details":
        # Details action - show modal with row info
        action_msg = f"Viewing details for Row {row + 1}"
        modal_content = html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            f"Row Details: {row_data.get('product', 'Unknown')}",
                            style={"marginTop": 0},
                        ),
                        html.Table(
                            [
                                html.Tbody(
                                    [
                                        html.Tr(
                                            [
                                                html.Td(
                                                    html.Strong(
                                                        f"{COLUMNS[i]['title']}:"
                                                    ),
                                                    style={
                                                        "padding": "8px",
                                                        "textAlign": "right",
                                                    },
                                                ),
                                                html.Td(
                                                    str(
                                                        row_data.get(
                                                            COLUMNS[i]["id"], "N/A"
                                                        )
                                                    ),
                                                    style={"padding": "8px"},
                                                ),
                                            ]
                                        )
                                        for i in range(len(COLUMNS))
                                    ]
                                )
                            ],
                            style={"width": "100%"},
                        ),
                        html.Button(
                            "Close",
                            id="close-modal",
                            n_clicks=0,
                            style={"marginTop": "15px", "padding": "8px 20px"},
                        ),
                    ],
                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0 4px 20px rgba(0,0,0,0.3)",
                        "maxWidth": "400px",
                        "margin": "auto",
                    },
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "backgroundColor": "rgba(0,0,0,0.5)",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "zIndex": 1000,
            },
        )
        modal_style = {"display": "block"}

    return new_data, action_msg, modal_content, modal_style


# Close modal callback
@callback(
    Output("details-modal", "style", allow_duplicate=True),
    Input("close-modal", "n_clicks"),
    prevent_initial_call=True,
)
def close_modal(n_clicks):
    if n_clicks:
        return {"display": "none"}
    return no_update


@callback(
    Output("context-menu-grid", "contextMenuScrollBehavior"),
    Input("scroll-behavior-dropdown", "value"),
)
def update_scroll_behavior(value):
    return value


@callback(
    Output("context-menu-grid", "contextMenuConfig"),
    Input("max-height-dropdown", "value"),
    State("context-menu-grid", "contextMenuConfig"),
)
def update_max_height(value, current_config):
    if not current_config:
        return no_update
    new_config = {**current_config}
    if value == "none":
        new_config.pop("maxHeight", None)
    else:
        new_config["maxHeight"] = value
    return new_config


@callback(
    Output("cells-edited-output", "children"),
    Input("context-menu-grid", "cellsEdited"),
    prevent_initial_call=True,
)
def show_cells_edited(edited):
    """Display cellsEdited prop - this is what you'd use to sync to a database."""
    if not edited:
        return "No edits"

    edits = edited.get("edits", [])
    count = edited.get("count", 0)

    # Format the edits for display
    lines = [f"Received {count} edit(s):"]
    for edit in edits[:5]:  # Show max 5 edits
        col = edit.get("col", "?")
        row = edit.get("row", "?")
        value = edit.get("value", "")
        # Truncate long values
        val_str = str(value)[:20] + "..." if len(str(value)) > 20 else str(value)
        lines.append(f"  [{row}, {col}] = '{val_str}'")

    if count > 5:
        lines.append(f"  ... and {count - 5} more")

    return "\n".join(lines)


if __name__ == "__main__":
    app.run(debug=True, port=8061)
