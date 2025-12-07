"""
Example: Frozen Trailing Rows (Totals Row)

Demonstrates freezeTrailingRows to keep summary/totals rows visible at the bottom
while scrolling through data.
"""

import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

# Column definitions
COLUMNS = [
    {"title": "Product", "id": "product", "width": 150},
    {"title": "Category", "id": "category", "width": 120},
    {"title": "Jan", "id": "jan", "width": 80},
    {"title": "Feb", "id": "feb", "width": 80},
    {"title": "Mar", "id": "mar", "width": 80},
    {"title": "Q1 Total", "id": "q1_total", "width": 100},
]

# Generate sample data - enough rows to need scrolling
DATA = []
products = [
    ("Widget A", "Electronics"),
    ("Widget B", "Electronics"),
    ("Gadget X", "Hardware"),
    ("Gadget Y", "Hardware"),
    ("Tool 1", "Tools"),
    ("Tool 2", "Tools"),
    ("Part Alpha", "Parts"),
    ("Part Beta", "Parts"),
    ("Supply A", "Supplies"),
    ("Supply B", "Supplies"),
    ("Device 1", "Devices"),
    ("Device 2", "Devices"),
    ("Component X", "Components"),
    ("Component Y", "Components"),
    ("Accessory A", "Accessories"),
]

totals = {"Jan": 0, "Feb": 0, "Mar": 0, "Q1": 0}

for i, (product, category) in enumerate(products):
    jan = 1000 + (i * 150)
    feb = 1200 + (i * 120)
    mar = 1100 + (i * 180)
    q1 = jan + feb + mar
    DATA.append({
        "product": product,
        "category": category,
        "jan": jan,
        "feb": feb,
        "mar": mar,
        "q1_total": q1
    })
    totals["Jan"] += jan
    totals["Feb"] += feb
    totals["Mar"] += mar
    totals["Q1"] += q1

# Add totals row with bold styling hint
TOTALS_ROW = {
    "product": "TOTAL",
    "category": "",
    "jan": totals["Jan"],
    "feb": totals["Feb"],
    "mar": totals["Mar"],
    "q1_total": totals["Q1"]
}
DATA.append(TOTALS_ROW)

app.layout = html.Div([
    html.H1("Frozen Trailing Rows Example"),
    html.P("Scroll down to see more data - the TOTAL row stays fixed at the bottom!"),

    html.Div([
        dgg.GlideGrid(
            id="frozen-rows-grid",
            columns=COLUMNS,
            data=DATA,
            height=350,  # Small height to enable scrolling
            rowHeight=34,
            headerHeight=40,

            # Key feature: freeze the last row (totals)
            freezeTrailingRows=1,

            # Freeze first column too
            freezeColumns=1,

            # Show shadows behind frozen areas
            fixedShadowX=True,
            fixedShadowY=True,

            # Row markers with custom start index
            rowMarkers="number",
            rowMarkerStartIndex=1,
        ),
    ], style={"margin": "20px"}),

    html.Div([
        html.H4("Props used:"),
        html.Code("freezeTrailingRows=1"),
        html.P("This keeps the totals row visible at the bottom while scrolling."),
        html.Code("freezeColumns=1"),
        html.P("This keeps the Product column visible while scrolling horizontally."),
        html.Code("fixedShadowX=True, fixedShadowY=True"),
        html.P("Adds visual shadows to indicate frozen areas."),
    ], style={"margin": "20px", "padding": "20px", "backgroundColor": "#f5f5f5"}),
])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
