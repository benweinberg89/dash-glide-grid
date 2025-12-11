"""
Example 40: Redraw Trigger with Pulsing Animation

Demonstrates the redrawTrigger prop for forcing grid redraws.
This example shows pulsing highlight regions that animate smoothly
by updating the highlight opacity on each interval tick.

Features:
- Pulsing highlight regions with animated opacity
- Configurable animation speed
- Multiple animation patterns

Run with: python examples/40_redraw_trigger.py
"""

import math
from dash import Dash, html, callback, Input, Output, dcc
from dash_glide_grid import GlideGrid

app = Dash(__name__, assets_folder="assets")

# Sample data
columns = [
    {"title": "Server", "width": 150, "id": "server"},
    {"title": "Status", "width": 100, "id": "status"},
    {"title": "CPU %", "width": 80, "id": "cpu"},
    {"title": "Memory %", "width": 80, "id": "memory"},
    {"title": "Alerts", "width": 100, "id": "alerts"},
]

data = [
    {"server": "prod-web-01", "status": "Online", "cpu": 45, "memory": 62, "alerts": "None"},
    {"server": "prod-web-02", "status": "Online", "cpu": 78, "memory": 85, "alerts": "High Memory"},
    {"server": "prod-db-01", "status": "Online", "cpu": 32, "memory": 71, "alerts": "None"},
    {"server": "prod-api-01", "status": "Warning", "cpu": 92, "memory": 45, "alerts": "High CPU"},
    {"server": "prod-cache-01", "status": "Online", "cpu": 15, "memory": 28, "alerts": "None"},
    {"server": "prod-worker-01", "status": "Critical", "cpu": 98, "memory": 95, "alerts": "Critical"},
    {"server": "prod-worker-02", "status": "Online", "cpu": 55, "memory": 48, "alerts": "None"},
    {"server": "staging-01", "status": "Offline", "cpu": 0, "memory": 0, "alerts": "Offline"},
]

app.layout = html.Div(
    [
        html.H1("Pulsing Highlight Animation"),
        html.P([
            "This example uses ",
            html.Code("redrawTrigger"),
            " combined with dynamically updated ",
            html.Code("highlightRegions"),
            " to create pulsing animations that draw attention to important cells."
        ]),

        html.Div(
            [
                html.Label("Animation Speed: ", style={"marginRight": "10px", "fontWeight": "bold"}),
                dcc.Slider(
                    id="speed-slider",
                    min=25,
                    max=250,
                    step=25,
                    value=100,
                    marks={25: "Fast", 125: "Medium", 250: "Slow"},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={"width": "400px", "marginBottom": "20px"},
        ),

        html.Div([
            html.Span("Legend: ", style={"fontWeight": "bold", "marginRight": "15px"}),
            html.Span("🔴 ", style={"fontSize": "16px"}),
            html.Span("Critical (pulsing red)", style={"marginRight": "20px"}),
            html.Span("🟡 ", style={"fontSize": "16px"}),
            html.Span("Warning (pulsing yellow)", style={"marginRight": "20px"}),
            html.Span("⚫ ", style={"fontSize": "16px"}),
            html.Span("Offline (pulsing gray)"),
        ], style={"marginBottom": "15px"}),

        # Interval component to trigger animation updates
        dcc.Interval(id="animation-interval", interval=100, n_intervals=0),

        GlideGrid(
            id="animated-grid",
            columns=columns,
            data=data,
            height=350,
            rowMarkers="number",
            highlightRegions=[],  # Will be updated by callback
            redrawTrigger=0,
        ),

        html.Hr(),

        html.H2("How It Works"),
        html.Div([
            html.P([
                "The animation works by updating both ",
                html.Code("highlightRegions"),
                " (with varying opacity) and ",
                html.Code("redrawTrigger"),
                " on each interval tick:"
            ]),
            html.Pre("""@callback(
    Output("animated-grid", "highlightRegions"),
    Output("animated-grid", "redrawTrigger"),
    Input("animation-interval", "n_intervals"),
)
def animate_highlights(n):
    # Calculate pulsing opacity using sine wave
    pulse = (math.sin(n * 0.15) + 1) / 2  # 0.0 to 1.0
    opacity = 0.1 + pulse * 0.4  # Range: 0.1 to 0.5

    highlights = [
        {
            "color": f"rgba(239, 68, 68, {opacity})",  # Red
            "range": {"x": 0, "y": row, "width": 5, "height": 1},
            "style": "solid-outline"
        }
        for row in critical_rows
    ]

    return highlights, n""",
                     style={"backgroundColor": "#f5f5f5", "padding": "15px", "borderRadius": "4px", "overflow": "auto"}),
        ], style={"marginTop": "20px"}),

        html.Hr(),

        html.H2("Use Cases"),
        html.Ul([
            html.Li("Alert indicators for monitoring dashboards"),
            html.Li("Drawing attention to cells that need user action"),
            html.Li("Live status indicators"),
            html.Li("Notification highlights that fade in/out"),
            html.Li("Selection animations"),
        ]),
    ],
    style={"padding": "20px", "maxWidth": "900px", "margin": "0 auto"},
)


@callback(
    Output("animation-interval", "interval"),
    Input("speed-slider", "value"),
)
def update_interval(speed):
    return speed


@callback(
    Output("animated-grid", "highlightRegions"),
    Output("animated-grid", "redrawTrigger"),
    Input("animation-interval", "n_intervals"),
)
def animate_highlights(n):
    # Calculate pulsing opacity using sine wave (smooth oscillation)
    pulse = (math.sin(n * 0.15) + 1) / 2  # Oscillates between 0.0 and 1.0

    highlights = []

    # Critical row (row 5) - pulsing red
    critical_opacity = 0.15 + pulse * 0.45  # 0.15 to 0.6
    highlights.append({
        "color": f"rgba(239, 68, 68, {critical_opacity})",
        "range": {"x": 0, "y": 5, "width": 5, "height": 1},
        "style": "solid-outline"
    })

    # Warning row (row 3) - pulsing yellow/orange (offset phase)
    warning_pulse = (math.sin(n * 0.15 + 2) + 1) / 2
    warning_opacity = 0.15 + warning_pulse * 0.35
    highlights.append({
        "color": f"rgba(245, 158, 11, {warning_opacity})",
        "range": {"x": 0, "y": 3, "width": 5, "height": 1},
        "style": "solid"
    })

    # High memory warning (row 1, columns 3-4) - pulsing orange
    mem_pulse = (math.sin(n * 0.2) + 1) / 2
    mem_opacity = 0.2 + mem_pulse * 0.3
    highlights.append({
        "color": f"rgba(249, 115, 22, {mem_opacity})",
        "range": {"x": 3, "y": 1, "width": 2, "height": 1},
        "style": "dashed"
    })

    # Offline row (row 7) - pulsing gray
    offline_pulse = (math.sin(n * 0.1) + 1) / 2
    offline_opacity = 0.1 + offline_pulse * 0.2
    highlights.append({
        "color": f"rgba(107, 114, 128, {offline_opacity})",
        "range": {"x": 0, "y": 7, "width": 5, "height": 1},
        "style": "no-outline"
    })

    return highlights, n


if __name__ == "__main__":
    app.run(debug=True, port=8050)
