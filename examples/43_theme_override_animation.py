"""
Example 43: Cell Animation with themeOverride

Demonstrates three methods for updating grid cells using themeOverride in cell data,
similar to the glide-data-grid storybook rapid-updates example.

This approach:
- Updates cell DATA with themeOverride for colors
- Uses the grid's built-in renderer (no custom drawCell)
- Preserves grid lines automatically
- Trades some flexibility for simplicity

Run with: python examples/43_theme_override_animation.py
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
    # Each cell starts with empty themeOverride - will be updated by animation
    data = [
        {f"col_{j}": {"kind": "text", "data": "", "displayData": ""} for j in range(cols)}
        for _ in range(rows)
    ]
    return columns, data, rows, cols


# Default grid size
DEFAULT_CELLS = 10000
columns, data, NUM_ROWS, NUM_COLS = generate_grid_data(DEFAULT_CELLS)

app.layout = html.Div(
    [
        html.H1("Cell Animation with themeOverride"),
        html.Div(
            [
                html.P(
                    [
                        "Grid: ",
                        html.Span(
                            id="grid-size-display",
                            children=f"{NUM_ROWS:,} x {NUM_COLS} = {NUM_ROWS * NUM_COLS:,}",
                        ),
                        " cells. This example uses themeOverride per cell instead of custom drawCell. ",
                        "Grid lines are preserved automatically by the built-in renderer.",
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
            experimental={"disableMinimumCellWidth": True},
        ),
        html.Hr(),
        html.H2("How themeOverride Works"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3(
                            "themeOverride Approach",
                            style={"color": "#10b981", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("Cell data includes themeOverride.bgCell"),
                                html.Li("Grid's built-in renderer handles everything"),
                                html.Li("Grid lines preserved automatically"),
                                html.Li("Simpler but less flexible than drawCell"),
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
                            "vs Custom drawCell",
                            style={"color": "#f59e0b", "marginTop": "0"},
                        ),
                        html.Ul(
                            [
                                html.Li("drawCell gives full canvas control"),
                                html.Li("Can draw anything (gradients, shapes)"),
                                html.Li("Must handle grid lines manually"),
                                html.Li("Higher performance ceiling"),
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
                html.H3("The Pattern", style={"marginTop": "20px"}),
                html.P("Cell data includes themeOverride for custom background:"),
                html.Pre(
                    """# Python - cell data with themeOverride
