"""
Example: Star Cell

Demonstrates the star cell type for displaying and editing star ratings (1-5).
Click on a star cell to open the editor and select a rating.
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

# Sample data with star ratings
DATA = [
    {
        "product": "Wireless Headphones",
        "rating": {
            "kind": "star-cell",
            "rating": 5,
            "maxStars": 5,
        },
        "reviews": 1234,
    },
    {
        "product": "USB-C Hub",
        "rating": {
            "kind": "star-cell",
            "rating": 4,
            "maxStars": 5,
        },
        "reviews": 567,
    },
    {
        "product": "Mechanical Keyboard",
        "rating": {
            "kind": "star-cell",
            "rating": 5,
            "maxStars": 5,
        },
        "reviews": 892,
    },
    {
        "product": "Monitor Stand",
        "rating": {
            "kind": "star-cell",
            "rating": 3,
            "maxStars": 5,
        },
        "reviews": 234,
    },
    {
        "product": "Webcam",
        "rating": {
            "kind": "star-cell",
            "rating": 2,
            "maxStars": 5,
        },
        "reviews": 156,
    },
    {
        "product": "Mouse Pad",
        "rating": {
            "kind": "star-cell",
            "rating": 4,
            "maxStars": 5,
        },
        "reviews": 789,
    },
]

COLUMNS = [
    {"id": "product", "title": "Product", "width": 200},
    {"id": "rating", "title": "Rating", "width": 120},
    {"id": "reviews", "title": "Reviews", "width": 100},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.Div(
            [
                html.H1("Star Cell Example", id="title"),
                html.P(
                    "Click on a star cell to open the rating editor.",
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
        rating = row.get("rating", {}).get("rating", 0)
        stars = "*" * rating + "-" * (5 - rating)
        lines.append(f"{row['product']}: [{stars}] ({rating}/5)")

    return html.Pre("\n".join(lines)), {"marginTop": "20px", "color": text_color}


if __name__ == "__main__":
    app.run(debug=True)
