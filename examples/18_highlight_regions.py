"""
Example 18: Highlight Regions

Demonstrates the highlightRegions prop for highlighting specific cell ranges.
Use cases include conditional formatting, search highlights, and validation errors.

Features:
- Basic highlight regions with colors
- Border style options: "dashed" (default), "solid", "solid-outline", "no-outline"
- Dynamic highlighting based on user interaction

Run with: python examples/18_highlight_regions.py
"""

from dash import Dash, html, callback, Input, Output, State
from dash_glide_grid import GlideGrid

app = Dash(__name__)

# Sample data - sales data with some validation issues
columns = [
    {"title": "Product", "width": 150, "id": "product"},
    {"title": "Q1 Sales", "width": 100, "id": "q1"},
    {"title": "Q2 Sales", "width": 100, "id": "q2"},
    {"title": "Q3 Sales", "width": 100, "id": "q3"},
    {"title": "Q4 Sales", "width": 100, "id": "q4"},
    {"title": "Total", "width": 100, "id": "total"},
    {"title": "Status", "width": 100, "id": "status"},
]

data = [
    {"product": "Widget A", "q1": 1200, "q2": 1500, "q3": 1800, "q4": 2100, "total": 6600, "status": "On Track"},
    {"product": "Widget B", "q1": 800, "q2": 750, "q3": 600, "q4": 400, "total": 2550, "status": "Declining"},
    {"product": "Widget C", "q1": 500, "q2": 700, "q3": 900, "q4": 1100, "total": 3200, "status": "Growing"},
    {"product": "Widget D", "q1": 2000, "q2": 1800, "q3": 1600, "q4": 1400, "total": 6800, "status": "Declining"},
    {"product": "Widget E", "q1": 300, "q2": 400, "q3": 500, "q4": 600, "total": 1800, "status": "Growing"},
    {"product": "Widget F", "q1": 1500, "q2": 1600, "q3": 1700, "q4": 1800, "total": 6600, "status": "On Track"},
    {"product": "Widget G", "q1": 100, "q2": 150, "q3": 200, "q4": 250, "total": 700, "status": "Low Volume"},
    {"product": "Widget H", "q1": 900, "q2": 1000, "q3": 1100, "q4": 1200, "total": 4200, "status": "Growing"},
    {"product": "Widget I", "q1": 1100, "q2": 1000, "q3": 900, "q4": 800, "total": 3800, "status": "Declining"},
    {"product": "Widget J", "q1": 600, "q2": 650, "q3": 700, "q4": 750, "total": 2700, "status": "Stable"},
]

# Define highlight regions for different purposes
highlight_regions = [
    # Highlight declining products (rows 1, 3, 8) with red background
    {
        "color": "rgba(239, 68, 68, 0.15)",
        "range": {"x": 0, "y": 1, "width": 7, "height": 1},
    },
    {
        "color": "rgba(239, 68, 68, 0.15)",
        "range": {"x": 0, "y": 3, "width": 7, "height": 1},
    },
    {
        "color": "rgba(239, 68, 68, 0.15)",
        "range": {"x": 0, "y": 8, "width": 7, "height": 1},
    },
    # Highlight growing products (rows 2, 4, 7) with green background
    {
        "color": "rgba(34, 197, 94, 0.15)",
        "range": {"x": 0, "y": 2, "width": 7, "height": 1},
    },
    {
        "color": "rgba(34, 197, 94, 0.15)",
        "range": {"x": 0, "y": 4, "width": 7, "height": 1},
    },
    {
        "color": "rgba(34, 197, 94, 0.15)",
        "range": {"x": 0, "y": 7, "width": 7, "height": 1},
    },
    # Highlight low volume warning (row 6) with yellow
    {
        "color": "rgba(234, 179, 8, 0.2)",
        "range": {"x": 0, "y": 6, "width": 7, "height": 1},
    },
    # Highlight the Q4 column (best quarter) with blue
    {
        "color": "rgba(59, 130, 246, 0.1)",
        "range": {"x": 4, "y": 0, "width": 1, "height": 10},
    },
]

