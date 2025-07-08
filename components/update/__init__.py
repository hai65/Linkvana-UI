from dash import html, dcc

def render(data=None, team_options=None, level_options=None):
    if data is None:
        return html.Div("❌ Không tìm thấy dữ liệu để cập nhật.")

    return html.Div([
        html.H2("✏️ Update Shortlink", style={"marginBottom": "20px"}),

        html.Div([
            html.Div([
                html.Strong("ID: "), html.Span(str(data.get("id", "")))
            ], style={"marginBottom": "6px"}),

            html.Div([
                html.Strong("Original: "), html.A(data.get("original_url", ""), href=data.get("original_url", "#"), target="_blank")
            ], style={"marginBottom": "6px"}),

            html.Div([
                html.Strong("Short: "), html.A(data.get("short_url", ""), href=data.get("short_url", "#"), target="_blank")
            ], style={"marginBottom": "12px"}),
        ], className="card-row-container"),

        html.Div([
            html.Label("Title", htmlFor="update-title"),
            dcc.Input(
                id="update-title",
                type="text",
                value=data.get("title", ""),
                placeholder="Nhập tiêu đề...",
                className="form-input"
            )
        ], className="form-group"),

        html.Div([
            html.Label("Team", htmlFor="update-team"),
            dcc.Dropdown(
                id="update-team",
                value=data["team"] if data.get("team") else None,
                options=[{"label": t, "value": t} for t in (team_options or [])],
                placeholder="Chọn team...",
                className="form-input"
            )
        ], className="form-group"),

        html.Div([
            html.Label("Level", htmlFor="update-level"),
            dcc.Dropdown(
                id="update-level",
                value=data["level"] if data.get("level") else None,
                options=[{"label": l, "value": l} for l in (level_options or [])],
                placeholder="Chọn level...",
                className="form-input"
            )
        ], className="form-group"),

        html.Div([
            html.Button("✅ Submit", id="update-submit-btn", n_clicks=0, className="submit-btn"),
            html.Button("❌ Cancel", id="update-cancel-btn", n_clicks=0, className="cancel-btn"),
        ], style={"marginTop": "20px"}),

        html.Div(id="update-status", style={"marginTop": "15px", "color": "#2c3e50", "fontWeight": "bold"}),

    ], className="update-form", style={"maxWidth": "500px", "margin": "auto", "padding": "30px"})
