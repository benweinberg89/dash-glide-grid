"""
Example 70: Server-Sent Events (SSE) Stock Ticker

Same live market data as Example 68, but using SSE instead of WebSocket.

Advantages over the WebSocket approach:
1. No DashMiddleware patch needed — SSE is plain HTTP
2. Auto-reconnect built into the browser's EventSource API
3. Works through HTTP proxies and CDNs that block WebSocket
4. Simpler server code — just yield from an async generator

Trade-off: SSE is one-way only (server → client). For bidirectional
use cases like collaborative editing (Example 69), you still need WebSocket.

Requirements:
    pip install "dash[fastapi]>=4.1.0" sse-starlette

Run with:
    python examples/70_sse_stock_ticker.py
"""

import asyncio
import json
import random
import time

from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request

import dash
from dash import dcc, html

import dash_glide_grid as dgg

# Create the FastAPI server first and register custom routes on it.
# Dash's catch-all route `/{path:path}` is added last during init, so
# routes registered here will be matched first.
server = FastAPI()

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

# -- SSE endpoint -------------------------------------------------------------

prices = {i: s["price"] for i, s in enumerate(STOCKS)}


async def _stock_generator(request: Request):
    """Async generator that yields SSE events with stock updates."""
    num_stocks = len(STOCKS)
    while True:
        if await request.is_disconnected():
            break

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

        yield {
            "event": "update",
            "data": json.dumps({"updates": updates, "ts": time.time()}),
        }
        await asyncio.sleep(0.2)  # ~5 updates/sec


@server.get("/api/stream")
async def stream(request: Request):
    """SSE endpoint — streams live market data to connected clients."""
    return EventSourceResponse(_stock_generator(request))


# Create the Dash app AFTER registering custom routes on the server.
# Dash appends its catch-all `/{path:path}` during init, so our routes
# are matched first.
app = dash.Dash(__name__, server=server, backend="fastapi", assets_folder="assets_70")


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
                    "Live Market Data (SSE)",
                    style={"margin": "0", "fontSize": "24px"},
                ),
                html.Div(
                    [
                        html.Span(
                            id="sse-status-dot",
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
                            id="sse-status-text",
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
                    html.Strong("Dash 4.1 + FastAPI + SSE"),
                    " \u2014 prices stream via Server-Sent Events directly to the "
                    "grid canvas. No WebSocket, no polling, no React re-renders. ",
                    "Auto-reconnects if the connection drops.",
                ],
                style={"margin": "0"},
            ),
            style={
                "backgroundColor": "#fef3c7",
                "padding": "12px 16px",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "border": "1px solid #fcd34d",
                "fontSize": "14px",
            },
        ),
        # Comparison box
        html.Div(
            [
                html.Strong(
                    "SSE vs WebSocket",
                    style={"display": "block", "marginBottom": "6px"},
                ),
                html.Ul(
                    [
                        html.Li(
                            "No DashMiddleware patch needed \u2014 SSE is plain HTTP"
                        ),
                        html.Li(
                            "Auto-reconnect built into EventSource API \u2014 "
                            "no manual retry logic"
                        ),
                        html.Li(
                            "Works through corporate proxies and CDNs that block "
                            "WebSocket"
                        ),
                        html.Li(
                            "Trade-off: one-way only (server \u2192 client) \u2014 "
                            "fine for live feeds, not for collaboration"
                        ),
                    ],
                    style={
                        "margin": "0",
                        "paddingLeft": "20px",
                        "fontSize": "13px",
                        "color": "#475569",
                    },
                ),
            ],
            style={
                "backgroundColor": "#f0fdf4",
                "padding": "12px 16px",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "border": "1px solid #86efac",
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
                                    "1. FastAPI + SSE",
                                    style={"marginTop": "0", "color": "#d97706"},
                                ),
                                html.Pre(
                                    "@app.server.get('/api/stream')\n"
                                    "async def stream(request):\n"
                                    "    return EventSourceResponse(\n"
                                    "        stock_generator(request)\n"
                                    "    )",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "An async generator yields SSE events. "
                                    "Each connected client gets its own generator "
                                    "instance \u2014 no connection tracking needed.",
                                    style={"fontSize": "13px", "color": "#475569"},
                                ),
                            ],
                            style={
                                "flex": "1",
                                "padding": "15px",
                                "backgroundColor": "#fffbeb",
                                "borderRadius": "8px",
                                "border": "1px solid #fde68a",
                            },
                        ),
                        html.Div(
                            [
                                html.H4(
                                    "2. EventSource API",
                                    style={"marginTop": "0", "color": "#7c3aed"},
                                ),
                                html.Pre(
                                    "var es = new EventSource(\n"
                                    "  '/api/stream'\n"
                                    ");\n"
                                    "es.addEventListener('update',\n"
                                    "  function(e) {\n"
                                    "    var msg = JSON.parse(e.data);\n"
                                    "    // apply to grid...\n"
                                    "  }\n"
                                    ");",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "The browser's EventSource connects and auto-"
                                    "reconnects. Named events ('update') keep the "
                                    "protocol clean.",
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
                                    "// Same as Example 68:\n"
                                    "var grid = window\n"
                                    "  .dashGlideGrid[id];\n"
                                    "grid.updateCells([\n"
                                    "  {row: 0, values: {price: 42},\n"
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
                                    "The grid update path is identical \u2014 only the "
                                    "transport layer changed. SSE delivers, JS applies "
                                    "imperatively.",
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
    app.run(debug=True, port=8069)
