"""
Example 71: Performance Stress Test — Multiple Grids

Demonstrates how column resize FPS degrades when many DGG grids are on the
same page.  Increase the grid count, then drag-resize a column to observe
the slowdown.

Root cause: GlideGrid is not wrapped in React.memo, so *every* grid
re-renders on each setProps({columnWidths}) call — even grids whose props
haven't changed.  Column resize fires setProps on every pixel of drag,
compounding the cost.

Run with: python examples/71_perf_stress_test.py
"""

from dash import Dash, html, dcc, Input, Output, clientside_callback

from dash_glide_grid import GlideGrid

app = Dash(__name__, assets_folder="assets")

NUM_COLS = 10
NUM_ROWS = 20
MAX_GRIDS = 10

columns = [
    {"title": f"Col {i}", "width": 120, "id": f"col_{i}"}
    for i in range(NUM_COLS)
]
data = [
    {f"col_{j}": f"R{i}C{j}" for j in range(NUM_COLS)}
    for i in range(NUM_ROWS)
]


def make_grid(index, with_animation=False):
    """Create a GlideGrid with optional drawCell animation."""
    props = dict(
        id=f"grid-{index}",
        columns=columns,
        data=data,
        height=300,
        columnResize=True,
        rowMarkers="number",
        lazyLoad=True,
    )
    if with_animation:
        props["drawCell"] = {
            "function": "drawPulsingCell(ctx, cell, theme, rect, col, row, "
            "hoverAmount, highlighted, cellData, rowData, drawContent)"
        }
    return html.Div(
        [
            html.H4(
                f"Grid {index}" + (" (animated)" if with_animation else ""),
                style={"margin": "8px 0 4px"},
            ),
            GlideGrid(**props),
        ],
        id=f"grid-wrapper-{index}",
        style={"marginBottom": "16px"},
    )


app.layout = html.Div(
    [
        html.H1("Performance Stress Test — Multiple Grids"),
        html.Div(
            [
                html.P(
                    [
                        "Drag-resize any column, then increase the grid count. ",
                        "Without React.memo every grid re-renders on each resize pixel, ",
                        "so FPS drops as you add grids.",
                    ],
                    style={"margin": "0"},
                ),
            ],
            style={
                "backgroundColor": "#dbeafe",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "20px",
                "border": "1px solid #3b82f6",
            },
        ),
        # Controls
        html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Number of grids:",
                            style={"fontWeight": "bold"},
                        ),
                        dcc.Slider(
                            id="grid-count",
                            min=1,
                            max=MAX_GRIDS,
                            step=1,
                            value=1,
                            marks={i: str(i) for i in range(1, MAX_GRIDS + 1)},
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                            },
                        ),
                    ],
                    style={"flex": "1", "minWidth": "300px"},
                ),
                html.Div(
                    [
                        html.Button(
                            "Start Animation",
                            id="start-btn",
                            n_clicks=0,
                            style={"marginRight": "10px"},
                        ),
                        html.Button(
                            "Stop",
                            id="stop-btn",
                            n_clicks=0,
                            style={"marginRight": "10px"},
                        ),
                        html.Button(
                            "Flash Random Cells",
                            id="flash-btn",
                            n_clicks=0,
                        ),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "gap": "30px",
                "alignItems": "center",
                "backgroundColor": "#f8fafc",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "flexWrap": "wrap",
            },
        ),
        # Metrics
        html.Div(
            [
                html.Strong("FPS: "),
                html.Span(id="fps-display", children="--"),
                html.Span(
                    " | ", style={"margin": "0 10px", "color": "#ccc"}
                ),
                html.Strong("Visible grids: "),
                html.Span(id="grid-display", children="1"),
            ],
            style={
                "fontFamily": "monospace",
                "fontSize": "13px",
                "marginBottom": "15px",
            },
        ),
        # Hidden outputs
        html.Div(id="animation-output", style={"display": "none"}),
        html.Div(id="flash-output", style={"display": "none"}),
        # All grids (hidden via CSS when not active)
        html.Div(
            id="grids-container",
            children=[make_grid(i, with_animation=(i == 0)) for i in range(MAX_GRIDS)],
        ),
    ],
    style={"padding": "20px", "maxWidth": "1400px", "margin": "0 auto"},
)

