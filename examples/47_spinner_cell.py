"""
Example: Spinner Cell

Demonstrates the spinner cell type for showing loading states.
Useful for indicating async operations or pending data.
Includes dark/light mode toggle to test theme compatibility.
"""

from dash import Dash, html, callback, Input, Output, State
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
    "textDark": "#f3f4f6",
    "textMedium": "#9ca3af",
    "textLight": "#6b7280",
    "textHeader": "#f3f4f6",
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
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "textLight": "#9ca3af",
    "textHeader": "#111827",
    "borderColor": "#e5e7eb",
    "horizontalBorderColor": "#e5e7eb",
}

# Sample data with some spinners indicating loading state
INITIAL_DATA = [
    {
        "task": "Fetch user data",
        "status": {"kind": "spinner-cell"},
        "result": "Loading...",
    },
    {
        "task": "Process images",
        "status": {"kind": "spinner-cell"},
        "result": "Loading...",
    },
    {
        "task": "Generate report",
        "status": "Queued",
        "result": "Waiting",
    },
    {
        "task": "Send notifications",
        "status": "Queued",
        "result": "Waiting",
    },
]

COLUMNS = [
    {"id": "task", "title": "Task", "width": 180},
    {"id": "status", "title": "Status", "width": 100},
    {"id": "result", "title": "Result", "width": 150},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Spinner Cell Example", id="title"),
        html.P(
            "Spinner cells show an animated loading indicator. Click buttons to interact.",
            id="subtitle",
        ),
        html.Div(
            [
                html.Button(
                    "Complete First Task",
                    id="complete-btn",
                    style={
                        "marginRight": "10px",
                        "padding": "8px 16px",
                        "cursor": "pointer",
                        "borderRadius": "6px",
                        "border": "1px solid #d1d5db",
                        "backgroundColor": "#f3f4f6",
                    },
                ),
                html.Button(
                    "Toggle Dark Mode",
                    id="theme-toggle",
                    style={
                        "padding": "8px 16px",
                        "cursor": "pointer",
                        "borderRadius": "6px",
                        "border": "1px solid #d1d5db",
                        "backgroundColor": "#f3f4f6",
                    },
                ),
            ],
            style={"marginBottom": "15px"},
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=220,
            theme=LIGHT_THEME,
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
    Output("complete-btn", "style"),
    Output("theme-toggle", "children"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

    button_style_light = {
        "padding": "8px 16px",
        "cursor": "pointer",
        "borderRadius": "6px",
        "border": "1px solid #d1d5db",
        "backgroundColor": "#f3f4f6",
        "color": "#111827",
    }
    button_style_dark = {
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
            button_style_dark,
            {**button_style_dark, "marginRight": "10px"},
            "Toggle Light Mode",
        )
    else:
        return (
            LIGHT_THEME,
            {"padding": "20px", "fontFamily": "system-ui, sans-serif"},
            {"color": "#111827"},
            {"color": "#6b7280"},
            button_style_light,
            {**button_style_light, "marginRight": "10px"},
            "Toggle Dark Mode",
        )


@callback(
    Output("grid", "data"),
    Input("complete-btn", "n_clicks"),
    State("grid", "data"),
    prevent_initial_call=True,
)
def complete_task(n_clicks, data):
    """Simulate completing a task by replacing spinner with text."""
    if not data:
        return data

    # Find the first row with a spinner and complete it
    for row in data:
        if isinstance(row.get("status"), dict) and row["status"].get("kind") == "spinner-cell":
            row["status"] = "Complete ✓"
            row["result"] = "Success"
            break

    return data


if __name__ == "__main__":
    app.run(debug=True)
