"""
Example 42: High-Performance Cell Updates

Demonstrates three methods for updating grid cells, comparing their performance:
1. Selective (direct ref) - Only redraw changed cells (fastest)
2. Full (direct ref) - Redraw all cells (slower, depends on grid size)
3. redrawTrigger (React) - Update via React prop (slowest)

The animation runs entirely client-side using requestAnimationFrame.
For best performance, run with a production server (not debug mode).

Run with: python examples/42_high_perf_animations.py
"""

from dash import Dash, html, dcc, Input, Output, clientside_callback, callback
import math

from dash_glide_grid import GlideGrid

app = Dash(__name__, assets_folder="assets")


def get_grid_dimensions(total_cells):
    """Calculate rows/cols for a given cell count (roughly 2:1 aspect ratio)."""
    cols = int(math.sqrt(total_cells * 2))
    rows = total_cells // cols
    return rows, cols


def generate_grid_data(total_cells):
    """Generate columns and data for a given cell count."""
    rows, cols = get_grid_dimensions(total_cells)
    columns = [{"title": "", "width": 4, "id": f"col_{i}"} for i in range(cols)]
    data = [{f"col_{j}": "" for j in range(cols)} for _ in range(rows)]
    return columns, data, rows, cols


# Default grid size
DEFAULT_CELLS = 10000
columns, data, NUM_ROWS, NUM_COLS = generate_grid_data(DEFAULT_CELLS)

app.layout = html.Div(
    [
        html.H1("High-Performance Cell Updates"),
        html.Div(
            [
                html.P(
                    [
                        "Grid: ",
                        html.Span(id="grid-size-display", children=f"{NUM_ROWS:,} x {NUM_COLS} = {NUM_ROWS * NUM_COLS:,}"),
                        " cells. Random cells pulse at your display's refresh rate. ",
                        "Switch between methods to compare performance. ",
                        html.Strong("Tip: "),
                        "For best performance, run with a production server (not debug mode).",
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
                            "Method:",
                            style={"fontWeight": "bold", "marginRight": "10px"},
                        ),
                        dcc.RadioItems(
                            id="update-method",
                            options=[
                                {
                                    "label": " Selective (direct ref)",
                                    "value": "selective",
                                },
                                {
                                    "label": " Full (direct ref)",
                                    "value": "full",
                                },
                                {
                                    "label": " redrawTrigger (React)",
                                    "value": "react",
                                },
                            ],
                            value="selective",
                            inline=True,
                            inputStyle={"marginRight": "5px"},
                            labelStyle={"marginRight": "20px"},
                        ),
                    ],
                    style={"marginBottom": "10px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Grid cells:",
                            style={"fontWeight": "bold", "marginRight": "10px"},
                        ),
                        dcc.Dropdown(
                            id="cell-count",
                            options=[
                                {"label": "100", "value": 100},
                                {"label": "1,000", "value": 1000},
                                {"label": "10,000", "value": 10000},
                                {"label": "50,000", "value": 50000},
                                {"label": "100,000", "value": 100000},
                            ],
                            value=DEFAULT_CELLS,
                            clearable=False,
                            style={"width": "120px"},
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                html.Div(
                    [
                        html.Label(
                            "New pulses per frame:",
                            style={"fontWeight": "bold", "marginRight": "10px"},
                        ),
                        dcc.Slider(
                            id="pulses-per-frame",
                            min=1,
                            max=100,
                            step=1,
                            value=20,
                            marks={1: "1", 25: "25", 50: "50", 100: "100"},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "250px"},
                ),
                html.Div(
                    [
                        html.Button(
                            "Start",
                            id="start-btn",
                            n_clicks=0,
                            style={"marginRight": "10px"},
                        ),
                        html.Button("Stop", id="stop-btn", n_clicks=0),
                    ],
                ),
            ],
            style={
                "display": "flex",
                "gap": "30px",
                "alignItems": "flex-start",
                "backgroundColor": "#f8fafc",
                "padding": "15px",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "flexWrap": "wrap",
            },
        ),
        html.Div(
            [
                html.Strong("FPS: "),
                html.Span(id="fps-display", children="--"),
                html.Span(" | ", style={"margin": "0 10px", "color": "#ccc"}),
                html.Strong("Active pulses: "),
                html.Span(id="pulse-count", children="0"),
                html.Span(" | ", style={"margin": "0 10px", "color": "#ccc"}),
                html.Strong("Frame: "),
                html.Span(id="frame-count", children="0"),
                html.Span(" | ", style={"margin": "0 10px", "color": "#ccc"}),
                html.Strong("Method: "),
                html.Span(id="current-method", children="selective"),
            ],
            style={
                "fontFamily": "monospace",
                "fontSize": "13px",
                "marginBottom": "15px",
            },
        ),
        # Hidden elements for state
        html.Div(id="animation-output", style={"display": "none"}),
        dcc.Store(id="grid-dims", data={"rows": NUM_ROWS, "cols": NUM_COLS}),
        GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=600,
            rowMarkers="none",
            rowHeight=4,
            headerHeight=0,
            theme={
                "bgCell": "#1e293b",
                "borderColor": "#334155",
                "textDark": "#64748b",
            },
            drawCell={
                "function": "drawPulsingCell(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent)"
            },
            experimental={"disableMinimumCellWidth": True},
        ),
        html.Hr(),
        html.H2("Compare the Methods"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "Selective (direct ref)",
                            style={"color": "#10b981", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Calls gridRef.updateCells() directly"),
                                html.Li("Bypasses React entirely"),
                                html.Li("Only redraws cells that changed"),
                                html.Li("60-120fps depending on pulse count"),
                            ],
                            style={"marginBottom": "0"},
                        ),
                    ],
                    style={
                        "flex": "1",
                        "backgroundColor": "#f0fdf4",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "border": "1px solid #10b981",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            "Full (direct ref)",
                            style={"color": "#f59e0b", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Also calls gridRef.updateCells() directly"),
                                html.Li("Redraws ALL cells every frame"),
                                html.Li("FPS depends on grid size"),
                                html.Li("Use when most cells change at once"),
                            ],
                            style={"marginBottom": "0"},
                        ),
                    ],
                    style={
                        "flex": "1",
                        "backgroundColor": "#fffbeb",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "border": "1px solid #f59e0b",
                    },
                ),
                html.Div(
                    [
                        html.H3(
                            "redrawTrigger (React)",
                            style={"color": "#ef4444", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Updates via React prop"),
                                html.Li("Goes through React reconciliation"),
                                html.Li("Slowest - React overhead"),
                                html.Li("Simple, but not for animations"),
                            ],
                            style={"marginBottom": "0"},
                        ),
                    ],
                    style={
                        "flex": "1",
                        "backgroundColor": "#fef2f2",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "border": "1px solid #ef4444",
                    },
                ),
            ],
            style={"display": "flex", "gap": "15px"},
        ),
        html.Div(
            [
                html.H3("How it works", style={"marginTop": "20px"}),
                html.P(
                    [
                        "The key to 120fps animations is bypassing React. GlideGrid exposes ",
                        html.Code("window._glideGridRefs[id]"),
                        " which gives direct access to the DataEditor's ",
                        html.Code("updateCells()"),
                        " method. This avoids React reconciliation overhead entirely.",
                    ]
                ),
                html.Pre(
                    "// Direct call - 120fps capable\n"
                    "const gridRef = window._glideGridRefs['grid'];\n"
                    "gridRef.updateCells([{cell: [col, row]}, ...]);",
                    style={
                        "backgroundColor": "#1e293b",
                        "color": "#e2e8f0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "overflow": "auto",
                    },
                ),
            ]
        ),
    ],
    style={"padding": "20px", "maxWidth": "1400px", "margin": "0 auto"},
)


