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

# Larger grid to show performance difference
NUM_ROWS = 500
NUM_COLS = 100

columns = [{"title": "", "width": 12, "id": f"col_{i}"} for i in range(NUM_COLS)]
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
                        html.Label("Method:", style={"fontWeight": "bold", "marginRight": "10px"}),
                        dcc.RadioItems(
                            id="update-method",
                            options=[
                                {"label": " cellsToUpdate (selective)", "value": "selective"},
                                {"label": " redrawTrigger (full canvas)", "value": "full"},
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
                        html.Label("New pulses per frame:", style={"fontWeight": "bold", "marginRight": "10px"}),
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
                        html.Button("Start", id="start-btn", n_clicks=0, style={"marginRight": "10px"}),
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
            style={"fontFamily": "monospace", "fontSize": "13px", "marginBottom": "15px"},
        ),
        # Hidden div for output (required by Dash)
        html.Div(id="animation-output", style={"display": "none"}),
        GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=600,
            rowMarkers="none",
            rowHeight=12,
            headerHeight=0,
            theme={"bgCell": "#1e293b", "borderColor": "#334155", "textDark": "#64748b"},
            drawCell={"function": "drawPulsingCell(ctx, cell, theme, rect, col, row, hoverAmount, highlighted, cellData, rowData, drawContent)"},
        ),
        html.Hr(),
        html.H2("Compare the Methods"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("cellsToUpdate", style={"color": "#10b981", "marginTop": "0"}),
                        html.Ul([
                            html.Li("Redraws ONLY the pulsing cells"),
                            html.Li("~20-200 cells per frame"),
                            html.Li("Smooth animations at full refresh rate"),
                        ], style={"marginBottom": "0"}),
                    ],
                    style={"flex": "1", "backgroundColor": "#f0fdf4", "padding": "15px", "borderRadius": "8px", "border": "1px solid #10b981"},
                ),
                html.Div(
                    [
                        html.H3("redrawTrigger", style={"color": "#f59e0b", "marginTop": "0"}),
                        html.Ul([
                            html.Li(f"Redraws ALL {NUM_ROWS * NUM_COLS:,} cells"),
                            html.Li(f"{NUM_ROWS * NUM_COLS:,} cells per frame"),
                            html.Li("May stutter or drop frames"),
                        ], style={"marginBottom": "0"}),
                    ],
                    style={"flex": "1", "backgroundColor": "#fffbeb", "padding": "15px", "borderRadius": "8px", "border": "1px solid #f59e0b"},
                ),
            ],
            style={"display": "flex", "gap": "15px"},
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
                lastFpsUpdate: Date.now(),
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
        const numRows = """ + str(NUM_ROWS) + """;
        const numCols = """ + str(NUM_COLS) + """;
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
            const gridEl = document.getElementById('grid');
            if (!gridEl) {
                animState.rafId = requestAnimationFrame(animate);
                return;
            }

            // Find setProps via React fiber
            let setProps = gridEl._dashprivate_setProps;
            if (!setProps) {
                const key = Object.keys(gridEl).find(k => k.startsWith('__reactFiber$') || k.startsWith('__reactInternalInstance$'));
                if (key) {
                    let fiber = gridEl[key];
                    while (fiber) {
                        if (fiber.memoizedProps && fiber.memoizedProps.setProps) {
                            setProps = fiber.memoizedProps.setProps;
                            break;
                        }
                        fiber = fiber.return;
                    }
                }
            }
            if (!setProps) {
                animState.rafId = requestAnimationFrame(animate);
                return;
            }

            if (!animState.running) {
                animState.rafId = null;
                return;
            }

            const now = Date.now();
            animState.frameCount++;
            animState.fpsFrameCount++;

            // Calculate FPS every second
            if (now - animState.lastFpsUpdate >= 1000) {
                animState.currentFps = animState.fpsFrameCount;
                animState.fpsFrameCount = 0;
                animState.lastFpsUpdate = now;

                // Update displays
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

            // Update displays
            const countEl = document.getElementById('pulse-count');
            const frameEl = document.getElementById('frame-count');
            if (countEl) countEl.textContent = activeCells.length;
            if (frameEl) frameEl.textContent = animState.frameCount;

            // Trigger grid update based on method
            if (activeCells.length > 0) {
                if (animState.method === "selective") {
                    setProps({ cellsToUpdate: activeCells });
                } else {
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
