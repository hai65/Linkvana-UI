import dash
from layout import create_layout
from router import register_routes
from callbacks import register_callbacks

app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Linkvana"
app.layout = create_layout()

register_routes(app)
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8051, host="0.0.0.0")
    
    