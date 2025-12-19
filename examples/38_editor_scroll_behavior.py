"""
Example 38: Editor Scroll Behavior

Demonstrates the editorScrollBehavior prop which controls how the grid behaves
when the user scrolls while a cell editor is open.

This example includes ALL 23 cell types to test scroll behavior variations:

Built-in types (11):
- text, number, boolean, markdown, uri, image, bubble, drilldown, loading, rowid, protected

Custom types (12):
- dropdown, multi-select, button, tags, user-profile, spinner,
  star, date-picker, range, links, sparkline, tree-view
"""
from dash import Dash, html, dcc, callback, Input, Output
import dash_glide_grid as dgg

app = Dash(__name__)

# Status options for dropdowns (many options to test scrollable dropdown)
STATUS_OPTIONS = [
    {"value": "active", "label": "Active", "color": "#10b981"},
    {"value": "pending", "label": "Pending", "color": "#f59e0b"},
    {"value": "completed", "label": "Completed", "color": "#3b82f6"},
    {"value": "archived", "label": "Archived", "color": "#6b7280"},
    {"value": "review", "label": "In Review", "color": "#8b5cf6"},
    {"value": "blocked", "label": "Blocked", "color": "#ef4444"},
    {"value": "deferred", "label": "Deferred", "color": "#a855f7"},
    {"value": "cancelled", "label": "Cancelled", "color": "#78716c"},
    {"value": "draft", "label": "Draft", "color": "#94a3b8"},
    {"value": "submitted", "label": "Submitted", "color": "#06b6d4"},
    {"value": "approved", "label": "Approved", "color": "#22c55e"},
    {"value": "rejected", "label": "Rejected", "color": "#dc2626"},
    {"value": "onhold", "label": "On Hold", "color": "#eab308"},
    {"value": "scheduled", "label": "Scheduled", "color": "#6366f1"},
    {"value": "inprogress", "label": "In Progress", "color": "#0ea5e9"},
    {"value": "testing", "label": "Testing", "color": "#f472b6"},
    {"value": "deployed", "label": "Deployed", "color": "#84cc16"},
    {"value": "maintenance", "label": "Maintenance", "color": "#fb923c"},
]

# Tag definitions
TAG_DEFS = [
    {"tag": "Bug", "color": "#ef4444"},
    {"tag": "Feature", "color": "#8b5cf6"},
    {"tag": "Critical", "color": "#f97316"},
    {"tag": "Low", "color": "#22c55e"},
    {"tag": "Documentation", "color": "#3b82f6"},
    {"tag": "Testing", "color": "#14b8a6"},
    {"tag": "Design", "color": "#ec4899"},
    {"tag": "Backend", "color": "#f97316"},
    {"tag": "Frontend", "color": "#a855f7"},
]

# Skill options for multi-select (many options to test scrollable dropdown)
SKILL_OPTIONS = [
    {"value": "python", "label": "Python", "color": "#3776ab"},
    {"value": "javascript", "label": "JavaScript", "color": "#f7df1e"},
    {"value": "rust", "label": "Rust", "color": "#dea584"},
    {"value": "go", "label": "Go", "color": "#00add8"},
    {"value": "sql", "label": "SQL", "color": "#336791"},
    {"value": "typescript", "label": "TypeScript", "color": "#3178c6"},
    {"value": "react", "label": "React", "color": "#61dafb"},
    {"value": "docker", "label": "Docker", "color": "#2496ed"},
    {"value": "kubernetes", "label": "Kubernetes", "color": "#326ce5"},
    {"value": "aws", "label": "AWS", "color": "#ff9900"},
    {"value": "gcp", "label": "GCP", "color": "#4285f4"},
    {"value": "azure", "label": "Azure", "color": "#0078d4"},
    {"value": "nodejs", "label": "Node.js", "color": "#339933"},
    {"value": "java", "label": "Java", "color": "#007396"},
    {"value": "csharp", "label": "C#", "color": "#239120"},
    {"value": "cpp", "label": "C++", "color": "#00599c"},
    {"value": "ruby", "label": "Ruby", "color": "#cc342d"},
    {"value": "php", "label": "PHP", "color": "#777bb4"},
    {"value": "swift", "label": "Swift", "color": "#fa7343"},
    {"value": "kotlin", "label": "Kotlin", "color": "#7f52ff"},
]

