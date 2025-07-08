from dash import Input, Output
from endpoints import HOME_PAGE, LINKS_PAGE, ANALYTICS_PAGE, UPDATE_PAGE
#-------------------------------------------------------------------------------------------------
from components.home import render as render_home
#-------------------------------------------------------------------------------------------------
import components.links as links
render_links = links.render
#-------------------------------------------------------------------------------------------------
import components.analytics as analytics
render_analytics = analytics.render
#-------------------------------------------------------------------------------------------------
import components.update as update
render_update = update.render


def register_routes(app):
    @app.callback(
        Output('page-content', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        if pathname == HOME_PAGE:
            return render_home()
        elif pathname == LINKS_PAGE:
            return render_links()
        elif pathname == ANALYTICS_PAGE:
            return render_analytics()
        elif pathname == UPDATE_PAGE:
            return render_update()
        else:
            return render_home()
