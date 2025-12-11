"""
Example: Hover Events Debug

A diagnostic tool for testing itemHovered behavior with various click patterns.
Tests single clicks, double clicks, rapid clicks, and shows when hover events
stop firing (a known issue when double-clicking).

This example helps diagnose issues like:
- Hover events stopping after double-click
- Hover state getting "stuck" on a cell
- itemHovered not firing after certain interactions
"""

import dash
from dash import html, callback, Input, Output, State, dcc
import dash_glide_grid as dgg
from datetime import datetime

app = dash.Dash(__name__)

COLUMNS = [
    {"title": "A", "id": "col_a", "width": 100},
    {"title": "B", "id": "col_b", "width": 100},
    {"title": "C", "id": "col_c", "width": 100},
    {"title": "D", "id": "col_d", "width": 100},
]

DATA = [
    {"col_a": f"A{i}", "col_b": f"B{i}", "col_c": f"C{i}", "col_d": f"D{i}"}
    for i in range(6)
]

app.layout = html.Div(
    [
        html.H1("Hover Events Debug Tool"),
        html.P(
            [
                "This tool helps diagnose hover event issues. ",
                html.Strong("Try these tests:"),
            ]
        ),
        html.Ol(
            [
                html.Li("Move mouse around - watch 'itemHovered Events' log"),
                html.Li("Single-click a cell - hover should continue working"),
                html.Li("Double-click a cell - check if hover events stop firing"),
                html.Li("Click outside grid and back - check if hover resumes"),
            ]
        ),
        html.Div(
            [
                html.Button("Clear Logs", id="clear-logs", n_clicks=0),
                html.Button("Reset Grid", id="reset-grid", n_clicks=0),
                html.Button("Toggle Readonly", id="toggle-readonly", n_clicks=0),
                html.Button("Toggle allowOverlay", id="toggle-overlay", n_clicks=0),
                html.Span(
                    id="grid-status",
                    children=" (editable, overlay ON)",
                    style={"marginLeft": "10px", "fontWeight": "bold"},
                ),
            ],
            style={"marginBottom": "10px"},
        ),
        html.Div(
            [
                # Grid
                html.Div(
                    [
                        dgg.GlideGrid(
                            id="debug-grid",
                            columns=COLUMNS,
                            data=DATA,
                            height=250,
                            rowHeight=40,
                            headerHeight=35,
                            rowMarkers="number",
                            readonly=False,
                        ),
                    ],
                    style={"flex": "1", "marginRight": "20px"},
                ),
                # Event counters
                html.Div(
                    [
                        html.H4("Event Counters"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Strong("itemHovered: "),
                                        html.Span(id="hover-count", children="0"),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Strong("nClicks: "),
                                        html.Span(id="click-count", children="0"),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Strong("cellActivated: "),
                                        html.Span(id="activated-count", children="0"),
                                    ]
                                ),
                            ],
                            style={
                                "fontFamily": "monospace",
                                "padding": "10px",
                                "backgroundColor": "#f0f0f0",
                                "marginBottom": "10px",
                            },
                        ),
                        html.H4("Current State"),
                        html.Div(
                            id="current-state",
                            style={
                                "fontFamily": "monospace",
                                "padding": "10px",
                                "backgroundColor": "#e8f4e8",
                                "fontSize": "12px",
                                "whiteSpace": "pre-wrap",
                            },
                        ),
                    ],
                    style={"width": "250px"},
                ),
            ],
            style={"display": "flex", "margin": "20px"},
        ),
        # Event log
        html.Div(
            [
                html.H4("Event Log (newest first)"),
                html.Div(
                    id="event-log",
                    style={
                        "fontFamily": "monospace",
                        "fontSize": "11px",
                        "padding": "10px",
                        "backgroundColor": "#1e1e1e",
                        "color": "#d4d4d4",
                        "height": "300px",
                        "overflowY": "auto",
                        "whiteSpace": "pre-wrap",
                    },
                ),
            ],
            style={"margin": "20px"},
        ),
        # Stores for tracking
        dcc.Store(id="event-log-store", data=[]),
        dcc.Store(id="hover-counter", data=0),
        dcc.Store(id="click-counter", data=0),
        dcc.Store(id="activated-counter", data=0),
        dcc.Store(id="last-hover", data=None),
        dcc.Store(id="last-click", data=None),
        dcc.Store(id="last-activated", data=None),
        dcc.Store(id="grid-readonly", data=False),
        dcc.Store(id="grid-allow-overlay", data=True),
        html.Div(
            [
                html.H4("Known Issues & Tips"),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.Strong("Double-click stops hover: "),
                                "After double-clicking a cell, itemHovered may stop firing. ",
                                "This appears to be related to glide-data-grid's internal state management.",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("Workaround: "),
                                "For applications that need reliable hover after double-click, ",
                                "implement manual pointermove tracking on the grid container.",
                            ]
                        ),
                        html.Li(
                            [
                                html.Strong("allowOverlay vs readonly: "),
                                "To fully prevent the overlay popup on double-click, you need BOTH: ",
                                "readonly=True on the grid AND allowOverlay=False in cell data (with kind='text').",
                            ]
                        ),
                    ]
                ),
            ],
            style={
                "margin": "20px",
                "padding": "15px",
                "backgroundColor": "#fff3cd",
                "borderRadius": "5px",
            },
        ),
    ]
)