# Column definitions - all 23 cell types
COLUMNS = [
    # Built-in types
    {"id": "id", "title": "ID", "width": 50},
    {"id": "name", "title": "Name (text)", "width": 120},
    {"id": "age", "title": "Age (number)", "width": 80},
    {"id": "active", "title": "Active (bool)", "width": 90},
    {"id": "description", "title": "Desc (markdown)", "width": 140},
    {"id": "website", "title": "Site (uri)", "width": 100},
    {"id": "avatar", "title": "Avatar (image)", "width": 70},
    {"id": "skills_bubble", "title": "Skills (bubble)", "width": 120},
    {"id": "details", "title": "Info (drilldown)", "width": 100},
    {"id": "row_id", "title": "RowID", "width": 80},
    {"id": "secret", "title": "Secret (protected)", "width": 100},
    {"id": "pending_data", "title": "Loading", "width": 80},
    # Custom types
    {"id": "status", "title": "Status (dropdown)", "width": 120},
    {"id": "tags", "title": "Tags", "width": 150},
    {"id": "rating", "title": "Rating (stars)", "width": 100},
    {"id": "due_date", "title": "Due Date", "width": 120},
    {"id": "progress", "title": "Progress (range)", "width": 120},
    {"id": "assignee", "title": "Assignee (profile)", "width": 130},
    {"id": "multi_skills", "title": "Skills (multi)", "width": 150},
    {"id": "links", "title": "Links", "width": 120},
    {"id": "trend", "title": "Trend (sparkline)", "width": 100},
    {"id": "category", "title": "Category (tree)", "width": 110},
    {"id": "action", "title": "Action (button)", "width": 90},
    {"id": "loading_indicator", "title": "Spinner", "width": 70},
]

# Generate comprehensive data with all 23 cell types
DATA = []
names = ["Alice Johnson", "Bob Smith", "Carol Williams", "David Lee", "Eve Martinez",
         "Frank Chen", "Grace Kim", "Henry Wong", "Ivy Zhang", "Jack Brown",
         "Kate Davis", "Leo Garcia", "Mia Lopez", "Noah Wilson", "Olivia Moore",
         "Paul Taylor", "Quinn Anderson", "Rosa Thomas", "Sam Jackson", "Tina White",
         "Uma Patel", "Victor Harris", "Wendy Clark", "Xavier Lewis", "Yuki Tanaka"]

