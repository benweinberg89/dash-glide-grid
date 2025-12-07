"""
Example 24: Value Formatters

This example demonstrates:
1. valueFormatter - format cell display values without changing underlying data
2. Different format types: currency, percentage, numbers, dates

SETUP REQUIRED:
---------------
Create `assets/dashGlideGridFunctions.js` with your functions.
See the file in this examples/assets/ folder for examples.

The valueFormatter prop uses the same namespace pattern as validateCell.
"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_glide_grid as dgg

app = Dash(__name__, suppress_callback_exceptions=True)

# Sample data with various numeric types
initial_data = [
    {"product": "Product A", "price": 1234.56, "growth": 0.156, "units": 15000, "date": 1699574400000},  # Nov 10, 2023
    {"product": "Product B", "price": 567.89, "growth": 0.089, "units": 8500, "date": 1700179200000},   # Nov 17, 2023
    {"product": "Product C", "price": 2345.00, "growth": 0.234, "units": 22000, "date": 1700784000000},  # Nov 24, 2023
    {"product": "Product D", "price": 890.12, "growth": 0.045, "units": 5200, "date": 1701388800000},   # Dec 1, 2023
    {"product": "Product E", "price": 3456.78, "growth": 0.312, "units": 35000, "date": 1701993600000},  # Dec 8, 2023
]

# Columns without formatters (raw values)
columns_raw = [
    {"title": "Product", "id": "product", "width": 120},
    {"title": "Price", "id": "price", "width": 120},
    {"title": "Growth Rate", "id": "growth", "width": 120},
    {"title": "Units Sold", "id": "units", "width": 120},
    {"title": "Release Date", "id": "date", "width": 150},
]

# Columns with formatters (formatted display)
columns_formatted = [
    {"title": "Product", "id": "product", "width": 120},
    {
        "title": "Price",
        "id": "price",
        "width": 120,
        "valueFormatter": {"function": "formatCurrency(value)"},
    },
    {
        "title": "Growth Rate",
        "id": "growth",
        "width": 120,
        "valueFormatter": {"function": "formatPercent(value)"},
    },
    {
        "title": "Units Sold",
        "id": "units",
        "width": 120,
        "valueFormatter": {"function": "formatNumber(value)"},
    },
    {
        "title": "Release Date",
        "id": "date",
        "width": 150,
        "valueFormatter": {"function": "formatDate(value)"},
    },
]

app.layout = html.Div(
    [
        html.H1("Value Formatter Demo"),
        html.P(
            "Value formatters change how data is displayed without modifying the underlying values. "
            "When you edit a cell, you work with the raw data."
        ),
        html.Div(
            [
                html.Label("Show formatters:"),
                dcc.RadioItems(
                    id="formatter-toggle",
                    options=[
                        {"label": "Raw Values", "value": "raw"},
                        {"label": "Formatted Values", "value": "formatted"},
                    ],
                    value="formatted",
                    inline=True,
                ),
            ],
            style={"marginBottom": "10px"},
        ),
        html.H3("Grid:"),
        dgg.GlideGrid(
            id="grid",
            columns=columns_formatted,
            data=initial_data,
            height=300,
            rowMarkers="number",
        ),
        html.Div(
            [
                html.H3("Available Formatters:"),
                html.Ul(
                    [
                        html.Li(
                            "formatCurrency(value) - Formats as USD currency ($1,234.56)"
                        ),
                        html.Li(
                            "formatPercent(value) - Formats as percentage (15.6%)"
                        ),
                        html.Li(
                            "formatNumber(value) - Adds thousands separators (15,000)"
                        ),
                        html.Li(
                            "formatDate(value) - Formats timestamps as dates (Nov 10, 2023)"
                        ),
                        html.Li(
                            "formatFixed2(value) - Fixed 2 decimal places (1234.56)"
                        ),
                        html.Li(
                            "formatUppercase(value) - Converts text to uppercase"
                        ),
                        html.Li(
                            "formatWithUnits(value) - Adds units suffix (15.0 kg)"
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            [
                html.H3("Last Cell Edited:"),
                html.Pre(id="edit-output", style={"padding": "10px", "background": "#f0f0f0"}),
            ]
        ),
    ],
    style={"padding": "20px", "maxWidth": "900px", "margin": "0 auto"},
)


@callback(
    Output("grid", "columns"),
    Input("formatter-toggle", "value"),
)
def toggle_formatters(mode):
    if mode == "raw":
        return columns_raw
    return columns_formatted


@callback(
    Output("edit-output", "children"),
    Input("grid", "cellEdited"),
    prevent_initial_call=True,
)
def show_edit(cell_edited):
    if cell_edited:
        return f"Edited cell [{cell_edited['col']}, {cell_edited['row']}]: {cell_edited['value']}"
    return "No edits yet"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
