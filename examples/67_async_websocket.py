"""
Example 67: Async & WebSocket Live Data

Demonstrates Dash 4.1's FastAPI backend with:
1. Real-time WebSocket data streaming (no polling)
2. Async callbacks (async def with await)
3. Direct access to the underlying FastAPI server

A simulated stock ticker streams live price updates via WebSocket.
Client-side JavaScript receives updates and merges them into the grid.

Requirements:
    pip install "dash[fastapi]>=4.1.0" websockets

Run with:
    python examples/67_async_websocket.py
"""

import asyncio
import json
import random
import time

import warnings

import dash
from dash import html, dcc, callback, Input, Output, State, clientside_callback
from fastapi import WebSocket, WebSocketDisconnect

import dash_glide_grid as dgg

app = dash.Dash(__name__, backend="fastapi", assets_folder="assets", update_title=None)

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

STOCKS = [
    {"symbol": "AAPL", "company": "Apple Inc.", "price": 178.50},
    {"symbol": "MSFT", "company": "Microsoft Corp.", "price": 378.20},
    {"symbol": "GOOGL", "company": "Alphabet Inc.", "price": 141.80},
    {"symbol": "AMZN", "company": "Amazon.com Inc.", "price": 178.25},
    {"symbol": "NVDA", "company": "NVIDIA Corp.", "price": 875.30},
    {"symbol": "META", "company": "Meta Platforms", "price": 505.75},
    {"symbol": "TSLA", "company": "Tesla Inc.", "price": 175.20},
    {"symbol": "BRK.B", "company": "Berkshire Hathaway", "price": 412.50},
    {"symbol": "JPM", "company": "JPMorgan Chase", "price": 195.80},
    {"symbol": "V", "company": "Visa Inc.", "price": 278.40},
    {"symbol": "UNH", "company": "UnitedHealth", "price": 527.30},
    {"symbol": "JNJ", "company": "Johnson & Johnson", "price": 156.20},
    {"symbol": "WMT", "company": "Walmart Inc.", "price": 165.80},
    {"symbol": "PG", "company": "Procter & Gamble", "price": 162.40},
    {"symbol": "MA", "company": "Mastercard", "price": 458.90},
    {"symbol": "HD", "company": "Home Depot", "price": 378.20},
    {"symbol": "DIS", "company": "Walt Disney", "price": 112.50},
    {"symbol": "NFLX", "company": "Netflix Inc.", "price": 628.40},
    {"symbol": "PFE", "company": "Pfizer Inc.", "price": 27.80},
    {"symbol": "KO", "company": "Coca-Cola Co.", "price": 59.40},
]

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
    prices = {s["symbol"]: s["price"] for s in STOCKS}

    while True:
        n = random.randint(3, 8)
        indices = random.sample(range(len(STOCKS)), min(n, len(STOCKS)))
        updates = []
        for idx in indices:
            sym = STOCKS[idx]["symbol"]
            base = STOCKS[idx]["price"]
            prices[sym] = round(prices[sym] + random.gauss(0, base * 0.001), 2)
            price = prices[sym]
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
                    " \u2014 prices stream via WebSocket, stats computed with ",
                    html.Code("async def"),
                    " callbacks. No polling.",
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
        # Bridge: WS messages -> Dash via Interval
        dcc.Interval(id="ws-poll", interval=100, n_intervals=0),
        dcc.Interval(id="stats-poll", interval=2000, n_intervals=0),
        html.Div(id="_ws-sink", style={"display": "none"}),
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
                                    "3. Async Callbacks",
                                    style={"marginTop": "0", "color": "#059669"},
                                ),
                                html.Pre(
                                    "@callback(...)\n"
                                    "async def compute(data):\n"
                                    "    result = await db.query(...)\n"
                                    "    return result",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Callbacks can be async def. Await database queries, "
                                    "API calls, or any async I/O without blocking.",
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


# -- Clientside callback: merge WS updates into grid data ----------------------

clientside_callback(
    """
    function(nIntervals, currentData) {
        if (!window._wsQueue || window._wsQueue.length === 0) {
            return [window.dash_clientside.no_update, window.dash_clientside.no_update];
        }

        var data = currentData.map(function(row) { return Object.assign({}, row); });
        var flash = {};
        var now = performance.now();

        while (window._wsQueue.length > 0) {
            var msg = window._wsQueue.shift();
            if (!msg.updates) continue;
            for (var i = 0; i < msg.updates.length; i++) {
                var u = msg.updates[i];
                var row = data[u.row];
                if (!row) continue;
                row.price = u.price;
                row.change = u.change;
                row.changePct = u.changePct;
                row.volume = u.volume;
                row.bid = u.bid;
                row.ask = u.ask;
                // Mark changed cells for flash (key format: "row,col")
                var color = u.change >= 0 ? '#10b981' : '#ef4444';
                for (var c = 2; c <= 7; c++) {
                    flash[u.row + ',' + c] = {t: now, color: color};
                }
            }
        }

        return [data, flash];
    }
    """,
    [Output("live-grid", "data"), Output("live-grid", "lastUpdatedCells")],
    Input("ws-poll", "n_intervals"),
    State("live-grid", "data"),
    prevent_initial_call=True,
)


# -- Async callback: compute market stats (runs server-side) -------------------


@callback(
    Output("stat-gainers", "children"),
    Output("stat-losers", "children"),
    Output("stat-avg", "children"),
    Output("stat-vol", "children"),
    Input("stats-poll", "n_intervals"),
    State("live-grid", "data"),
)
async def compute_stats(n_intervals, data):
    """Async callback — demonstrates async def with await on the FastAPI backend."""
    if not data:
        return "\u2014", "\u2014", "\u2014", "\u2014"

    # Simulate an async I/O operation (e.g. database query)
    await asyncio.sleep(0.01)

    gainers = sum(1 for r in data if r.get("change", 0) > 0)
    losers = sum(1 for r in data if r.get("change", 0) < 0)
    avg = sum(r.get("changePct", 0) for r in data) / len(data)
    vol = sum(r.get("volume", 0) for r in data)

    avg_color = "#10b981" if avg >= 0 else "#ef4444"

    return (
        str(gainers),
        str(losers),
        html.Span(f"{avg:+.2f}%", style={"color": avg_color}),
        f"{vol:,.0f}",
    )


if __name__ == "__main__":
    app.run(debug=True, port=8055)
