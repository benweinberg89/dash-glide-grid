"""
Dash Glide Grid - Comprehensive Usage Example

This example demonstrates many key features of the GlideGrid component:
- Records-based data format (compatible with df.to_dict('records'))
- All 13 cell types (text, number, boolean, markdown, image, uri, bubble, drilldown, rowid, protected, loading, dropdown, multi-select)
- Column sorting and filtering
- Row markers with checkboxes
- Fill handle for Excel-like data entry
- Undo/redo support
- Search functionality
- Event callbacks
"""

import dash
from dash import html, dcc, Input, Output, callback, ctx
import dash_glide_grid as dgg
import random
import time

app = dash.Dash(__name__)

# Status options for dropdown
status_options = [
    {"value": "active", "label": "Active", "color": "#10b981"},
    {"value": "pending", "label": "Pending", "color": "#f59e0b"},
    {"value": "inactive", "label": "Inactive", "color": "#ef4444"},
    {"value": "review", "label": "In Review", "color": "#8b5cf6"},
    {"value": "approved", "label": "Approved", "color": "#06b6d4"},
]

# Skills options for multi-select
skill_options = [
    {"value": "python", "label": "Python", "color": "#3776ab"},
    {"value": "javascript", "label": "JavaScript", "color": "#f7df1e"},
    {"value": "react", "label": "React", "color": "#61dafb"},
    {"value": "sql", "label": "SQL", "color": "#336791"},
    {"value": "rust", "label": "Rust", "color": "#dea584"},
    {"value": "go", "label": "Go", "color": "#00add8"},
    {"value": "typescript", "label": "TypeScript", "color": "#3178c6"},
    {"value": "docker", "label": "Docker", "color": "#2496ed"},
]

columns = [
    {"title": "ID", "id": "rowid", "width": 90},
    {"title": "Name", "id": "name", "width": 150, "sortable": True},
    {"title": "Avatar", "id": "image", "width": 70},
    {"title": "Salary", "id": "salary", "width": 100, "sortable": True},
    {"title": "Active", "id": "active", "width": 70},
    {"title": "Role", "id": "role", "width": 140, "sortable": True, "filterable": True, "hasMenu": True},
    {"title": "Profile", "id": "profile", "width": 90},
    {"title": "Tags", "id": "tags", "width": 160},
    {"title": "Team", "id": "team", "width": 180},
    {"title": "Status", "id": "status", "width": 120},
    {"title": "Skills", "id": "skills", "width": 200},
]

# Generate 1000 rows of realistic data
first_names = [
    "Alice", "Bob", "Carol", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack",
    "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter", "Quinn", "Rachel", "Sam", "Tina",
    "Uma", "Victor", "Wendy", "Xavier", "Yuki", "Zoe", "Aaron", "Bella", "Carlos", "Diana",
]
last_names = [
    "Johnson", "Smith", "White", "Brown", "Davis", "Miller", "Lee", "Wilson", "Chen", "Taylor",
    "Anderson", "Thomas", "Jackson", "Garcia", "Martinez", "Robinson", "Foster", "Kim", "Wright", "Lopez",
]
roles = [
    "**Lead** Engineer", "*Senior* Developer", "~~Junior~~ **Mid-level**", "`DevOps` Specialist",
    "**Staff** Engineer", "*Principal* Architect", "**Tech** Lead", "*Senior* Manager",
]
teams = [
    ["Engineering", "Backend"], ["Engineering", "Frontend"], ["Design", "UX"], ["Design", "Product"],
    ["Data Science", "ML"], ["Infrastructure", "DevOps"], ["Security", "Platform"], ["QA", "Automation"],
]
tag_sets = [
    ["backend", "api"], ["frontend", "ux"], ["data", "ml"], ["devops", "cloud"],
    ["mobile", "ios"], ["security", "auth"], ["testing", "qa"], ["platform", "infra"],
]
statuses = ["active", "pending", "inactive", "review", "approved"]
skill_sets = [
    ["python", "rust", "docker"], ["javascript", "react", "typescript"], ["python", "sql"],
    ["go", "docker", "rust"], ["python", "javascript", "sql"], ["react", "typescript", "docker"],
    ["go", "sql", "docker"], ["python", "react", "sql"],
]

random.seed(42)  # Reproducible data

data = []
for i in range(1000):
    first = random.choice(first_names)
    last = random.choice(last_names)
    name = f"{first} {last}"
    user_id = f"{first.lower()}{i}"
    status = random.choice(statuses)
    skills = random.choice(skill_sets)
    team_data = random.choice(teams)

    data.append({
        "image": {"kind": "image", "data": [f"https://i.pravatar.cc/40?u={user_id}"]},
        "name": name,
        "salary": random.randint(60, 200) * 1000,
        "active": random.choice([True, True, True, False]),
        "role": {"kind": "markdown", "data": random.choice(roles)},
        "profile": {"kind": "uri", "data": f"https://github.com/{user_id}", "displayData": "GitHub"},
        "tags": {"kind": "bubble", "data": random.choice(tag_sets)},
        "team": {
            "kind": "drilldown",
            "data": [{"text": t, "img": f"https://i.pravatar.cc/20?u={t.lower()}"} for t in team_data],
        },
        "rowid": {"kind": "rowid", "data": f"EMP-{i+1:04d}"},
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": status, "options": status_options, "allowedValues": [o["value"] for o in status_options]},
            "allowOverlay": True,
            "copyData": status,
        },
        "skills": {
            "kind": "multi-select-cell",
            "data": {"values": skills, "options": skill_options, "allowedValues": [o["value"] for o in skill_options], "allowDuplicates": False, "allowCreation": True},
            "allowOverlay": True,
            "copyData": ", ".join(skills),
        },
    })

