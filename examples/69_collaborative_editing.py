"""
Example 69: Collaborative Editing (Google Sheets-style)

Demonstrates Dash 4.1's FastAPI backend with:
1. Real-time collaborative editing via WebSocket
2. Multi-user cursor presence (colored highlight regions)
3. Imperative grid updates for instant remote edits

Multiple browser tabs act as independent users. Each user gets a unique
color and name. Cursor positions and cell edits are broadcast to all
other users in real time.

Requirements:
    pip install "dash[fastapi]>=4.1.0" websockets

Run with:
    python examples/69_collaborative_editing.py
"""

import asyncio
import json
import warnings

import dash
from dash import dcc, html, Input, Output, State

from fastapi import WebSocket, WebSocketDisconnect

import dash_glide_grid as dgg

app = dash.Dash(__name__, backend="fastapi", assets_folder="assets_69")

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

# -- User identity palette ----------------------------------------------------

USER_COLORS = [
    "#3b82f6",  # blue
    "#ef4444",  # red
    "#10b981",  # emerald
    "#f59e0b",  # amber
    "#8b5cf6",  # violet
    "#ec4899",  # pink
    "#06b6d4",  # cyan
    "#f97316",  # orange
]

USER_NAMES = ["Alice", "Bob", "Carol", "Dave", "Eve", "Frank", "Grace", "Hank"]

# -- Sample data: project tracker ---------------------------------------------

COLUMNS = [
    {"title": "Task", "id": "task", "width": 200},
    {"title": "Assignee", "id": "assignee", "width": 120},
    {"title": "Status", "id": "status", "width": 110},
    {"title": "Priority", "id": "priority", "width": 100},
    {"title": "Estimate (h)", "id": "estimate", "width": 110},
    {"title": "Notes", "id": "notes", "width": 250},
]

INITIAL_DATA = [
    {
        "task": "Design landing page",
        "assignee": "Alice",
        "status": "In Progress",
        "priority": "High",
        "estimate": 8,
        "notes": "Mobile-first approach",
    },
    {
        "task": "Set up CI/CD pipeline",
        "assignee": "Bob",
        "status": "Done",
        "priority": "High",
        "estimate": 4,
        "notes": "Using GitHub Actions",
    },
    {
        "task": "Write API documentation",
        "assignee": "Carol",
        "status": "To Do",
        "priority": "Medium",
        "estimate": 6,
        "notes": "OpenAPI spec",
    },
    {
        "task": "Implement auth flow",
        "assignee": "Dave",
        "status": "In Progress",
        "priority": "High",
        "estimate": 12,
        "notes": "OAuth2 + JWT",
    },
    {
        "task": "Database schema review",
        "assignee": "Alice",
        "status": "To Do",
        "priority": "Medium",
        "estimate": 3,
        "notes": "Check indexes",
    },
    {
        "task": "Performance testing",
        "assignee": "Eve",
        "status": "To Do",
        "priority": "Low",
        "estimate": 5,
        "notes": "Load test with k6",
    },
    {
        "task": "Update dependencies",
        "assignee": "Bob",
        "status": "Done",
        "priority": "Low",
        "estimate": 2,
        "notes": "Security patches",
    },
    {
        "task": "User feedback survey",
        "assignee": "Carol",
        "status": "In Progress",
        "priority": "Medium",
        "estimate": 4,
        "notes": "SurveyMonkey",
    },
    {
        "task": "Fix timezone bug",
        "assignee": "Dave",
        "status": "To Do",
        "priority": "High",
        "estimate": 3,
        "notes": "UTC conversion issue",
    },
    {
        "task": "Onboarding tutorial",
        "assignee": "Eve",
        "status": "To Do",
        "priority": "Medium",
        "estimate": 10,
        "notes": "Interactive walkthrough",
    },
    {
        "task": "Refactor payment module",
        "assignee": "Alice",
        "status": "To Do",
        "priority": "High",
        "estimate": 16,
        "notes": "Stripe v3 migration",
    },
    {
        "task": "Add dark mode",
        "assignee": "Bob",
        "status": "In Progress",
        "priority": "Low",
        "estimate": 8,
        "notes": "CSS variables approach",
    },
]

