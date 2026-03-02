/**
 * WebSocket client for Example 67 — Live Market Data
 *
 * Connects to the FastAPI WebSocket endpoint and queues incoming
 * price updates for the Dash clientside callback to consume.
 */

(function () {
    "use strict";

    // Message queue — drained by the Dash clientside callback every 100ms
    window._wsQueue = [];

    // Updates-per-second counter
    var msgCount = 0;
    var lastCountReset = Date.now();

    function updateStatus(connected) {
        var dot = document.getElementById("ws-status-dot");
        var text = document.getElementById("ws-status-text");
        if (dot) dot.style.backgroundColor = connected ? "#10b981" : "#ef4444";
        if (text) text.textContent = connected ? "Connected" : "Reconnecting\u2026";
    }

    function connect() {
        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        var ws = new WebSocket(protocol + "//" + location.host + "/ws/live-data");

        ws.onopen = function () {
            updateStatus(true);
            ws.send("ping");
        };

        ws.onmessage = function (event) {
            window._wsQueue.push(JSON.parse(event.data));
            msgCount++;

            // Update msg/s display directly (no Dash round-trip needed)
            var elapsed = (Date.now() - lastCountReset) / 1000;
            if (elapsed >= 1) {
                var ups = document.getElementById("stat-ups");
                if (ups) ups.textContent = (msgCount / elapsed).toFixed(1);
                msgCount = 0;
                lastCountReset = Date.now();
            }
        };

        ws.onclose = function () {
            updateStatus(false);
            setTimeout(connect, 2000);
        };

        ws.onerror = function () {
            ws.close();
        };
    }

    // Connect once the page is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", connect);
    } else {
        connect();
    }
})();
