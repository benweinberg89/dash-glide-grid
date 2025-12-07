"""
Example 8: Merged Cells
Demonstrates how to use the span property to merge cells horizontally across columns.
This creates an Excel-like merged cell experience.
"""

import dash
from dash import html, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Q1", "id": "q1", "width": 100},
    {"title": "Q2", "id": "q2", "width": 100},
    {"title": "Q3", "id": "q3", "width": 100},
    {"title": "Q4", "id": "q4", "width": 100},
    {"title": "Total", "id": "total", "width": 100},
]

# Example data with merged cells
# The span property defines horizontal cell merging: [start_column, end_column] (inclusive)
# IMPORTANT: All cells in a span range must report the same span value
DATA = [
    # Row 0: Header row with merged title spanning all columns (editable!)
    {
        "name": {
            "kind": "text",
            "data": "2024 Quarterly Sales Report",
            "allowOverlay": True,  # Make this merged cell editable
            "span": [0, 5],  # Merge across all 6 columns (0-5 inclusive)
            "themeOverride": {
                "bgCell": "#2563eb",
                "textDark": "#ffffff",
                "baseFontStyle": "bold 16px",
            },
        },
        # All cells in the span must have the same span property
        "q1": {
            "kind": "text",
            "data": "",  # Empty content for spanned cells
            "allowOverlay": False,
            "span": [0, 5],
        },
        "q2": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 5]},
        "q3": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 5]},
        "q4": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 5]},
        "total": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 5]},
    },
    # Row 1: Regular data row (editable)
    {
        "name": "Alice Johnson",
        "q1": {"kind": "number", "data": 45000, "allowOverlay": True},
        "q2": {"kind": "number", "data": 52000, "allowOverlay": True},
        "q3": {"kind": "number", "data": 48000, "allowOverlay": True},
        "q4": {"kind": "number", "data": 55000, "allowOverlay": True},
        "total": {"kind": "number", "data": 200000, "allowOverlay": True},
    },
    # Row 2: Regular data row (editable)
    {
        "name": "Bob Smith",
        "q1": {"kind": "number", "data": 38000, "allowOverlay": True},
        "q2": {"kind": "number", "data": 41000, "allowOverlay": True},
        "q3": {"kind": "number", "data": 39000, "allowOverlay": True},
        "q4": {"kind": "number", "data": 44000, "allowOverlay": True},
        "total": {"kind": "number", "data": 162000, "allowOverlay": True},
    },
    # Row 3: Section header with merged cells spanning Q1-Q4 (editable!)
    {
        "name": {
            "kind": "text",
            "data": "Team Average",
            "allowOverlay": True,  # Editable
            "themeOverride": {"bgCell": "#e0e7ff", "textDark": "#1e40af"},
        },
        "q1": {
            "kind": "text",
            "data": "Performance Metrics",
            "allowOverlay": True,  # Make this merged cell editable too!
            "span": [1, 4],  # Merge Q1 through Q4 columns
            "themeOverride": {"bgCell": "#e0e7ff", "textDark": "#1e40af"},
        },
        "q2": {
            "kind": "text",
            "data": "",
            "allowOverlay": False,
            "span": [1, 4],
            "themeOverride": {"bgCell": "#e0e7ff"},
        },
        "q3": {
            "kind": "text",
            "data": "",
            "allowOverlay": False,
            "span": [1, 4],
            "themeOverride": {"bgCell": "#e0e7ff"},
        },
        "q4": {
            "kind": "text",
            "data": "",
            "allowOverlay": False,
            "span": [1, 4],
            "themeOverride": {"bgCell": "#e0e7ff"},
        },
        "total": {
            "kind": "number",
            "data": 181000,
            "allowOverlay": False,
            "themeOverride": {
                "bgCell": "#e0e7ff",
                "textDark": "#1e40af",
                "baseFontStyle": "bold 14px",
            },
        },
    },
    # Row 4: Another regular data row
    {
        "name": "Carol Williams",
        "q1": {"kind": "number", "data": 51000},
        "q2": {"kind": "number", "data": 49000},
        "q3": {"kind": "number", "data": 53000},
        "q4": {"kind": "number", "data": 58000},
        "total": {"kind": "number", "data": 211000},
    },
    # Row 5: Merged note spanning first 3 columns (editable!)
    {
        "name": {
            "kind": "text",
            "data": "* Note: All values in USD",
            "allowOverlay": True,  # Make this editable too
            "span": [0, 2],
            "themeOverride": {
                "textDark": "#6b7280",
                "baseFontStyle": "italic 12px",
            },
        },
        "q1": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 2]},
        "q2": {"kind": "text", "data": "", "allowOverlay": False, "span": [0, 2]},
        "q3": "",
        "q4": "",
        "total": "",
    },
]

