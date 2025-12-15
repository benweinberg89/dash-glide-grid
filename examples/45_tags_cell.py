"""
Example: Tags Cell

Demonstrates the tags cell type for displaying colored labels/badges.
Tags are read-only and useful for showing categories, statuses, or labels.
"""

from dash import Dash, html
import dash_glide_grid as dgg

app = Dash(__name__)

# Sample data with tags
data = [
    {
        "project": "Dashboard App",
        "status": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Active", "color": "#22c55e"},
                {"tag": "Priority", "color": "#ef4444"},
            ],
        },
        "tech": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Python", "color": "#3776ab"},
                {"tag": "React", "color": "#61dafb"},
                {"tag": "PostgreSQL", "color": "#336791"},
            ],
        },
    },
    {
        "project": "Mobile App",
        "status": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "In Progress", "color": "#f59e0b"},
            ],
        },
        "tech": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "React Native", "color": "#61dafb"},
                {"tag": "TypeScript", "color": "#3178c6"},
            ],
        },
    },
    {
        "project": "API Service",
        "status": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Completed", "color": "#6b7280"},
                {"tag": "Archived", "color": "#9ca3af"},
            ],
        },
        "tech": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Go", "color": "#00add8"},
                {"tag": "gRPC", "color": "#244c5a"},
            ],
        },
    },
    {
        "project": "ML Pipeline",
        "status": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Active", "color": "#22c55e"},
            ],
        },
        "tech": {
            "kind": "tags-cell",
            "tags": [
                {"tag": "Python", "color": "#3776ab"},
                {"tag": "TensorFlow", "color": "#ff6f00"},
                {"tag": "Docker", "color": "#2496ed"},
                {"tag": "Kubernetes", "color": "#326ce5"},
            ],
        },
    },
]

columns = [
    {"id": "project", "title": "Project", "width": 150},
    {"id": "status", "title": "Status", "width": 180},
    {"id": "tech", "title": "Technologies", "width": 300},
]

app.layout = html.Div(
    [
        html.H1("Tags Cell Example"),
        html.P("Tags display colored labels. Great for categories, statuses, or technology stacks."),
        dgg.GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=300,
        ),
    ],
    style={"padding": "20px"},
)

if __name__ == "__main__":
    app.run(debug=True)
