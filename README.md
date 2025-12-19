# Dash Glide Grid

[![PyPI version](https://badge.fury.io/py/dash-glide-grid.svg)](https://pypi.org/project/dash-glide-grid/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Dash 3.3+](https://img.shields.io/badge/dash-3.3+-blue.svg)](https://dash.plotly.com/)

> **Note:** This project is under active development and not yet recommended for production use. Expect breaking changes until v1.0 is released.

A high-performance, fully-featured data grid component for [Plotly Dash](https://dash.plotly.com/), powered by [Glide Data Grid](https://github.com/glideapps/glide-data-grid).

📖 **[Documentation & Interactive Examples](https://dgg-docs.onrender.com/)**

<!-- TODO: Add demo GIF here -->
<!-- ![Demo](assets/demo.gif) -->

## Why Dash Glide Grid?

| Feature | Dash Glide Grid | Dash DataTable | Dash AG Grid Community | Dash AG Grid Enterprise |
|---------|----------------|----------------|-------------------|-------------------|
| **License** | MIT | MIT | MIT | Commercial |
| **Cost** | Free | Free | Free | \$999/developer + \$750/deployment |
| **Rendering** | Canvas | DOM | DOM | DOM |
| **Large Data** | 1M+ cells | Good | Good | Good |
| **Cell Types** | 23  | 3  | 6 | 7 |
| **Fill Handle** | ✅ | ❌ | ❌ | ✅ |
| **Copy/Paste** | ✅ | ✅ | Limited | ✅ |
| **Range Selection** | ✅ | Limited | ❌ | ✅ |
| **Undo/Redo** | ✅ | ❌ | ✅ | ✅ |
| **Sorting** | ✅ | ✅ | ✅ | ✅ |
| **Search** | ✅ | ❌ | ❌ | ✅ |
| **Filtering** | ✅ | ❌ | ✅ | ✅ |
| **Header Menu Support** | ✅ | ❌ | ❌ | ✅ |
| **Context Menu Support** | ✅ | ❌ | ❌ | ✅ |
| **Row Grouping** | ❌ | ❌ | ❌ | ✅ |
| **Pivoting** | ❌ | ❌ | ❌ | ✅ |
| **Master/Detail** | ❌ | ❌ | ❌ | ✅ |
| **Pagination** | ❌ | ✅ | ✅ | ✅ |
| **Custom JS Functions** | ✅ | ❌ | ✅ | ✅ |


**Choose Dash Glide Grid when you need:**
- Excel-like editing (fill handle, copy/paste, range selection)
- Blazing-fast canvas rendering for large datasets (1M+ cells)
- Rich cell types (dropdowns, multi-select, range sliders, buttons) in a free, MIT-licensed package
- A modern alternative to the deprecated Dash DataTable

## Features

- **High Performance** - Canvas-based rendering handles millions of rows smoothly
- **Rich Cell Types** - Text, numbers, booleans, markdown, URIs, images, dropdowns, multi-select bubbles, and more
- **Excel-like Editing** - Fill handle, copy/paste, undo/redo
- **Flexible Selection** - Cell, row, column, and range selection modes
- **Sorting & Filtering** - Built-in column sorting and header filter menus
- **Theming** - Full theme customization at grid, row, column, and cell level
- **Column Groups** - Organize columns under collapsible group headers
- **Cell Merging** - Horizontal cell spanning
- **Row/Column Reordering** - Drag-and-drop reordering
- **Frozen Rows** - Pin rows to the top or bottom
- **Validation** - Client-side cell validation with visual feedback
- **Search** - Built-in search

## Installation

```bash
pip install dash-glide-grid
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add dash-glide-grid
```

## Requirements

- Python 3.9+
- Dash 3.3+

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
| `columns` | Column definitions with `title`, `id`, `width`, `type`, etc. |
| `data` | List of row dicts |
| `height` | Grid height in pixels |
| `readonly` | Make the entire grid read-only |
| `theme` | Custom theme object |
| `fillHandle` | Enable Excel-like fill handle |
| `copyPaste` | Enable copy/paste support |
| `rowSelect` | Row selection: `'none'`, `'single'`, `'multi'` |
| `columnSelect` | Column selection: `'none'`, `'single'`, `'multi'` |
| `sortable` | Enable column sorting |
| `showSearch` | Show search box |
| `enableUndoRedo` | Enable undo/redo support |
| `freezeTrailingRows` | Number of rows to freeze at bottom |
| `columnGroups` | Group columns under headers |

See the [full documentation](https://dgg-docs.onrender.com/) for all props and callbacks.

## Examples

The `examples/` folder contains 39 examples covering many features:

```bash
# Basic usage
python examples/01_basic_grid.py

# With uv
uv run examples/01_basic_grid.py
```

Then open http://localhost:8050 in your browser.

**Highlights**
- [01_basic_grid.py](examples/01_basic_grid.py) - Simple read-only grid
- [02_editable_grid.py](examples/02_editable_grid.py) - Cell editing with callbacks
- [04_large_dataset.py](examples/04_large_dataset.py) - Performance with 10,000+ rows
- [05_basic_cell_types.py](examples/05_basic_cell_types.py) - All basic cell types
- [07_fill_handle_example.py](examples/07_fill_handle_example.py) - Excel-like drag-to-fill
- [37_undo_redo.py](examples/37_undo_redo.py) - Undo/redo support

See [examples/README.md](examples/README.md) for the complete list.

## Development

```bash
# Clone the repo
git clone https://github.com/benweinberg89/dash-glide-grid.git
cd dash-glide-grid

# Install dependencies
npm install
uv sync

# Build the component
npm run build

# Run an example
uv run examples/01_basic_grid.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](./LICENSE)

## Credits

Built on [Glide Data Grid](https://github.com/glideapps/glide-data-grid) by [Glide](https://www.glideapps.com/).
