"""
Example: Fill Handle Double-Click (Excel-like Auto-Fill)

Demonstrates the Excel-like double-click fill handle feature:
- Select a range of cells (e.g., B1:C2 with a pattern)
- Double-click the fill handle (small square at bottom-right of selection)
- Pattern is automatically filled down to the last row with data in the left column

How it works:
- The grid looks at the column immediately to the LEFT of the selection
- It scans down from the selection start to find the first empty cell
- The pattern is repeated to fill down to the row above that empty cell

Edge cases:
- If selection starts at column 0, double-click does nothing (no left column)
- If left column has a gap, fill stops at the row before the gap

Try it:
1. Select cells B1:C2 (containing the pattern "X", "Y", "A", "B")
2. Double-click the fill handle (small blue square at bottom-right)
3. Watch the pattern repeat down to row 10 (where column A has data)
4. Try selecting column A cells - double-click does nothing (no left column)
"""

from dash import Dash, html, callback, Output, Input
import dash_glide_grid as dgg

app = Dash(__name__)

# Sample data with column A having data to row 10, but B and C only have data in first 2 rows
DATA = [
    {"id": 1, "formula": "X", "value": "A"},
    {"id": 2, "formula": "Y", "value": "B"},
    {"id": 3, "formula": "", "value": ""},
    {"id": 4, "formula": "", "value": ""},
    {"id": 5, "formula": "", "value": ""},
    {"id": 6, "formula": "", "value": ""},
    {"id": 7, "formula": "", "value": ""},
    {"id": 8, "formula": "", "value": ""},
    {"id": 9, "formula": "", "value": ""},
    {"id": 10, "formula": "", "value": ""},
    # Row 11 has empty "id" - this is where the fill should stop
    {"id": "", "formula": "", "value": ""},
    {"id": "", "formula": "", "value": ""},
]

COLUMNS = [
    {"id": "id", "title": "ID (Left Column)", "width": 150},
    {"id": "formula", "title": "Formula", "width": 120},
    {"id": "value", "title": "Value", "width": 120},
]

app.layout = html.Div(
    [
        html.H1("Fill Handle Double-Click (Excel-like Auto-Fill)"),
        html.P(
            [
                "Double-click the fill handle to auto-fill down to the last row with data in the left column. ",
                "This mimics Excel's behavior for quickly filling formulas or patterns.",
            ]
        ),
        # Fill handle hover indicator
        html.Div(
            [
                html.Strong("Fill Handle Status: "),
                html.Span(
                    id="fill-handle-indicator",
                    children="NOT hovering",
                    style={
                        "padding": "5px 15px",
                        "borderRadius": "4px",
                        "backgroundColor": "#ffcccc",
                        "color": "#333",
                        "fontWeight": "bold",
                    },
                ),
            ],
            style={"marginBottom": "15px"},
        ),
        html.H3("Instructions:"),
        html.Ul(
            [
                html.Li("Select cells B1:C2 (Formula: X,Y and Value: A,B)"),
                html.Li("Move mouse to the fill handle - indicator should turn GREEN"),
                html.Li("Double-click the fill handle when indicator is GREEN"),
                html.Li("Watch the pattern fill down to row 10 (last row where ID column has data)"),
            ]
        ),
        html.H3("Edge Cases to Try:"),
        html.Ul(
            [
                html.Li("Select column A (ID) cells only - double-click does nothing (no left column)"),
                html.Li("Clear some ID values to create gaps - fill stops at the gap"),
            ]
        ),
        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=400,
            fillHandle=True,  # Enable fill handle
            rowMarkers="number",
        ),
        html.Div(id="output", style={"marginTop": "20px", "fontFamily": "monospace"}),
    ],
    style={"padding": "20px"},
)


@callback(
    Output("fill-handle-indicator", "children"),
    Output("fill-handle-indicator", "style"),
    Input("grid", "itemHovered"),
)
def update_fill_handle_indicator(item_hovered):
    is_fill_handle = item_hovered and item_hovered.get("isFillHandle", False)

    if is_fill_handle:
        return "HOVERING over fill handle - DOUBLE-CLICK NOW!", {
            "padding": "5px 15px",
            "borderRadius": "4px",
            "backgroundColor": "#90EE90",  # Light green
            "color": "#006400",  # Dark green text
            "fontWeight": "bold",
        }
    else:
        return "NOT hovering over fill handle", {
            "padding": "5px 15px",
            "borderRadius": "4px",
            "backgroundColor": "#ffcccc",  # Light red
            "color": "#8B0000",  # Dark red text
            "fontWeight": "bold",
        }


@callback(
    Output("output", "children"),
    Input("grid", "cellEdited"),
    prevent_initial_call=True,
)
def show_edit(cell_edited):
    if cell_edited:
        return f"Last edit: {cell_edited}"
    return ""


if __name__ == "__main__":
    app.run(debug=True)