def format_timestamp():
    return datetime.now().strftime("%H:%M:%S.%f")[:-3]


@callback(
    Output("event-log-store", "data"),
    Output("hover-counter", "data"),
    Output("last-hover", "data"),
    Input("debug-grid", "itemHovered"),
    State("event-log-store", "data"),
    State("hover-counter", "data"),
    prevent_initial_call=True,
)
def log_hover(item_hovered, log, count):
    if not item_hovered:
        return log, count, None

    count += 1
    kind = item_hovered.get("kind", "?")
    col = item_hovered.get("col")
    row = item_hovered.get("row")
    timestamp = item_hovered.get("timestamp", 0)

    entry = f"[{format_timestamp()}] HOVER #{count}: kind={kind}, col={col}, row={row}, ts={timestamp}"

    log = [entry] + log[:99]  # Keep last 100 entries
    return log, count, item_hovered


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("click-counter", "data"),
    Output("last-click", "data"),
    Input("debug-grid", "nClicks"),
    State("event-log-store", "data"),
    State("click-counter", "data"),
    State("debug-grid", "cellClicked"),
    prevent_initial_call=True,
)
def log_click(n_clicks, log, count, cell_clicked):
    if not n_clicks:
        return log, count, None

    count = n_clicks
    col = cell_clicked.get("col") if cell_clicked else "?"
    row = cell_clicked.get("row") if cell_clicked else "?"

    entry = f"[{format_timestamp()}] CLICK #{count}: col={col}, row={row}"

    log = [entry] + log[:99]
    return log, count, cell_clicked


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("activated-counter", "data"),
    Output("last-activated", "data"),
    Input("debug-grid", "cellActivated"),
    State("event-log-store", "data"),
    State("activated-counter", "data"),
    prevent_initial_call=True,
)
def log_activated(cell_activated, log, count):
    if not cell_activated:
        return log, count, None

    count += 1
    col = cell_activated.get("col")
    row = cell_activated.get("row")
    timestamp = cell_activated.get("timestamp", 0)

    entry = f"[{format_timestamp()}] ACTIVATED #{count}: col={col}, row={row}, ts={timestamp} (double-click/Enter)"

    log = [entry] + log[:99]
    return log, count, cell_activated


@callback(
    Output("event-log", "children"),
    Input("event-log-store", "data"),
)
def update_log_display(log):
    if not log:
        return "No events yet. Move mouse over the grid..."
    return "\n".join(log)


