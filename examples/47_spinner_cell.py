"""
Example: Spinner Cell

Demonstrates the spinner cell type for showing loading states.
Useful for indicating async operations or pending data.
"""

from dash import Dash, html, callback, Input, Output, State
import dash_glide_grid as dgg
import time

app = Dash(__name__)

# Sample data with some spinners indicating loading state
initial_data = [
    {
        "task": "Fetch user data",
        "status": {"kind": "spinner-cell"},
        "result": "Loading...",
    },
    {
        "task": "Process images",
        "status": {"kind": "spinner-cell"},
        "result": "Loading...",
    },
    {
        "task": "Generate report",
        "status": "Queued",
        "result": "Waiting",
    },
    {
        "task": "Send notifications",
        "status": "Queued",
        "result": "Waiting",
    },
]

columns = [
    {"id": "task", "title": "Task", "width": 180},
    {"id": "status", "title": "Status", "width": 100},
    {"id": "result", "title": "Result", "width": 150},
]

app.layout = html.Div(
    [
        html.H1("Spinner Cell Example"),
        html.P("Spinner cells show an animated loading indicator. Click the button to simulate completing tasks."),
        html.Button("Complete First Task", id="complete-btn", style={"marginBottom": "10px"}),
        dgg.GlideGrid(
            id="grid",
            columns=columns,
            data=initial_data,
            height=220,
        ),
    ],
    style={"padding": "20px"},
)


@callback(
    Output("grid", "data"),
    Input("complete-btn", "n_clicks"),
    State("grid", "data"),
    prevent_initial_call=True,
)
def complete_task(n_clicks, data):
    """Simulate completing a task by replacing spinner with text."""
    if not data:
        return data

    # Find the first row with a spinner and complete it
    for row in data:
        if isinstance(row.get("status"), dict) and row["status"].get("kind") == "spinner-cell":
            row["status"] = "Complete ✓"
            row["result"] = "Success"
            break

    return data


if __name__ == "__main__":
    app.run(debug=True)
