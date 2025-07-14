from dash import html, dcc

def render(data=None, team_options=None, level_options=None):
    if data is None:
        return html.Div("❌ Không tìm thấy dữ liệu để cập nhật.")

    return html.Div([
        html.Div([   
            
            html.Div([ 
                html.H2("Update Shortlink", style={"marginBottom": "20px", "text-align": "start", "flex": "5", "fontSize":"50px"}),
                html.Div([
                    html.Button("Submit", id="update-submit-btn", n_clicks=0, className="submit-btn"),
                    html.Button("✖", id="update-cancel-btn", n_clicks=0, className="cancel-btn"),
                ], className="update-btn"),
             ], className="update-header"),


            html.Div([
                html.Label("Info:", htmlFor="read-only"),
                html.Div(id="read-only", children=[
                    html.Div([
                        html.Strong("ID: ", style={"font-family": "Amarillo USAF"}), html.Span(str(data.get("id", "")), style={"font-family": "Amarillo USAF"})
                    ], style={"marginBottom": "6px"}),

                    html.Div([
                        html.Strong("Original: ", style={"font-family": "Amarillo USAF"}), html.A(data.get("original_url", ""), href=data.get("original_url", "#"), target="_blank")
                    ], style={"marginBottom": "6px", "display": "flex"}),

                    html.Div([
                        html.Strong("Short: ", style={"font-family": "Amarillo USAF"}), html.A(data.get("short_url", ""), href=data.get("short_url", "#"), target="_blank")
                    ], style={}),
                ], className="read-only-info"),
            ], className="read-only-container"),

            html.Div([
                html.Label("Title:", htmlFor="update-title"),
                dcc.Input(
                    id="update-title",
                    type="text",
                    value=data.get("title", ""),
                    placeholder="Nhập tiêu đề...",
                    className="form-input-title"
                )
            ], className="form-group-title"),

            html.Div([
                html.Label("Team:", htmlFor="update-team"),
                dcc.Dropdown(
                    id="update-team",
                    value=data["team"] if data.get("team") else None,
                    options=[
                                {
                                    "label": html.Span("OPS", style={"color": "#7E57C2"}),
                                    "value": "OPS"
                                },
                                {
                                    "label": html.Span("OMS", style={"color": "#42A5F5"}),
                                    "value": "OMS"
                                },
                                {
                                    "label": html.Span("TMS", style={"color": "#5C6BC0"}),
                                    "value": "TMS"
                                },
                                {
                                    "label": html.Span("WMS", style={"color": "#26C6DA"}),
                                    "value": "WMS"
                                },
                            ],
                    placeholder="Chọn team...",
                    className="form-input"
                )
            ], className="form-group-team"),

            html.Div([
                html.Label("Level:", htmlFor="update-level"),
                dcc.Dropdown(
                    id="update-level",
                    value=data["level"] if data.get("level") else None,
                    options=[
                            {
                                "label": html.Span("Warn", style={"color": "orange"}),
                                "value": "Warn"
                            },
                            {
                                "label": html.Span("Error", style={"color": "#F44336"}),
                                "value": "Error"
                            },
                            {
                                "label": html.Span("Fatal", style={"color": "#8B0000"}),
                                "value": "Fatal"
                            },
                        ],
                    placeholder="Chọn level...",
                    className="form-input",
                )
            ], className="form-group-level"),

            

            dcc.Loading(   
                html.Div(id="update-status", style={"marginTop": "15px", "color": "#2c3e50", "fontWeight": "bold"}),
            ),

             dcc.Loading(
                dcc.ConfirmDialog(
                    id='update-confirm-dialog',
                    message='',
                )
             )
        ], className="update-border")
], className="update-form", style={"margin": "200px", "padding": "30px"})
