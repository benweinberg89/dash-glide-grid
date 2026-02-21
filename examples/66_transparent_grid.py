"""
Example 66: Transparent Grid
Demonstrates using rgba theme colors to make the grid translucent,
allowing an animated background to show through. Sliders let you
adjust the opacity of each theme element independently.

Includes a "Glass Panel" toggle that applies a glassmorphism effect
(backdrop-filter blur, subtle border, box-shadow) via the style prop,
matching the lc-glass-panel aesthetic.

Includes multiple editor types to verify bgCellEditor works across all of them.
"""

import dash
from dash import html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

STATUS_OPTIONS = ["active", "pending", "completed", "archived"]
TAG_DEFS = [
    {"tag": "Capital", "color": "#8b5cf6"},
    {"tag": "Coastal", "color": "#3b82f6"},
    {"tag": "Historic", "color": "#f97316"},
    {"tag": "Megacity", "color": "#ef4444"},
]

COLUMNS = [
    {"title": "City", "id": "city", "width": 140},
    {"title": "Country", "id": "country", "width": 140},
    {"title": "Population", "id": "population", "width": 120},
    {"title": "Status", "id": "status", "width": 120},
    {"title": "Tags", "id": "tags", "width": 180},
    {"title": "Founded", "id": "founded", "width": 130},
    {"title": "Rating", "id": "rating", "width": 110},
    {"title": "Growth", "id": "growth", "width": 120},
]

DATA = [
    {
        "city": "Tokyo",
        "country": "Japan",
        "population": 13960000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "active", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Megacity", "Capital"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "1457-01-01",
            "displayDate": "1457",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 5}},
        "growth": {
            "kind": "range-cell",
            "value": 82,
            "min": 0,
            "max": 100,
            "label": "82%",
        },
    },
    {
        "city": "Paris",
        "country": "France",
        "population": 2161000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "active", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Capital", "Historic"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "0259-01-01",
            "displayDate": "259 AD",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 5}},
        "growth": {
            "kind": "range-cell",
            "value": 35,
            "min": 0,
            "max": 100,
            "label": "35%",
        },
    },
    {
        "city": "New York",
        "country": "USA",
        "population": 8336000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "active", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Megacity", "Coastal"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "1624-01-01",
            "displayDate": "1624",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 4}},
        "growth": {
            "kind": "range-cell",
            "value": 45,
            "min": 0,
            "max": 100,
            "label": "45%",
        },
    },
    {
        "city": "Sydney",
        "country": "Australia",
        "population": 5312000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "completed", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {"kind": "tags-cell", "tags": ["Coastal"], "possibleTags": TAG_DEFS},
        "founded": {
            "kind": "date-picker-cell",
            "date": "1788-01-01",
            "displayDate": "1788",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 4}},
        "growth": {
            "kind": "range-cell",
            "value": 60,
            "min": 0,
            "max": 100,
            "label": "60%",
        },
    },
    {
        "city": "Cairo",
        "country": "Egypt",
        "population": 9540000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "pending", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Capital", "Historic", "Megacity"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "0969-01-01",
            "displayDate": "969 AD",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 3}},
        "growth": {
            "kind": "range-cell",
            "value": 72,
            "min": 0,
            "max": 100,
            "label": "72%",
        },
    },
    {
        "city": "London",
        "country": "UK",
        "population": 8982000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "active", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Capital", "Historic", "Megacity"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "0047-01-01",
            "displayDate": "47 AD",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 5}},
        "growth": {
            "kind": "range-cell",
            "value": 30,
            "min": 0,
            "max": 100,
            "label": "30%",
        },
    },
    {
        "city": "Mumbai",
        "country": "India",
        "population": 12478000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "active", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Megacity", "Coastal"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "1507-01-01",
            "displayDate": "1507",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 3}},
        "growth": {
            "kind": "range-cell",
            "value": 90,
            "min": 0,
            "max": 100,
            "label": "90%",
        },
    },
    {
        "city": "Istanbul",
        "country": "Turkey",
        "population": 15460000,
        "status": {
            "kind": "dropdown-cell",
            "data": {"value": "completed", "allowedValues": STATUS_OPTIONS},
        },
        "tags": {
            "kind": "tags-cell",
            "tags": ["Megacity", "Historic", "Coastal"],
            "possibleTags": TAG_DEFS,
        },
        "founded": {
            "kind": "date-picker-cell",
            "date": "0660-01-01",
            "displayDate": "660 AD",
        },
        "rating": {"kind": "star-cell", "data": {"rating": 4}},
        "growth": {
            "kind": "range-cell",
            "value": 68,
            "min": 0,
            "max": 100,
            "label": "68%",
        },
    },
]

