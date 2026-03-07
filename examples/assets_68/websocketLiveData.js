/**
 * WebSocket client + Stress Test for Example 68 — Live Market Data
 *
 * Two modes:
 * 1. WebSocket mode: server pushes updates via WS, JS applies them imperatively
 * 2. Stress test mode: client-side loop generates random updates at configurable rate
 *
 * Both use window.dashGlideGrid for zero-React grid updates.
 */

(function () {
    "use strict";

    var GRID_ID = "live-grid";

    // ========== SHARED HELPERS ==========

    function updateStatus(connected) {
        var dot = document.getElementById("ws-status-dot");
        var text = document.getElementById("ws-status-text");
        if (dot) dot.style.backgroundColor = connected ? "#10b981" : "#ef4444";
        if (text) text.textContent = connected ? "Connected" : "Reconnecting\u2026";
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

    // ========== WEBSOCKET MODE ==========

    var msgCount = 0;
    var lastCountReset = Date.now();

    function connect() {
        var protocol = location.protocol === "https:" ? "wss:" : "ws:";
        var ws = new WebSocket(protocol + "//" + location.host + "/ws/live-data");

        ws.onopen = function () {
            function tryUpdate() {
                if (document.getElementById("ws-status-dot")) {
                    updateStatus(true);
                } else {
                    setTimeout(tryUpdate, 100);
                }
            }
            tryUpdate();
        };

        ws.onmessage = function (event) {
            var msg = JSON.parse(event.data);
            if (!msg.updates) return;

            var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
            if (!updater) return;

            var updates = [];
            for (var i = 0; i < msg.updates.length; i++) {
                var u = msg.updates[i];
                updates.push({
                    row: u.row,
                    data: {
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

            msgCount++;
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

    // ========== STRESS TEST MODE ==========

    var stressRunning = false;
    var stressTimerId = null;

    // Perf tracking
    var stressFrames = 0;
    var stressCells = 0;
    var stressPerfStart = 0;
    var stressLastPerfUpdate = 0;

    // Simple fast PRNG (xorshift32) — Math.random() is slow in tight loops
    var _seed = 1;
    function xrand() {
        _seed ^= _seed << 13;
        _seed ^= _seed >> 17;
        _seed ^= _seed << 5;
        return (_seed >>> 0);
    }

    function stressTick() {
        var updater = window.dashGlideGrid && window.dashGlideGrid[GRID_ID];
        if (!updater || !stressRunning) return;

        var data = updater.getData();
        if (!data) return;
        var totalRows = data.length;

        // Read controls
        var rowsPerTick = parseInt(document.getElementById("stress-rows").value) || 50;
        if (rowsPerTick > totalRows) rowsPerTick = totalRows;

        var updates = [];
        for (var i = 0; i < rowsPerTick; i++) {
            var rowIdx = xrand() % totalRows;
            var row = data[rowIdx];
            if (!row) continue;

            // Random walk the price
            var basePrice = row.price || 100;
            var delta = ((xrand() % 200) - 100) / 10000 * basePrice; // ~1% max move
            var newPrice = Math.round((basePrice + delta) * 100) / 100;
            var origPrice = row._origPrice || basePrice;
            if (!row._origPrice) row._origPrice = basePrice;
            var change = Math.round((newPrice - origPrice) * 100) / 100;
            var changePct = Math.round(change / origPrice * 10000) / 100;
            var spread = Math.round((xrand() % 10 + 1) / 100 * 100) / 100;

            updates.push({
                row: rowIdx,
                data: {
                    price: newPrice,
                    change: change,
                    changePct: changePct,
                    volume: (xrand() % 50000000) + 1000000,
                    bid: Math.round((newPrice - spread) * 100) / 100,
                    ask: Math.round((newPrice + spread) * 100) / 100
                },
                flash: change >= 0 ? "#10b981" : "#ef4444"
            });
        }

        var t0 = performance.now();
        updater.updateCells(updates);
        var dt = performance.now() - t0;

        // Track perf
        stressFrames++;
        stressCells += updates.length * 6; // 6 columns updated per row

        var now = performance.now();
        if (now - stressLastPerfUpdate > 500) {
            var elapsed = (now - stressPerfStart) / 1000;
            var fps = stressFrames / elapsed;
            var cellsPerSec = stressCells / elapsed;
            var perfEl = document.getElementById("stress-perf");
            if (perfEl) {
                perfEl.textContent =
                    fps.toFixed(0) + " fps | " +
                    (cellsPerSec / 1000).toFixed(1) + "k cells/s | " +
                    dt.toFixed(1) + "ms/tick";
                perfEl.style.color = dt > 16 ? "#ef4444" : "#10b981";
            }
            stressLastPerfUpdate = now;
        }

        // Update stats every ~10 frames
        if (stressFrames % 10 === 0) {
            updateStats(updater);
        }
    }

    function startStress() {
        if (stressRunning) return;
        stressRunning = true;

        stressFrames = 0;
        stressCells = 0;
        stressPerfStart = performance.now();
        stressLastPerfUpdate = 0;

        var rate = parseInt(document.getElementById("stress-rate").value) || 30;
        scheduleStress(rate);

        var btn = document.getElementById("stress-btn");
        if (btn) {
            btn.textContent = "Stop";
            btn.style.backgroundColor = "#fee2e2";
            btn.style.borderColor = "#fca5a5";
        }
    }

    function stopStress() {
        stressRunning = false;
        if (stressTimerId !== null) {
            clearInterval(stressTimerId);
            stressTimerId = null;
        }

        var btn = document.getElementById("stress-btn");
        if (btn) {
            btn.textContent = "Start";
            btn.style.backgroundColor = "#fff";
            btn.style.borderColor = "#d1d5db";
        }
    }

    function scheduleStress(hz) {
        if (stressTimerId !== null) clearInterval(stressTimerId);
        if (hz >= 60) {
            // Use rAF for max frame rate
            function rafLoop() {
                if (!stressRunning) return;
                stressTick();
                requestAnimationFrame(rafLoop);
            }
            stressTimerId = -1; // sentinel
            requestAnimationFrame(rafLoop);
        } else {
            stressTimerId = setInterval(stressTick, 1000 / hz);
        }
    }

    // ========== INIT ==========

    function initControls() {
        var btn = document.getElementById("stress-btn");
        if (!btn) {
            // Dash layout hasn't rendered yet — retry
            setTimeout(initControls, 200);
            return;
        }

        btn.addEventListener("click", function () {
            if (stressRunning) {
                stopStress();
            } else {
                startStress();
            }
        });

        // Rate slider label
        var rateSlider = document.getElementById("stress-rate");
        var rateLabel = document.getElementById("stress-rate-label");
        if (rateSlider && rateLabel) {
            rateSlider.addEventListener("input", function () {
                var v = parseInt(rateSlider.value);
                rateLabel.textContent = v >= 60 ? "rAF" : v + " Hz";
                if (stressRunning) {
                    // Reschedule at new rate
                    if (stressTimerId !== null && stressTimerId !== -1) clearInterval(stressTimerId);
                    scheduleStress(v);
                }
            });
        }

        // Rows/tick slider label
        var rowsSlider = document.getElementById("stress-rows");
        var rowsLabel = document.getElementById("stress-rows-label");
        if (rowsSlider && rowsLabel) {
            rowsSlider.addEventListener("input", function () {
                rowsLabel.textContent = rowsSlider.value;
            });
        }
    }

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
        waitForGrid(function () {
            connect();
            initControls();
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