# Callback to update grid size when dropdown changes
@callback(
    Output("grid", "columns"),
    Output("grid", "data"),
    Output("grid-dims", "data"),
    Output("grid-size-display", "children"),
    Input("cell-count", "value"),
)
def update_grid_size(total_cells):
    columns, data, rows, cols = generate_grid_data(total_cells)
    dims = {"rows": rows, "cols": cols}
    display = f"{rows:,} x {cols} = {rows * cols:,}"
    return columns, data, dims, display


# Single callback to handle start/stop and animation
clientside_callback(
    """
    function(startClicks, stopClicks, method, pulsesPerFrame, gridDims) {
        // Initialize animation system once
        if (!window._animState) {
            window._animState = {
                frameCount: 0,
                lastFpsUpdate: performance.now(),
                lastRedrawTime: 0,
                fpsFrameCount: 0,
                currentFps: 0,
                rafId: null,
                running: false,
                method: "selective",
                pulsesPerFrame: 20,
                numRows: 0,
                numCols: 0
            };
            window.pulsingCells = {};
        }

        const animState = window._animState;

        // Update grid dimensions from store (reset allCells cache if changed)
        const numRows = gridDims?.rows || 100;
        const numCols = gridDims?.cols || 100;
        if (animState.numRows !== numRows || animState.numCols !== numCols) {
            animState.numRows = numRows;
            animState.numCols = numCols;
            window._allCells = null;  // Reset cache when grid size changes
            window.pulsingCells = {};  // Clear active pulses
        }
        const pulseDuration = 600;

        // Update settings
        animState.method = method;
        animState.pulsesPerFrame = pulsesPerFrame;

        // Determine if we should start or stop
        const ctx = dash_clientside.callback_context;
        if (ctx.triggered && ctx.triggered.length > 0) {
            const triggerId = ctx.triggered[0].prop_id.split('.')[0];
            if (triggerId === 'start-btn') {
                animState.running = true;
            } else if (triggerId === 'stop-btn') {
                animState.running = false;
            }
        }

        // If not running, cancel any existing animation
        if (!animState.running) {
            if (animState.rafId) {
                cancelAnimationFrame(animState.rafId);
                animState.rafId = null;
            }
            return "stopped";
        }

        // Already running, don't start another loop
        if (animState.rafId) {
            return "already running";
        }

        function animate() {
            // Get direct grid ref (exposed by GlideGrid component for high-perf access)
            const gridRef = window._glideGridRefs?.['grid'];

            // Find setProps for redrawTrigger method (fallback)
            const gridEl = document.getElementById('grid');
            let setProps = gridEl?._dashprivate_setProps;
            if (!setProps && gridEl) {
                const key = Object.keys(gridEl).find(k => k.startsWith('__reactFiber$'));
                if (key) {
                    let fiber = gridEl[key];
                    while (fiber) {
                        if (fiber.memoizedProps?.setProps) {
                            setProps = fiber.memoizedProps.setProps;
                            break;
                        }
                        fiber = fiber.return;
                    }
                }
            }

            if (!gridRef && !setProps) {
                animState.rafId = requestAnimationFrame(animate);
                return;
            }

            if (!animState.running) {
                animState.rafId = null;
                return;
            }

            const now = performance.now();
            animState.frameCount++;

            // Calculate FPS every second (counts actual redraws, not RAF frames)
            if (now - animState.lastFpsUpdate >= 1000) {
                animState.currentFps = animState.fpsFrameCount;
                animState.fpsFrameCount = 0;
                animState.lastFpsUpdate = now;

                // Update displays directly (faster than Dash callbacks)
                const fpsEl = document.getElementById('fps-display');
                const methodEl = document.getElementById('current-method');
                if (fpsEl) fpsEl.textContent = animState.currentFps;
                if (methodEl) methodEl.textContent = animState.method;
            }

            // Add new random pulses (use animState dimensions so changes take effect immediately)
            for (let i = 0; i < animState.pulsesPerFrame; i++) {
                const row = Math.floor(Math.random() * animState.numRows);
                const col = Math.floor(Math.random() * animState.numCols);
                const key = col + "," + row;
                window.pulsingCells[key] = { startTime: now, duration: pulseDuration };
            }

            // Get active pulses and clean up expired ones
            const activeCells = [];
            for (const key in window.pulsingCells) {
                const pulse = window.pulsingCells[key];
                const elapsed = now - pulse.startTime;
                if (elapsed < pulse.duration) {
                    const parts = key.split(",");
                    activeCells.push([parseInt(parts[0]), parseInt(parts[1])]);
                } else {
                    delete window.pulsingCells[key];
                }
            }

            // Update displays directly
            const countEl = document.getElementById('pulse-count');
            const frameEl = document.getElementById('frame-count');
            if (countEl) countEl.textContent = activeCells.length;
            if (frameEl) frameEl.textContent = animState.frameCount;

            // Cache render time ONCE before setProps (used by all cells in drawPulsingCell)
            window._renderTime = now;

            // No throttling - run at full RAF speed to demonstrate true performance
            if (activeCells.length > 0) {
                animState.fpsFrameCount++;  // Count actual redraws
                if (animState.method === "selective" && gridRef) {
                    // Selective: only redraw changed cells (bypasses React)
                    gridRef.updateCells(activeCells.map(c => ({ cell: c })));
                } else if (animState.method === "full" && gridRef) {
                    // Full: redraw ALL cells (bypasses React)
                    if (!window._allCells) {
                        window._allCells = [];
                        for (let row = 0; row < animState.numRows; row++) {
                            for (let col = 0; col < animState.numCols; col++) {
                                window._allCells.push({ cell: [col, row] });
                            }
                        }
                    }
                    gridRef.updateCells(window._allCells);
                } else if (animState.method === "react" && setProps) {
                    // React: update via redrawTrigger prop (goes through React)
                    setProps({redrawTrigger: animState.frameCount});
                }
            }

            // Schedule next frame
            animState.rafId = requestAnimationFrame(animate);
        }

        // Start animation loop
        animState.rafId = requestAnimationFrame(animate);

        return "started";
    }
    """,
    Output("animation-output", "children"),
    Input("start-btn", "n_clicks"),
    Input("stop-btn", "n_clicks"),
    Input("update-method", "value"),
    Input("pulses-per-frame", "value"),
    Input("grid-dims", "data"),
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