app.layout = html.Div(
    [
        html.H1("Merged Cells Demo", style={"marginBottom": "10px"}),
        html.Div(
            [
                html.H3("About Merged Cells:", style={"marginTop": 0}),
                html.P(
                    [
                        "The ",
                        html.Code("span"),
                        " property allows you to merge cells horizontally across columns. ",
                        "This is useful for creating section headers, titles, and grouping related data.",
                    ]
                ),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Strong("Format: "),
                                html.Code("span: [start_column, end_column]"),
                                " (inclusive)",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Important: "),
                                "All cells in the span range must have the same span property",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Example: "),
                                html.Code("span: [0, 2]"),
                                " merges columns 0, 1, and 2",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Editing: "),
                                "Double-click merged cells to edit them - only the first cell stores data",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Note: "),
                                "Only horizontal (column) spanning is supported, not vertical (row) spanning",
                            ]
                        ),
                    ]
                ),
            ],
            style={
                "marginBottom": "20px",
                "backgroundColor": "#f9fafb",
                "padding": "20px",
                "borderRadius": "8px",
                "border": "1px solid #e5e7eb",
            },
        ),
        dgg.GlideGrid(
            id="merged-cells-grid",
            columns=COLUMNS,
            data=DATA,
            height=400,
            rowMarkers="number",
            columnResize=True,
            theme={"borderColor": "#d1d5db", "horizontalBorderColor": "#e5e7eb"},
        ),
        html.Div(
            [
                html.H4("Click on a cell to see its details:"),
                html.Div(
                    id="cell-info",
                    style={
                        "padding": "15px",
                        "backgroundColor": "#f3f4f6",
                        "borderRadius": "4px",
                        "fontFamily": "monospace",
                        "minHeight": "60px",
                    },
                ),
            ],
            style={"marginTop": "30px"},
        ),
        html.Div(
            [
                html.H4("Last Edit:", style={"marginTop": "20px"}),
                html.Div(
                    id="edit-log",
                    style={
                        "padding": "15px",
                        "backgroundColor": "#ecfdf5",
                        "borderRadius": "4px",
                        "fontFamily": "monospace",
                        "minHeight": "40px",
                        "color": "#065f46",
                    },
                ),
            ]
        ),
        html.Div(
            [
                html.H4("How to create merged cells:", style={"marginTop": "30px"}),
                html.Pre(
                    """
# Example: Merge cells across columns 0-2
data = [
    [
        {
            "kind": "text",
            "data": "Merged Header",
            "span": [0, 2]  # Start at column 0, end at column 2 (inclusive)
        },
        # All other cells in the span must also have the same span
        {
            "kind": "text",
            "data": "",  # Empty data for spanned cells
            "span": [0, 2]
        },
        {
            "kind": "text",
            "data": "",
            "span": [0, 2]
        },
        # Regular cell in column 3
        "Regular cell"
    ]
]
        """,
                    style={
                        "backgroundColor": "#1e293b",
                        "color": "#e2e8f0",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "overflow": "auto",
                    },
                ),
            ]
        ),
    ],
    style={
        "margin": "40px",
        "fontFamily": "system-ui, -apple-system, sans-serif",
        "maxWidth": "1200px",
    },
)


@callback(Output("cell-info", "children"), Input("merged-cells-grid", "cellClicked"))
def display_cell_info(cell_clicked):
    if not cell_clicked:
        return "Click on any cell to see its details..."

    col = cell_clicked["col"]
    row = cell_clicked["row"]

    col_id = COLUMNS[col]["id"]
    cell_data = DATA[row][col_id]

    info_lines = [
        html.Div([html.Strong("Row: "), str(row)]),
        html.Div([html.Strong("Column: "), str(col)]),
    ]

    if isinstance(cell_data, dict):
        if "span" in cell_data:
            span_start, span_end = cell_data["span"]
            info_lines.append(
                html.Div(
                    [
                        html.Strong("Span: "),
                        f"[{span_start}, {span_end}] ",
                        html.Span(
                            f"(merges {span_end - span_start + 1} columns)",
                            style={"color": "#059669", "fontWeight": "bold"},
                        ),
                    ]
                )
            )
        info_lines.append(
            html.Div([html.Strong("Kind: "), cell_data.get("kind", "N/A")])
        )
        info_lines.append(
            html.Div([html.Strong("Data: "), str(cell_data.get("data", ""))])
        )
    else:
        info_lines.append(html.Div([html.Strong("Value: "), str(cell_data)]))

    return info_lines


@callback(Output("edit-log", "children"), Input("merged-cells-grid", "cellEdited"))
def display_edit_info(cell_edited):
    if not cell_edited:
        return "Double-click any cell to edit it..."

    col = cell_edited["col"]
    row = cell_edited["row"]
    value = cell_edited["value"]

    col_id = COLUMNS[col]["id"]
    cell_data = DATA[row][col_id]
    is_merged = isinstance(cell_data, dict) and "span" in cell_data

    edit_info = [
        html.Div([html.Strong("Edited Cell: "), f"Row {row}, Column {col}"]),
        html.Div([html.Strong("New Value: "), str(value)]),
    ]

    if is_merged:
        span_start, span_end = cell_data["span"]
        edit_info.append(
            html.Div(
                [
                    html.Strong("Note: "),
                    f"This is a merged cell spanning columns {span_start}-{span_end}. ",
                    "Only the first cell in the span stores the data.",
                ],
                style={"marginTop": "5px", "fontStyle": "italic"},
            )
        )

    return edit_info


if __name__ == "__main__":
    app.run(debug=True, port=8050)
