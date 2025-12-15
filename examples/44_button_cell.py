"""
Example 44: Button Cell with Dialog

This example demonstrates the button cell type with dialog interactions:
- Click "View" to open a details dialog
- Click "Delete" to open a confirmation dialog that actually removes the row
Includes dark/light mode toggle to test theme compatibility.

Button cells support:
- Custom colors (backgroundColor, color, borderColor)
- Custom border radius
- Click callbacks with row/column information
"""

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Theme configurations
DARK_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.2)",
    "bgCell": "#1f2937",
    "bgCellMedium": "#374151",
    "bgHeader": "#111827",
    "bgHeaderHasFocus": "#374151",
    "bgHeaderHovered": "#374151",
    "textDark": "#f3f4f6",
    "textMedium": "#9ca3af",
    "textLight": "#6b7280",
    "textHeader": "#f3f4f6",
    "borderColor": "rgba(255, 255, 255, 0.1)",
    "horizontalBorderColor": "rgba(255, 255, 255, 0.1)",
}

LIGHT_THEME = {
    "accentColor": "#3b82f6",
    "accentLight": "rgba(59, 130, 246, 0.1)",
    "bgCell": "#ffffff",
    "bgCellMedium": "#f9fafb",
    "bgHeader": "#f3f4f6",
    "bgHeaderHasFocus": "#e5e7eb",
    "bgHeaderHovered": "#e5e7eb",
    "textDark": "#111827",
    "textMedium": "#6b7280",
    "textLight": "#9ca3af",
    "textHeader": "#111827",
    "borderColor": "#e5e7eb",
    "horizontalBorderColor": "#e5e7eb",
}

# Sample data with button cells
INITIAL_DATA = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "status": "Active",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 2,
        "name": "Bob Smith",
        "email": "bob@example.com",
        "status": "Pending",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 3,
        "name": "Carol White",
        "email": "carol@example.com",
        "status": "Active",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
    {
        "id": 4,
        "name": "David Brown",
        "email": "david@example.com",
        "status": "Inactive",
        "action": {
            "kind": "button-cell",
            "title": "View",
            "backgroundColor": "#3b82f6",
            "color": "#ffffff",
            "borderRadius": 4
        },
        "delete": {
            "kind": "button-cell",
            "title": "Delete",
            "backgroundColor": "#ef4444",
            "color": "#ffffff",
            "borderRadius": 4
        }
    },
]

COLUMNS = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Status", "id": "status", "width": 100},
    {"title": "Action", "id": "action", "width": 80},
    {"title": "Delete", "id": "delete", "width": 80},
]

app.layout = html.Div(
    id="app-container",
    children=[
        html.H1("Button Cell with Dialog Example", id="title"),
        html.P("Click 'View' to see details, or 'Delete' to remove a row.", id="subtitle"),
        html.Button(
            "Toggle Dark Mode",
            id="theme-toggle",
            style={
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
            },
        ),
        GlideGrid(
            id="grid",
            columns=COLUMNS,
            data=INITIAL_DATA,
            height=300,
            width="100%",
            theme=LIGHT_THEME,
        ),
        # Store for tracking which row to delete
        dcc.Store(id="pending-delete-row", data=None),
        dcc.Store(id="is-dark-mode", data=False),
        # Hidden placeholder buttons (needed for callback registration)
        html.Button(id="close-view-dialog", style={"display": "none"}),
        html.Button(id="cancel-delete", style={"display": "none"}),
        html.Button(id="confirm-delete", style={"display": "none"}),
        # View Details Dialog
        html.Div(id="view-dialog", style={"display": "none"}),
        # Delete Confirmation Dialog
        html.Div(id="delete-dialog", style={"display": "none"}),
    ],
    style={"padding": "20px", "maxWidth": "900px", "fontFamily": "system-ui, sans-serif"},
)


@callback(
    Output("grid", "theme"),
    Output("app-container", "style"),
    Output("title", "style"),
    Output("subtitle", "style"),
    Output("theme-toggle", "style"),
    Output("theme-toggle", "children"),
    Output("is-dark-mode", "data"),
    Input("theme-toggle", "n_clicks"),
    prevent_initial_call=True,
)
def toggle_theme(n_clicks):
    is_dark = (n_clicks or 0) % 2 == 1

    if is_dark:
        return (
            DARK_THEME,
            {
                "padding": "20px",
                "maxWidth": "900px",
                "fontFamily": "system-ui, sans-serif",
                "backgroundColor": "#111827",
                "minHeight": "100vh",
            },
            {"color": "#f3f4f6"},
            {"color": "#9ca3af"},
            {
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #4b5563",
                "backgroundColor": "#374151",
                "color": "#f3f4f6",
            },
            "Toggle Light Mode",
            True,
        )
    else:
        return (
            LIGHT_THEME,
            {
                "padding": "20px",
                "maxWidth": "900px",
                "fontFamily": "system-ui, sans-serif",
            },
            {"color": "#111827"},
            {"color": "#6b7280"},
            {
                "marginBottom": "15px",
                "padding": "8px 16px",
                "cursor": "pointer",
                "borderRadius": "6px",
                "border": "1px solid #d1d5db",
                "backgroundColor": "#f3f4f6",
                "color": "#111827",
            },
            "Toggle Dark Mode",
            False,
        )


