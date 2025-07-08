from dash import html, dcc
from dash import Input, Output, State, callback
from endpoints import HOME_PAGE, LINKS_PAGE, ANALYTICS_PAGE

def create_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),

        # ✅ Các Store dùng toàn cục (đặt ở đây tránh trùng lặp giữa các page)
        dcc.Store(id="cached-table-data", data=[]),
        dcc.Store(id="initial-load-trigger", data=True),
        dcc.Store(id="selected-row-id", data=None),
        dcc.Clipboard(id="clipboard", content="", style={"display": "none"}),  # nếu cần dùng nhiều nơi

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