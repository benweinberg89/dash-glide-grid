"""
Example: User Profile Cell

Demonstrates the user profile cell type for displaying user avatars with names.
Shows circular avatar with initials or images, plus the user's name.
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

# Sample data with user profiles
DATA = [
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Alice Johnson",
            "initial": "A",
            "tint": "#3b82f6",
        },
        "role": "Engineering Manager",
        "department": "Engineering",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Bob Smith",
            "initial": "B",
            "tint": "#22c55e",
        },
        "role": "Senior Developer",
        "department": "Engineering",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Carol Williams",
            "initial": "C",
            "tint": "#f59e0b",
        },
        "role": "Product Designer",
        "department": "Design",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "David Brown",
            "initial": "D",
            "tint": "#ef4444",
        },
        "role": "DevOps Engineer",
        "department": "Infrastructure",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Emma Davis",
            "initial": "E",
            "tint": "#8b5cf6",
        },
        "role": "Data Scientist",
        "department": "Analytics",
    },
]

COLUMNS = [
    {"id": "user", "title": "Team Member", "width": 200},
    {"id": "role", "title": "Role", "width": 180},
    {"id": "department", "title": "Department", "width": 120},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("User Profile Cell Example", id="title"),
        html.P(
            "User profile cells display an avatar circle with initials and the user's name.",
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
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=280,
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


if __name__ == "__main__":
    app.run(debug=True)