for i, name in enumerate(names):
    first_name = name.split()[0].lower()
    DATA.append({
        # Built-in types
        "id": i + 1,
        "name": name,
        "age": 25 + (i * 2) % 30,
        "active": i % 3 != 0,
        "description": {"kind": "markdown", "data": f"**{name.split()[0]}** - Team member"},
        "website": {"kind": "uri", "data": f"https://{first_name}.dev", "displayData": f"{first_name}.dev"},
        "avatar": {"kind": "image", "data": [f"https://i.pravatar.cc/40?u={first_name}"]},
        "skills_bubble": {"kind": "bubble", "data": ["Python", "JS"][:((i % 3) + 1)]},
        "details": {"kind": "drilldown", "data": [{"text": ["Engineering", "Design", "Product"][i % 3]}]},
        "row_id": {"kind": "rowid", "data": f"ROW-{i+1:03d}"},
        "secret": {"kind": "protected"},
        "pending_data": {"kind": "loading", "skeletonWidth": 60},
        # Custom types
        "status": {
            "kind": "dropdown-cell",
            "value": STATUS_OPTIONS[i % len(STATUS_OPTIONS)]["value"],
            "allowedValues": STATUS_OPTIONS,
        },
        "tags": {
            "kind": "tags-cell",
            "tags": [TAG_DEFS[i % len(TAG_DEFS)]["tag"], TAG_DEFS[(i + 2) % len(TAG_DEFS)]["tag"]],
            "possibleTags": TAG_DEFS,
        },
        "rating": {"kind": "star-cell", "rating": (i % 5) + 1, "maxStars": 5},
        "due_date": {
            "kind": "date-picker-cell",
            "date": f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}",
            "displayDate": f"{['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][i % 12]} {(i % 28) + 1}, 2024",
        },
        "progress": {
            "kind": "range-cell",
            "value": (i * 13) % 101,
            "min": 0,
            "max": 100,
            "step": 5,
            "label": f"{(i * 13) % 101}%",
        },
        "assignee": {
            "kind": "user-profile-cell",
            "name": name,
            "initial": name[0],
            "tint": ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#6366f1"][i % 5],
        },
        "multi_skills": {
            "kind": "multi-select-cell",
            "values": [SKILL_OPTIONS[i % len(SKILL_OPTIONS)]["value"],
                      SKILL_OPTIONS[(i + 3) % len(SKILL_OPTIONS)]["value"]],
            "options": SKILL_OPTIONS,
        },
        "links": {
            "kind": "links-cell",
            "links": [
                {"title": "GitHub", "href": f"https://github.com/{first_name}"},
                {"title": "LinkedIn", "href": f"https://linkedin.com/in/{first_name}"},
            ] if i % 2 == 0 else [{"title": "Portfolio", "href": f"https://{first_name}.dev"}],
        },
        "trend": {
            "kind": "sparkline-cell",
            "values": [(i * 7 + j * 11) % 50 for j in range(5)],
            "yAxis": [0, 50],
            "graphKind": ["line", "area", "bar"][i % 3],
        },
        "category": {
            "kind": "tree-view-cell",
            "text": ["Engineering", "Design", "Product", "Marketing", "Sales"][i % 5],
            "depth": i % 2,
            "canOpen": i % 3 == 0,
            "isOpen": i % 4 == 0,
        },
        "action": {"kind": "button-cell", "title": ["Edit", "View", "Delete", "Archive"][i % 4]},
        "loading_indicator": {"kind": "spinner-cell"},
    })

