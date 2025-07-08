from dash import Input, Output
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime
from dash.exceptions import PreventUpdate
from endpoints import GET_EVENTS

API_URL = GET_EVENTS

TEAM_COLORS = {"OPS": "#1f77b4", "OMS": "#ff7f0e", "TMS": "#2ca02c", "WMS": "#d62728"}
LEVEL_COLORS = {"Warn": "#f0ad4e", "Error": "#d9534f", "Fatal": "#5e5e5e"}

def parse_date_safe(d):
    try:
        return datetime.strptime(d, "%Y-%m-%d")
    except:
        return None

def apply_chart_style(fig):
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20), legend_title=None)
    return fig

def register_analytics_callbacks(app):
    
    
    from dash import Output, Input


    @app.callback(
    Output("cached-chart-data", "data"),
    Input("cached-chart-data", "id"),  # gọi 1 lần khi layout khởi tạo
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
    Input('cached-chart-data', 'data'),
    Input('filter-team-s', 'value'),
    Input('filter-level-s', 'value'),
    Input('filter-date-s', 'start_date'),
    Input('filter-date-s', 'end_date'),
)
    def update_statistics(data, team, level, start_date, end_date):
        if not data:
            raise PreventUpdate

        def match(d):
            if team and d.get("team") != team:
                return False
            if level and d.get("level") != level:
                return False
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

        filtered = [d for d in data if match(d)]
        df = pd.DataFrame(filtered)
        print("✅ Filtered levels:", df['level'].unique() if not df.empty else [])

        if not df.empty:
            pie_fig = px.pie(df, names="team", title="Team-wise Ratio", hole=0.4)
            pie_fig.update_traces(marker=dict(colors=[TEAM_COLORS.get(t, "#888888") for t in df["team"]]))
            pie_fig = apply_chart_style(pie_fig)

            level_counts = df["level"].value_counts().reset_index()
            level_counts.columns = ["level", "count"]
            bar_fig = px.bar(
                level_counts,
                x="level",
                y="count",
                title="Level-wise Count",
                color="level",
                color_discrete_map=LEVEL_COLORS
            )
            bar_fig = apply_chart_style(bar_fig)
        else:
            pie_fig = px.pie(names=["No data"], values=[1], title="No data", hole=0.4)
            bar_fig = px.bar(x=["No data"], y=[0], title="No data")

        return pie_fig, bar_fig


      

    @app.callback(
        Output('filter-team-s', 'value'),
        Output('filter-level-s', 'value'),
        Output('filter-date-s', 'start_date'),
        Output('filter-date-s', 'end_date'),
        Input('refresh-btn', 'n_clicks'),
        prevent_initial_call=True,
    )
    def reset_filters(n_clicks):
        return None, None, None, None
