"""
Example 44: Button Cell with Dialog

This example demonstrates the button cell type with dialog interactions:
- Click "View" to open a details dialog
- Click "Delete" to open a confirmation dialog that actually removes the row

Button cells support:
- Custom colors (backgroundColor, color, borderColor)
- Custom border radius
- Click callbacks with row/column information
"""

import dash
from dash import html, dcc, callback, Input, Output, State, no_update
from dash_glide_grid import GlideGrid

app = dash.Dash(__name__)

# Sample data with button cells
initial_data = [
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

columns = [
    {"title": "ID", "id": "id", "width": 60},
    {"title": "Name", "id": "name", "width": 150},
    {"title": "Email", "id": "email", "width": 200},
    {"title": "Status", "id": "status", "width": 100},
    {"title": "Action", "id": "action", "width": 80},
    {"title": "Delete", "id": "delete", "width": 80},
]

# Dialog styles
dialog_overlay_style = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "right": 0,
    "bottom": 0,
    "backgroundColor": "rgba(0, 0, 0, 0.5)",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "center",
    "zIndex": 1000,
}

dialog_content_style = {
    "backgroundColor": "white",
    "padding": "24px",
    "borderRadius": "8px",
    "minWidth": "300px",
    "maxWidth": "500px",
    "boxShadow": "0 4px 20px rgba(0, 0, 0, 0.15)",
}

button_style = {
    "padding": "8px 16px",
    "borderRadius": "4px",
    "border": "none",
    "cursor": "pointer",
    "marginLeft": "8px",
    "fontSize": "14px",
}

app.layout = html.Div([
    html.H1("Button Cell with Dialog Example"),
    html.P("Click 'View' to see details, or 'Delete' to remove a row."),

    GlideGrid(
        id="grid",
        columns=columns,
        data=initial_data,
        height=300,
        width="100%",
    ),

    # Store for tracking which row to delete
    dcc.Store(id="pending-delete-row", data=None),

    # View Details Dialog
    html.Div(id="view-dialog", style={"display": "none"}, children=[
        html.Div(style=dialog_overlay_style, children=[
            html.Div(style=dialog_content_style, children=[
                html.H2("User Details", style={"marginTop": 0}),
                html.Div(id="view-dialog-content"),
                html.Div(style={"marginTop": "20px", "textAlign": "right"}, children=[
                    html.Button("Close", id="close-view-dialog", style={
                        **button_style,
                        "backgroundColor": "#6b7280",
                        "color": "white",
                    })
                ])
            ])
        ])
    ]),

    # Delete Confirmation Dialog
    html.Div(id="delete-dialog", style={"display": "none"}, children=[
        html.Div(style=dialog_overlay_style, children=[
            html.Div(style=dialog_content_style, children=[
                html.H2("Confirm Delete", style={"marginTop": 0, "color": "#ef4444"}),
                html.P(id="delete-dialog-content"),
                html.Div(style={"marginTop": "20px", "textAlign": "right"}, children=[
                    html.Button("Cancel", id="cancel-delete", style={
                        **button_style,
                        "backgroundColor": "#e5e7eb",
                        "color": "#374151",
                    }),
                    html.Button("Delete", id="confirm-delete", style={
                        **button_style,
                        "backgroundColor": "#ef4444",
                        "color": "white",
                    })
                ])
            ])
        ])
    ]),

], style={"padding": "20px", "maxWidth": "900px"})


@callback(
    Output("view-dialog", "style"),
    Output("view-dialog-content", "children"),
    Input("grid", "buttonClicked"),
    Input("close-view-dialog", "n_clicks"),
    State("grid", "data"),
    prevent_initial_call=True
)
def handle_view_button(click_info, close_clicks, data):
    from dash import ctx

    if ctx.triggered_id == "close-view-dialog":
        return {"display": "none"}, no_update

    if click_info and click_info.get("title") == "View":
        row_data = data[click_info['row']]
        content = html.Div([
            html.P([html.Strong("ID: "), str(row_data.get('id', 'N/A'))]),
            html.P([html.Strong("Name: "), row_data.get('name', 'N/A')]),
            html.P([html.Strong("Email: "), row_data.get('email', 'N/A')]),
            html.P([html.Strong("Status: "), row_data.get('status', 'N/A')]),
        ])
        return {"display": "block"}, content

    return no_update, no_update


@callback(
    Output("delete-dialog", "style"),
    Output("delete-dialog-content", "children"),
    Output("pending-delete-row", "data"),
    Input("grid", "buttonClicked"),
    Input("cancel-delete", "n_clicks"),
    Input("confirm-delete", "n_clicks"),
    State("grid", "data"),
    State("pending-delete-row", "data"),
    prevent_initial_call=True
)
def handle_delete_button(click_info, cancel_clicks, confirm_clicks, data, pending_row):
    from dash import ctx

    if ctx.triggered_id == "cancel-delete":
        return {"display": "none"}, no_update, None

    if ctx.triggered_id == "confirm-delete":
        return {"display": "none"}, no_update, None

    if click_info and click_info.get("title") == "Delete":
        row_data = data[click_info['row']]
        name = row_data.get('name', 'this user')
        content = f"Are you sure you want to delete {name}? This action cannot be undone."
        return {"display": "block"}, content, click_info['row']

    return no_update, no_update, no_update


@callback(
    Output("grid", "data"),
    Input("confirm-delete", "n_clicks"),
    State("pending-delete-row", "data"),
    State("grid", "data"),
    prevent_initial_call=True
)
def delete_row(confirm_clicks, pending_row, data):
    if pending_row is not None and data:
        # Remove the row from data
        new_data = [row for i, row in enumerate(data) if i != pending_row]
        return new_data
    return no_update


if __name__ == "__main__":
    app.run(debug=True, port=8044)