app.layout = html.Div(
    [
        html.H1("Highlight Regions Example"),
        html.P(
            "This example shows how to highlight specific cell ranges for conditional formatting."
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Span(
                            style={
                                "backgroundColor": "rgba(239, 68, 68, 0.3)",
                                "padding": "2px 8px",
                                "marginRight": "10px",
                            }
                        ),
                        html.Span("Declining", style={"marginRight": "20px"}),
                        html.Span(
                            style={
                                "backgroundColor": "rgba(34, 197, 94, 0.3)",
                                "padding": "2px 8px",
                                "marginRight": "10px",
                            }
                        ),
                        html.Span("Growing", style={"marginRight": "20px"}),
                        html.Span(
                            style={
                                "backgroundColor": "rgba(234, 179, 8, 0.4)",
                                "padding": "2px 8px",
                                "marginRight": "10px",
                            }
                        ),
                        html.Span("Low Volume Warning", style={"marginRight": "20px"}),
                        html.Span(
                            style={
                                "backgroundColor": "rgba(59, 130, 246, 0.2)",
                                "padding": "2px 8px",
                                "marginRight": "10px",
                            }
                        ),
                        html.Span("Best Quarter (Q4)"),
                    ],
                    style={
                        "marginBottom": "15px",
                        "display": "flex",
                        "alignItems": "center",
                    },
                ),
            ]
        ),
        GlideGrid(
            id="grid-highlights",
            columns=columns,
            data=data,
            height=400,
            highlightRegions=highlight_regions,
            rowMarkers="number",
        ),
        html.Hr(),
        html.H2("Border Styles Demo"),
        html.P(
            "Highlight regions support different border styles. Compare the four available styles:"
        ),
        html.Div(
            [
                html.Div([
                    html.Strong("dashed (default)"),
                    html.Span(" - Dashed border outline", style={"color": "#666"}),
                ], style={"marginBottom": "5px"}),
                html.Div([
                    html.Strong("solid"),
                    html.Span(" - Solid border outline", style={"color": "#666"}),
                ], style={"marginBottom": "5px"}),
                html.Div([
                    html.Strong("solid-outline"),
                    html.Span(" - Thicker solid outline with background fill", style={"color": "#666"}),
                ], style={"marginBottom": "5px"}),
                html.Div([
                    html.Strong("no-outline"),
                    html.Span(" - Background fill only, no border", style={"color": "#666"}),
                ], style={"marginBottom": "15px"}),
            ]
        ),
        GlideGrid(
            id="grid-styles",
            columns=columns,
            data=data,
            height=400,
            highlightRegions=[
                # Row 0-1: dashed style (default)
                {
                    "color": "rgba(59, 130, 246, 0.3)",
                    "range": {"x": 1, "y": 0, "width": 2, "height": 2},
                    "style": "dashed",
                },
                # Row 0-1: solid style
                {
                    "color": "rgba(34, 197, 94, 0.3)",
                    "range": {"x": 3, "y": 0, "width": 2, "height": 2},
                    "style": "solid",
                },
                # Row 3-4: solid-outline style
                {
                    "color": "rgba(239, 68, 68, 0.3)",
                    "range": {"x": 1, "y": 3, "width": 2, "height": 2},
                    "style": "solid-outline",
                },
                # Row 3-4: no-outline style
                {
                    "color": "rgba(147, 51, 234, 0.3)",
                    "range": {"x": 3, "y": 3, "width": 2, "height": 2},
                    "style": "no-outline",
                },
            ],
            rowMarkers="number",
        ),
        html.Hr(),
        html.H2("Dynamic Highlights Demo"),
        html.P("Click cells to add highlight regions dynamically:"),
        html.Div(
            [
                html.Button(
                    "Clear Highlights", id="btn-clear", style={"marginRight": "10px"}
                ),
                html.Button(
                    "Highlight Row", id="btn-row", style={"marginRight": "10px"}
                ),
                html.Button(
                    "Highlight Column", id="btn-col", style={"marginRight": "10px"}
                ),
                html.Button("Highlight 2x2 Block", id="btn-block"),
            ],
            style={"marginBottom": "15px"},
        ),
        html.Div(id="dynamic-info", style={"marginBottom": "15px", "color": "#666"}),
        GlideGrid(
            id="grid-dynamic",
            columns=columns,
            data=data,
            height=400,
            highlightRegions=[],
            rowMarkers="number",
        ),
    ],
    style={"padding": "20px", "maxWidth": "1000px", "margin": "0 auto"},
)


@callback(
    Output("grid-dynamic", "highlightRegions"),
    Output("dynamic-info", "children"),
    Input("btn-clear", "n_clicks"),
    Input("btn-row", "n_clicks"),
    Input("btn-col", "n_clicks"),
    Input("btn-block", "n_clicks"),
    State("grid-dynamic", "selectedCell"),
    prevent_initial_call=True,
)
def update_highlights(
    clear_clicks, row_clicks, col_clicks, block_clicks, selected_cell
):
    from dash import ctx

    if ctx.triggered_id == "btn-clear":
        return [], "Highlights cleared"

    if not selected_cell:
        return [], "Click a cell first, then use the buttons to highlight"

    col = selected_cell["col"]
    row = selected_cell["row"]

    if ctx.triggered_id == "btn-row":
        highlights = [
            {
                "color": "rgba(147, 51, 234, 0.2)",
                "range": {"x": 0, "y": row, "width": 7, "height": 1},
            }
        ]
        return highlights, f"Highlighted row {row}"

    elif ctx.triggered_id == "btn-col":
        highlights = [
            {
                "color": "rgba(236, 72, 153, 0.2)",
                "range": {"x": col, "y": 0, "width": 1, "height": 10},
            }
        ]
        return highlights, f"Highlighted column {col}"

    elif ctx.triggered_id == "btn-block":
        highlights = [
            {
                "color": "rgba(14, 165, 233, 0.25)",
                "range": {"x": col, "y": row, "width": 2, "height": 2},
            }
        ]
        return highlights, f"Highlighted 2x2 block starting at ({col}, {row})"

    return [], "Select a cell and click a button"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