@callback(
    Output("hover-count", "children"),
    Input("hover-counter", "data"),
)
def update_hover_count(count):
    return str(count)


@callback(
    Output("click-count", "children"),
    Input("click-counter", "data"),
)
def update_click_count(count):
    return str(count)


@callback(
    Output("activated-count", "children"),
    Input("activated-counter", "data"),
)
def update_activated_count(count):
    return str(count)


@callback(
    Output("current-state", "children"),
    Input("last-hover", "data"),
    Input("last-click", "data"),
    Input("last-activated", "data"),
)
def update_current_state(last_hover, last_click, last_activated):
    lines = []

    if last_hover:
        lines.append(
            f"Hover: ({last_hover.get('col')}, {last_hover.get('row')}) [{last_hover.get('kind')}]"
        )
    else:
        lines.append("Hover: None")

    if last_click:
        lines.append(f"Last Click: ({last_click.get('col')}, {last_click.get('row')})")
    else:
        lines.append("Last Click: None")

    if last_activated:
        lines.append(
            f"Last Activated: ({last_activated.get('col')}, {last_activated.get('row')})"
        )
    else:
        lines.append("Last Activated: None")

    return "\n".join(lines)


@callback(
    Output("event-log-store", "data", allow_duplicate=True),
    Output("hover-counter", "data", allow_duplicate=True),
    Output("click-counter", "data", allow_duplicate=True),
    Output("activated-counter", "data", allow_duplicate=True),
    Output("last-hover", "data", allow_duplicate=True),
    Output("last-click", "data", allow_duplicate=True),
    Output("last-activated", "data", allow_duplicate=True),
    Input("clear-logs", "n_clicks"),
    prevent_initial_call=True,
)
def clear_logs(_):
    return [], 0, 0, 0, None, None, None


@callback(
    Output("debug-grid", "data"),
    Input("reset-grid", "n_clicks"),
    prevent_initial_call=True,
)
def reset_grid(_):
    # Return fresh data to force grid re-render
    return [
        {"col_a": f"A{i}", "col_b": f"B{i}", "col_c": f"C{i}", "col_d": f"D{i}"}
        for i in range(6)
    ]


@callback(
    Output("debug-grid", "readonly"),
    Output("grid-readonly", "data"),
    Input("toggle-readonly", "n_clicks"),
    State("grid-readonly", "data"),
    prevent_initial_call=True,
)
def toggle_readonly(n_clicks, current_readonly):
    new_readonly = not current_readonly
    return new_readonly, new_readonly


@callback(
    Output("grid-allow-overlay", "data"),
    Input("toggle-overlay", "n_clicks"),
    State("grid-allow-overlay", "data"),
    prevent_initial_call=True,
)
def toggle_overlay(n_clicks, current_overlay):
    return not current_overlay


@callback(
    Output("debug-grid", "data", allow_duplicate=True),
    Input("grid-allow-overlay", "data"),
    prevent_initial_call=True,
)
def update_data_overlay(allow_overlay):
    """Update cell data with allowOverlay setting."""
    return [
        {
            "col_a": {"kind": "text", "data": f"A{i}", "allowOverlay": allow_overlay},
            "col_b": {"kind": "text", "data": f"B{i}", "allowOverlay": allow_overlay},
            "col_c": {"kind": "text", "data": f"C{i}", "allowOverlay": allow_overlay},
            "col_d": {"kind": "text", "data": f"D{i}", "allowOverlay": allow_overlay},
        }
        for i in range(6)
    ]


@callback(
    Output("grid-status", "children"),
    Input("grid-readonly", "data"),
    Input("grid-allow-overlay", "data"),
)
def update_status(readonly, allow_overlay):
    readonly_str = "READONLY" if readonly else "editable"
    overlay_str = "overlay ON" if allow_overlay else "overlay OFF"
    return f" ({readonly_str}, {overlay_str})"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
