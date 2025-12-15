/**
 * Custom UserProfileCellRenderer for Dash integration.
 *
 * Displays an avatar (circle with initials or image) and optional name. Read-only.
 *
 * Data structure:
 * {
 *   kind: "user-profile-cell",
 *   name: "Alice Johnson",
 *   image: "https://example.com/avatar.jpg",  // Optional
 *   initial: "A",                              // Single char fallback
 *   tint: "#3b82f6"                            // Avatar background color
 * }
 */
import { GridCellKind, getMiddleCenterBias } from "@glideapps/glide-data-grid";

// Simple image cache
const imageCache = new Map();

function loadImage(url) {
    if (imageCache.has(url)) {
        return imageCache.get(url);
    }

    const img = new Image();
    img.crossOrigin = "anonymous";
    img.src = url;

    const promise = new Promise((resolve) => {
        img.onload = () => resolve(img);
        img.onerror = () => resolve(null);
    });

    imageCache.set(url, { img, loaded: false, promise });

    promise.then((result) => {
        if (result) {
            imageCache.set(url, { img: result, loaded: true });
        } else {
            imageCache.delete(url);
        }
    });

    return imageCache.get(url);
}

/**
 * Factory function to create a UserProfileCellRenderer
 */
export function createUserProfileCellRenderer() {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "user-profile-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect, requestAnimationFrame } = args;
            const { name, image, initial, tint } = cell.data;

            const padding = theme.cellHorizontalPadding;
            const verticalPadding = 4;

            // Avatar dimensions
            const avatarRadius = Math.min(14, (rect.height - verticalPadding * 2) / 2);
            const avatarX = rect.x + padding + avatarRadius;
            const avatarY = rect.y + rect.height / 2;

            // Draw avatar background circle
            ctx.beginPath();
            ctx.arc(avatarX, avatarY, avatarRadius, 0, Math.PI * 2);
            ctx.closePath();

            // Fill with tint color (with some transparency)
            const bgColor = tint || theme.accentColor || "#3b82f6";
            ctx.fillStyle = bgColor + "33"; // 20% opacity
            ctx.fill();

            // Try to draw image
            let imageDrawn = false;
            if (image) {
                const cached = loadImage(image);
                if (cached && cached.loaded && cached.img) {
                    // Save state for clipping
                    ctx.save();

                    // Clip to circle
                    ctx.beginPath();
                    ctx.arc(avatarX, avatarY, avatarRadius, 0, Math.PI * 2);
                    ctx.clip();

                    // Draw image centered and covering the circle
                    const img = cached.img;
                    const size = avatarRadius * 2;
                    ctx.drawImage(
                        img,
                        avatarX - avatarRadius,
                        avatarY - avatarRadius,
                        size,
                        size
                    );

                    ctx.restore();
                    imageDrawn = true;
                } else if (cached && !cached.loaded && requestAnimationFrame) {
                    // Image still loading, request redraw
                    cached.promise.then(() => {
                        requestAnimationFrame();
                    });
                }
            }

            // Draw initial if no image
            if (!imageDrawn && initial) {
                ctx.fillStyle = tint || theme.accentColor || "#3b82f6";
                ctx.font = `600 ${Math.round(avatarRadius)}px ${theme.fontFamily}`;
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText(initial.charAt(0).toUpperCase(), avatarX, avatarY);
            }

            // Draw name text
            if (name) {
                const nameX = rect.x + padding + avatarRadius * 2 + 8;
                ctx.fillStyle = theme.textDark;
                ctx.font = `${theme.baseFontStyle} ${theme.fontFamily}`;
                ctx.textAlign = "start";
                ctx.textBaseline = "middle";
                ctx.fillText(name, nameX, rect.y + rect.height / 2 + getMiddleCenterBias(ctx, theme));
            }

            // Reset text align
            ctx.textAlign = "start";

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { name } = cell.data;
            const avatarWidth = 28 + 8; // diameter + spacing

            ctx.font = `${theme.baseFontStyle} ${theme.fontFamily}`;
            const nameWidth = name ? ctx.measureText(name).width : 0;

            return theme.cellHorizontalPadding * 2 + avatarWidth + nameWidth;
        },

        // No click handling - read only
        onClick: () => undefined,

        // No editor - read only
        provideEditor: undefined,

        // Copy name as text
        onPaste: (val, data) => ({
            ...data,
            name: val
        })
    };
}

export default createUserProfileCellRenderer;
