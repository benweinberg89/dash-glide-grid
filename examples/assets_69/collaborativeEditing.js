/**
 * Collaborative editing client for Example 69.
 *
 * Connects to the /ws/collab WebSocket endpoint and:
 * - Sends local cursor (selectedCell) and cell edits to the server
 * - Receives remote cursors and renders them as highlight regions
 * - Receives remote edits and applies them imperatively via updateCells()
 * - Manages the connected users bar in the DOM
 *
 * The WebSocket object is stored on window._collabWs so that Dash
 * clientside callbacks can send messages through it.
 */

(function () {
    "use strict";

    var GRID_ID = "collab-grid";
    var NUM_COLUMNS = 6;

    // Local user identity (assigned by server on init)
    var myUserId = null;
    var myUserName = null;
    var myUserColor = null;

    // Remote users: userId -> {name, color, cursor: {col, row} | null}
    var remoteUsers = {};

    // ========== HELPERS ==========

    function updateStatus(connected) {
        var dot = document.getElementById("ws-status-dot");
        var text = document.getElementById("ws-status-text");
        if (dot) dot.style.backgroundColor = connected ? "#10b981" : "#ef4444";
        if (text) text.textContent = connected ? "Connected" : "Reconnecting\u2026";
    }

    function hexToRgba(hex, alpha) {
        var r = parseInt(hex.slice(1, 3), 16);
        var g = parseInt(hex.slice(3, 5), 16);
        var b = parseInt(hex.slice(5, 7), 16);
        return "rgba(" + r + "," + g + "," + b + "," + alpha + ")";
    }

    function makeUserBadge(name, color, isSelf) {
        var badge = document.createElement("div");
        badge.style.display = "flex";
        badge.style.alignItems = "center";
        badge.style.gap = "5px";

        var dot = document.createElement("span");
        dot.style.width = "10px";
        dot.style.height = "10px";
        dot.style.borderRadius = "50%";
        dot.style.backgroundColor = color;
        dot.style.display = "inline-block";
        dot.style.flexShrink = "0";

        var label = document.createElement("span");
        label.textContent = isSelf ? name + " (you)" : name;
        label.style.fontSize = "13px";
        label.style.fontWeight = "500";
        label.style.color = color;

        badge.appendChild(dot);
        badge.appendChild(label);
        return badge;
    }

    // ========== USERS BAR ==========

    function updateUsersBar() {
        var bar = document.getElementById("users-bar");
        if (!bar) return;

        bar.innerHTML = "";

        // Self first
        if (myUserId) {
            bar.appendChild(makeUserBadge(myUserName, myUserColor, true));
        }

        // Remote users
        var ids = Object.keys(remoteUsers);
        for (var i = 0; i < ids.length; i++) {
            var user = remoteUsers[ids[i]];
            bar.appendChild(makeUserBadge(user.name, user.color, false));
        }
    }

    // ========== CURSOR HIGHLIGHTS ==========

    function updateCursorHighlights() {
        var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
        if (!updater || !updater.setHighlightRegions) return;

        var regions = [];
        var ids = Object.keys(remoteUsers);
        for (var i = 0; i < ids.length; i++) {
            var user = remoteUsers[ids[i]];
            if (user.cursor) {
                regions.push({
                    color: hexToRgba(user.color, 0.25),
                    range: {
                        x: user.cursor.col,
                        y: user.cursor.row,
                        width: 1,
                        height: 1,
                    },
                });
            }
        }
        updater.setHighlightRegions(regions);
    }

    // ========== MESSAGE HANDLERS ==========

    function handleInit(msg) {
        myUserId = msg.userId;
        myUserName = msg.userName;
        myUserColor = msg.userColor;

        // Build remote users map (exclude self)
        remoteUsers = {};
        for (var i = 0; i < msg.users.length; i++) {
            var u = msg.users[i];
            if (u.id !== myUserId) {
                remoteUsers[u.id] = {
                    name: u.name,
                    color: u.color,
                    cursor: u.cursor,
                };
            }
        }

        // Set grid accent color to this user's color
        var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
        if (updater && updater.setProps) {
            updater.setProps({
                theme: {
                    accentColor: myUserColor,
                    accentLight: hexToRgba(myUserColor, 0.2),
                },
            });
        }

        // Sync full data from server (source of truth)
        if (updater && msg.data) {
            var dataRef = updater.getData();
            if (dataRef) {
                // Overwrite all rows in place
                for (var r = 0; r < msg.data.length && r < dataRef.length; r++) {
                    Object.assign(dataRef[r], msg.data[r]);
                }

                // Force full repaint
                var gridRef = updater.ref;
                if (gridRef) {
                    var cells = [];
                    for (var row = 0; row < dataRef.length; row++) {
                        for (var col = 0; col < NUM_COLUMNS; col++) {
                            cells.push({ cell: [col, row] });
                        }
                    }
                    gridRef.updateCells(cells);
                }
            }
        }

        updateUsersBar();
        updateCursorHighlights();
    }

    function handleCursorUpdate(msg) {
        if (!remoteUsers[msg.userId]) {
            remoteUsers[msg.userId] = {
                name: msg.userName,
                color: msg.color,
                cursor: null,
            };
        }
        remoteUsers[msg.userId].cursor = { col: msg.col, row: msg.row };
        updateCursorHighlights();
    }

    function handleRemoteEdit(msg) {
        var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
        if (!updater) return;

        var data = {};
        data[msg.colId] = msg.value;

        updater.updateCells([
            {
                row: msg.row,
                data: data,
                flash: msg.color,
            },
        ]);
    }

    function handleUserJoined(msg) {
        remoteUsers[msg.userId] = {
            name: msg.userName,
            color: msg.userColor,
            cursor: null,
        };
        updateUsersBar();
    }

    function handleUserLeft(msg) {
        delete remoteUsers[msg.userId];
        updateUsersBar();
        updateCursorHighlights();
    }

    // ========== WEBSOCKET ==========

    function connect() {
        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        var ws = new WebSocket(protocol + "//" + location.host + "/ws/collab");
        window._collabWs = ws;

        ws.onopen = function () {
            updateStatus(true);
        };

        ws.onmessage = function (event) {
            var msg = JSON.parse(event.data);
            switch (msg.type) {
                case "init":
                    handleInit(msg);
                    break;
                case "cursor":
                    handleCursorUpdate(msg);
                    break;
                case "edit":
                    handleRemoteEdit(msg);
                    break;
                case "user_joined":
                    handleUserJoined(msg);
                    break;
                case "user_left":
                    handleUserLeft(msg);
                    break;
            }
        };

        ws.onclose = function () {
            updateStatus(false);
            window._collabWs = null;
            setTimeout(connect, 2000);
        };

        ws.onerror = function () {
            ws.close();
        };
    }

    // ========== INIT ==========

    var _waitAttempts = 0;
    var _maxWaitAttempts = 50; // ~10 seconds

    function waitForGrid(cb) {
        if (document.getElementById(GRID_ID)) {
            cb();
        } else if (_waitAttempts++ < _maxWaitAttempts) {
            setTimeout(function () {
                waitForGrid(cb);
            }, 200);
        }
    }

    function init() {
        waitForGrid(connect);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
