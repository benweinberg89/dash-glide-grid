"""
Example: Visible Region Tracking

Demonstrates visibleRegion to track which rows/columns are currently visible.
Useful for lazy loading, infinite scroll, or analytics.
"""

import dash
from dash import html, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions - many columns to enable horizontal scrolling
COLUMNS = [
    {"title": f"Col {i}", "id": f"col_{i}", "width": 100}
    for i in range(20)
]

# Generate lots of data to enable scrolling
DATA = [
    {f"col_{col}": f"R{row}C{col}" for col in range(20)}
    for row in range(200)
]

app.layout = html.Div([
    html.H1("Visible Region Tracking Example"),
    html.P("Scroll the grid to see the visible region update in real-time."),

    html.Div([
        # Visible region stats
        html.Div([
            html.Div([
                html.H4("Visible Region:"),
                html.Div(id="visible-region-display", style={
                    "fontFamily": "monospace",
                    "padding": "15px",
                    "backgroundColor": "#f0f8ff",
                    "borderRadius": "5px",
                    "lineHeight": "1.8"
                }),
            ], style={"flex": "1", "marginRight": "20px"}),

            html.Div([
                html.H4("Stats:"),
                html.Div(id="region-stats", style={
                    "fontFamily": "monospace",
                    "padding": "15px",
                    "backgroundColor": "#fff8f0",
                    "borderRadius": "5px",
                    "lineHeight": "1.8"
                }),
            ], style={"flex": "1"}),
        ], style={"display": "flex", "marginBottom": "20px"}),

        dgg.GlideGrid(
            id="visible-region-grid",
            columns=COLUMNS,
            data=DATA,
            height=400,
            width="100%",
            rowHeight=34,
            headerHeight=40,
            rowMarkers="number",
            smoothScrollX=True,
            smoothScrollY=True,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Use Cases:"),
        html.Ul([
            html.Li("Lazy loading: Only fetch data for visible rows"),
            html.Li("Infinite scroll: Load more data when user scrolls near the end"),
            html.Li("Analytics: Track which data users spend time viewing"),
            html.Li("Virtual scrolling optimizations"),
        ]),
        html.H4("Props used:"),
        html.Code("visibleRegion"),
        html.P("Updates whenever the visible area changes. Contains x, y (start indices), width, height (visible count), and tx, ty (pixel offsets)."),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])


@callback(
    Output("visible-region-display", "children"),
    Output("region-stats", "children"),
    Input("visible-region-grid", "visibleRegion"),
)
def update_visible_region(visible_region):
    """Update the visible region display."""
    if not visible_region:
        return "No data yet - scroll the grid!", ""

    x = visible_region.get("x", 0)
    y = visible_region.get("y", 0)
    width = visible_region.get("width", 0)
    height = visible_region.get("height", 0)
    tx = visible_region.get("tx", 0)
    ty = visible_region.get("ty", 0)

    region_text = f"""
First visible column: {x}
First visible row: {y}
Visible columns: {width}
Visible rows: {height}
Pixel offset X: {tx:.1f}px
Pixel offset Y: {ty:.1f}px
    """.strip()

    # Calculate stats
    total_rows = len(DATA)
    total_cols = len(COLUMNS)
    last_visible_row = y + height - 1
    last_visible_col = x + width - 1

    percent_rows = (height / total_rows) * 100
    percent_cols = (width / total_cols) * 100

    stats_text = f"""
Total rows: {total_rows}
Total columns: {total_cols}

Viewing rows {y} to {last_visible_row}
Viewing cols {x} to {last_visible_col}

{percent_rows:.1f}% of rows visible
{percent_cols:.1f}% of columns visible

{"📍 Near bottom - load more?" if last_visible_row > total_rows - 20 else ""}
    """.strip()

    return region_text, stats_text


if __name__ == "__main__":
    app.run(debug=True, port=8050)
