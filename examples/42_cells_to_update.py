"""
Example 42: cellsToUpdate vs redrawTrigger Performance Test

Demonstrates the performance difference between cellsToUpdate and redrawTrigger
using requestAnimationFrame for true 60fps animations. The animation runs entirely
client-side to eliminate server round-trip overhead.

Run with: python examples/42_cells_to_update.py
"""

from dash import Dash, html, dcc, Input, Output, clientside_callback

from dash_glide_grid import GlideGrid

app = Dash(__name__, assets_folder="assets")

# Grid size - 100k cells is too many for 120fps, try smaller
NUM_ROWS = 150
NUM_COLS = 300

columns = [{"title": "", "width": 4, "id": f"col_{i}"} for i in range(NUM_COLS)]
data = [{f"col_{j}": "" for j in range(NUM_COLS)} for _ in range(NUM_ROWS)]

app.layout = html.Div(
    [
        html.H1("cellsToUpdate vs redrawTrigger"),
        html.Div(
            [
                html.P(
                    [
                        f"Grid: {NUM_ROWS:,} x {NUM_COLS} = {NUM_ROWS * NUM_COLS:,} cells. ",
                        "Random cells pulse at your display's refresh rate. ",
                        "Switch between methods to compare performance.",
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
                                    "label": " cellsToUpdate (selective)",
                                    "value": "selective",
                                },
                                {
                                    "label": " redrawTrigger (full canvas)",
                                    "value": "full",
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
        # Hidden div for output (required by Dash)
        html.Div(id="animation-output", style={"display": "none"}),
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
                            "cellsToUpdate (direct)",
                            style={"color": "#10b981", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Calls gridRef.updateCells() directly"),
                                html.Li("Bypasses React entirely"),
                                html.Li("~120fps with 1-20 pulses/frame"),
                                html.Li("~60fps even at 100 pulses/frame"),
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
                            "redrawTrigger (React)",
                            style={"color": "#f59e0b", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Goes through React setProps"),
                                html.Li(f"Redraws all {NUM_ROWS * NUM_COLS:,} cells"),
                                html.Li("~10fps regardless of pulse count"),
                                html.Li("Use for infrequent full refreshes"),
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


# Single callback to handle start/stop and animation
clientside_callback(
    """
    function(startClicks, stopClicks, method, pulsesPerFrame) {
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
                pulsesPerFrame: 20
            };
            window.pulsingCells = {};
        }

        const animState = window._animState;
        const numRows = """
    + str(NUM_ROWS)
    + """;
        const numCols = """
    + str(NUM_COLS)
    + """;
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

            // Add new random pulses
            for (let i = 0; i < animState.pulsesPerFrame; i++) {
                const row = Math.floor(Math.random() * numRows);
                const col = Math.floor(Math.random() * numCols);
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
                    // Direct call to updateCells - bypasses React entirely!
                    gridRef.updateCells(activeCells.map(c => ({ cell: c })));
                } else {
                    // Full redraw via React (will be slower)
                    setProps({ redrawTrigger: animState.frameCount });
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
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
