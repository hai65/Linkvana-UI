from dash import Input, Output, State, html, ctx, ALL, dcc
import requests
from datetime import datetime, timedelta
from endpoints import GET_EVENTS, HARD_DELETE, UPDATE
from dash import no_update
from dash import Output, Input, State, ctx, no_update
from components.update import render as update_layout
from components.links import render as links_layout
from dash.exceptions import PreventUpdate
API_URL = GET_EVENTS

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



def truncate_url(url, max_len=33):
    return url if len(url) <= max_len else url[:30] + "..."



def normalize_row(row):
    raw_date = row.get("createDate", "")
    try:
        # Loại bỏ 'Z' nếu có (UTC marker), và parse microsecond
        if raw_date.endswith("Z"):
            raw_date = raw_date[:-1]
        dt = datetime.strptime(raw_date, "%Y-%m-%dT%H:%M:%S.%f")
        dt_vietnam = dt + timedelta(hours=7)  # 👉 chuyển sang giờ Việt Nam
        created = dt_vietnam.strftime("%Y-%m-%d %H:%M:%S")
    except:
        created = raw_date  # fallback nếu lỗi
    return {
        "id": row.get("id"),
        "original_url": row.get("originalUrl"),
        "short_url": row.get("shortenedUrl"),
        "team": row.get("team"),
        "level": row.get("level"),
        "title": row.get("title", ""),
        "created": created,
    }

def filter_data(data, team, level, start, end, search, order=None):
    if search:
        data = [d for d in data if search in d["original_url"] or search in d["short_url"]]
    if team:
        data = [d for d in data if d["team"] == team]
    if level:
        data = [d for d in data if d["level"] == level]
    if start:
        start_dt = parse_date(start)
        data = [d for d in data if parse_date(d["created"]) is not None and parse_date(d["created"]) >= start_dt]
    if end:
        end_dt = parse_date(end)
        if end_dt:
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
        data = [d for d in data if parse_date(d["created"]) is not None and parse_date(d["created"]) <= end_dt]

    # ✅ Sắp xếp theo thời gian nếu có chỉ định
    if order == "ASC":
        data.sort(key=lambda x: parse_date(x["created"]) or datetime.min)
    elif order == "DESC":
        data.sort(key=lambda x: parse_date(x["created"]) or datetime.min, reverse=True)

    return data



def render_cards(data):
    # Nếu không có data thật sự -> hiển thị thông báo + 2 card ẩn để giữ layout
    if not data:
        return [
            html.Div("No data found", className="data-card no-data-card", style={
                "minWidth": "280px",
                "padding": "20px",
                "textAlign": "center",
                "display": "flex",
                "justifyContent": "center",  # canh giữa ngang
                "alignItems": "center",      # canh giữa dọc
                "height": "100px",            # hoặc tuỳ chỉnh chiều cao
                "font-family": "Amarillo USAF"
            }),
            html.Div("", className="data-card", style={"visibility": "hidden"}),
            html.Div("", className="data-card", style={"visibility": "hidden"}),
            html.Div("", className="data-card", style={"visibility": "hidden"})
        ]

    cards = []
    for d in data:
        cards.append(html.Div([
            
            html.Div([

                html.Div([
                    html.Strong("Title: ", style={"font-family": "Amarillo USAF"}), html.Span(d["title"], style={"font-family": "system-ui"})
                ], className="card-row"),
                
                html.Div([
                    html.Strong("ID: ", style={"font-family": "Amarillo USAF"}), html.Span(str(d["id"]), style={"font-family": "Amarillo USAF"})
                ], className="card-row"),

                html.Div([
                    html.Strong("Original: ", style={"font-family": "Amarillo USAF"}), html.A(truncate_url(d["original_url"]), href=d["original_url"], target="_blank", style={"font-family": "system-ui"})
                ], className="card-row"),

                html.Div([
                    html.Strong("Short: ", style={"font-family": "Amarillo USAF"}), html.A(truncate_url(d["short_url"]), href=d["short_url"], target="_blank", style={"font-family": "system-ui"})
                ], className="card-row"),

                html.Div([
                    html.Strong("Team: ", style={"font-family": "Amarillo USAF"}), html.Span(d["team"], className=f"team-{d['team'].strip().lower()}")
                ], className="card-row"),

                html.Div([
                    html.Strong("Level: ", style={"font-family": "Amarillo USAF"}), html.Span(d["level"], className=f"level-{d['level'].strip().lower()}")
                ], className="card-row"),

                html.Div([
                    html.Strong("Created: ", style={"font-family": "Amarillo USAF"}),

                    # 🟢 Phần ngày: giữ nguyên
                    html.Span(d["created"].split(" ")[0] + " ", style={"font-family": "Amarillo USAF"}),

                    # 🟠 Phần giờ: tô màu
                    html.Span(d["created"].split(" ")[1], style={
                        "font-family": "Amarillo USAF",
                        "color": "#FF5722",        # 👈 màu cam nổi bật
                        "font-weight": "bold"
                    }),
                ], className="card-row"),

            ], className="card-row-container"),

            html.Div([
                dcc.Clipboard(
                    id={'type': 'clipboard', 'index': d["id"]},
                    content=d["short_url"],
                    className="clipboard-icon",
                    style={
                        "display": "inline-block",
                        "padding": "6px 10px",
                        "fontSize": "50px",              # 👈 làm text/icon to hơn
                        "backgroundColor": "#f0f0f0",    # 👈 màu nền
                        "border": "2px solid black",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                        "text-align": "center",
                        "filter": "drop-shadow(rgb(68, 68, 68) 4px 4px 0px)"
                    },
                    title="Click để copy"
                ),
                html.Button("🗑", id={'type': 'hard-btn', 'index': d["id"]}, n_clicks=0, className="action-btn"),
                html.Button("✎", id={'type': 'update-btn', 'index': d["id"]}, n_clicks=0, className="action-btn"),
            ], className="card-actions"),
            
        ], className="data-card"))

    # ✅ Nếu có ít hơn 3 card -> thêm card ẩn để giữ layout
    while len(cards) < 10:
        cards.append(html.Div("", className="data-card", style={"visibility": "hidden"}))

    return cards



