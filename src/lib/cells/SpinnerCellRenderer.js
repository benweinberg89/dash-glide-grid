/**
 * Custom SpinnerCellRenderer for Dash integration.
 *
 * Displays an animated loading spinner. Read-only.
 *
 * Data structure:
 * {
 *   kind: "spinner-cell"
 * }
 */
import { GridCellKind } from "@glideapps/glide-data-grid";

/**
 * Factory function to create a SpinnerCellRenderer
 */
export function createSpinnerCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "spinner-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect, requestAnimationFrame } = args;

            // Calculate animation progress (0 to 1, loops every 1 second)
            const progress = (performance.now() % 1000) / 1000;

            // Spinner dimensions
            const centerX = rect.x + rect.width / 2;
            const centerY = rect.y + rect.height / 2;
            const radius = Math.min(12, rect.height / 4);

            // Calculate rotation angle
            const startAngle = progress * Math.PI * 2;
            const arcLength = Math.PI * 1.5; // 270 degrees

            // Draw spinner arc
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, startAngle, startAngle + arcLength);
            ctx.strokeStyle = theme.textMedium || "#6b7280";
            ctx.lineWidth = 2;
            ctx.lineCap = "round";
            ctx.stroke();

            // Request next animation frame for continuous animation
            if (requestAnimationFrame) {
                requestAnimationFrame();
            }

            return true;
        },

        measure: () => {
            // Fixed width for spinner
            return 50;
        },

        // No click handling - read only
        onClick: () => undefined,

        // No editor - read only
        provideEditor: undefined,

        // Nothing to paste
        onPaste: (val, data) => data
    };
}

export default createSpinnerCellRenderer;