# -- Server-side shared state -------------------------------------------------

shared_data = [dict(row) for row in INITIAL_DATA]
connected_clients = {}  # ws_id -> WebSocket
users = {}  # ws_id -> {id, name, color, cursor}
_next_user_idx = 0

# -- WebSocket endpoint -------------------------------------------------------


async def _broadcast_except(exclude_ws_id, message):
    """Send message to all connected clients except the sender."""
    payload = json.dumps(message)
    gone = []
    for ws_id, ws in list(connected_clients.items()):
        if ws_id == exclude_ws_id:
            continue
        try:
            await ws.send_text(payload)
        except Exception:
            gone.append(ws_id)
    for ws_id in gone:
        connected_clients.pop(ws_id, None)
        users.pop(ws_id, None)


async def _broadcast_all(message):
    """Send message to all connected clients."""
    payload = json.dumps(message)
    gone = []
    for ws_id, ws in list(connected_clients.items()):
        try:
            await ws.send_text(payload)
        except Exception:
            gone.append(ws_id)
    for ws_id in gone:
        connected_clients.pop(ws_id, None)
        users.pop(ws_id, None)


@app.server.websocket("/ws/collab")
async def collab_ws(websocket: WebSocket):
    global _next_user_idx
    await websocket.accept()

    # Assign user identity
    ws_id = id(websocket)
    user_idx = _next_user_idx % len(USER_COLORS)
    _next_user_idx += 1

    user_info = {
        "id": str(ws_id),
        "name": USER_NAMES[user_idx % len(USER_NAMES)],
        "color": USER_COLORS[user_idx],
        "cursor": None,
    }

    users[ws_id] = user_info
    connected_clients[ws_id] = websocket

    # Send init with full state
    await websocket.send_text(
        json.dumps(
            {
                "type": "init",
                "userId": user_info["id"],
                "userName": user_info["name"],
                "userColor": user_info["color"],
                "data": shared_data,
                "users": [
                    {
                        "id": u["id"],
                        "name": u["name"],
                        "color": u["color"],
                        "cursor": u["cursor"],
                    }
                    for u in users.values()
                ],
            }
        )
    )

    # Notify others
    await _broadcast_except(
        ws_id,
        {
            "type": "user_joined",
            "userId": user_info["id"],
            "userName": user_info["name"],
            "userColor": user_info["color"],
        },
    )

    try:
        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw)

            if msg["type"] == "cursor":
                users[ws_id]["cursor"] = {"col": msg["col"], "row": msg["row"]}
                await _broadcast_except(
                    ws_id,
                    {
                        "type": "cursor",
                        "userId": user_info["id"],
                        "col": msg["col"],
                        "row": msg["row"],
                        "color": user_info["color"],
                        "userName": user_info["name"],
                    },
                )

            elif msg["type"] == "edit":
                row_idx = msg["row"]
                col_id = msg["colId"]
                value = msg["value"]
                if 0 <= row_idx < len(shared_data):
                    shared_data[row_idx][col_id] = value

                await _broadcast_except(
                    ws_id,
                    {
                        "type": "edit",
                        "userId": user_info["id"],
                        "row": row_idx,
                        "col": msg["col"],
                        "colId": col_id,
                        "value": value,
                        "color": user_info["color"],
                        "userName": user_info["name"],
                    },
                )

    except WebSocketDisconnect:
        pass
    finally:
        connected_clients.pop(ws_id, None)
        users.pop(ws_id, None)
        await _broadcast_all({"type": "user_left", "userId": user_info["id"]})


# -- Layout --------------------------------------------------------------------

