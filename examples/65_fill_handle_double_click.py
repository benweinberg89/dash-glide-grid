"""
Example: Fill Handle Double-Click (Excel-like Auto-Fill)

Demonstrates the Excel-like double-click fill handle feature with various cell types.

Tests:
1. Left column cell types - what counts as "empty" to stop the fill?
2. Right column cell types - how do different types copy/fill?
3. Right column blocking - fill stops before existing data in fill columns (Excel behavior)
"""

from dash import Dash, html, callback, Output, Input, dcc
import dash_glide_grid as dgg

app = Dash(__name__)

DROPDOWN_OPTIONS = ["Option A", "Option B", "Option C"]

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
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "Option A", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 1: Pattern row 2
    {
        "left_text": "Text B",
        "left_number": 200,
        "left_bool": False,
        "fill_text": "Pattern 2",
        "fill_number": 20,
        "fill_bool": False,
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "Option B", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 2: Has data
    {
        "left_text": "Text C",
        "left_number": 300,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 3: Number is 0 (falsy but not empty!)
    {
        "left_text": "Text D",
        "left_number": 0,
        "left_bool": False,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 4: Has EXISTING DATA in fill columns - fill should stop BEFORE this row!
    {
        "left_text": "Text E",
        "left_number": 500,
        "left_bool": False,
        "fill_text": "EXISTING",
        "fill_number": 999,
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 5: Last row with data
    {
        "left_text": "Text F",
        "left_number": 600,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 6: EMPTY - fill should stop here
    {
        "left_text": "",
        "left_number": "",
        "left_bool": "",
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
    },
    # Row 7: More data after gap (should not be filled to)
    {
        "left_text": "After Gap",
        "left_number": 700,
        "left_bool": True,
        "fill_text": "",
        "fill_number": "",
        "fill_bool": "",
        "fill_dropdown": {"kind": "dropdown-cell", "data": {"value": "", "allowedValues": DROPDOWN_OPTIONS}},
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

        html.Div([
            html.Label("Allowed Fill Directions: ", style={"marginRight": "10px", "fontWeight": "bold"}),
            dcc.RadioItems(
                id="fill-direction",
                options=[
                    {"label": "Horizontal only", "value": "horizontal"},
                    {"label": "Vertical only", "value": "vertical"},
                    {"label": "Orthogonal (H or V)", "value": "orthogonal"},
                    {"label": "Any direction", "value": "any"},
                ],
                value="orthogonal",
                inline=True,
            ),
        ], style={"marginBottom": "15px"}),

        html.H3("Test Cases:"),
        html.Div([
            html.H4("1. Left Column Detection (what stops the fill?)"),
            html.Ul([
                html.Li("Row 6 is empty in left columns → Fill stops at row 5"),
                html.Li("Row 3 has left_number=0 (falsy but not empty) → Should NOT stop fill"),
            ]),

            html.H4("2. Right Column Blocking (Excel behavior)"),
            html.Ul([
                html.Li("Row 4 has EXISTING data in Fill:Text and Fill:Number"),
                html.Li("Select Fill:Text rows 0-1, double-click → Should fill to row 3 only (stops BEFORE row 4)"),
                html.Li("Select Fill:Bool rows 0-1, double-click → Should fill to row 5 (row 4's bool is empty)"),
                html.Li("Select Fill:Dropdown rows 0-1, double-click → Should fill to row 5 (row 4's dropdown is empty)"),
            ]),

            html.H4("3. Fill Direction"),
            html.Ul([
                html.Li("Set to 'Horizontal only' → Double-click auto-fill should NOT work"),
                html.Li("Set to any other option → Double-click auto-fill should work"),
            ]),
        ], style={"backgroundColor": "#f5f5f5", "padding": "15px", "borderRadius": "8px", "marginBottom": "20px"}),

        dgg.GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=DATA,
            height=350,
            fillHandle=True,
            allowedFillDirections="orthogonal",
            rowMarkers="number",
        ),

        html.Div(id="output", style={"marginTop": "20px", "fontFamily": "monospace", "whiteSpace": "pre-wrap"}),
    ],
    style={"padding": "20px"},
)


@callback(
    Output("grid", "allowedFillDirections"),
    Input("fill-direction", "value"),
)
def update_fill_direction(direction):
    return direction


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
            fill_dd = fill_dd.get("data", {}).get("value", "") if "data" in fill_dd else fill_dd.get("value", "")
        parts.append(f"  Row {i}: text='{fill_text}', num={fill_num}, bool={fill_bool}, dropdown='{fill_dd}'")

    return "\n".join(parts)


if __name__ == "__main__":
    app.run(debug=True)
