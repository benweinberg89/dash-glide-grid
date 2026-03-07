"""
Example 68: WebSocket + Imperative Grid Updates

Demonstrates Dash 4.1's FastAPI backend with:
1. Real-time WebSocket data streaming (no polling)
2. Imperative grid updates via window.dashGlideGrid (bypasses React)
3. Direct access to the underlying FastAPI server

A simulated stock ticker streams live price updates via WebSocket.
Client-side JavaScript receives updates and pushes them directly to the
grid canvas — no Intervals, no Dash callbacks, no React re-renders.

Requirements:
    pip install "dash[fastapi]>=4.1.0" websockets

Run with:
    python examples/68_async_websocket.py
"""

import asyncio
import json
import random
import time

import warnings

import dash
from dash import dcc, html
from fastapi import WebSocket, WebSocketDisconnect

import dash_glide_grid as dgg

app = dash.Dash(__name__, backend="fastapi", assets_folder="assets_68")

# Workaround: Dash 4.1.0rc0's DashMiddleware creates an HTTP Request object for
# WebSocket scopes, which crashes on Starlette's assert scope["type"] == "http".
# Patch the middleware to pass WebSocket scopes straight through.
from dash.backends._fastapi import DashMiddleware  # noqa: E402

_original_mw_call = DashMiddleware.__call__


async def _patched_mw_call(self, scope, receive, send):
    if scope["type"] == "websocket":
        await self.app(scope, receive, send)
        return
    return await _original_mw_call(self, scope, receive, send)


DashMiddleware.__call__ = _patched_mw_call

# -- Stock data ---------------------------------------------------------------

_REAL_STOCKS = [
    ("AAPL", "Apple Inc.", 178.50),
    ("MSFT", "Microsoft Corp.", 378.20),
    ("GOOGL", "Alphabet Inc.", 141.80),
    ("AMZN", "Amazon.com Inc.", 178.25),
    ("NVDA", "NVIDIA Corp.", 875.30),
    ("META", "Meta Platforms", 505.75),
    ("TSLA", "Tesla Inc.", 175.20),
    ("BRK.B", "Berkshire Hathaway", 412.50),
    ("JPM", "JPMorgan Chase", 195.80),
    ("V", "Visa Inc.", 278.40),
    ("UNH", "UnitedHealth", 527.30),
    ("JNJ", "Johnson & Johnson", 156.20),
    ("WMT", "Walmart Inc.", 165.80),
    ("PG", "Procter & Gamble", 162.40),
    ("MA", "Mastercard", 458.90),
    ("HD", "Home Depot", 378.20),
    ("DIS", "Walt Disney", 112.50),
    ("NFLX", "Netflix Inc.", 628.40),
    ("PFE", "Pfizer Inc.", 27.80),
    ("KO", "Coca-Cola Co.", 59.40),
]

NUM_ROWS = 1000


def _generate_stocks(n):
    """Generate n stock entries, cycling through real names + synthetics."""
    stocks = []
    for i in range(n):
        if i < len(_REAL_STOCKS):
            sym, company, price = _REAL_STOCKS[i]
        else:
            sym = f"SYN{i:04d}"
            company = f"Synthetic Corp #{i}"
            price = round(random.uniform(10, 900), 2)
        stocks.append({"symbol": sym, "company": company, "price": price})
    return stocks


STOCKS = _generate_stocks(NUM_ROWS)

COLUMNS = [
    {"title": "Symbol", "id": "symbol", "width": 90},
    {"title": "Company", "id": "company", "width": 180},
    {"title": "Price", "id": "price", "width": 110},
    {"title": "Change", "id": "change", "width": 100},
    {"title": "Change %", "id": "changePct", "width": 100},
    {"title": "Volume", "id": "volume", "width": 130},
    {"title": "Bid", "id": "bid", "width": 100},
    {"title": "Ask", "id": "ask", "width": 100},
]


def make_initial_data():
    data = []
    for stock in STOCKS:
        change = round(random.uniform(-3, 3), 2)
        pct = round(change / stock["price"] * 100, 2)
        spread = round(random.uniform(0.01, 0.10), 2)
        data.append(
            {
                "symbol": stock["symbol"],
                "company": stock["company"],
                "price": round(stock["price"], 2),
                "change": change,
                "changePct": pct,
                "volume": random.randint(1_000_000, 50_000_000),
                "bid": round(stock["price"] - spread, 2),
                "ask": round(stock["price"] + spread, 2),
            }
        )
    return data


