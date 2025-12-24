import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import PropTypes from 'prop-types';

/**
 * CellContextMenu - A context menu component for cell right-click actions
 * Renders as a portal positioned near the cell
 */
const CellContextMenu = ({
    isOpen,
    onClose,
    position,
    cellInfo,
    items,
    onItemClick,
    theme
}) => {
    const menuRef = useRef(null);
    const [hoveredIndex, setHoveredIndex] = useState(-1);

    // Click outside to close
    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (e) => {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                onClose();
            }
        };

        // Use capture phase to ensure we catch clicks on canvas elements
        document.addEventListener('mousedown', handleClickOutside, true);
        return () => document.removeEventListener('mousedown', handleClickOutside, true);
    }, [isOpen, onClose]);

    // Escape to close
    useEffect(() => {
        if (!isOpen) return;

        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                onClose();
            }
        };

        document.addEventListener('keydown', handleEscape);
        return () => document.removeEventListener('keydown', handleEscape);
    }, [isOpen, onClose]);

    // Reset hover state when menu closes
    useEffect(() => {
        if (!isOpen) {
            setHoveredIndex(-1);
        }
    }, [isOpen]);

    // Theme-based styles
    const styles = useMemo(() => {
        const t = theme || {};
        const bgColor = t.bgCell || '#ffffff';
        const textColor = t.textDark || '#1a1a1a';
        const borderColor = t.borderColor || '#e0e0e0';
        const fontFamily = t.fontFamily || '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        const fontSize = t.baseFontStyle || '13px';

        return {
            container: {
                position: 'fixed',
                backgroundColor: bgColor,
                border: `1px solid ${borderColor}`,
                borderRadius: '6px',
                boxShadow: '0 4px 16px rgba(0,0,0,0.15)',
                fontFamily: fontFamily,
                fontSize: fontSize,
                color: textColor,
                minWidth: '160px',
                maxWidth: '280px',
                overflow: 'hidden',
                zIndex: 10000,
                padding: '4px 0'
            },
            menuItem: {
                padding: '8px 12px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                transition: 'background-color 0.1s',
                userSelect: 'none'
            },
            menuItemHover: {
                backgroundColor: t.bgHeaderHovered || '#f0f0f0'
            },
            menuItemDisabled: {
                opacity: 0.5,
                cursor: 'not-allowed'
            },
            icon: {
                width: '16px',
                textAlign: 'center',
                flexShrink: 0
            },
            label: {
                flex: 1,
                overflow: 'hidden',
                textOverflow: 'ellipsis',
                whiteSpace: 'nowrap'
            },
            divider: {
                height: '1px',
                backgroundColor: borderColor,
                margin: '4px 0'
            }
        };
    }, [theme]);

    // Calculate menu position with viewport bounds checking
    const menuStyle = useMemo(() => {
        if (!position) return { ...styles.container, display: 'none' };

        const menuWidth = 200;
        const menuHeight = (items?.length || 0) * 36 + 8; // Approximate height

        let left = position.x;
        let top = position.y;

        // Check if we're in a browser environment
        if (typeof window !== 'undefined') {
            // Flip horizontally if would overflow right edge
            if (left + menuWidth > window.innerWidth - 10) {
                left = Math.max(10, window.innerWidth - menuWidth - 10);
            }

            // Flip vertically if would overflow bottom edge
            if (top + menuHeight > window.innerHeight - 10) {
                top = Math.max(10, position.y - menuHeight);
            }
        }

        return {
            ...styles.container,
            left: `${left}px`,
            top: `${top}px`
        };
    }, [position, styles.container, items]);

    // Handle item click
    const handleItemClick = useCallback((item) => {
        if (item.disabled) return;
        onItemClick(item.id);
    }, [onItemClick]);

    if (!isOpen || !items || items.length === 0) return null;

    const menuContent = (
        <>
            {/* Invisible backdrop to catch clicks outside */}
            <div
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    bottom: 0,
                    zIndex: 9999
                }}
                onClick={onClose}
            />
            <div ref={menuRef} style={menuStyle}>
                {items.map((item, index) => (
                    <React.Fragment key={item.id}>
                        <div
                            style={{
                                ...styles.menuItem,
                                ...(hoveredIndex === index && !item.disabled ? styles.menuItemHover : {}),
                                ...(item.disabled ? styles.menuItemDisabled : {})
                            }}
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(-1)}
                            onClick={() => handleItemClick(item)}
                        >
                            {item.icon && (
                                <span style={styles.icon}>{item.icon}</span>
                            )}
                            <span style={styles.label}>{item.label}</span>
                        </div>
                        {item.dividerAfter && <div style={styles.divider} />}
                    </React.Fragment>
                ))}
            </div>
        </>
    );

    // Portal to body
    if (typeof document !== 'undefined') {
        return createPortal(menuContent, document.body);
    }

    return null;
};

CellContextMenu.propTypes = {
    /** Whether the menu is open */
    isOpen: PropTypes.bool.isRequired,
    /** Callback when menu should close */
    onClose: PropTypes.func.isRequired,
    /** Screen position {x, y} where menu should appear */
    position: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number
    }),
    /** Information about the cell: {col, row} */
    cellInfo: PropTypes.shape({
        col: PropTypes.number,
        row: PropTypes.number
    }),
    /** Menu items to display */
    items: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        icon: PropTypes.string,
        dividerAfter: PropTypes.bool,
        disabled: PropTypes.bool
    })),
    /** Callback when an item is clicked: (itemId) => void */
    onItemClick: PropTypes.func.isRequired,
    /** Grid theme object for styling */
    theme: PropTypes.object
};

CellContextMenu.defaultProps = {
    items: []
};

export default CellContextMenu;