@callback(
    Output("view-dialog", "style"),
    Output("view-dialog", "children"),
    Input("grid", "buttonClicked"),
    Input("close-view-dialog", "n_clicks"),
    State("grid", "data"),
    State("is-dark-mode", "data"),
    prevent_initial_call=True,
)
def handle_view_button(click_info, close_clicks, data, is_dark):
    from dash import ctx

    if ctx.triggered_id == "close-view-dialog":
        return {"display": "none"}, no_update

    if click_info and click_info.get("title") == "View":
        row_data = data[click_info["row"]]

        # Theme-aware colors
        overlay_bg = "rgba(0, 0, 0, 0.7)" if is_dark else "rgba(0, 0, 0, 0.5)"
        dialog_bg = "#1f2937" if is_dark else "white"
        text_color = "#f3f4f6" if is_dark else "#111827"
        text_muted = "#9ca3af" if is_dark else "#6b7280"
        btn_bg = "#374151" if is_dark else "#e5e7eb"
        btn_color = "#f3f4f6" if is_dark else "#374151"

        content = html.Div(
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "backgroundColor": overlay_bg,
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "zIndex": 1000,
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": dialog_bg,
                        "padding": "24px",
                        "borderRadius": "8px",
                        "minWidth": "300px",
                        "maxWidth": "500px",
                        "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.3)",
                    },
                    children=[
                        html.H2("User Details", style={"marginTop": 0, "color": text_color}),
                        html.P([html.Strong("ID: ", style={"color": text_muted}), str(row_data.get("id", "N/A"))], style={"color": text_color}),
                        html.P([html.Strong("Name: ", style={"color": text_muted}), row_data.get("name", "N/A")], style={"color": text_color}),
                        html.P([html.Strong("Email: ", style={"color": text_muted}), row_data.get("email", "N/A")], style={"color": text_color}),
                        html.P([html.Strong("Status: ", style={"color": text_muted}), row_data.get("status", "N/A")], style={"color": text_color}),
                        html.Div(
                            style={"marginTop": "20px", "textAlign": "right"},
                            children=[
                                html.Button(
                                    "Close",
                                    id="close-view-dialog",
                                    style={
                                        "padding": "8px 16px",
                                        "borderRadius": "4px",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "backgroundColor": btn_bg,
                                        "color": btn_color,
                                    },
                                )
                            ],
                        ),
                    ],
                )
            ],
        )
        return {"display": "block"}, content

    return no_update, no_update


@callback(
    Output("delete-dialog", "style"),
    Output("delete-dialog", "children"),
    Output("pending-delete-row", "data"),
    Input("grid", "buttonClicked"),
    Input("cancel-delete", "n_clicks"),
    Input("confirm-delete", "n_clicks"),
    State("grid", "data"),
    State("pending-delete-row", "data"),
    State("is-dark-mode", "data"),
    prevent_initial_call=True,
)
def handle_delete_button(click_info, cancel_clicks, confirm_clicks, data, pending_row, is_dark):
    from dash import ctx

    if ctx.triggered_id in ["cancel-delete", "confirm-delete"]:
        return {"display": "none"}, no_update, None

    if click_info and click_info.get("title") == "Delete":
        row_data = data[click_info["row"]]
        name = row_data.get("name", "this user")

        # Theme-aware colors
        overlay_bg = "rgba(0, 0, 0, 0.7)" if is_dark else "rgba(0, 0, 0, 0.5)"
        dialog_bg = "#1f2937" if is_dark else "white"
        text_color = "#f3f4f6" if is_dark else "#111827"
        cancel_bg = "#374151" if is_dark else "#e5e7eb"
        cancel_color = "#f3f4f6" if is_dark else "#374151"

        content = html.Div(
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "right": 0,
                "bottom": 0,
                "backgroundColor": overlay_bg,
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "zIndex": 1000,
            },
            children=[
                html.Div(
                    style={
                        "backgroundColor": dialog_bg,
                        "padding": "24px",
                        "borderRadius": "8px",
                        "minWidth": "300px",
                        "maxWidth": "500px",
                        "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.3)",
                    },
                    children=[
                        html.H2("Confirm Delete", style={"marginTop": 0, "color": "#ef4444"}),
                        html.P(f"Are you sure you want to delete {name}? This action cannot be undone.", style={"color": text_color}),
                        html.Div(
                            style={"marginTop": "20px", "textAlign": "right"},
                            children=[
                                html.Button(
                                    "Cancel",
                                    id="cancel-delete",
                                    style={
                                        "padding": "8px 16px",
                                        "borderRadius": "4px",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "marginRight": "8px",
                                        "backgroundColor": cancel_bg,
                                        "color": cancel_color,
                                    },
                                ),
                                html.Button(
                                    "Delete",
                                    id="confirm-delete",
                                    style={
                                        "padding": "8px 16px",
                                        "borderRadius": "4px",
                                        "border": "none",
                                        "cursor": "pointer",
                                        "backgroundColor": "#ef4444",
                                        "color": "white",
                                    },
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
        return {"display": "block"}, content, click_info["row"]

    return no_update, no_update, no_update


@callback(
    Output("grid", "data"),
    Input("confirm-delete", "n_clicks"),
    State("pending-delete-row", "data"),
    State("grid", "data"),
    prevent_initial_call=True,
)
def delete_row(confirm_clicks, pending_row, data):
    if pending_row is not None and data:
        new_data = [row for i, row in enumerate(data) if i != pending_row]
        return new_data
    return no_update


if __name__ == "__main__":
    app.run(debug=True, port=8044)