INITIAL_DATA = make_initial_data()

# -- WebSocket endpoint -------------------------------------------------------

connected_clients: set[WebSocket] = set()


@app.server.websocket("/ws/live-data")
async def live_data_ws(websocket: WebSocket):
    """WebSocket endpoint — streams live market data to connected clients."""
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connected_clients.discard(websocket)


async def _broadcast_loop():
    """Background task: simulate random-walk price changes and push to clients."""
    prices = {i: s["price"] for i, s in enumerate(STOCKS)}
    num_stocks = len(STOCKS)

    while True:
        n = random.randint(3, min(15, num_stocks))
        indices = random.sample(range(num_stocks), n)
        updates = []
        for idx in indices:
            base = STOCKS[idx]["price"]
            prices[idx] = round(prices[idx] + random.gauss(0, base * 0.001), 2)
            price = prices[idx]
            change = round(price - base, 2)
            pct = round(change / base * 100, 2)
            spread = round(random.uniform(0.01, 0.10), 2)
            updates.append(
                {
                    "row": idx,
                    "price": price,
                    "change": change,
                    "changePct": pct,
                    "volume": random.randint(1_000_000, 50_000_000),
                    "bid": round(price - spread, 2),
                    "ask": round(price + spread, 2),
                }
            )

        payload = json.dumps({"updates": updates, "ts": time.time()})
        gone = set()
        for ws in list(connected_clients):
            try:
                await ws.send_text(payload)
            except Exception:
                gone.add(ws)
        connected_clients.difference_update(gone)
        await asyncio.sleep(0.2)  # ~5 updates/sec


with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)

    @app.server.on_event("startup")
    async def _start_broadcaster():
        asyncio.create_task(_broadcast_loop())


# -- Helpers -------------------------------------------------------------------


def _stat(label, elem_id, color=None):
    return html.Div(
        [
            html.Span(
                f"{label}: ",
                style={"color": "#64748b", "fontSize": "12px"},
            ),
            html.Span(
                "\u2014",
                id=elem_id,
                style={
                    "fontWeight": "bold",
                    "fontFamily": "monospace",
                    **({"color": color} if color else {}),
                },
            ),
        ]
    )


# -- Layout --------------------------------------------------------------------

