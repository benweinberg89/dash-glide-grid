/**
 * Custom LinksCellRenderer for Dash integration.
 *
 * Renders multiple hyperlinks in a cell with click handling.
 * Fires Dash callbacks when a link is clicked.
 */
import { GridCellKind, getMiddleCenterBias } from "@glideapps/glide-data-grid";

/**
 * Factory function to create a LinksCellRenderer with a click callback
 * @param {Function} onLinkClick - Callback receiving { col, row, href, title, linkIndex }
 */
export function createLinksCellRenderer(onLinkClick) {
    return {
        kind: GridCellKind.Custom,
        isMatch: (c) => c.data?.kind === "links-cell",

        draw: (args, cell) => {
            const { ctx, theme, rect, hoverX, hoverY } = args;
            const { links = [], maxLinks, underlineOffset = 5 } = cell.data;

            const padding = theme.cellHorizontalPadding ?? 8;
            const baselineY = rect.height / 2 + getMiddleCenterBias(ctx, theme);
            const drawY = rect.y + baselineY;
            const availableWidth = rect.width - padding * 2;

            ctx.font = `${theme.baseFontStyle} ${theme.fontFamily}`;

            // Calculate link positions (relative to cell, not absolute)
            const separator = ", ";
            const separatorWidth = ctx.measureText(separator).width;
            const linkPositions = [];
            let relativeX = padding; // Start position relative to cell left edge

            // Limit links if maxLinks specified
            const displayLinks = maxLinks ? links.slice(0, maxLinks) : links;

            for (let i = 0; i < displayLinks.length; i++) {
                const link = displayLinks[i];
                const title = link.title || link.href || "Link";
                const textWidth = ctx.measureText(title).width;

                // Check if this link fits
                const needsSeparator = i < displayLinks.length - 1;
                const totalWidth = textWidth + (needsSeparator ? separatorWidth : 0);

                if (relativeX + totalWidth > availableWidth + padding && linkPositions.length > 0) {
                    // Draw ellipsis if we can't fit more
                    ctx.fillStyle = theme.textMedium || theme.textDark;
                    ctx.fillText("...", rect.x + relativeX, drawY);
                    break;
                }

                linkPositions.push({
                    relX: relativeX,  // Relative to cell left
                    width: textWidth,
                    title: title,
                    href: link.href,
                    index: i
                });

                relativeX += textWidth;

                // Draw separator if not last
                if (needsSeparator) {
                    ctx.fillStyle = theme.textMedium || theme.textDark;
                    ctx.fillText(separator, rect.x + relativeX, drawY);
                    relativeX += separatorWidth;
                }
            }

            // Check which link is hovered (hoverX/hoverY are relative to cell)
            let hoveredLink = null;
            if (hoverX !== undefined && hoverY !== undefined) {
                // hoverX is relative to cell left edge
                for (const pos of linkPositions) {
                    if (hoverX >= pos.relX && hoverX <= pos.relX + pos.width) {
                        hoveredLink = pos;
                        break;
                    }
                }
            }

            // Draw links
            for (const pos of linkPositions) {
                const isHovered = hoveredLink === pos;
                const drawX = rect.x + pos.relX;

                // Use accent color for links, brighter on hover
                ctx.fillStyle = isHovered
                    ? (theme.accentColor || "#2563eb")
                    : (theme.linkColor || theme.accentLight || "#3b82f6");

                ctx.fillText(pos.title, drawX, drawY);

                // Draw underline on hover
                if (isHovered) {
                    const underlineY = drawY + underlineOffset;
                    ctx.beginPath();
                    ctx.moveTo(drawX, underlineY);
                    ctx.lineTo(drawX + pos.width, underlineY);
                    ctx.strokeStyle = theme.accentColor || "#2563eb";
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }

            // Store link positions for click handling (relative coordinates)
            cell.data._linkPositions = linkPositions;

            return true;
        },

        measure: (ctx, cell, theme) => {
            const { links = [] } = cell.data;
            const separator = ", ";
            const separatorWidth = ctx.measureText(separator).width;

            let totalWidth = 0;
            for (let i = 0; i < links.length; i++) {
                const link = links[i];
                const title = link.title || link.href || "Link";
                totalWidth += ctx.measureText(title).width;
                if (i < links.length - 1) {
                    totalWidth += separatorWidth;
                }
            }

            return totalWidth + (theme.cellHorizontalPadding ?? 8) * 2;
        },

        onClick: (args) => {
            const { cell, posX, bounds, location } = args;
            const { links = [] } = cell.data;

            // Recalculate link positions since _linkPositions may not persist
            const padding = 8; // Default padding
            const separator = ", ";

            // Simple recalculation of positions
            let relativeX = padding;
            for (let i = 0; i < links.length; i++) {
                const link = links[i];
                const title = link.title || link.href || "Link";
                // Approximate text width (we don't have ctx here, use char count * 7)
                const textWidth = title.length * 7;

                if (posX >= relativeX && posX <= relativeX + textWidth) {
                    if (onLinkClick) {
                        onLinkClick({
                            col: location[0],
                            row: location[1],
                            href: link.href || "",
                            title: title,
                            linkIndex: i
                        });
                    }

                    // Open link in new tab if href exists and navigateOn is "click"
                    const navigateOn = cell.data.navigateOn ?? "click";
                    if (link.href && navigateOn === "click") {
                        window.open(link.href, "_blank", "noopener,noreferrer");
                    }

                    return undefined;
                }

                relativeX += textWidth;
                if (i < links.length - 1) {
                    relativeX += separator.length * 7; // separator width
                }
            }

            return undefined;
        },

        // Show pointer cursor when hovering over links
        onPointerEnter: () => ({ cursor: "pointer" }),
        onPointerLeave: () => undefined,

        // Prevent cell selection when clicking links
        onSelect: (args) => {
            args.preventDefault();
        },

        // No editor for links
        provideEditor: undefined,

        // Copy link URLs
        onPaste: (val, data) => {
            // Parse comma-separated URLs
            const urls = val.split(",").map(u => u.trim()).filter(u => u);
            return {
                ...data,
                links: urls.map(url => ({ title: url, href: url }))
            };
        }
    };
}

export default createLinksCellRenderer;
