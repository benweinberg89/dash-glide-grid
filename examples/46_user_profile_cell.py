"""
Example: User Profile Cell

Demonstrates the user profile cell type for displaying user avatars with names.
Shows circular avatar with initials or images, plus the user's name.
"""

from dash import Dash, html
import dash_glide_grid as dgg

app = Dash(__name__)

# Sample data with user profiles
data = [
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Alice Johnson",
            "initial": "A",
            "tint": "#3b82f6",
        },
        "role": "Engineering Manager",
        "department": "Engineering",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Bob Smith",
            "initial": "B",
            "tint": "#22c55e",
        },
        "role": "Senior Developer",
        "department": "Engineering",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Carol Williams",
            "initial": "C",
            "tint": "#f59e0b",
        },
        "role": "Product Designer",
        "department": "Design",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "David Brown",
            "initial": "D",
            "tint": "#ef4444",
        },
        "role": "DevOps Engineer",
        "department": "Infrastructure",
    },
    {
        "user": {
            "kind": "user-profile-cell",
            "name": "Emma Davis",
            "initial": "E",
            "tint": "#8b5cf6",
            # You can also provide an image URL:
            # "image": "https://example.com/avatar.jpg",
        },
        "role": "Data Scientist",
        "department": "Analytics",
    },
]

columns = [
    {"id": "user", "title": "Team Member", "width": 200},
    {"id": "role", "title": "Role", "width": 180},
    {"id": "department", "title": "Department", "width": 120},
]

app.layout = html.Div(
    [
        html.H1("User Profile Cell Example"),
        html.P("User profile cells display an avatar circle with initials and the user's name."),
        dgg.GlideGrid(
            id="grid",
            columns=columns,
            data=data,
            height=280,
        ),
    ],
    style={"padding": "20px"},
)

if __name__ == "__main__":
    app.run(debug=True)
