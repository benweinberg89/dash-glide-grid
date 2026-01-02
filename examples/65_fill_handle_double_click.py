"""
Example: Fill Handle Double-Click (Excel-like Auto-Fill)

Demonstrates the Excel-like double-click fill handle feature with various cell types.

Tests:
1. Left column cell types - what counts as "empty" to stop the fill?
2. Right column cell types - how do different types copy/fill?
"""

from dash import Dash, html, callback, Output, Input
import dash_glide_grid as dgg

app = Dash(__name__)

# Test data with various cell types
DATA = [
    # Row 0: Pattern row 1
    {
        "left_text": "Text A",
        "left_number": 100,
        "left_bool": True,
        "fill_text": "Pattern 1",
        "fill_number": 10,
        "fill_bool": True,
        "fill_dropdown": {"kind": "dropdown-cell", "value": "Option A", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 1: Pattern row 2
    {
        "left_text": "Text B",
        "left_number": 200,
        "left_bool": False,
        "fill_text": "Pattern 2",
        "fill_number": 20,
        "fill_bool": False,
        "fill_dropdown": {"kind": "dropdown-cell", "value": "Option B", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 2: Has data
    {
        "left_text": "Text C",
        "left_number": 300,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 3: Number is 0 (falsy but not empty!)
    {
        "left_text": "Text D",
        "left_number": 0,
        "left_bool": False,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 4: Bool is False (falsy but not empty!)
    {
        "left_text": "Text E",
        "left_number": 500,
        "left_bool": False,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 5: Last row with data
    {
        "left_text": "Text F",
        "left_number": 600,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 6: EMPTY - fill should stop here
    {
        "left_text": "",
        "left_number": "",
        "left_bool": "",
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
    # Row 7: More data after gap (should not be filled to)
    {
        "left_text": "After Gap",
        "left_number": 700,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "value": "", "allowedValues": ["Option A", "Option B", "Option C"]},
    },
]

COLUMNS = [
    {"id": "left_text", "title": "Left: Text", "width": 100},
    {"id": "left_number", "title": "Left: Number", "width": 100},
    {"id": "left_bool", "title": "Left: Bool", "width": 100},
    {"id": "fill_text", "title": "Fill: Text", "width": 100},
    {"id": "fill_number", "title": "Fill: Number", "width": 100},
    {"id": "fill_bool", "title": "Fill: Bool", "width": 100},
    {"id": "fill_dropdown", "title": "Fill: Dropdown", "width": 120},
]

app.layout = html.Div(
    [
        html.H1("Fill Handle Double-Click - Cell Type Testing"),

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

        html.H3("Test Cases:"),
        html.Div([
            html.H4("1. Left Column Detection (what stops the fill?)"),
            html.Ul([
                html.Li("Select Fill:Text rows 0-1, double-click → Should fill to row 5 (row 6 is empty)"),
                html.Li("Row 3 has left_number=0 (falsy but not empty) → Should NOT stop fill"),
                html.Li("Row 4 has left_bool=False (falsy but not empty) → Should NOT stop fill"),
            ]),

            html.H4("2. Fill Column Types (how do they copy?)"),
            html.Ul([
                html.Li("Fill:Text - Simple text pattern"),
                html.Li("Fill:Number - Number pattern"),
                html.Li("Fill:Bool - Boolean pattern (True/False alternating)"),
                html.Li("Fill:Dropdown - Dropdown cell pattern"),
            ]),

            html.H4("3. Try These:"),
            html.Ul([
                html.Li("Select cells in 'Fill: Text' column (rows 0-1), double-click fill handle"),
                html.Li("Select cells in 'Fill: Dropdown' column (rows 0-1), double-click fill handle"),
                html.Li("Select cells spanning multiple Fill columns, double-click fill handle"),
            ]),
        ], style={"backgroundColor": "#f5f5f5", "padding": "15px", "borderRadius": "8px", "marginBottom": "20px"}),

        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            fillHandle=True,
            rowMarkers="number",
        ),

        html.Div(id="output", style={"marginTop": "20px", "fontFamily": "monospace", "whiteSpace": "pre-wrap"}),
    ],
    style={"padding": "20px"},
)


@callback(
    Output("fill-handle-indicator", "children"),
    Output("fill-handle-indicator", "style"),
    Input("grid", "mouseMove"),
)
def update_fill_handle_indicator(mouse_move):
    is_fill_handle = mouse_move and mouse_move.get("isFillHandle", False)

    if is_fill_handle:
        return "HOVERING over fill handle - DOUBLE-CLICK NOW!", {
            "padding": "5px 15px",
            "borderRadius": "4px",
            "backgroundColor": "#90EE90",
            "color": "#006400",
            "fontWeight": "bold",
        }
    else:
        return "NOT hovering over fill handle", {
            "padding": "5px 15px",
            "borderRadius": "4px",
            "backgroundColor": "#ffcccc",
            "color": "#8B0000",
            "fontWeight": "bold",
        }


@callback(
    Output("output", "children"),
    Input("grid", "cellEdited"),
    Input("grid", "data"),
    prevent_initial_call=True,
)
def show_changes(cell_edited, data):
    parts = []
    if cell_edited:
        parts.append(f"Last edit: {cell_edited}")

    # Show current state of fill columns
    parts.append("\nCurrent Fill Column Values:")
    for i, row in enumerate(data[:8]):
        fill_text = row.get("fill_text", "")
        fill_num = row.get("fill_number", "")
        fill_bool = row.get("fill_bool", "")
        fill_dd = row.get("fill_dropdown", {})
        if isinstance(fill_dd, dict):
            fill_dd = fill_dd.get("value", "")
        parts.append(f"  Row {i}: text='{fill_text}', num={fill_num}, bool={fill_bool}, dropdown='{fill_dd}'")

    return "\n".join(parts)


if __name__ == "__main__":
    app.run(debug=True)