data = [
    {
        "col_0": {
            "kind": "text",
            "data": "value",
            "themeOverride": {"bgCell": "#3b82f6"}
        }
    }
]""",
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
        if (!window._animState43) {
            window._animState43 = {
                frameCount: 0,
                lastFpsUpdate: performance.now(),
                fpsFrameCount: 0,
                currentFps: 0,
                rafId: null,
                running: false,
                method: "selective",
                pulsesPerFrame: 20,
                numRows: 0,
                numCols: 0
            };
            window.pulsingCells43 = {};
        }

        const animState = window._animState43;

        // Update grid dimensions from store
        const numRows = gridDims?.rows || 100;
        const numCols = gridDims?.cols || 100;
        if (animState.numRows !== numRows || animState.numCols !== numCols) {
            animState.numRows = numRows;
            animState.numCols = numCols;
            window._allCells43 = null;  // Reset cache when grid size changes
            window.pulsingCells43 = {};
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
            const gridRef = window._glideGridRefs?.['grid'];

            // Access the component's internal data through React fiber
            const gridEl = document.getElementById('grid');
            let gridData = null;
            let setProps = gridEl?._dashprivate_setProps;
            if (gridEl) {
                const key = Object.keys(gridEl).find(k => k.startsWith('__reactFiber$'));
                if (key) {
                    let fiber = gridEl[key];
                    while (fiber) {
                        if (fiber.memoizedProps?.data) {
                            gridData = fiber.memoizedProps.data;
                        }
                        if (fiber.memoizedProps?.setProps) {
                            setProps = fiber.memoizedProps.setProps;
                        }
                        if (gridData && setProps) break;
                        fiber = fiber.return;
                    }
                }
            }

            if (!gridRef || !gridData) {
                animState.rafId = requestAnimationFrame(animate);
                return;
            }

            if (!animState.running) {
                animState.rafId = null;
                return;
            }

            const now = performance.now();
            animState.frameCount++;

            // Calculate FPS every second
            if (now - animState.lastFpsUpdate >= 1000) {
                animState.currentFps = animState.fpsFrameCount;
                animState.fpsFrameCount = 0;
                animState.lastFpsUpdate = now;

                const fpsEl = document.getElementById('fps-display');
                const methodEl = document.getElementById('current-method');
                if (fpsEl) fpsEl.textContent = animState.currentFps;
                if (methodEl) methodEl.textContent = animState.method;
            }

            // Add new random pulses
            for (let i = 0; i < animState.pulsesPerFrame; i++) {
                const row = Math.floor(Math.random() * animState.numRows);
                const col = Math.floor(Math.random() * animState.numCols);
                const key = col + "," + row;
                window.pulsingCells43[key] = { startTime: now, duration: pulseDuration, col, row };
            }

            // Update cell data with themeOverride colors and collect cells to update
            const cellsToUpdate = [];
            for (const key in window.pulsingCells43) {
                const pulse = window.pulsingCells43[key];
                const elapsed = now - pulse.startTime;
                const progress = Math.min(elapsed / pulse.duration, 1);
                const col = pulse.col;
                const row = pulse.row;
                const colId = "col_" + col;

                if (progress < 1) {
                    // Calculate color: bright blue fading to dark background
                    const intensity = 1 - progress;
                    const r = Math.round(30 + (59 - 30) * intensity);
                    const g = Math.round(41 + (130 - 41) * intensity);
                    const b = Math.round(59 + (246 - 59) * intensity);

                    // Update cell data with themeOverride
                    if (gridData[row] && gridData[row][colId] !== undefined) {
                        gridData[row][colId] = {
                            kind: "text",
                            data: "",
                            displayData: "",
                            themeOverride: { bgCell: "rgb(" + r + "," + g + "," + b + ")" }
                        };
                    }
                    cellsToUpdate.push({ cell: [col, row] });
                } else {
                    // Expired - reset to default and remove
                    if (gridData[row] && gridData[row][colId] !== undefined) {
                        gridData[row][colId] = {
                            kind: "text",
                            data: "",
                            displayData: ""
                        };
                    }
                    cellsToUpdate.push({ cell: [col, row] });
                    delete window.pulsingCells43[key];
                }
            }

            // Update displays
            const countEl = document.getElementById('pulse-count');
            const frameEl = document.getElementById('frame-count');
            if (countEl) countEl.textContent = Object.keys(window.pulsingCells43).length;
            if (frameEl) frameEl.textContent = animState.frameCount;

            // Trigger redraw based on method
            if (cellsToUpdate.length > 0) {
                animState.fpsFrameCount++;
                if (animState.method === "selective" && gridRef) {
                    // Selective: only redraw changed cells (bypasses React)
                    gridRef.updateCells(cellsToUpdate);
                } else if (animState.method === "full" && gridRef) {
                    // Full: redraw ALL cells (bypasses React)
                    if (!window._allCells43) {
                        window._allCells43 = [];
                        for (let row = 0; row < animState.numRows; row++) {
                            for (let col = 0; col < animState.numCols; col++) {
                                window._allCells43.push({ cell: [col, row] });
                            }
                        }
                    }
                    gridRef.updateCells(window._allCells43);
                } else if (animState.method === "react" && setProps) {
                    // React: update via redrawTrigger prop (goes through React)
                    setProps({redrawTrigger: animState.frameCount});
                }
            }

            animState.rafId = requestAnimationFrame(animate);
        }

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
    app.run(debug=True, port=8051)