app.layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.H1(
                    "Collaborative Spreadsheet",
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
        # Connected users bar
        html.Div(
            [
                html.Span(
                    "Online: ",
                    style={
                        "fontWeight": "bold",
                        "fontSize": "13px",
                        "marginRight": "10px",
                    },
                ),
                html.Div(
                    id="users-bar",
                    children="No users connected",
                    style={
                        "display": "flex",
                        "gap": "12px",
                        "alignItems": "center",
                        "flexWrap": "wrap",
                    },
                ),
            ],
            style={
                "padding": "10px 16px",
                "backgroundColor": "#f0fdf4",
                "borderRadius": "8px",
                "marginBottom": "15px",
                "border": "1px solid #86efac",
                "display": "flex",
                "alignItems": "center",
            },
        ),
        # Info banner
        html.Div(
            html.P(
                [
                    "Open this page in ",
                    html.Strong("multiple browser tabs"),
                    " to simulate different users. Each tab gets a unique color "
                    "and name. Edits and cursor movements are shared in real time "
                    "via WebSocket.",
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
        # Grid (editable)
        dgg.GlideGrid(
            id="collab-grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=500,
            readonly=False,
            rowMarkers="number",
            smoothScrollX=True,
            smoothScrollY=True,
        ),
        # Hidden outputs for clientside callbacks
        html.Div(id="collab-dummy", style={"display": "none"}),
        html.Div(id="collab-dummy2", style={"display": "none"}),
        # Footer
        html.Div(
            [
                html.H3("How it works", style={"marginTop": "25px"}),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4(
                                    "1. WebSocket Sync",
                                    style={"marginTop": "0", "color": "#2563eb"},
                                ),
                                html.Pre(
                                    '@app.server.websocket("/ws/collab")\n'
                                    "async def collab_ws(ws):\n"
                                    "    await ws.accept()\n"
                                    "    # broadcast edits + cursors",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Server holds shared data as source of truth. "
                                    "Edits and cursor positions are broadcast to "
                                    "all connected clients via WebSocket.",
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
                                    "2. Cursor Presence",
                                    style={"marginTop": "0", "color": "#7c3aed"},
                                ),
                                html.Pre(
                                    "// JS receives cursor pos\n"
                                    "updater.setHighlightRegions(\n"
                                    "  [{color: userColor,\n"
                                    "    range: {x: col, y: row,\n"
                                    "      width: 1, height: 1}}]\n"
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
                                    "Each user's cursor is rendered as a colored "
                                    "highlight region on other users' grids. The "
                                    "imperative API avoids React overhead.",
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
                                    "3. Instant Cell Updates",
                                    style={"marginTop": "0", "color": "#059669"},
                                ),
                                html.Pre(
                                    "// Remote edit arrives via WS\n"
                                    "grid.updateCells([{\n"
                                    "  row: 3,\n"
                                    '  data: {status: "Done"},\n'
                                    '  flash: "#3b82f6"\n'
                                    "}]);",
                                    style={
                                        "backgroundColor": "#1e293b",
                                        "color": "#e2e8f0",
                                        "padding": "10px",
                                        "borderRadius": "6px",
                                        "fontSize": "13px",
                                    },
                                ),
                                html.P(
                                    "Remote edits are applied imperatively \u2014 "
                                    "only the changed cell repaints on the canvas. "
                                    "The flash color matches the editing user.",
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

# -- Clientside callbacks: forward selection + edits to WebSocket --------------

app.clientside_callback(
    """function(selectedCell) {
        if (window._collabWs && window._collabWs.readyState === 1 && selectedCell) {
            window._collabWs.send(JSON.stringify({
                type: 'cursor', col: selectedCell.col, row: selectedCell.row
            }));
        }
        return window.dash_clientside.no_update;
    }""",
    Output("collab-dummy", "children"),
    Input("collab-grid", "selectedCell"),
)

app.clientside_callback(
    """function(cellEdited, columns) {
        if (window._collabWs && window._collabWs.readyState === 1 && cellEdited) {
            var colId = columns[cellEdited.col].id;
            window._collabWs.send(JSON.stringify({
                type: 'edit',
                row: cellEdited.row,
                col: cellEdited.col,
                colId: colId,
                value: cellEdited.value
            }));
        }
        return window.dash_clientside.no_update;
    }""",
    Output("collab-dummy2", "children"),
    Input("collab-grid", "cellEdited"),
    State("collab-grid", "columns"),
)


if __name__ == "__main__":
    app.run(debug=True, port=8068)
