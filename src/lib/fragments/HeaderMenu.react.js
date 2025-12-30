import React, { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import PropTypes from 'prop-types';

/**
 * HeaderMenu - A filter menu component for column headers
 * Renders as a portal positioned near the column header
 */
const HeaderMenu = ({
    isOpen,
    onClose,
    position,
    columnIndex,
    columnTitle,
    uniqueValues,
    selectedValues,
    onFilterChange,
    theme,
    customItems,
    onCustomItemClick,
    anchorToHeader = true,
    zIndex = 1000
}) => {
    // Local state for search within filter list
    const [filterSearch, setFilterSearch] = useState('');
    const menuRef = useRef(null);
    const searchInputRef = useRef(null);

    // Track scroll offset to reposition menu when page scrolls
    const [scrollOffset, setScrollOffset] = useState({ x: 0, y: 0 });
    const initialScrollRef = useRef({ x: 0, y: 0 });

    // Focus search input when menu opens
    useEffect(() => {
        if (isOpen && searchInputRef.current) {
            // Small delay to ensure the menu is rendered
            setTimeout(() => {
                searchInputRef.current?.focus();
            }, 50);
        }
    }, [isOpen]);

    // Reset search when menu closes
    useEffect(() => {
        if (!isOpen) {
            setFilterSearch('');
        }
    }, [isOpen]);

    // Click outside to close
    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (e) => {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                onClose();
            }
        };

        // Use capture phase to ensure we catch clicks on canvas elements (like Glide grid)
        // that might not bubble events properly
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

    // Track scroll position to keep menu anchored to header
    // When page scrolls, we adjust menu position by the scroll delta
    // This feature can be toggled off with anchorToHeader=false
    useEffect(() => {
        if (!isOpen || !anchorToHeader) {
            // Reset when menu closes or anchoring is disabled
            setScrollOffset({ x: 0, y: 0 });
            return;
        }

        // Capture initial scroll position when menu opens
        initialScrollRef.current = {
            x: window.scrollX || window.pageXOffset,
            y: window.scrollY || window.pageYOffset
        };

        const handleScroll = () => {
            const currentX = window.scrollX || window.pageXOffset;
            const currentY = window.scrollY || window.pageYOffset;

            // Calculate how much we've scrolled since menu opened
            setScrollOffset({
                x: initialScrollRef.current.x - currentX,
                y: initialScrollRef.current.y - currentY
            });
        };

        // Listen for scroll on window (capture phase to catch all scroll events)
        window.addEventListener('scroll', handleScroll, true);
        return () => window.removeEventListener('scroll', handleScroll, true);
    }, [isOpen, anchorToHeader]);

    // Theme-based styles
    const styles = useMemo(() => {
        const t = theme || {};
        const bgColor = t.bgCell || '#ffffff';
        const headerBg = t.bgHeader || '#f8f9fa';
        const textColor = t.textDark || '#1a1a1a';
        const borderColor = t.borderColor || '#e0e0e0';
        const accentColor = t.accentColor || '#2563eb';
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
                minWidth: '220px',
                maxWidth: '320px',
                maxHeight: '400px',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                zIndex: zIndex
            },
            header: {
                padding: '10px 12px',
                borderBottom: `1px solid ${borderColor}`,
                backgroundColor: headerBg,
                fontWeight: '600',
                fontSize: '13px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            },
            closeButton: {
                background: 'none',
                border: 'none',
                cursor: 'pointer',
                padding: '4px',
                fontSize: '16px',
                color: t.textMedium || '#666',
                lineHeight: 1
            },
            searchContainer: {
                padding: '8px 12px',
                borderBottom: `1px solid ${borderColor}`
            },
            searchInput: {
                width: '100%',
                padding: '6px 10px',
                border: `1px solid ${borderColor}`,
                borderRadius: '4px',
                fontSize: fontSize,
                fontFamily: fontFamily,
                outline: 'none',
                boxSizing: 'border-box'
            },
            filterList: {
                flex: 1,
                overflowY: 'auto',
                padding: '4px 0',
                maxHeight: '250px'
            },
            filterItem: {
                padding: '6px 12px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                transition: 'background-color 0.1s'
            },
            filterItemHover: {
                backgroundColor: t.bgHeaderHovered || '#f0f0f0'
            },
            checkbox: {
                width: '16px',
                height: '16px',
                accentColor: accentColor,
                cursor: 'pointer',
                margin: 0
            },
            selectAllContainer: {
                padding: '8px 12px',
                borderBottom: `1px solid ${borderColor}`,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontWeight: '500'
            },
            clearButton: {
                padding: '6px 12px',
                borderTop: `1px solid ${borderColor}`,
                backgroundColor: headerBg,
                color: accentColor,
                cursor: 'pointer',
                textAlign: 'center',
                fontSize: '12px',
                fontWeight: '500'
            },
            noResults: {
                padding: '16px 12px',
                textAlign: 'center',
                color: t.textMedium || '#666',
                fontStyle: 'italic'
            },
            divider: {
                height: '1px',
                backgroundColor: borderColor,
                margin: '4px 0'
            },
            customItem: {
                padding: '8px 12px',
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
            }
        };
    }, [theme, zIndex]);

    // Calculate menu position with viewport bounds checking and scroll offset
    const menuStyle = useMemo(() => {
        if (!position) return { ...styles.container, display: 'none' };

        const menuWidth = 280;

        // Calculate actual menu height based on content
        // Fixed elements: header (~35px) + search (~45px) + selectAll (~35px) = ~115px
        const fixedHeight = 115;
        // Filter list: 8px padding + 28px per item, capped at 250px (maxHeight in CSS)
        // Use uniqueValues (not filteredValues) since search filtering happens after menu opens
        const filterListHeight = Math.min(8 + (uniqueValues?.length || 0) * 28, 250);
        // Custom items: 9px divider + 36px per item
        const customItemsHeight = customItems && customItems.length > 0
            ? 9 + customItems.length * 36
            : 0;
        // Clear button: ~25px (only shown when filter is active)
        const hasActiveFilter = selectedValues !== null && selectedValues.length !== uniqueValues.length;
        const clearButtonHeight = hasActiveFilter ? 25 : 0;

        // Total height, capped at 400px (maxHeight in CSS)
        const menuHeight = Math.min(
            fixedHeight + filterListHeight + customItemsHeight + clearButtonHeight,
            400
        );

        // Apply scroll offset to keep menu anchored to header when page scrolls
        let left = position.x + scrollOffset.x;
        let top = position.y + scrollOffset.y;

        // Check if we're in a browser environment
        if (typeof window !== 'undefined') {
            // Flip horizontally if would overflow right edge
            if (left + menuWidth > window.innerWidth - 10) {
                left = Math.max(10, window.innerWidth - menuWidth - 10);
            }

            // Flip vertically if would overflow bottom edge
            if (top + menuHeight > window.innerHeight - 10) {
                top = Math.max(10, position.y + scrollOffset.y - menuHeight);
            }
        }

        return {
            ...styles.container,
            left: `${left}px`,
            top: `${top}px`,
            zIndex: zIndex  // Explicitly set to ensure it's applied
        };
    }, [position, styles.container, scrollOffset, zIndex, customItems, selectedValues, uniqueValues]);

    // Filter unique values based on search
    const filteredValues = useMemo(() => {
        if (!filterSearch.trim()) {
            return uniqueValues;
        }
        const searchLower = filterSearch.toLowerCase();
        return uniqueValues.filter(val =>
            String(val).toLowerCase().includes(searchLower)
        );
    }, [uniqueValues, filterSearch]);

    // Compute selection state
    const allSelected = selectedValues === null ||
        (uniqueValues.length > 0 && selectedValues && selectedValues.length === uniqueValues.length);

    const noneSelected = selectedValues && selectedValues.length === 0;

    const someSelected = selectedValues !== null &&
        selectedValues.length > 0 &&
        selectedValues.length < uniqueValues.length;

    // Handle Select All toggle
    const handleSelectAll = useCallback(() => {
        if (allSelected) {
            // Deselect all
            onFilterChange(columnIndex, []);
        } else {
            // Select all (null means no filter = all selected)
            onFilterChange(columnIndex, null);
        }
    }, [allSelected, columnIndex, onFilterChange]);

    // Handle individual value toggle
    const handleValueToggle = useCallback((value) => {
        let newSelection;

        if (selectedValues === null) {
            // All were selected, now deselect this one
            newSelection = uniqueValues.filter(v => v !== value);
        } else if (selectedValues.includes(value)) {
            // Remove from selection
            newSelection = selectedValues.filter(v => v !== value);
        } else {
            // Add to selection
            newSelection = [...selectedValues, value];
        }

        // If all selected, convert to null (no filter)
        if (newSelection.length === uniqueValues.length) {
            onFilterChange(columnIndex, null);
        } else {
            onFilterChange(columnIndex, newSelection);
        }
    }, [selectedValues, uniqueValues, columnIndex, onFilterChange]);

    // Handle clear filter
    const handleClearFilter = useCallback(() => {
        onFilterChange(columnIndex, null);
        onClose();
    }, [columnIndex, onFilterChange, onClose]);

    // Check if a value is selected
    const isValueSelected = useCallback((value) => {
        if (selectedValues === null) return true;
        return selectedValues.includes(value);
    }, [selectedValues]);

    // Track hovered item for styling
    const [hoveredIndex, setHoveredIndex] = useState(-1);

    if (!isOpen) return null;

    // Backdrop style - invisible overlay to catch clicks outside the menu
    const backdropStyle = {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        zIndex: zIndex - 1  // Just below the menu
    };

    // Render via portal - backdrop + menu
    const menuContent = (
        <>
            {/* Invisible backdrop to catch clicks outside */}
            <div style={backdropStyle} onClick={onClose} />
            <div ref={menuRef} style={menuStyle}>
            {/* Header */}
            <div style={styles.header}>
                <span>Filter: {columnTitle}</span>
                <button
                    style={styles.closeButton}
                    onClick={onClose}
                    title="Close"
                >
                    ×
                </button>
            </div>

            {/* Search Input */}
            <div style={styles.searchContainer}>
                <input
                    ref={searchInputRef}
                    type="text"
                    placeholder="Search values..."
                    value={filterSearch}
                    onChange={(e) => setFilterSearch(e.target.value)}
                    style={styles.searchInput}
                />
            </div>

            {/* Select All */}
            <div style={styles.selectAllContainer}>
                <input
                    type="checkbox"
                    checked={allSelected}
                    ref={el => {
                        if (el) el.indeterminate = someSelected;
                    }}
                    onChange={handleSelectAll}
                    style={styles.checkbox}
                />
                <span onClick={handleSelectAll} style={{ cursor: 'pointer' }}>
                    Select All
                </span>
            </div>

            {/* Filter List */}
            <div style={styles.filterList}>
                {filteredValues.length === 0 ? (
                    <div style={styles.noResults}>
                        {filterSearch ? 'No matching values' : 'No values available'}
                    </div>
                ) : (
                    filteredValues.map((value, index) => (
                        <div
                            key={index}
                            style={{
                                ...styles.filterItem,
                                ...(hoveredIndex === index ? styles.filterItemHover : {})
                            }}
                            onMouseEnter={() => setHoveredIndex(index)}
                            onMouseLeave={() => setHoveredIndex(-1)}
                            onClick={() => handleValueToggle(value)}
                        >
                            <input
                                type="checkbox"
                                checked={isValueSelected(value)}
                                onChange={() => handleValueToggle(value)}
                                onClick={(e) => e.stopPropagation()}
                                style={styles.checkbox}
                            />
                            <span style={{
                                overflow: 'hidden',
                                textOverflow: 'ellipsis',
                                whiteSpace: 'nowrap'
                            }}>
                                {value === '(Blank)' ? (
                                    <em style={{ color: theme?.textMedium || '#666' }}>(Blank)</em>
                                ) : (
                                    String(value)
                                )}
                            </span>
                        </div>
                    ))
                )}
            </div>

            {/* Custom Items */}
            {customItems && customItems.length > 0 && (
                <>
                    <div style={styles.divider} />
                    {customItems.map((item, index) => (
                        <React.Fragment key={item.id}>
                            <div
                                style={{
                                    ...styles.customItem,
                                    ...(hoveredIndex === `custom-${index}` ? styles.filterItemHover : {})
                                }}
                                onMouseEnter={() => setHoveredIndex(`custom-${index}`)}
                                onMouseLeave={() => setHoveredIndex(-1)}
                                onClick={() => {
                                    onCustomItemClick && onCustomItemClick(item.id, columnIndex);
                                    onClose();
                                }}
                            >
                                {item.icon && <span>{item.icon}</span>}
                                <span>{item.label}</span>
                            </div>
                            {item.dividerAfter && <div style={styles.divider} />}
                        </React.Fragment>
                    ))}
                </>
            )}

            {/* Clear Filter Button (only show if filter is active) */}
            {selectedValues !== null && selectedValues.length !== uniqueValues.length && (
                <div
                    style={styles.clearButton}
                    onClick={handleClearFilter}
                >
                    Clear Filter
                </div>
            )}
        </div>
        </>
    );

    // Portal to body
    if (typeof document !== 'undefined') {
        return createPortal(menuContent, document.body);
    }

    return null;
};

