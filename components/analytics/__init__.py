from dash import html, dcc

def render():
    return html.Div([
        
            html.Div([
                html.Div("Filter by:", className="filter-name", style={"margin-left": "10px"}),

                dcc.DatePickerRange(id='filter-date-s', className="filter-item"),

                html.Div([    
                    html.Button("⟳", id="refresh-btn", n_clicks=0, className="refresh-button-s"),
                ], className="refresh-button-container-s"),


                html.Div([
                    html.Div([
                        html.Div("Total", className="stat-label"),
                        html.Div(id="stat-total", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("Warn", className="stat-label", style={"color": "orange"}),
                        html.Div(id="stat-warn", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("Error", className="stat-label", style={"color": "#F44336"}),
                        html.Div(id="stat-error", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("Fatal", className="stat-label", style={"color": "#8B0000"}),
                        html.Div(id="stat-fatal", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("OPS", className="stat-label", style={"color": "#7E57C2"}),
                        html.Div(id="stat-ops", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("OMS", className="stat-label", style={"color": "#42A5F5"}),
                        html.Div(id="stat-oms", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("TMS", className="stat-label", style={"color": "#5C6BC0"}),
                        html.Div(id="stat-tms", className="stat-value")
                    ], className="stat-card"),

                    html.Div([
                        html.Div("WMS", className="stat-label", style={"color": "#26C6DA"}),
                        html.Div(id="stat-wms", className="stat-value")
                    ], className="stat-card"),
                ], className="stat-container")
        ], className="filter-bar"),

     html.Div([   
        
        
        
        html.Div([
            html.Div([
                    dcc.Graph(id="pie-chart-s", config={"responsive": True, "displaylogo": False}, style={"height": "100%", "width": "100%"})
                ], className="pie-chart-container"),
            html.Div([
            dcc.Graph(id="pie-chart-level-s", config={"responsive": True, "displaylogo": False}, style={"height": "100%", "width": "100%"})
        ], className="pie-chart-container"),

        ], className="global-pie-chart-container"),


            
         html.Div([
            html.Div([
                dcc.Dropdown(
                    id='filter-team-s',
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
                    placeholder="Team",
                    className="filter-item-bar",
                ),
                dcc.Graph(id="bar-chart-s",  config={"responsive": True, "displaylogo": False}, style={"height": "100%", "width": "100%"})
            ], className="chart-container"),
        ], className="global-chart-container"), 
     ], className="hahaha"),

        dcc.Store(id="cached-chart-data"),
        
    ], className="analytics-content-area")
