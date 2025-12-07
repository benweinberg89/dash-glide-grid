# Build Guide

This document describes the build process for dash-glide-grid.

## Prerequisites

1. **Node.js** (v16+) - For building JavaScript/React components
2. **Python 3.8+** - For generating Python bindings and running Dash
3. **npm** - Comes with Node.js
4. **uv** - Python package manager (https://docs.astral.sh/uv/)

## Project Structure

```
dash-glide-grid/
├── src/lib/
│   ├── components/         # Component prop definitions (lazy-loading wrapper)
│   └── fragments/          # Core React implementation
├── dash_glide_grid/        # Generated Python package
├── node_modules/           # JavaScript dependencies
└── package.json            # Build scripts
```

## Initial Setup

### 1. Clone and install Node dependencies

```bash
git clone <repo-url>
cd dash-glide-grid
npm install
```

### 2. Install Python dependencies with uv

```bash
uv sync
```

This installs all Python dependencies (including `dash`) from `pyproject.toml`.

## Build Commands

### Full Build

```bash
npm run build
```

This runs two steps:
1. `npm run build:js` - Webpack compiles React components to `dash_glide_grid.min.js`
2. `npm run build:backends` - Generates Python component bindings (uses `uv run`)

### JavaScript Only

```bash
npm run build:js
```

Outputs:
- `dash_glide_grid/dash_glide_grid.min.js` - Production bundle
- `dash_glide_grid/async-*.js` - Async chunks for code splitting

### Python Bindings Only

```bash
npm run build:backends
```

Generates:
- `dash_glide_grid/GlideGrid.py` - Python component

## Common Issues

### "dash-generate-components: command not found"

**Cause:** The `dash` Python package is not installed.

**Solution:**
```bash
# Install dependencies with uv
uv sync

# Then run build
npm run build:backends
```

### Webpack warnings about asset size

```
WARNING in asset size limit: The following asset(s) exceed the recommended size limit (244 KiB).
```

This is expected. The bundle includes the Glide Data Grid library which is large but necessary.

### Python package not updating after changes

After modifying React components, you must:
1. Run `npm run build` to regenerate the Python package
2. If using `uv pip install -e .` (editable install), changes take effect immediately
3. Otherwise, reinstall: `uv pip install .`

## Development Workflow

### Making Changes

1. Edit React components in `src/lib/fragments/GlideGrid.react.js`
2. Update PropTypes in `src/lib/components/GlideGrid.react.js`
3. Build: `npm run build`
4. Test: `uv run python examples/<example>.py`

### Adding New Props

**IMPORTANT:** You must edit BOTH files when adding new props:

| File | Purpose |
|------|---------|
| `src/lib/components/GlideGrid.react.js` | Wrapper with PropTypes - **used by Python generator** |
| `src/lib/fragments/GlideGrid.react.js` | Actual implementation |

Steps:

1. **In `src/lib/components/GlideGrid.react.js`:**
   - Add default value to `defaultProps`
   - Add PropType definition with JSDoc comment to `propTypes`

2. **In `src/lib/fragments/GlideGrid.react.js`:**
   - Add default value to `defaultProps`
   - Add PropType definition with JSDoc comment to `propTypes`
   - Destructure the prop from `props`
   - Implement handler/logic
   - Pass prop to DataEditor component if needed

3. **Rebuild:**
   ```bash
   npm run build
   ```

4. **Verify prop was generated:**
   ```bash
   grep "yourNewProp" dash_glide_grid/GlideGrid.py
   ```

> **Why two files?** The `components/` file is a thin wrapper that the Dash component generator reads to create Python bindings. The `fragments/` file contains the actual React implementation. Both need the PropTypes for the component to work correctly.

### Running Examples

```bash
uv run python examples/01_basic_grid.py
```

## Watch Mode (Development)

For faster iteration during development:

```bash
npm run start
```

This runs webpack in watch mode and starts a development server.

## Production Build

```bash
npm run build
```

The `--mode production` flag is already set in the build script, which:
- Minifies JavaScript
- Removes development-only code
- Optimizes bundle size

## Verifying the Build

After building, verify:

1. **JavaScript bundle exists:**
   ```bash
   ls -la dash_glide_grid/*.js
   ```

2. **Python component was generated:**
   ```bash
   ls -la dash_glide_grid/GlideGrid.py
   ```

3. **Component imports correctly:**
   ```bash
   uv run python -c "from dash_glide_grid import GlideGrid; print('OK')"
   ```

4. **Run an example:**
   ```bash
   uv run python examples/01_basic_grid.py
   ```
