"""
Example 29: Text Wrapping in Cells
Demonstrates the allowWrapping property for multi-line text in cells.
"""

import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "Name", "width": 120, "id": "name"},
    {"title": "Description (Wrapped)", "width": 250, "id": "description"},
    {"title": "Notes (Wrapped)", "width": 200, "id": "notes"},
    {"title": "Status", "width": 100, "id": "status"},
]

# Sample data with text wrapping and smaller notes column
DATA = [
    {
        "name": "Wireless Headphones Pro",
        "description": {
            "kind": "text",
            "data": "Premium over-ear wireless headphones with active noise cancellation, 30-hour battery life, and hi-res audio support. Features Bluetooth 5.2, multipoint connection for 2 devices, and foldable design for easy transport.",
            "allowWrapping": True,
        },
        "notes": {
            "kind": "text",
            "data": "Ships within 2-3 business days. 30-day return policy. 2-year manufacturer warranty included.",
            "allowWrapping": True,
            "themeOverride": {"baseFontStyle": "11px"},
        },
        "status": "Active",
    },
    {
        "name": "Mechanical Keyboard",
        "description": {
            "kind": "text",
            "data": "Full-size mechanical keyboard with Cherry MX Blue switches, RGB per-key backlighting, and aluminum frame. Includes detachable USB-C cable, magnetic wrist rest, and keycap puller.",
            "allowWrapping": True,
        },
        "notes": {
            "kind": "text",
            "data": "Available in Black, White, and Space Gray. Custom keycaps sold separately. Check compatibility before ordering.",
            "allowWrapping": True,
            "themeOverride": {"baseFontStyle": "11px"},
        },
        "status": "Active",
    },
    {
        "name": "4K Monitor 27-inch",
        "description": {
            "kind": "text",
            "data": "Professional-grade 27-inch 4K UHD monitor with IPS panel, 99% sRGB color accuracy, and USB-C power delivery up to 65W. Height adjustable stand with pivot and tilt. Built-in KVM switch.",
            "allowWrapping": True,
        },
        "notes": {
            "kind": "text",
            "data": "Requires DisplayPort 1.4 or HDMI 2.0 for 4K@60Hz. Stand sold separately for VESA mount version.",
            "allowWrapping": True,
            "themeOverride": {"baseFontStyle": "11px"},
        },
        "status": "Pending",
    },
    {
        "name": "USB-C Hub",
        "description": {
            "kind": "text",
            "data": "7-in-1 USB-C hub with 4K HDMI output, 100W power delivery passthrough, SD/microSD card readers, 2x USB-A 3.0 ports, and Gigabit Ethernet. Compact aluminum design with braided cable.",
            "allowWrapping": True,
        },
        "notes": {
            "kind": "text",
            "data": "Not compatible with Nintendo Switch. Some laptops may require USB-C with DisplayPort Alt Mode for video output.",
            "allowWrapping": True,
            "themeOverride": {"baseFontStyle": "11px"},
        },
        "status": "Active",
    },
    {
        "name": "Laptop Stand",
        "description": {
            "kind": "text",
            "data": "Ergonomic aluminum laptop stand with adjustable height and angle. Supports laptops from 10 to 17 inches. Improves airflow and reduces neck strain. Non-slip silicone pads protect your device.",
            "allowWrapping": True,
        },
        "notes": {
            "kind": "text",
            "data": "Weight capacity: 20 lbs. Foldable for travel. Cable management clips included.",
            "allowWrapping": True,
            "themeOverride": {"baseFontStyle": "11px"},
        },
        "status": "Active",
    },
]

app.layout = html.Div(
    [
        html.H1("Text Wrapping Example"),
        html.P(
            "This example demonstrates the allowWrapping property for text cells. "
            "When enabled, long text will wrap to multiple lines instead of being truncated."
        ),
        html.Div(
            [
                html.H3("Key Points:"),
                html.Ul(
                    [
                        html.Li(
                            "Set allowWrapping=True on text cell objects to enable multi-line display"
                        ),
                        html.Li("Increase rowHeight to accommodate wrapped text"),
                        html.Li(
                            "Use themeOverride with baseFontStyle for smaller text (e.g., '11px')"
                        ),
                        html.Li("Description column: default font size with wrapping"),
                        html.Li(
                            "Notes column: smaller 11px font for secondary information"
                        ),
                    ]
                ),
            ],
            style={
                "marginBottom": "20px",
                "backgroundColor": "#f9f9f9",
                "padding": "15px",
                "borderRadius": "4px",
            },
        ),
        dgg.GlideGrid(
            id="wrapping-grid",
            columns=COLUMNS,
            data=DATA,
            height=500,
            rowHeight=40,  # Taller rows to show wrapped text
            headerHeight=40,
            rowMarkers="number",
            columnResize=True,
        ),
        html.Div(
            [
                html.H4("How to use text wrapping:"),
                html.Pre(
                    """
# Description column - default font with wrapping:
{
    "kind": "text",
    "data": "Long product description that will wrap...",
    "allowWrapping": True
}

# Notes column - smaller font for secondary info:
{
    "kind": "text",
    "data": "Ships in 2-3 days. 30-day return policy.",
    "allowWrapping": True,
    "themeOverride": {"baseFontStyle": "11px"}
}

# Grid setup with taller rows:
dgg.GlideGrid(
    ...
    rowHeight=80,  # Taller rows for wrapped content
)
        """,
                    style={
                        "backgroundColor": "#282c34",
                        "color": "#abb2bf",
                        "padding": "15px",
                        "borderRadius": "4px",
                    },
                ),
            ],
            style={"marginTop": "30px"},
        ),
    ],
    style={"margin": "40px", "fontFamily": "Arial, sans-serif"},
)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
