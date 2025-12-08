# Dash Glide Grid

A high-performance data grid component for Plotly Dash, wrapping [Glide Data Grid](https://github.com/glideapps/glide-data-grid).

## Features

- **High Performance** - Canvas-based rendering handles millions of rows
- **Fully Free & Open Source** - MIT-licensed so you can use in commercial projects for free
- **Rich Cell Types** - Text, numbers, booleans, markdown, images, dropdowns, multi-select
- **Excel-like Editing** - Fill handle, copy/paste, undo/redo
- **Flexible Selection** - Cell, row, column, and range selection
- **Sorting & Filtering** - Built-in column sorting and filtering via header menus
- **Theming** - Full customization with dark mode support

## Installation

```bash
pip install dash-glide-grid
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add dash-glide-grid
```

## Quick Start

```python
import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__)

app.layout = html.Div([
    dgg.GlideGrid(
        id='grid',
        columns=[
            {'title': 'Name', 'id': 'name', 'width': 200},
            {'title': 'Age', 'id': 'age', 'width': 100},
            {'title': 'City', 'id': 'city', 'width': 150}
        ],
        data=[
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'San Francisco'},
        ],
        height=400
    )
])

if __name__ == '__main__':
    app.run(debug=True)
```

## Data Format

Use records format (compatible with `df.to_dict('records')`):

```python
# From a list of dicts
data = [
    {'name': 'Alice', 'age': 30, 'active': True},
    {'name': 'Bob', 'age': 25, 'active': False}
]

# From pandas
data = df.to_dict('records')
```

## Key Props

| Prop | Description |
|------|-------------|
| `columns` | Column definitions with `title`, `id`, `width` |
| `data` | List of row dicts |
| `height` | Grid height in pixels |
| `theme` | Custom theme object |
| `fillHandle` | Enable Excel-like fill handle |
| `rowSelect` | Row selection: `'none'`, `'single'`, `'multi'` |
| `sortable` | Enable column sorting |
| `showSearch` | Show search box (Ctrl+F) |
| `enableUndoRedo` | Enable undo/redo support |

## Examples

The `examples/` folder contains 37 examples covering all features:

```bash
python examples/01_basic_grid.py      # Basic usage
```
Or with [uv](https://docs.astral.sh/uv/):

```bash
uv run examples/01_basic_grid.py      # Basic usage
```

See [examples/README.md](examples/README.md) for the full list.

## Development

```bash
# Setup
npm install
uv sync

# Build
npm run build

# Run examples
uv run examples/01_basic_grid.py
```

## License

MIT License - see [LICENSE](./LICENSE)

## Credits

Built on [Glide Data Grid](https://github.com/glideapps/glide-data-grid) by Glide.