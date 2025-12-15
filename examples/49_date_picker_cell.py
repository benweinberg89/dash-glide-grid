"""
Example: Date Picker Cell

Demonstrates the date picker cell type for displaying and editing dates.
Click on a date cell to open the native date picker.
Includes dark/light mode toggle to test theme compatibility.
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

# Sample data with dates
DATA = [
    {
        "task": "Project kickoff",
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-01-15",
            "displayDate": "Jan 15, 2024",
            "format": "date",
        },
        "status": "Completed",
    },
    {
        "task": "Design review",
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-02-01",
            "displayDate": "Feb 1, 2024",
            "format": "date",
        },
        "status": "Completed",
    },
    {
        "task": "Development sprint 1",
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-03-15",
            "displayDate": "Mar 15, 2024",
            "format": "date",
        },
        "status": "In Progress",
    },
    {
        "task": "Testing phase",
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-04-01",
            "displayDate": "Apr 1, 2024",
            "format": "date",
        },
        "status": "Pending",
    },
    {
        "task": "Launch",
        "due_date": {
            "kind": "date-picker-cell",
            "date": "2024-05-01",
            "displayDate": "May 1, 2024",
            "format": "date",
        },
        "status": "Pending",
    },
    {
        "task": "Post-launch review",
        "due_date": {
            "kind": "date-picker-cell",
            "date": None,
            "displayDate": "",
            "format": "date",
        },
        "status": "Not Scheduled",
    },
]

COLUMNS = [
    {"id": "task", "title": "Task", "width": 200},
    {"id": "due_date", "title": "Due Date", "width": 150},
    {"id": "status", "title": "Status", "width": 120},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            [
                html.H1("Date Picker Cell Example", id="title"),
                html.P(
                    "Click on a date cell to open the date picker.",
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
            height=320,
            theme=LIGHT_THEME,
            columnResize=True,
        ),
        html.Div(id="output", style={"marginTop": "20px"}),
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
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

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
        )
    else:
        return (
            LIGHT_THEME,
            {"padding": "20px", "fontFamily": "system-ui, sans-serif"},
            {"color": "#111827"},
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
        )


@callback(
    Output("output", "children"),
    Output("output", "style"),
    Input("grid", "data"),
    Input("grid", "theme"),
)
def show_data(grid_data, theme):
    if not grid_data:
        return "", {}

    is_dark = theme and theme.get("bgCell") == "#1f2937"
    text_color = "#f3f4f6" if is_dark else "#111827"

    lines = []
    for row in grid_data:
        date_info = row.get("due_date", {})
        display = date_info.get("displayDate") or date_info.get("date") or "Not set"
        lines.append(f"{row['task']}: {display} ({row['status']})")

    return html.Pre("\n".join(lines)), {"marginTop": "20px", "color": text_color}


if __name__ == "__main__":
    app.run(debug=True)
