from dash import html, dcc

def render():
    return html.Div([
        
        # Header cố định
        html.Div("Analytics", className="header-content"),


         html.Div([
                dcc.DatePickerRange(id='filter-date-s', className="filter-item"),
                dcc.Dropdown(
                    id='filter-team-s',
                    options=[{"label": t, "value": t} for t in ["OPS", "OMS", "TMS", "WMS"]],
                    placeholder="Team",
                    className="filter-item",
                ),
                dcc.Dropdown(
                    id='filter-level-s',
                    options=[{"label": l, "value": l} for l in ["Warn", "Error", "Fatal"]],
                    placeholder="Level",
                    className="filter-item"
                ),

                html.Button("Refresh", id="refresh-btn", n_clicks=0, className="refresh-button"),
            
            ], className="global-filter-s"),
        # Nội dung chính
        html.Div([
            html.Div([
                    dcc.Graph(id="pie-chart-s", config={"responsive": True}, style={"height": "100%", "width": "100%"})
                ], className="chart-container"),

                # Biểu đồ cột (Bar Chart)
                html.Div([
                    dcc.Graph(id="bar-chart-s",  config={"responsive": True}, style={"height": "100%", "width": "100%"})
                ], className="chart-container"),

        ], className="global-chart-container"), 

        dcc.Store(id="cached-chart-data"),
        
    ], className="analytics-content-area")
