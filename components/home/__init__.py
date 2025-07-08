from dash import html, dcc

def render():
    return html.Div([
        
        html.Div("Quick create", className="header-create-content"),
        
        html.Div([
            
            html.Div("Team *"),
            html.Div([
                dcc.Dropdown(id='select-team', 
                            options=[{"label": team, "value": team} for team in ["OPS", "OMS", "TMS", "WMS"]],
                            placeholder="Select team",
                            style={"flex": "3"},
                            className="dropdown-item"
                ),
                html.Div([], className="invisible-container"),
            ], className="dropdown-container"),
            
            html.Div("Level *"),
            html.Div([
                dcc.Dropdown(
                    id='select-level',
                    options=[{"label": level, "value": level} for level in ["Warn", "Error", "Fatal"]],
                    placeholder="Select impact level",
                    style={"flex": "3"},
                    className="dropdown-item"
                ),
                html.Div([], className="invisible-container"),
            ], className="dropdown-container"),

            html.Div("Enter a short title / description"),
             
             html.Div([ 
                dcc.Input(
                    id='input-title',
                    type='text',
                    placeholder='e.g. Service unreachable on production',
                    style={"height": "40px", "width": "100%"}
                ),
            ], className="input-title-container"),

            html.Div("Enter your destination URL *"),
            
            html.Div([
                dcc.Input(id='input-url', type='text', placeholder='https://example.com/my-long-url', style={"height": "40px", "width": "100%"}),
            ], className="input-url-container"),

            html.Div([
                html.Button("Create", id='btn-create'),
            ], className="btn-create-container"),
            html.Div(id="create-status")
        ], className="global-create"),
        
        
        html.Div([  # Modal
            html.Div([
                html.Div("Status", className="modal-header"),
                html.Div(id="modal-body", className="modal-body"),
                html.Div([  # 👇 luôn có nút Close
                    dcc.Link("View Detail", href="/links", id="link-view-detail", className="modal-button"),
                    html.Button("Close", id="btn-close-modal", className="modal-button"),
                ], id="modal-footer", className="modal-footer")
            ], className="modal-content"),
        ], id="shortlink-modal", className="modal", style={"display": "none"})

    ], className="content-area")
