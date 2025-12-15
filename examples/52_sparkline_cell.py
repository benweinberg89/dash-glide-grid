"""
Example 52: Sparkline Cell

This example demonstrates the sparkline cell type which renders mini charts:
- Line charts: Connected data points
- Area charts: Filled region under the line with gradient
- Bar charts: Individual bars for each value
- Hover shows a vertical line and value (requires displayValues)
- Supports dark/light mode themes

Sparkline cell data structure:
{
    "kind": "sparkline-cell",
    "values": [10, 25, 15, 30, 22],  # Data points
    "graphKind": "line",             # "line" | "bar" | "area"
    "yAxis": [0, 100],               # [min, max] for normalization
    "color": "#3b82f6",              # Optional: custom chart color
    "displayValues": ["10", "25"],   # Optional: hover labels (enables hover)
    "hoverStyle": "line",            # "line" (default) or "dot" (dot + tooltip)
    "hideAxis": False                # Optional: hide zero line
}
"""

import dash
from dash import html, callback, Input, Output
from dash_glide_grid import GlideGrid
import random

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


def generate_trend_data(base, volatility=10, length=12):
    """Generate random trend data with values and display strings"""
    values = [base]
    for _ in range(length - 1):
        change = random.uniform(-volatility, volatility)
        values.append(max(0, min(100, values[-1] + change)))
    values = [round(v, 1) for v in values]
    display_values = [str(int(v)) for v in values]
    return values, display_values


# Generate data with displayValues for hover support
rev_line, rev_line_disp = generate_trend_data(50, 8)
rev_area, rev_area_disp = generate_trend_data(50, 8)
rev_bar, _ = generate_trend_data(50, 15)

user_line, user_line_disp = generate_trend_data(30, 10)
user_area, user_area_disp = generate_trend_data(30, 10)
user_bar, _ = generate_trend_data(30, 12)

err_line, err_line_disp = generate_trend_data(15, 5)
err_area, err_area_disp = generate_trend_data(15, 5)
err_bar, _ = generate_trend_data(15, 8)

lat_line, lat_line_disp = generate_trend_data(45, 12)
lat_area, lat_area_disp = generate_trend_data(45, 12)
lat_bar, _ = generate_trend_data(45, 15)

cpu_line, cpu_line_disp = generate_trend_data(60, 15)
cpu_area, cpu_area_disp = generate_trend_data(60, 15)
cpu_bar, _ = generate_trend_data(60, 20)

# Sample data with different sparkline types
DATA = [
    {
        "metric": "Revenue",
        "line_trend": {
            "kind": "sparkline-cell",
            "values": rev_line,
            "displayValues": rev_line_disp,
            "graphKind": "line",
            "yAxis": [0, 100],
            "color": "#10b981",  # Green
        },
        "area_trend": {
            "kind": "sparkline-cell",
            "values": rev_area,
            "displayValues": rev_area_disp,
            "graphKind": "area",
            "yAxis": [0, 100],
            "color": "#10b981",
        },
        "bar_trend": {
            "kind": "sparkline-cell",
            "values": rev_bar,
            "displayValues": [str(int(v)) for v in rev_bar],
            "graphKind": "bar",
            "yAxis": [0, 100],
            "color": "#10b981",
        },
    },
    {
        "metric": "Users",
        "line_trend": {
            "kind": "sparkline-cell",
            "values": user_line,
            "displayValues": user_line_disp,
            "graphKind": "line",
            "yAxis": [0, 100],
            "color": "#3b82f6",  # Blue
        },
        "area_trend": {
            "kind": "sparkline-cell",
            "values": user_area,
            "displayValues": user_area_disp,
            "graphKind": "area",
            "yAxis": [0, 100],
            "color": "#3b82f6",
        },
        "bar_trend": {
            "kind": "sparkline-cell",
            "values": user_bar,
            "displayValues": [str(int(v)) for v in user_bar],
            "graphKind": "bar",
            "yAxis": [0, 100],
            "color": "#3b82f6",
            "hoverStyle": "dot",  # Use dot + tooltip style
        },
    },
    {
        "metric": "Errors",
        "line_trend": {
            "kind": "sparkline-cell",
            "values": err_line,
            "displayValues": err_line_disp,
            "graphKind": "line",
            "yAxis": [0, 50],
            "color": "#ef4444",  # Red
        },
        "area_trend": {
            "kind": "sparkline-cell",
            "values": err_area,
            "displayValues": err_area_disp,
            "graphKind": "area",
            "yAxis": [0, 50],
            "color": "#ef4444",
        },
        "bar_trend": {
            "kind": "sparkline-cell",
            "values": err_bar,
            "displayValues": [str(int(v)) for v in err_bar],
            "graphKind": "bar",
            "yAxis": [0, 50],
            "color": "#ef4444",
        },
    },
    {
        "metric": "Latency (ms)",
        "line_trend": {
            "kind": "sparkline-cell",
            "values": lat_line,
            "displayValues": [f"{v}ms" for v in lat_line_disp],
            "graphKind": "line",
            "yAxis": [0, 100],
            "color": "#f59e0b",  # Amber
        },
        "area_trend": {
            "kind": "sparkline-cell",
            "values": lat_area,
            "displayValues": [f"{v}ms" for v in lat_area_disp],
            "graphKind": "area",
            "yAxis": [0, 100],
            "color": "#f59e0b",
        },
        "bar_trend": {
            "kind": "sparkline-cell",
            "values": lat_bar,
            "displayValues": [f"{int(v)}ms" for v in lat_bar],
            "graphKind": "bar",
            "yAxis": [0, 100],
            "color": "#f59e0b",
        },
    },
    {
        "metric": "CPU Usage",
        "line_trend": {
            "kind": "sparkline-cell",
            "values": cpu_line,
            "displayValues": [f"{v}%" for v in cpu_line_disp],
            "graphKind": "line",
            "yAxis": [0, 100],
            "color": "#8b5cf6",  # Purple
            "hoverStyle": "dot",  # Use dot + tooltip style
        },
        "area_trend": {
            "kind": "sparkline-cell",
            "values": cpu_area,
            "displayValues": [f"{v}%" for v in cpu_area_disp],
            "graphKind": "area",
            "yAxis": [0, 100],
            "color": "#8b5cf6",
            "hoverStyle": "dot",  # Use dot + tooltip style
        },
        "bar_trend": {
            "kind": "sparkline-cell",
            "values": cpu_bar,
            "displayValues": [f"{int(v)}%" for v in cpu_bar],
            "graphKind": "bar",
            "yAxis": [0, 100],
            "color": "#8b5cf6",
            "hoverStyle": "dot",  # Use dot + tooltip style
        },
    },
]

COLUMNS = [
    {"title": "Metric", "id": "metric", "width": 120},
    {"title": "Line Chart", "id": "line_trend", "width": 150},
    {"title": "Area Chart", "id": "area_trend", "width": 150},
    {"title": "Bar Chart", "id": "bar_trend", "width": 150},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Sparkline Cell Example", id="title"),
        html.P("Hover over line/area charts to see data point values.", id="subtitle"),
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
            rowHeight=50,  # Taller rows for better chart visibility
        ),
    ],
    style={"padding": "20px", "maxWidth": "700px", "fontFamily": "system-ui, sans-serif"},
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
                "maxWidth": "700px",
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
            {
                "padding": "20px",
                "maxWidth": "700px",
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
        )


if __name__ == "__main__":
    app.run(debug=True, port=8052)
