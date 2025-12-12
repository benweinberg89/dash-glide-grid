"""
Example 42: cellsToUpdate vs redrawTrigger with Custom drawCell

Demonstrates the performance difference between cellsToUpdate and redrawTrigger
when using a custom drawCell function. Random cells are continuously highlighted
with a pulse animation - switch between methods to see the difference.

Run with: python examples/42_cells_to_update.py
"""

from dash import Dash, html, dcc, Input, Output, State, clientside_callback

from dash_glide_grid import GlideGrid

app = Dash(__name__, assets_folder="assets")

# Grid data - larger grid to show performance difference
NUM_ROWS = 100
NUM_COLS = 20

columns = [{"title": f"C{i}", "width": 50, "id": f"col_{i}"} for i in range(NUM_COLS)]
data = [{f"col_{j}": f"{i},{j}" for j in range(NUM_COLS)} for i in range(NUM_ROWS)]

app.layout = html.Div(
    [
        html.H1("cellsToUpdate vs redrawTrigger"),
        html.Div(
            [
                html.P(
                    [
                        "Random cells pulse with animations. The pulse state is tracked in JavaScript. ",
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
                        html.Label("New pulses per tick:", style={"fontWeight": "bold", "marginRight": "10px"}),
                        dcc.Slider(
                            id="pulses-per-tick",
                            min=1,
                            max=20,
                            step=1,
                            value=5,
                            marks={1: "1", 5: "5", 10: "10", 20: "20"},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    style={"flex": "1", "minWidth": "250px"},
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
        # Animation interval
        dcc.Interval(id="animation-interval", interval=50, n_intervals=0),
        GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=500,
            rowMarkers="none",
            rowHeight=20,
            headerHeight=24,
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
                            html.Li(f"~5-50 cells per frame"),
                            html.Li("Smooth animations"),
                        ], style={"marginBottom": "0"}),
                    ],
                    style={"flex": "1", "backgroundColor": "#f0fdf4", "padding": "15px", "borderRadius": "8px", "border": "1px solid #10b981"},
                ),
                html.Div(
                    [
                        html.H3("redrawTrigger", style={"color": "#f59e0b", "marginTop": "0"}),
                        html.Ul([
                            html.Li(f"Redraws ALL {NUM_ROWS * NUM_COLS} cells"),
                            html.Li(f"{NUM_ROWS * NUM_COLS} cells per frame"),
                            html.Li("May stutter at high pulse rates"),
                        ], style={"marginBottom": "0"}),
                    ],
                    style={"flex": "1", "backgroundColor": "#fffbeb", "padding": "15px", "borderRadius": "8px", "border": "1px solid #f59e0b"},
                ),
            ],
            style={"display": "flex", "gap": "15px"},
        ),
    ],
    style={"padding": "20px", "maxWidth": "1200px", "margin": "0 auto"},
)


# Clientside callback - handles everything in JS for performance
clientside_callback(
    """
    function(n_intervals, method, pulsesPerTick) {
        const noUpdate = window.dash_clientside.no_update;

        // Initialize pulse tracking if needed
        if (!window.pulsingCells) {
            window.pulsingCells = {};
        }

        // Add new random pulses
        const numRows = """ + str(NUM_ROWS) + """;
        const numCols = """ + str(NUM_COLS) + """;
        const now = Date.now();
        const pulseDuration = 800;

        for (let i = 0; i < pulsesPerTick; i++) {
            const row = Math.floor(Math.random() * numRows);
            const col = Math.floor(Math.random() * numCols);
            const key = col + "," + row;
            window.pulsingCells[key] = { startTime: now, duration: pulseDuration };
        }

        // Get all currently active pulses and clean up expired ones
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

        const count = String(activeCells.length);
        const frame = String(n_intervals);

        if (activeCells.length === 0) {
            return [noUpdate, noUpdate, "0", frame, method];
        }

        // Return based on method
        if (method === "selective") {
            return [activeCells, noUpdate, count, frame, method];
        } else {
            return [noUpdate, n_intervals, count, frame, method];
        }
    }
    """,
    Output("grid", "cellsToUpdate"),
    Output("grid", "redrawTrigger"),
    Output("pulse-count", "children"),
    Output("frame-count", "children"),
    Output("current-method", "children"),
    Input("animation-interval", "n_intervals"),
    State("update-method", "value"),
    State("pulses-per-tick", "value"),
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