# Styles
button_style = {
    "padding": "6px 12px",
    "marginRight": "8px",
    "border": "1px solid #e2e8f0",
    "borderRadius": "6px",
    "backgroundColor": "#f8fafc",
    "cursor": "pointer",
    "fontSize": "14px",
}
status_row_style = {
    "display": "flex",
    "gap": "8px",
    "marginBottom": "4px",
    "fontSize": "14px",
}
label_style = {"fontWeight": "600", "minWidth": "80px"}
value_style = {"color": "#64748b"}

app.layout = html.Div([
    html.H1("Dash Glide Grid", style={"color": "#1e293b", "marginBottom": "4px"}),
    html.P("A high-performance data grid for Dash applications", style={"color": "#64748b", "marginBottom": "24px"}),

    # Toolbar
    html.Div([
        html.Button("Undo", id="undo-btn", n_clicks=0, style=button_style),
        html.Button("Redo", id="redo-btn", n_clicks=0, style=button_style),
        html.Button("Clear Filters", id="clear-filters-btn", n_clicks=0, style=button_style),
        html.Button("Search", id="search-btn", n_clicks=0, style=button_style),
    ], style={"marginBottom": "16px"}),

    # Grid with rounded corners
    html.Div(
        dgg.GlideGrid(
            id="main-grid",
            columns=columns,
            data=data,
            height=500,
            rowHeight=40,
            headerHeight=44,
            rowMarkers="both",
            rowSelect="multi",
            columnSelect="none",
            rangeSelect="multi-rect",
            fillHandle=True,
            freezeColumns=2,
            sortable=True,
            sortColumns=[],
            columnFilters={},
            showSearch=False,
            hoverRow=True,
            smoothScrollX=True,
            smoothScrollY=True,
            enableUndoRedo=True,
            maxUndoSteps=50,
        ),
        style={"border": "1px solid #e2e8f0", "borderRadius": "8px", "overflow": "hidden"},
    ),

    # Status panel
    html.Div([
        html.Div([html.Span("Selection:", style=label_style), html.Span(id="selection-display", children="None", style=value_style)], style=status_row_style),
        html.Div([html.Span("Last Edit:", style=label_style), html.Span(id="edit-display", children="None", style=value_style)], style=status_row_style),
        html.Div([html.Span("Sort:", style=label_style), html.Span(id="sort-display", children="None", style=value_style)], style=status_row_style),
        html.Div([html.Span("Filters:", style=label_style), html.Span(id="filter-display", children="None", style=value_style)], style=status_row_style),
    ], style={
        "marginTop": "16px",
        "padding": "16px",
        "backgroundColor": "#f8fafc",
        "borderRadius": "8px",
        "border": "1px solid #e2e8f0",
    }),

], style={"maxWidth": "1400px", "margin": "40px auto", "padding": "0 20px", "fontFamily": "system-ui, -apple-system, sans-serif"})


@callback(
    Output("main-grid", "showSearch"),
    Input("search-btn", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_search(n_clicks):
    return (n_clicks or 0) % 2 == 1


@callback(
    Output("selection-display", "children"),
    Input("main-grid", "selectedCell"),
    Input("main-grid", "selectedRows"),
    Input("main-grid", "selectedRange"),
)
def update_selection(cell, rows, range_sel):
    parts = []
    if cell:
        parts.append(f"Cell({cell['row']}, {cell['col']})")
    if rows:
        parts.append(f"Rows{rows}")
    if range_sel:
        parts.append(f"Range({range_sel['startRow']}:{range_sel['endRow']}, {range_sel['startCol']}:{range_sel['endCol']})")
    return " | ".join(parts) if parts else "None"


@callback(
    Output("edit-display", "children"),
    Input("main-grid", "cellEdited"),
)
def update_edit(edit):
    if edit:
        return f"Row {edit['row']}, Col {edit['col']} = {edit['value']}"
    return "None"


@callback(
    Output("sort-display", "children"),
    Input("main-grid", "sortColumns"),
)
def update_sort(sort_cols):
    if sort_cols:
        parts = [f"{columns[s['columnIndex']]['id']} ({s['direction']})" for s in sort_cols]
        return ", ".join(parts)
    return "None"


@callback(
    Output("filter-display", "children"),
    Input("main-grid", "columnFilters"),
)
def update_filters(filters):
    if filters:
        parts = [f"{columns[int(k)]['id']}: {v}" for k, v in filters.items()]
        return " | ".join(parts)
    return "None"


@callback(
    Output("main-grid", "columnFilters"),
    Input("clear-filters-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_filters(_):
    return {}


@callback(
    Output("main-grid", "undoRedoAction"),
    Input("undo-btn", "n_clicks"),
    Input("redo-btn", "n_clicks"),
    prevent_initial_call=True,
)
def handle_undo_redo(_undo, _redo):
    triggered = ctx.triggered_id
    if triggered == "undo-btn":
        return {"action": "undo", "timestamp": int(time.time() * 1000)}
    elif triggered == "redo-btn":
        return {"action": "redo", "timestamp": int(time.time() * 1000)}
    return None


if __name__ == "__main__":
    app.run(debug=True)