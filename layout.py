from dash import Input, Output, State, callback
from endpoints import HOME_PAGE, LINKS_PAGE, ANALYTICS_PAGE, IMPORT, EXPORT
import requests
from dash import ctx, Output, Input, callback, dcc, html
import dash

def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),

        # ✅ Các Store dùng toàn cục (đặt ở đây tránh trùng lặp giữa các page)
        dcc.Store(id="cached-table-data", data=[]),
        dcc.Store(id="initial-load-trigger", data=True),
        dcc.Store(id="selected-row-id", data=None),
        dcc.Clipboard(id="clipboard", content="", style={"display": "none"}),  # nếu cần dùng nhiều nơi
        dcc.Download(id="download-exported-file"),
        dcc.ConfirmDialog(id="import-success-dialog", message=""),


        html.Div([
            # Sidebar
            html.Div([
                html.Div([
                    html.Div("Linkvana", className="sidebar-logo"),
                    html.Button("◀", id="sidebar-toggle", className="sidebar-toggle-btn"),
                ], className="sidebar-header"),

                html.Div([
                    html.Div(dcc.Link([
                        html.Img(src="/assets/icons/home.png", className="sidebar-icon-img"),
                        html.Span("Home", className="sidebar-text")
                    ], href=HOME_PAGE), className="sidebar-item-container"),

                    html.Div(dcc.Link([
                        html.Img(src="/assets/icons/link.png", className="sidebar-icon-img"),
                        html.Span("Links", className="sidebar-text")
                    ], href=LINKS_PAGE), className="sidebar-item-container"),

                    html.Div(dcc.Link([
                        html.Img(src="/assets/icons/pie-chart.png", className="sidebar-icon-img"),
                        html.Span("Analytics", className="sidebar-text")
                    ], href=ANALYTICS_PAGE), className="sidebar-item-container"),

                    html.Div([
                        html.Div([
                            html.Img(src="/assets/icons/upload.png", className="sidebar-icon-img"),
                            html.Span("Import", className="sidebar-text"),
                        ], className="sidebar-button", style={"position": "relative"}),

                        dcc.Upload(
                            id="upload-import-file",
                            children=html.Div(),  # Không cần children, vì mình overlay lên button thật
                            multiple=False,
                            accept=".xlsx",
                            style={
                                "position": "absolute",
                                "top": 0,
                                "left": 0,
                                "width": "100%",
                                "height": "100%",
                                "opacity": 0,
                                "cursor": "pointer",
                                "zIndex": 10,
                            }
                        ),
                    ], className="sidebar-item-container", style={"position": "relative"}),




                    html.Div([
                        html.Button([
                            html.Img(src="/assets/icons/download.png", className="sidebar-icon-img"),
                            html.Span("Export", className="sidebar-text"),
                        ], id="btn-export", n_clicks=0, className="sidebar-button")
                    ], className="sidebar-item-container"),



                ], className="sidebar-items")
            ], id="sidebar", className="sidebar expanded"),

            # Page content
            html.Div(id='page-content', className="page-content")
        ], className="main-container"),

        dcc.Store(id="delete-target-id", data=None),
        dcc.ConfirmDialog(
            id="delete-confirm-dialog",
            message=""
        )

        

    ])
@callback(
    Output("sidebar", "className"),
    Output("sidebar-toggle", "children"),
    Input("sidebar-toggle", "n_clicks"),
    State("sidebar", "className"),
    prevent_initial_call=True
)
def toggle_sidebar(n_clicks, current_class):
    if "collapsed" in current_class:
        return "sidebar expanded", "◀"
    return "sidebar collapsed", "▶"


@callback(
    Output("download-exported-file", "data"),
    Input("btn-export", "n_clicks"),
    prevent_initial_call=True
)
def handle_export(n_clicks):
    response = requests.get(EXPORT)
    if response.status_code == 200:
        return dcc.send_bytes(response.content, filename="exported_links.xlsx")
    return dash.no_update


import base64
import io

from dash.exceptions import PreventUpdate
from dash import no_update

from dash.exceptions import PreventUpdate
from dash import no_update

@callback(
    Output("upload-import-file", "contents", allow_duplicate=True),
    Output("import-success-dialog", "message", allow_duplicate=True),
    Output("import-success-dialog", "displayed", allow_duplicate=True),
    Input("upload-import-file", "contents"),
    State("upload-import-file", "filename"),
    prevent_initial_call="initial_duplicate"
)
def handle_import(contents, filename):
    if not contents:
        raise PreventUpdate

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    files = {
        'file': (
            filename,
            io.BytesIO(decoded),
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    }

    response = requests.post(IMPORT, files=files)

    if response.ok:
        try:
            msg = response.json().get("message", "")
        except Exception:
            msg = ""
        full_message = f"✅ Import successful!\n{msg}\nPlease reload the page to view the updated data."

        return None, full_message, True
    else:
        return None, "", False