HeaderMenu.propTypes = {
    /** Whether the menu is open */
    isOpen: PropTypes.bool.isRequired,
    /** Callback when menu should close */
    onClose: PropTypes.func.isRequired,
    /** Screen position {x, y} where menu should appear */
    position: PropTypes.shape({
        x: PropTypes.number,
        y: PropTypes.number
    }),
    /** Index of the column this menu is for */
    columnIndex: PropTypes.number,
    /** Title of the column (shown in header) */
    columnTitle: PropTypes.string,
    /** Array of unique values for this column */
    uniqueValues: PropTypes.array,
    /** Currently selected values (null = all selected, [] = none, [...] = specific values) */
    selectedValues: PropTypes.array,
    /** Callback when filter selection changes: (columnIndex, newSelectedValues) => void */
    onFilterChange: PropTypes.func.isRequired,
    /** Grid theme object for styling */
    theme: PropTypes.object,
    /** Custom menu items */
    customItems: PropTypes.arrayOf(PropTypes.shape({
        id: PropTypes.string.isRequired,
        label: PropTypes.string.isRequired,
        icon: PropTypes.string,
        dividerAfter: PropTypes.bool
    })),
    /** Callback when custom item is clicked: (itemId, columnIndex) => void */
    onCustomItemClick: PropTypes.func,
    /** Whether menu stays anchored to header when page scrolls. Default: true */
    anchorToHeader: PropTypes.bool,
    /** z-index for the menu. Default: 1000 */
    zIndex: PropTypes.number
};

HeaderMenu.defaultProps = {
    uniqueValues: [],
    selectedValues: null,
    customItems: [],
    anchorToHeader: true,
    zIndex: 1000
};

export default HeaderMenu;