def register_links_callbacks(app):
    
    
    @app.callback(
    Output("cached-table-data", "data"),
    Output("initial-load-trigger", "data"),
    Input("initial-load-trigger", "data"),
    prevent_initial_call=False  # Cho phép chạy khi app vừa load
    )
    def load_initial_data(_):
        try:
            print("🔄 Loading initial data...")
            url = f"{API_URL}?page=1&pageSize=999999"
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print("⚠️ Failed to load initial data")
                return [], datetime.now().isoformat()

            data = response.json().get("data", [])
            normalized = [normalize_row(d) for d in data]
            normalized.sort(key=lambda x: parse_date(x["created"]) or datetime.min, reverse=True)
            return normalized, datetime.now().isoformat()
        except Exception as e:
            print(f"❌ Error loading initial data: {e}")
            return [], datetime.now().isoformat()
    
    
    
    
    # Callback cập nhật bảng
    @app.callback(
    Output('card-container', 'children'),
    Output('filter-team', 'value'),
    Output('filter-level', 'value'),
    Output('filter-date', 'start_date'),
    Output('filter-date', 'end_date'),
    Output('filter-search', 'value'),
    Output('filter-order', 'value'),

    Input('filter-order', 'value'),
    Input('filter-team', 'value'),
    Input('filter-level', 'value'),
    Input('filter-date', 'start_date'),
    Input('filter-date', 'end_date'),
    Input('search-btn', 'n_clicks'),
    Input('refresh-btn', 'n_clicks'),
    State('filter-search', 'value'),
    State('cached-table-data', 'data'),  # ✅ Dùng dữ liệu đã normalize từ đây
    Input("initial-load-trigger", "data"),  # ép chạy lúc đầu
    prevent_initial_call=False
)
    def update_card(order, team, level, start, end, search_clicks, refresh_clicks, search, data,_):
        triggered_id = ctx.triggered_id

        if not data:
            return [], team, level, start, end, search, order

        if triggered_id == "refresh-btn":
            return render_cards(data), None, None, None, None, "", None

        # if triggered_id == "search-btn":
        #     filtered = filter_data(data, team=None, level=None, start=None, end=None, search=search, order=None)
        #     return render_cards(filtered), None, None, None, None, search, None

        # Các bộ lọc khác hoặc lần đầu load
        filtered = filter_data(data, team=team, level=level, start=start, end=end, search=search, order=order)
        return render_cards(filtered), team, level, start, end, search, order




    @app.callback(
        Output("page-content", "children", allow_duplicate=True),
        Output("selected-row-id", "data"),
        Input({"type": "update-btn", "index": ALL}, "n_clicks"),
        State("cached-table-data", "data"),
        prevent_initial_call=True
    )
    def handle_update_click(n_clicks_list, data):
        triggered = ctx.triggered_id
        if not triggered or not data:
            raise PreventUpdate

        # Tìm index của nút vừa được nhấn
        row_id = triggered["index"]
        # ✅ Kiểm tra xem n_clicks của nút đó có > 0 không
        for i, btn_id in enumerate(ctx.inputs_list[0]):
            if btn_id["id"]["index"] == row_id and n_clicks_list[i] > 0:
                break
        else:
            raise PreventUpdate  # Không có nút nào được click thật sự

        selected = next((d for d in data if d["id"] == row_id), None)
        if not selected:
            return no_update, no_update

        team_options = sorted(set(d["team"] for d in data if d.get("team")))
        level_options = sorted(set(d["level"] for d in data if d.get("level")))

        return update_layout(selected, team_options, level_options), row_id





    @app.callback(
    Output("update-confirm-dialog", "message"),
    Output("update-confirm-dialog", "displayed"),
    Input("update-submit-btn", "n_clicks"),
    State("selected-row-id", "data"),
    State("update-title", "value"),
    State("update-team", "value"),
    State("update-level", "value"),
    State("cached-table-data", "data"),
    prevent_initial_call=True
)
    def handle_submit_update(n_clicks, row_id, title, team, level, table_data):
        if not row_id:
            return "❌ Không xác định được ID.", True

        original = next((d for d in table_data if d["id"] == row_id), {})

        payload = {
            "title": title if title is not None else original.get("title", ""),
            "team": team if team is not None else original.get("team", ""),
            "level": level if level is not None else original.get("level", "")
        }

        try:
            url = f"{UPDATE}{row_id}"
            print("📦 Payload gửi:", payload)
            response = requests.put(url, json=payload, timeout=10)

            if response.status_code == 200:
                return "✅ Cập nhật thành công!", True
            else:
                return f"❌ Lỗi cập nhật: {response.status_code} - {response.text}", True
        except Exception as e:
            return f"❌ Exception: {str(e)}", True



    

    @app.callback(
    Output("page-content", "children", allow_duplicate=True),
    Output("cached-table-data", "data", allow_duplicate=True),  # 👈 lưu lại dữ liệu mới
    Output("update-status", "children", allow_duplicate=True),
    Input("update-cancel-btn", "n_clicks"),
    prevent_initial_call=True
)
    def handle_cancel(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        try:
            print("🔄 Cancel clicked —> Reloading fresh data from API")
            response = requests.get(f"{API_URL}?page=1&pageSize=999999", timeout=10)
            if response.status_code != 200:
                print(f"⚠️ Cancel reload failed: {response.status_code}")
                return html.Div("⚠️ Error loading data"), [], "❌ Không thể tải lại dữ liệu."

            data = response.json().get("data", [])
            normalized = [normalize_row(d) for d in data]
            normalized.sort(key=lambda x: parse_date(x["created"]) or datetime.min, reverse=True)

            return links_layout(normalized), normalized, ""
        
        except Exception as e:
            print(f"❌ Exception on cancel reload: {e}")
            return html.Div("❌ Exception loading data"), [], f"❌ Lỗi tải lại dữ liệu: {str(e)}"

    
    

    @app.callback(
    Output("delete-confirm-dialog", "displayed"),
    Output("delete-confirm-dialog", "message"),     # 🆕
    Output("delete-target-id", "data"),
    Input({"type": "hard-btn", "index": ALL}, "n_clicks"),
    State("cached-table-data", "data"),             # 🆕 để lấy thêm short_url nếu cần
    prevent_initial_call=True
)
    def open_delete_confirm(n_clicks_list, data):
        triggered = ctx.triggered_id

        if not triggered or not any(n_clicks_list):
            raise PreventUpdate

        row_id = triggered["index"]

        # ✅ Tìm row để hiển thị thêm thông tin
        row = next((d for d in data if d["id"] == row_id), {})
        short_url = row.get("short_url", "")

        message = f"❗Bạn có chắc muốn xoá link này?\nID: {row_id}\nShort: {short_url}"

        return True, message, row_id




    @app.callback(
    Output("cached-table-data", "data", allow_duplicate=True),
    Output("card-container", "children", allow_duplicate=True),
    Input("delete-confirm-dialog", "submit_n_clicks"),
    State("delete-target-id", "data"),
    State("cached-table-data", "data"),
    State("filter-team", "value"),
    State("filter-level", "value"),
    State("filter-date", "start_date"),
    State("filter-date", "end_date"),
    State("filter-search", "value"),
    State("filter-order", "value"),
    prevent_initial_call=True
)
    def confirm_delete(submit_n_clicks, row_id, cached_data, team, level, start, end, search, order):
        if not submit_n_clicks or not row_id or not cached_data:
            raise PreventUpdate

        try:
            response = requests.delete(f"{HARD_DELETE}{row_id}", timeout=10)
            if response.status_code != 200:
                print(f"❌ Lỗi xóa: {response.status_code} - {response.text}")
                return cached_data, render_cards(filter_data(cached_data, team, level, start, end, search, order))
        except Exception as e:
            print(f"❌ Exception khi xóa: {e}")
            return cached_data, render_cards(filter_data(cached_data, team, level, start, end, search, order))

        # ✅ Cập nhật cache
        new_data = [d for d in cached_data if d["id"] != row_id]
        filtered = filter_data(new_data, team, level, start, end, search, order)
        return new_data, render_cards(filtered)

