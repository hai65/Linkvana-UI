from dash import html, dcc


def render(data=None):
    return html.Div([
        html.Div("Link Management Console", className="header-content"),

        html.Div([  
            html.Div([

                dcc.Dropdown(
                id='filter-order',
                options=[
                    {
                        "label": html.Span("ASC", style={"color": "black"}),
                        "value": "ASC"
                    },
                    {
                        "label": html.Span("DESC", style={"color": "black"}),
                        "value": "DESC"
                    },
                ],
                placeholder="Chronology",
                className="filter-item-order", 
            ),
                dcc.Dropdown(
                    id='filter-team',
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
                    className="filter-item",
                ),
            
            dcc.Dropdown(
                id='filter-level',
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
                placeholder="Level",
                className="filter-item", 
            ),
           
            dcc.DatePickerRange(id='filter-date', className="filter-item"),
            
            html.Div([   
                dcc.Input(
                    id='filter-search',
                    type='text',
                    placeholder='Search URL...',
                    className='filter-item',
                    debounce=True,
                    style={"height": "40px", "width": "100%"}
                ),

                html.Button("⌕", id="search-btn", n_clicks=0, className="search-button"),
                html.Button("⟳", id="refresh-btn", n_clicks=0, className="refresh-button"),

            ], className="search-container"),
               
            ], className="filter-bar"),

            html.Div([
                html.Div(id="card-container", className="links-card-container")
            ], className="links-card-container"),

        ], className="main-content-links") 
    ], className="links-content-area")

