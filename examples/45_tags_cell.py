"""
Example: Tags Cell

Demonstrates the tags cell type for displaying and editing colored labels/badges.
Click on a tags cell to open a checkbox dropdown for selecting tags.
"""

from dash import Dash, html, callback, Input, Output
import dash_glide_grid as dgg

app = Dash(__name__)

# Define available tags with their colors
POSSIBLE_TAGS = [
    {"tag": "Bug", "color": "#ef4444"},
    {"tag": "Feature", "color": "#8b5cf6"},
    {"tag": "Enhancement", "color": "#3b82f6"},
    {"tag": "First Issue", "color": "#f59e0b"},
    {"tag": "PR", "color": "#22c55e"},
    {"tag": "Assigned", "color": "#ec4899"},
]

# Sample data with tags
data = [
    {
        "issue": "Fix login bug",
        "tags": {
            "kind": "tags-cell",
            "tags": ["Bug", "Assigned"],
            "possibleTags": POSSIBLE_TAGS,
        },
    },
    {
        "issue": "Add dark mode",
        "tags": {
            "kind": "tags-cell",
            "tags": ["Feature", "Enhancement"],
            "possibleTags": POSSIBLE_TAGS,
        },
    },
    {
        "issue": "Update documentation",
        "tags": {
            "kind": "tags-cell",
            "tags": ["First Issue", "PR"],
            "possibleTags": POSSIBLE_TAGS,
        },
    },
    {
        "issue": "Refactor API",
        "tags": {
            "kind": "tags-cell",
            "tags": ["PR", "Feature", "Assigned"],
            "possibleTags": POSSIBLE_TAGS,
        },
    },
]

columns = [
    {"id": "issue", "title": "Issue", "width": 200},
    {"id": "tags", "title": "Tags", "width": 300},
]

app.layout = html.Div(
    [
        html.H1("Tags Cell Example"),
        html.P("Click on a tags cell to open the editor. Check/uncheck to toggle tags."),
        dgg.GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=250,
        ),
        html.Div(id="output", style={"marginTop": "20px"}),
    ],
    style={"padding": "20px"},
)


@callback(
    Output("output", "children"),
    Input("grid", "data"),
)
def show_data(grid_data):
    if not grid_data:
        return ""

    # Show current tag selections
    lines = []
    for row in grid_data:
        tags = row.get("tags", {}).get("tags", [])
        lines.append(f"{row['issue']}: {', '.join(tags) if tags else 'No tags'}")

    return html.Pre("\n".join(lines))


if __name__ == "__main__":
    app.run(debug=True)