# Show/hide grids based on slider
clientside_callback(
    """
    function(count) {
        var container = document.getElementById('grids-container');
        if (container) {
            for (var i = 0; i < container.children.length; i++) {
                container.children[i].style.display = i < count ? 'block' : 'none';
            }
        }
        return String(count);
    }
    """,
    Output("grid-display", "children"),
    Input("grid-count", "value"),
)

# Flash random cells on grid-0 using the DGG imperative API
clientside_callback(
    """
    function(n) {
        if (!n) return '';
        var gridApi = window.dashGlideGrid && window.dashGlideGrid['grid-0'];
        if (!gridApi) return 'no grid';
        var updates = [];
        for (var i = 0; i < 30; i++) {
            var row = Math.floor(Math.random() * """
    + str(NUM_ROWS)
    + """);
            var colIdx = Math.floor(Math.random() * """
    + str(NUM_COLS)
    + """);
            var obj = {};
            obj['col_' + colIdx] = 'FLASH';
            updates.push({ row: row, data: obj, flash: '#10b981' });
        }
        gridApi.updateCells(updates);
        return 'flashed ' + n;
    }
    """,
    Output("flash-output", "children"),
    Input("flash-btn", "n_clicks"),
)

# Animation loop — pulse random cells on grid-0 via drawCell
clientside_callback(
    """
    function(startClicks, stopClicks) {
        if (!window._perfAnimState) {
            window._perfAnimState = {
                rafId: null,
                running: false,
                fpsFrameCount: 0,
                lastFpsUpdate: performance.now()
            };
            window.pulsingCells = window.pulsingCells || {};
        }

        var state = window._perfAnimState;
        var ctx = dash_clientside.callback_context;
        if (ctx.triggered && ctx.triggered.length > 0) {
            var id = ctx.triggered[0].prop_id.split('.')[0];
            if (id === 'start-btn') state.running = true;
            if (id === 'stop-btn') state.running = false;
        }

        if (!state.running) {
            if (state.rafId) { cancelAnimationFrame(state.rafId); state.rafId = null; }
            return 'stopped';
        }
        if (state.rafId) return 'already running';

        function animate() {
            if (!state.running) { state.rafId = null; return; }

            var gridRef = window.dashGlideGrid && window.dashGlideGrid['grid-0'] && window.dashGlideGrid['grid-0'].ref;
            if (!gridRef) { state.rafId = requestAnimationFrame(animate); return; }

            var now = performance.now();
            state.fpsFrameCount++;

            if (now - state.lastFpsUpdate >= 1000) {
                var fpsEl = document.getElementById('fps-display');
                if (fpsEl) fpsEl.textContent = state.fpsFrameCount;
                state.fpsFrameCount = 0;
                state.lastFpsUpdate = now;
            }

            // Add random pulses
            for (var i = 0; i < 10; i++) {
                var row = Math.floor(Math.random() * """
    + str(NUM_ROWS)
    + """);
                var col = Math.floor(Math.random() * """
    + str(NUM_COLS)
    + """);
                window.pulsingCells[col + ',' + row] = { startTime: now, duration: 600 };
            }

            // Collect active cells
            var cells = [];
            for (var key in window.pulsingCells) {
                if (now - window.pulsingCells[key].startTime < window.pulsingCells[key].duration) {
                    var p = key.split(',');
                    cells.push({ cell: [parseInt(p[0]), parseInt(p[1])] });
                } else {
                    delete window.pulsingCells[key];
                }
            }

            window._renderTime = now;
            if (cells.length > 0) gridRef.updateCells(cells);

            state.rafId = requestAnimationFrame(animate);
        }

        state.rafId = requestAnimationFrame(animate);
        return 'started';
    }
    """,
    Output("animation-output", "children"),
    Input("start-btn", "n_clicks"),
    Input("stop-btn", "n_clicks"),
)


if __name__ == "__main__":
    app.run(debug=True, port=8071)
