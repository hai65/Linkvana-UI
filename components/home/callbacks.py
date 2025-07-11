from dash import Input, Output, State, html, callback_context, no_update
import requests
from endpoints import CREATE_SHORTLINK, GET_EVENTS
import dash
from datetime import datetime, timedelta

API_URL = CREATE_SHORTLINK
GET_URL = GET_EVENTS


def parse_date(d):
    if not d:
        return None
    d = d.strip().rstrip("Z")
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%f"):
        try:
            return datetime.strptime(d, fmt)
        except:
            continue
    return None


def normalize_row(row):
    raw_date = row.get("createDate", "")
    try:
        if raw_date.endswith("Z"):
            raw_date = raw_date[:-1]
        dt = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f")
        dt_vietnam = dt + timedelta(hours=7)
        created = dt_vietnam.strftime("%Y-%m-%d %H:%M:%S")
    except:
        created = raw_date
    return {
        "id": row.get("id"),
        "original_url": row.get("originalUrl"),
        "short_url": row.get("shortenedUrl"),
        "team": row.get("team"),
        "level": row.get("level"),
        "title": row.get("title", ""),
        "created": created,
    }


def register_home_callbacks(app):
    @app.callback(
        Output("shortlink-modal", "style"),
        Output("modal-body", "children"),
        Output("link-view-detail", "style"),
        Output("input-url", "value"),
        Output("select-team", "value"),
        Output("select-level", "value"),
        Output("input-title", "value"),
        Output("cached-table-data", "data", allow_duplicate=True),  
        Input("btn-create", "n_clicks"),
        Input("btn-close-modal", "n_clicks"),
        State("input-url", "value"),
        State("select-team", "value"),
        State("select-level", "value"),
        State("input-title", "value"),
        prevent_initial_call=True
    )
    def handle_modal(btn_create, btn_close, url, team, level, title):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        trigger = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger == "btn-close-modal" and btn_close:
            return {"display": "none"}, "", {"display": "none"}, no_update, no_update, no_update, no_update, no_update

        if trigger == "btn-create" and not btn_create:
            raise dash.exceptions.PreventUpdate

        missing_fields = []
        if not url:
            missing_fields.append("Original URL")
        if not team:
            missing_fields.append("Team")
        if not level:
            missing_fields.append("Impact Level")

        if missing_fields:
            return {
                "display": "flex"
            }, f"❗ Missing field(s): {', '.join(missing_fields)}.", {"display": "none"}, no_update, no_update, no_update, no_update, no_update

        if title and len(title) > 200:
            return {
                "display": "flex"
            }, "❗ Title can only be up to 200 characters.", {"display": "none"}, no_update, no_update, no_update, no_update, no_update

        payload = {
            "originalUrl": url,
            "team": team,
            "level": level,
            "title": title
        }

        try:
            res = requests.post(API_URL, json=payload)
            if res.status_code == 200:
                # ✅ Tạo thành công -> gọi lại API GET
                response = requests.get(f"{GET_URL}?page=1&pageSize=999999", timeout=10)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    normalized = [normalize_row(d) for d in data]
                    normalized.sort(key=lambda x: parse_date(x["created"]) or datetime.min, reverse=True)
                    return (
                        {"display": "flex"},
                        "✅ Link created successfully!",
                        {"display": "inline-block"},
                        "", None, None, "",
                        normalized
                    )
                else:
                    return (
                        {"display": "flex"},
                        "✅ Link created, but failed to reload data.",
                        {"display": "inline-block"},
                        "", None, None, "",
                        no_update
                    )
            else:
                try:
                    error_msg = res.json().get("message", "Unknown error")
                except Exception:
                    error_msg = res.text
                return {"display": "flex"}, f"❌ {error_msg}", {"display": "none"}, no_update, no_update, no_update, no_update, no_update

        except Exception as e:
            return {"display": "flex"}, f"❌ Request failed: {str(e)}", {"display": "none"}, no_update, no_update, no_update, no_update, no_update
