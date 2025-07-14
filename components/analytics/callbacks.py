from dash import Input, Output
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime
from dash.exceptions import PreventUpdate
from endpoints import GET_EVENTS

API_URL = GET_EVENTS

TEAM_COLORS = {"OPS": "#7E57C2", "OMS": "#42A5F5", "TMS": "#5C6BC0", "WMS": "#26C6DA"}
LEVEL_COLORS = {"Warn": "orange", "Error": "#F44336", "Fatal": "#8B0000"}

def parse_date_safe(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except:
        return None

def apply_chart_style(fig):
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title=None,
        font=dict(
            family="Amarillo USAF, sans-serif",
            size=14,
            color="#333"
        ),
        title=dict(
            font=dict(
                family="Amarillo USAF, sans-serif",
                size=24,        # 👉 chỉnh size lớn hơn ở đây
                color="#222"
            ),
            x=0.5,             # 👉 căn giữa tiêu đề (tùy chọn)
            xanchor='center'
        )
    )
    return fig



def register_analytics_callbacks(app):

    @app.callback(
        Output("cached-chart-data", "data"),
        Input("cached-chart-data", "id"),
    )
    def fetch_data(_):
        try:
            url = f"{API_URL}?page=1&pageSize=999999"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            raw = response.json()
            data = raw.get("data", [])
        except Exception as e:
            print("API Error:", e)
            return []
        return data

    @app.callback(
        Output('pie-chart-s', 'figure'),
        Output('bar-chart-s', 'figure'),
        Output('pie-chart-level-s', 'figure'),
        Output('stat-total', 'children'),
        Output('stat-warn', 'children'),
        Output('stat-error', 'children'),
        Output('stat-fatal', 'children'),
        Output('stat-ops', 'children'),
        Output('stat-oms', 'children'),
        Output('stat-tms', 'children'),
        Output('stat-wms', 'children'),
        Input('cached-chart-data', 'data'),
        Input('filter-team-s', 'value'),
        Input('filter-date-s', 'start_date'),
        Input('filter-date-s', 'end_date'),
    )
    def update_statistics(data, team, start_date, end_date):
        if not data:
            raise PreventUpdate

        def match_by_date(d):
            created = parse_date_safe(d.get("createDate", "")[:10])
            if start_date:
                start_dt = parse_date_safe(start_date)
                if created and created < start_dt:
                    return False
            if end_date:
                end_dt = parse_date_safe(end_date)
                if created and created > end_dt:
                    return False
            return True

        def match_by_date_and_team(d):
            if team and d.get("team") != team:
                return False
            return match_by_date(d)

        df_date = pd.DataFrame([d for d in data if match_by_date(d)])
        df_team = pd.DataFrame([d for d in data if match_by_date_and_team(d)])

        if not df_date.empty:
            pie_fig = px.pie(df_date, names="team", title="Team-wise Ratio", hole=0.4)
            pie_fig.update_traces(
                textinfo='percent+label',              
                textfont_size=20,                     
                marker=dict(
                    colors=[TEAM_COLORS.get(t, "#888888") for t in df_date["team"]],
                    line=dict(color="black", width=4)  # Thêm viền đen
                )
            )
            pie_fig = apply_chart_style(pie_fig)

            level_pie = px.pie(df_date, names="level", title="Level-wise Ratio", hole=0.4)
            level_pie.update_traces(
                textinfo='percent+label',             
                textfont_size=20,                     
                marker=dict(
                    colors=[LEVEL_COLORS.get(l, "#888888") for l in df_date["level"]],
                    line=dict(color="black", width=4)  # Thêm viền đen
                )
            )

            level_pie = apply_chart_style(level_pie)

            warn_count = int((df_date["level"] == "Warn").sum())
            error_count = int((df_date["level"] == "Error").sum())
            fatal_count = int((df_date["level"] == "Fatal").sum())
            total_count = len(df_date)

            ops_count = int((df_date["team"] == "OPS").sum())
            oms_count = int((df_date["team"] == "OMS").sum())
            tms_count = int((df_date["team"] == "TMS").sum())
            wms_count = int((df_date["team"] == "WMS").sum())
        else:
            pie_fig = px.pie(names=["No data"], values=[1], title="No data", hole=0.4)
            level_pie = px.pie(names=["No data"], values=[1], title="No data", hole=0.4)
            warn_count = error_count = fatal_count = total_count = 0
            ops_count = oms_count = tms_count = wms_count = 0

        if not df_team.empty:
            level_counts = df_team["level"].value_counts().reset_index()
            level_counts.columns = ["level", "count"]
            bar_fig = px.bar(
                level_counts,
                x="level",
                y="count",
                title="Level-wise Count (Filtered by Team)",
                color="level",
                color_discrete_map=LEVEL_COLORS
            )
            bar_fig.update_traces(
                marker=dict(
                    line=dict(color="black", width=4)
                )
            )
            bar_fig = apply_chart_style(bar_fig)
        else:
            bar_fig = px.bar(x=["No data"], y=[0], title="No data")

        return (
            pie_fig, bar_fig, level_pie,
            total_count, warn_count, error_count, fatal_count,
            ops_count, oms_count, tms_count, wms_count
        )

    @app.callback(
        Output('filter-team-s', 'value'),
        Output('filter-date-s', 'start_date'),
        Output('filter-date-s', 'end_date'),
        Input('refresh-btn', 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset_filters(n_clicks):
        return None, None, None