BLOB_CONFIGS = [
    {
        "x": 200,
        "y": 200,
        "size": 180,
        "color": "#ff6b6b",
        "opacity": 0.35,
        "dur": "8s",
        "dx": 120,
        "dy": 80,
    },
    {
        "x": 500,
        "y": 300,
        "size": 150,
        "color": "#ffd93d",
        "opacity": 0.30,
        "dur": "10s",
        "dx": 100,
        "dy": 120,
    },
    {
        "x": 350,
        "y": 150,
        "size": 220,
        "color": "#6bcb77",
        "opacity": 0.25,
        "dur": "7s",
        "dx": 140,
        "dy": 60,
    },
    {
        "x": 150,
        "y": 400,
        "size": 160,
        "color": "#4d96ff",
        "opacity": 0.30,
        "dur": "12s",
        "dx": 90,
        "dy": 110,
    },
]

# Theme elements: (id_suffix, label, base_rgb, default_alpha_pct 0-100)
THEME_CONTROLS = [
    ("bgCell", "Cell Background", "255, 255, 255", 35),
    ("bgHeader", "Header Background", "255, 255, 255", 55),
    ("bgHeaderHasFocus", "Header Focus", "255, 255, 255", 65),
    ("bgHeaderHovered", "Header Hovered", "255, 255, 255", 60),
    ("bgCellMedium", "Cell Medium", "255, 255, 255", 25),
    ("borderColor", "Border", "255, 255, 255", 40),
    ("horizontalBorderColor", "Horizontal Border", "255, 255, 255", 30),
    ("accentLight", "Accent Light", "100, 180, 255", 25),
]


def make_blob(cfg, i):
    name = f"blob{i}"
    x, y = cfg["x"], cfg["y"]
    return html.Div(
        style={
            "position": "absolute",
            "left": f"{x}px",
            "top": f"{y}px",
            "width": f'{cfg["size"]}px',
            "height": f'{cfg["size"]}px',
            "borderRadius": "50%",
            "background": cfg["color"],
            "opacity": cfg["opacity"],
            "filter": "blur(2px)",
            "animation": f'{name} {cfg["dur"]} ease-in-out infinite',
        }
    )


def make_slider(id_suffix, label, default_pct):
    return html.Div(
        [
            html.Label(
                label,
                style={
                    "fontSize": "12px",
                    "color": "white",
                    "minWidth": "130px",
                    "textShadow": "1px 1px 2px black",
                },
            ),
            html.Div(
                dcc.Slider(
                    id=f"alpha-{id_suffix}",
                    min=0,
                    max=100,
                    step=5,
                    value=default_pct,
                    marks={0: "0%", 50: "50%", 100: "100%"},
                ),
                style={"flex": "1", "minWidth": "150px"},
            ),
        ],
        style={
            "display": "flex",
            "alignItems": "center",
            "gap": "8px",
            "marginBottom": "6px",
        },
    )