app.layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.H1(
                    "Live Market Data",
                    style={"margin": "0", "fontSize": "24px"},
                ),
                html.Div(
                    [
                        html.Span(
                            id="ws-status-dot",
                            style={
                                "width": "8px",
                                "height": "8px",
                                "borderRadius": "50%",
                                "backgroundColor": "#ef4444",
                                "display": "inline-block",
                                "marginRight": "6px",
                            },
                        ),
                        html.Span(
                            "Connecting\u2026",
                            id="ws-status-text",
                            style={"fontSize": "13px", "color": "#64748b"},
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "marginBottom": "15px",
            },
        ),
        # Banner
        html.Div(
            html.P(
                [
                    "Powered by ",
                    html.Strong("Dash 4.1 + FastAPI"),
                    " \u2014 prices stream via WebSocket directly to the grid canvas. ",
                    "No polling, no React re-renders.",
                ],
                style={"margin": "0"},
            ),
            style={
                "backgroundColor": "#dbeafe",
                "padding": "12px 16px",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "border": "1px solid #93c5fd",
                "fontSize": "14px",
            },
        ),
        # Stats row
        html.Div(
            [
                _stat("Gainers", "stat-gainers", "#10b981"),
                _stat("Losers", "stat-losers", "#ef4444"),
                _stat("Avg \u0394", "stat-avg"),
                _stat("Total Vol", "stat-vol"),
                _stat("Updates/s", "stat-ups"),
            ],
            style={
                "display": "flex",
                "gap": "30px",
                "padding": "10px 16px",
                "backgroundColor": "#f8fafc",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "fontSize": "14px",
            },
        ),
        # Stress test controls (pure HTML — JS reads values directly, no Dash callbacks)
        html.Div(
            [
                html.Div(
                    [
                        html.Strong(
                            "Stress Test",
                            style={"marginRight": "15px", "fontSize": "13px"},
                        ),
                        html.Button(
                            "Start",
                            id="stress-btn",
                            style={
                                "padding": "4px 16px",
                                "borderRadius": "6px",
                                "border": "1px solid #d1d5db",
                                "backgroundColor": "#fff",
                                "cursor": "pointer",
                                "fontSize": "13px",
                                "fontWeight": "bold",
                                "marginRight": "20px",
                            },
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center"},
                ),
                # Rate slider
                html.Div(
                    [
                        html.Label(
                            "Rate: ",
                            style={"fontSize": "12px", "color": "#64748b"},
                        ),
                        dcc.Input(
                            id="stress-rate",
                            type="range",
                            min="1",
                            max="60",
                            value="30",
                            style={"width": "100px", "verticalAlign": "middle"},
                        ),
                        html.Span(
                            "30 Hz",
                            id="stress-rate-label",
                            style={
                                "fontSize": "12px",
                                "fontFamily": "monospace",
                                "marginLeft": "4px",
                                "minWidth": "45px",
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "gap": "4px"},
                ),
                # Rows per tick slider
                html.Div(
                    [
                        html.Label(
                            "Rows/tick: ",
                            style={"fontSize": "12px", "color": "#64748b"},
                        ),
                        dcc.Input(
                            id="stress-rows",
                            type="range",
                            min="1",
                            max="500",
                            value="50",
                            style={"width": "100px", "verticalAlign": "middle"},
                        ),
                        html.Span(
                            "50",
                            id="stress-rows-label",
                            style={
                                "fontSize": "12px",
                                "fontFamily": "monospace",
                                "marginLeft": "4px",
                                "minWidth": "35px",
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={"display": "flex", "alignItems": "center", "gap": "4px"},
                ),
                # Perf metrics
                html.Div(
                    [
                        html.Span(
                            "\u2014",
                            id="stress-perf",
                            style={
                                "fontSize": "12px",
                                "fontFamily": "monospace",
                                "color": "#64748b",
                            },
                        ),
                    ],
                    style={"marginLeft": "auto"},
                ),
            ],
            style={
                "display": "flex",
                "alignItems": "center",
                "gap": "20px",
                "padding": "8px 16px",
                "backgroundColor": "#fefce8",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "border": "1px solid #fde68a",
                "fontSize": "14px",
            },
        ),
        # Grid
        dgg.GlideGrid(
            id="live-grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=600,
            readonly=True,
            rowMarkers="number",
            smoothScrollX=True,
            smoothScrollY=True,
        ),
        # Footer
        html.Div(
            [
                html.H3("How it works", style={"marginTop": "25px"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "1. FastAPI Backend",
                                    style={"marginTop": "0", "color": "#2563eb"},
                                ),
                                html.Pre(
                                    'app = Dash(backend="fastapi")',
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Dash 4.1 runs on FastAPI/uvicorn instead of Flask. "
                                    "Full ASGI support with native async.",
                                    style={"fontSize": "13px", "color": "#475569"},
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "15px",
                                "backgroundColor": "#eff6ff",
                                "borderRadius": "8px",
                                "border": "1px solid #bfdbfe",
                            },
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "2. WebSocket Endpoint",
                                    style={"marginTop": "0", "color": "#7c3aed"},
                                ),
                                html.Pre(
                                    '@app.server.websocket("/ws")\n'
                                    "async def ws(websocket):\n"
                                    "    await websocket.accept()\n"
                                    "    await websocket.send_json(data)",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Add WebSocket routes directly to the underlying "
                                    "FastAPI server. No extensions needed.",
                                    style={"fontSize": "13px", "color": "#475569"},
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "15px",
                                "backgroundColor": "#f5f3ff",
                                "borderRadius": "8px",
                                "border": "1px solid #c4b5fd",
                            },
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "3. Imperative Grid Updates",
                                    style={"marginTop": "0", "color": "#059669"},
                                ),
                                html.Pre(
                                    "// In JS asset file:\n"
                                    "var grid = window\n"
                                    "  .dashGlideGrid[id];\n"
                                    "grid.updateCells([\n"
                                    "  {row: 0, data: {price: 42},\n"
                                    '   flash: "#10b981"}\n'
                                    "]);",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Update grid cells directly via the canvas API. "
                                    "Bypasses React \u2014 only changed cells repaint.",
                                    style={"fontSize": "13px", "color": "#475569"},
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "15px",
                                "backgroundColor": "#ecfdf5",
                                "borderRadius": "8px",
                                "border": "1px solid #6ee7b7",
                            },
                        ),
                    ],
                    style={"display": "flex", "gap": "15px"},
                ),
            ]
        ),
    ],
    style={
        "padding": "20px",
        "maxWidth": "1100px",
        "margin": "0 auto",
        "fontFamily": "system-ui, -apple-system, sans-serif",
    },
)


if __name__ == "__main__":
    app.run(debug=True, port=8055)