app.layout = html.Div([
    html.H1("Editor Scroll Behavior - All 23 Cell Types"),
    html.P([
        "This example demonstrates the ",
        html.Code("editorScrollBehavior"),
        " prop with ALL cell types to test how different editors behave when scrolling."
    ]),

    # Controls
    html.Div([
        html.Label("Scroll Behavior Mode:", style={"fontWeight": "bold", "marginRight": "15px"}),
        dcc.RadioItems(
            id="scroll-behavior-mode",
            options=[
                {"label": " default - Editor stays at original position", "value": "default"},
                {"label": " close-overlay-on-scroll - Editor closes on scroll", "value": "close-overlay-on-scroll"},
                {"label": " lock-scroll - Scrolling disabled while editing", "value": "lock-scroll"},
            ],
            value="default",
            labelStyle={"display": "block", "marginBottom": "8px"}
        ),
    ], style={"marginBottom": "20px", "padding": "15px", "backgroundColor": "#f5f5f5", "borderRadius": "8px"}),

    # Instructions
    html.Div([
        html.Strong("Try this: "),
        "Click cells to open editors, then scroll. Test different cell types to compare behaviors.",
    ], style={"marginBottom": "15px", "padding": "10px", "backgroundColor": "#e0f2fe", "borderRadius": "4px"}),

    # Grid container
    html.Div(id="grid-container"),

    # Cell types reference
    html.Div([
        html.H3("All 23 Cell Types:"),
        html.Div([
            html.Div([
                html.H4("Built-in Types (11):"),
                html.Ul([
                    html.Li([html.Strong("text"), " - Name column"]),
                    html.Li([html.Strong("number"), " - Age column"]),
                    html.Li([html.Strong("boolean"), " - Active column (checkbox)"]),
                    html.Li([html.Strong("markdown"), " - Description column"]),
                    html.Li([html.Strong("uri"), " - Website column"]),
                    html.Li([html.Strong("image"), " - Avatar column"]),
                    html.Li([html.Strong("bubble"), " - Skills bubble column"]),
                    html.Li([html.Strong("drilldown"), " - Info column"]),
                    html.Li([html.Strong("rowid"), " - RowID column"]),
                    html.Li([html.Strong("protected"), " - Secret column"]),
                    html.Li([html.Strong("loading"), " - Loading column"]),
                ]),
            ], style={"flex": "1", "minWidth": "250px"}),
            html.Div([
                html.H4("Custom Types (12):"),
                html.Ul([
                    html.Li([html.Strong("dropdown-cell"), " - Status (overlay editor)"]),
                    html.Li([html.Strong("tags-cell"), " - Tags (overlay editor)"]),
                    html.Li([html.Strong("star-cell"), " - Rating (overlay editor)"]),
                    html.Li([html.Strong("date-picker-cell"), " - Due Date (overlay editor)"]),
                    html.Li([html.Strong("range-cell"), " - Progress (overlay editor)"]),
                    html.Li([html.Strong("user-profile-cell"), " - Assignee (display only)"]),
                    html.Li([html.Strong("multi-select-cell"), " - Skills multi (overlay editor)"]),
                    html.Li([html.Strong("links-cell"), " - Links (overlay editor)"]),
                    html.Li([html.Strong("sparkline-cell"), " - Trend (display only)"]),
                    html.Li([html.Strong("tree-view-cell"), " - Category (inline toggle)"]),
                    html.Li([html.Strong("button-cell"), " - Action (click handler)"]),
                    html.Li([html.Strong("spinner-cell"), " - Spinner (display only)"]),
                ]),
            ], style={"flex": "1", "minWidth": "250px"}),
        ], style={"display": "flex", "flexWrap": "wrap", "gap": "20px"}),
    ], style={"marginTop": "30px", "color": "#666"}),

    # Scroll behavior explanation
    html.Div([
        html.H3("Scroll Behavior Modes:"),
        html.Ul([
            html.Li([
                html.Strong("default"),
                ": Editor overlay stays at original position when you scroll. ",
                "May appear disconnected from cell after scrolling."
            ]),
            html.Li([
                html.Strong("close-overlay-on-scroll"),
                ": Editor overlay closes when scroll is detected. ",
                "Prevents orphaned editors."
            ]),
            html.Li([
                html.Strong("lock-scroll"),
                ": Scrolling is disabled while editor is open. ",
                "Editor stays perfectly aligned with cell."
            ]),
        ]),
    ], style={"marginTop": "20px", "color": "#666"}),

    # Extra content for scrolling
    html.Div([
        html.H3("Additional Content (for page scrolling)"),
        html.P("Open an editor above, then try scrolling down here."),
        html.Div([
            html.P(f"Paragraph {i+1}: Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                   "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
            for i in range(5)
        ], style={"color": "#888"}),
    ], style={"marginTop": "40px", "paddingTop": "20px", "borderTop": "1px solid #ddd"}),

], style={"margin": "40px", "fontFamily": "Arial, sans-serif"})


@callback(
    Output("grid-container", "children"),
    Input("scroll-behavior-mode", "value"),
)
def update_grid(scroll_mode):
    return dgg.GlideGrid(
        id="scroll-behavior-grid",
        columns=COLUMNS,
        data=DATA,
        height=400,
        rowMarkers="number",
        cellActivationBehavior="second-click",
        editorScrollBehavior=scroll_mode,
        columnResize=True,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8038)