def hex_to_rgba(hex_color, alpha):
    """Convert hex color + alpha (0-100) to rgba string."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        return f"rgba(255, 255, 255, {alpha / 100})"
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"rgba({r}, {g}, {b}, {alpha / 100})"


# Build @keyframes CSS for each blob
keyframes_css = ""
for i, cfg in enumerate(BLOB_CONFIGS):
    name = f"blob{i}"
    dx, dy = cfg["dx"], cfg["dy"]
    keyframes_css += f"""
    @keyframes {name} {{
        0%   {{ transform: translate(0, 0); }}
        25%  {{ transform: translate({dx}px, {-dy}px); }}
        50%  {{ transform: translate({-dx//2}px, {dy}px); }}
        75%  {{ transform: translate({-dx}px, {-dy//2}px); }}
        100% {{ transform: translate(0, 0); }}
    }}
    """

app.index_string = (
    """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>"""
    + keyframes_css
    + """</style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
)

label_style = {
    "fontSize": "12px",
    "color": "white",
    "minWidth": "130px",
    "textShadow": "1px 1px 2px black",
}

GLASS_STYLE = {
    "backdropFilter": "blur(8px)",
    "WebkitBackdropFilter": "blur(8px)",
    "background": "rgba(0, 0, 0, 0.12)",
    "border": "1px solid rgba(255, 255, 255, 0.06)",
    "borderRadius": "16px",
    "overflow": "hidden",
    "boxShadow": "0 8px 32px rgba(0, 0, 0, 0.12), 0 2px 8px rgba(0, 0, 0, 0.06)",
}

slider_panel = html.Div(
    [
        html.H4(
            "Theme Opacity",
            style={
                "color": "white",
                "margin": "0 0 10px 0",
                "textShadow": "1px 1px 2px black",
            },
        ),
        html.Div(
            [
                dcc.Checklist(
                    id="glass-toggle",
                    options=[{"label": " Glass Panel", "value": "glass"}],
                    value=[],
                    style={"color": "white", "fontSize": "14px"},
                    inputStyle={"marginRight": "6px"},
                ),
            ],
            style={"marginBottom": "10px"},
        ),
        *[make_slider(tc[0], tc[1], tc[3]) for tc in THEME_CONTROLS],
        html.Hr(
            style={
                "border": "none",
                "borderTop": "1px solid rgba(255,255,255,0.2)",
                "margin": "10px 0",
            }
        ),
        html.Div(
            [
                html.Label("Editor Background", style=label_style),
                dcc.Input(
                    id="editor-bg-color",
                    type="text",
                    value="#ffffff",
                    placeholder="#rrggbb",
                    debounce=True,
                    style={
                        "width": "80px",
                        "height": "28px",
                        "border": "1px solid rgba(255,255,255,0.3)",
                        "borderRadius": "4px",
                        "background": "rgba(0,0,0,0.2)",
                        "color": "white",
                        "fontSize": "12px",
                        "padding": "0 6px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "8px",
                "marginBottom": "6px",
            },
        ),
        html.Div(
            [
                html.Label("Editor Opacity", style=label_style),
                html.Div(
                    dcc.Slider(
                        id="editor-bg-alpha",
                        min=0,
                        max=100,
                        step=5,
                        value=100,
                        marks={0: "0%", 50: "50%", 100: "100%"},
                    ),
                    style={"flex": "1", "minWidth": "150px"},
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "8px",
                "marginBottom": "6px",
            },
        ),
        html.Div(
            "Double-click cells to open editors",
            style={
                "fontSize": "11px",
                "color": "rgba(255,255,255,0.5)",
                "marginTop": "8px",
                "textShadow": "1px 1px 2px black",
            },
        ),
    ],
    style={
        "width": "380px",
        "background": "rgba(0, 0, 0, 0.3)",
        "borderRadius": "12px",
        "padding": "16px",
        "backdropFilter": "blur(10px)",
    },
)

app.layout = html.Div(
    [
        html.H2(
            "Transparent Grid",
            style={
                "color": "white",
                "textShadow": "1px 1px 3px black",
                "position": "relative",
                "zIndex": 1,
                "margin": "0 0 20px 0",
            },
        ),
        html.Div(
            [
                html.Div(
                    dgg.GlideGrid(
                        id="transparent-grid",
                        columns=COLUMNS,
                        data=DATA,
                        height=350,
                        rowMarkers="number",
                        smoothScrollX=True,
                        smoothScrollY=True,
                        theme={
                            "bgCell": f"rgba({THEME_CONTROLS[0][2]}, {THEME_CONTROLS[0][3] / 100})",
                            "bgHeader": f"rgba({THEME_CONTROLS[1][2]}, {THEME_CONTROLS[1][3] / 100})",
                            "bgHeaderHasFocus": f"rgba({THEME_CONTROLS[2][2]}, {THEME_CONTROLS[2][3] / 100})",
                            "bgHeaderHovered": f"rgba({THEME_CONTROLS[3][2]}, {THEME_CONTROLS[3][3] / 100})",
                            "bgCellMedium": f"rgba({THEME_CONTROLS[4][2]}, {THEME_CONTROLS[4][3] / 100})",
                            "borderColor": f"rgba({THEME_CONTROLS[5][2]}, {THEME_CONTROLS[5][3] / 100})",
                            "horizontalBorderColor": f"rgba({THEME_CONTROLS[6][2]}, {THEME_CONTROLS[6][3] / 100})",
                            "accentLight": f"rgba({THEME_CONTROLS[7][2]}, {THEME_CONTROLS[7][3] / 100})",
                            "textDark": "#1a1a2e",
                            "textHeader": "#1a1a2e",
                            "bgCellEditor": "#ffffff",
                        },
                    ),
                    style={"width": "900px"},
                ),
                slider_panel,
            ],
            style={
                "display": "flex",
                "gap": "24px",
                "alignItems": "flex-start",
                "position": "relative",
                "zIndex": 1,
            },
        ),
        # Animated blobs
        html.Div(
            [make_blob(cfg, i) for i, cfg in enumerate(BLOB_CONFIGS)],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "zIndex": 0,
                "overflow": "hidden",
                "pointerEvents": "none",
            },
        ),
    ],
    style={
        "margin": 0,
        "padding": "40px",
        "fontFamily": "Arial, sans-serif",
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "minHeight": "100vh",
        "position": "relative",
    },
)


@callback(
    Output("transparent-grid", "theme"),
    Output("transparent-grid", "style"),
    *[Input(f"alpha-{tc[0]}", "value") for tc in THEME_CONTROLS],
    Input("editor-bg-color", "value"),
    Input("editor-bg-alpha", "value"),
    Input("glass-toggle", "value"),
)
def update_theme(*args):
    pcts = args[: len(THEME_CONTROLS)]
    editor_hex = args[-3]
    editor_alpha = args[-2]
    glass_values = args[-1] or []
    glass_on = "glass" in glass_values

    theme = {
        "textDark": "#1a1a2e",
        "textHeader": "#1a1a2e",
        "bgCellEditor": hex_to_rgba(editor_hex or "#ffffff", editor_alpha),
    }
    for (key, _label, rgb, _default), pct in zip(THEME_CONTROLS, pcts):
        theme[key] = f"rgba({rgb}, {pct / 100})"

    if glass_on:
        # Override bgCell to transparent so the glass backdrop shows through
        theme["bgCell"] = "transparent"
        theme["bgCellMedium"] = "transparent"
        theme["bgHeader"] = "rgba(255, 255, 255, 0.08)"
        theme["bgHeaderHasFocus"] = "rgba(255, 255, 255, 0.12)"
        theme["bgHeaderHovered"] = "rgba(255, 255, 255, 0.10)"
        theme["borderColor"] = "rgba(255, 255, 255, 0.08)"
        theme["horizontalBorderColor"] = "rgba(255, 255, 255, 0.06)"
        theme["textDark"] = "rgba(255, 255, 255, 0.9)"
        theme["textHeader"] = "rgba(255, 255, 255, 0.9)"
        return theme, GLASS_STYLE

    return theme, {}


if __name__ == "__main__":
    app.run(debug=True, port=8066)
