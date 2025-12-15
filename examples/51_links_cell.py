"""
Example 51: Links Cell

This example demonstrates the links cell type which displays multiple hyperlinks:
- Multiple clickable links in a single cell
- Links open in new tabs by default
- Callback fires when a link is clicked
- Supports dark/light mode themes

Links cell data structure:
{
    "kind": "links-cell",
    "links": [
        {"title": "Display Text", "href": "https://example.com"},
        {"title": "Another Link", "href": "https://another.com"}
    ],
    "maxLinks": 3,        # Optional: limit displayed links
    "navigateOn": "click" # "click" opens link, "control-click" requires Ctrl/Cmd
}
"""

import dash
from dash import html, callback, Input, Output
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__)

# Theme configurations
DARK_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.2)",
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
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.1)",
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

# Sample data with links cells
DATA = [
    {
        "project": "React",
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": "https://github.com/facebook/react"},
                {"title": "Docs", "href": "https://react.dev"},
                {"title": "NPM", "href": "https://www.npmjs.com/package/react"},
            ]
        },
        "description": "A JavaScript library for building user interfaces",
    },
    {
        "project": "Vue",
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": "https://github.com/vuejs/vue"},
                {"title": "Docs", "href": "https://vuejs.org"},
            ]
        },
        "description": "Progressive JavaScript framework",
    },
    {
        "project": "Angular",
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": "https://github.com/angular/angular"},
                {"title": "Docs", "href": "https://angular.io"},
                {"title": "CLI", "href": "https://cli.angular.io"},
            ]
        },
        "description": "Platform for building mobile and desktop apps",
    },
    {
        "project": "Svelte",
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": "https://github.com/sveltejs/svelte"},
                {"title": "Docs", "href": "https://svelte.dev"},
            ]
        },
        "description": "Cybernetically enhanced web apps",
    },
    {
        "project": "Dash",
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": "https://github.com/plotly/dash"},
                {"title": "Docs", "href": "https://dash.plotly.com"},
                {"title": "Gallery", "href": "https://dash.gallery"},
            ]
        },
        "description": "Python framework for building analytical web apps",
    },
]

COLUMNS = [
    {"title": "Project", "id": "project", "width": 120},
    {"title": "Links", "id": "links", "width": 200},
    {"title": "Description", "id": "description", "width": 350},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Links Cell Example", id="title"),
        html.P("Click on any link to open it in a new tab. The callback below shows which link was clicked.", id="subtitle"),
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
        GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=300,
            width="100%",
            theme=LIGHT_THEME,
        ),
        html.Div(
            id="click-output",
            style={
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#f3f4f6",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
            },
            children="Click a link to see callback data here..."
        ),
    ],
    style={"padding": "20px", "maxWidth": "900px", "fontFamily": "system-ui, sans-serif"},
)


@callback(
    Output("grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Output("click-output", "style"),
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
                "maxWidth": "900px",
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
            {
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#374151",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
                "color": "#f3f4f6",
            },
        )
    else:
        return (
            LIGHT_THEME,
            {
                "padding": "20px",
                "maxWidth": "900px",
                "fontFamily": "system-ui, sans-serif",
            },
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
            {
                "marginTop": "15px",
                "padding": "12px",
                "backgroundColor": "#f3f4f6",
                "borderRadius": "6px",
                "fontFamily": "monospace",
                "fontSize": "14px",
                "color": "#111827",
            },
        )


@callback(
    Output("click-output", "children"),
    Input("grid", "linkClicked"),
    prevent_initial_call=True,
)
def handle_link_click(link_info):
    if link_info:
        return f"Link clicked: {link_info}"
    return "Click a link to see callback data here..."


if __name__ == "__main__":
    app.run(debug=True, port=8051)
