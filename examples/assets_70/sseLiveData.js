/**
 * SSE (Server-Sent Events) client for Example 70 — Live Market Data via SSE
 *
 * Uses the browser's EventSource API instead of WebSocket.
 * Key differences from websocketLiveData.js:
 * - EventSource auto-reconnects on disconnect (no manual retry)
 * - Named events ("update") instead of raw onmessage
 * - No DashMiddleware patch needed on the server
 * - Grid update logic is identical — only the transport changed
 */

(function () {
    "use strict";

    var GRID_ID = "live-grid";

    // ========== HELPERS ==========

    function updateStatus(connected) {
        var dot = document.getElementById("sse-status-dot");
        var text = document.getElementById("sse-status-text");
        if (dot) dot.style.backgroundColor = connected ? "#10b981" : "#ef4444";
        if (text) text.textContent = connected ? "Connected (SSE)" : "Reconnecting\u2026";
    }

    function updateStats(updater) {
        var data = updater.getData();
        if (!data) return;
        var gainers = 0, losers = 0, totalPct = 0, totalVol = 0;
        for (var j = 0; j < data.length; j++) {
            var r = data[j];
            if (r.change > 0) gainers++;
            else if (r.change < 0) losers++;
            totalPct += r.changePct || 0;
            totalVol += r.volume || 0;
        }
        var avg = totalPct / data.length;
        var el;
        if ((el = document.getElementById("stat-gainers"))) el.textContent = gainers;
        if ((el = document.getElementById("stat-losers"))) el.textContent = losers;
        if ((el = document.getElementById("stat-avg"))) {
            el.textContent = (avg >= 0 ? "+" : "") + avg.toFixed(2) + "%";
            el.style.color = avg >= 0 ? "#10b981" : "#ef4444";
        }
        if ((el = document.getElementById("stat-vol"))) {
            el.textContent = totalVol.toLocaleString();
        }
    }

    // ========== SSE CONNECTION ==========

    var msgCount = 0;
    var lastCountReset = Date.now();

    function connect() {
        // EventSource: one line, auto-reconnects on failure
        var es = new EventSource("/api/stream");

        es.addEventListener("open", function () {
            updateStatus(true);
        });

        // Listen for named "update" events from the server
        es.addEventListener("update", function (event) {
            var msg = JSON.parse(event.data);
            if (!msg.updates) return;

            var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
            if (!updater) return;

            var updates = [];
            for (var i = 0; i < msg.updates.length; i++) {
                var u = msg.updates[i];
                updates.push({
                    row: u.row,
                    values: {
                        price: u.price,
                        change: u.change,
                        changePct: u.changePct,
                        volume: u.volume,
                        bid: u.bid,
                        ask: u.ask
                    },
                    flash: u.change >= 0 ? "#10b981" : "#ef4444"
                });
            }

            updater.updateCells(updates);
            updateStats(updater);

            // Track updates/sec
            msgCount++;
            var elapsed = (Date.now() - lastCountReset) / 1000;
            if (elapsed >= 1) {
                var ups = document.getElementById("stat-ups");
                if (ups) ups.textContent = (msgCount / elapsed).toFixed(1);
                msgCount = 0;
                lastCountReset = Date.now();
            }
        });

        es.addEventListener("error", function () {
            // EventSource auto-reconnects — just update the UI
            updateStatus(false);
        });
    }

    // ========== INIT ==========

    var _waitAttempts = 0;
    var _maxWaitAttempts = 50; // ~10 seconds

    function waitForGrid(cb) {
        if (document.getElementById(GRID_ID)) {
            cb();
        } else if (_waitAttempts++ < _maxWaitAttempts) {
            setTimeout(function () { waitForGrid(cb); }, 200);
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
