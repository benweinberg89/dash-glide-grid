"""
Example 23: Client-Side Validation & Row Styling

This example demonstrates:
1. validateCell - real-time client-side validation
2. getRowThemeOverride - conditional row coloring based on data

SETUP REQUIRED:
---------------
Create `assets/dashGlideGridFunctions.js` with your functions.
See the file in this examples/assets/ folder for examples.

This follows the same pattern as Dash AG Grid's dashAgGridFunctions namespace.
"""

from dash import Dash, html, dcc, callback, Output, Input
import dash_glide_grid as dgg

app = Dash(__name__, suppress_callback_exceptions=True)

# Sample data with various types including a status column
initial_data = [
    {"name": "Alice Johnson", "age": 28, "email": "alice@example.com", "score": 95, "status": "success"},
    {"name": "Bob Smith", "age": 35, "email": "bob@example.com", "score": 42, "status": "error"},
    {"name": "Carol White", "age": 42, "email": "carol@company.org", "score": 78, "status": "pending"},
    {"name": "David Brown", "age": 31, "email": "david@test.net", "score": 88, "status": "success"},
    {"name": "Eve Davis", "age": 27, "email": "eve@email.com", "score": 55, "status": "warning"},
    {"name": "Frank Miller", "age": 150, "email": "frank@test.com", "score": 100, "status": "success"},  # Invalid age!
    {"name": "Grace Lee", "age": 38, "email": "grace@example.org", "score": 35, "status": "error"},
]

columns = [
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Age", "id": "age", "width": 80},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Score", "id": "score", "width": 80},
    {"title": "Status", "id": "status", "width": 100},
]

app.layout = html.Div(
    [
        html.H1("Client-Side Validation & Row Styling Demo"),
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Row Styling:"),
                        html.Label("Select row coloring mode:"),
                        dcc.Dropdown(
                            id="row-theme-mode",
                            options=[
                                {
                                    "label": "Color by Status column",
                                    "value": "rowThemeByStatus(row, rowData)",
                                },
                                {
                                    "label": "Color by Score (green ≥90, red <50)",
                                    "value": "rowThemeByScore(row, rowData)",
                                },
                                {
                                    "label": "Multi-condition (invalid age=red, perfect score=green)",
                                    "value": "multiConditionTheme(row, rowData)",
                                },
                                {
                                    "label": "Zebra stripes",
                                    "value": "zebraStripes(row, rowData)",
                                },
                                {"label": "No row styling", "value": ""},
                            ],
                            value="rowThemeByStatus(row, rowData)",
                            style={"width": "100%", "marginBottom": "10px"},
                        ),
                    ],
                    style={"flex": "1", "marginRight": "20px"},
                ),
                html.Div(
                    [
                        html.H3("Validation:"),
                        html.Label("Select validation mode:"),
                        dcc.Dropdown(
                            id="validation-mode",
                            options=[
                                {
                                    "label": "Column-aware validation",
                                    "value": "validateByColumn(cell, newValue)",
                                },
                                {
                                    "label": "Age only (0-120)",
                                    "value": "validateAge(cell, newValue)",
                                },
                                {
                                    "label": "Debug mode (console)",
                                    "value": "debugValidation(cell, newValue)",
                                },
                                {"label": "No validation", "value": ""},
                            ],
                            value="validateByColumn(cell, newValue)",
                            style={"width": "100%", "marginBottom": "10px"},
                        ),
                    ],
                    style={"flex": "1"},
                ),
            ],
            style={
                "display": "flex",
                "marginBottom": "20px",
                "padding": "15px",
                "backgroundColor": "#f5f5f5",
                "borderRadius": "8px",
            },
        ),
        html.Div(id="grid-container"),
        html.Div(
            [
                html.H4("Last Edit Event:"),
                html.Pre(
                    id="edit-output",
                    style={"backgroundColor": "#f0f0f0", "padding": "10px"},
                ),
            ],
            style={"marginTop": "20px"},
        ),
        html.Div(
            [
                html.H4("Features Demonstrated:"),
                html.Ul(
                    [
                        html.Li(
                            "Row Styling: Rows colored based on Status or Score values"
                        ),
                        html.Li("Validation: Edit cells - invalid values are rejected"),
                        html.Li("Notice: Frank Miller (row 6) has invalid age (150)"),
                        html.Li("Try changing Status to 'error', 'success', 'pending', 'warning'"),
                    ]
                ),
            ],
            style={"marginTop": "20px", "color": "#666"},
        ),
    ]
)


@callback(
    Output("grid-container", "children"),
    Input("validation-mode", "value"),
    Input("row-theme-mode", "value"),
)
def update_grid(validation_function, row_theme_function):
    """Recreate grid with selected validation and row styling."""
    # Build props - empty string means disabled
    validate_cell = {"function": validation_function} if validation_function else None
    row_theme = {"function": row_theme_function} if row_theme_function else None

    return dgg.GlideGrid(
        id="validated-grid",
        columns=columns,
        data=initial_data,
        height=350,
        rowMarkers="number",
        # Client-side validation - runs in JavaScript, no Python round-trip!
        validateCell=validate_cell,
        # Client-side row styling - colors rows based on data values
        getRowThemeOverride=row_theme,
        # Enable paste with smart coercion
        coercePasteValue={"function": "smartPaste(val, cell)"},
    )


@callback(
    Output("edit-output", "children"),
    Input("validated-grid", "cellEdited"),
    prevent_initial_call=True,
)
def show_edit(cell_edited):
    """Display the last edit event."""
    if cell_edited:
        return f"Column: {cell_edited['col']}, Row: {cell_edited['row']}\nValue: {cell_edited['value']}"
    return "No edits yet"


if __name__ == "__main__":
    app.run(debug=True, port=8050)
