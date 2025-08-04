from dash import html, dcc

def render():
    return html.Div([

        html.Div([
            
             html.Div([
                html.Button("+", id='btn-create', style={"fontSize": "50px", "minWidth": "90px"}),
            ], className="btn-create-container"),
            html.Div("Quick create:", className="header-create-content"),
           
        ], className="create-header"),

        html.Div([

           
            html.Div([
                html.Label("Please select a team *", htmlFor="select-team"),
                dcc.Dropdown(
                    id='select-team',
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
                    placeholder="Select team",
                    style={"flex": "3"},
                    className="dropdown-item"
                ),
            ], className="dropdown-container-team"),

           
            html.Div([
                html.Label("Please select a level *", htmlFor="select-level"),
                dcc.Dropdown(
                    id='select-level',
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
                    placeholder="Select impact level",
                    style={"flex": "3"},
                    className="dropdown-item"
                ),
            ], className="dropdown-container-level"),

            
            html.Div([
                dcc.Input(
                    id='input-url',
                    type='text',
                    placeholder='Enter your Original URL *',
                    className='custom-placeholder-input',
                    style={
                        "fontFamily": "Arial",  
                        "backgroundColor": "white",
                        "border": "3px solid",
                        "borderRadius": "8px",
                        "filter": "drop-shadow(rgb(68, 68, 68) 4px 4px 0px)",
                        "height": "50px",
                        "width": "100%"
                    }

                ),
            ], className="input-url-container"),



            html.Div([
                dcc.Input(
                    id='input-title',
                    type='text',
                    placeholder='Enter a short title / description',
                    style={
                        "fontFamily": "'Amarillo USAF'",
                        "backgroundColor": "white",
                        "border": "3px solid",
                        "borderRadius": "8px",
                        "filter": "drop-shadow(rgb(68, 68, 68) 4px 4px 0px)",
                        "height": "50px",
                        "width": "100%"
                    }
                ),
            ], className="input-title-container"),

            html.Div(id="create-status")
        ], className="global-create"),

        dcc.Loading(
            html.Div([ 
                html.Div([
                    html.Div("Status", className="modal-header"),
                    html.Div(id="modal-body", className="modal-body"),
                    html.Div([
                        dcc.Link("View Detail", href="/links", id="link-view-detail", className="modal-button"),
                        html.Button("Close", id="btn-close-modal", className="modal-button"),
                    ], id="modal-footer", className="modal-footer")
                ], className="modal-content"),
            ], id="shortlink-modal", className="modal", style={"display": "none"})
        )

    ], className="create-form", style={"margin": "200px", "padding": "30px"})
