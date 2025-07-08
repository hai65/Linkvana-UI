def register_callbacks(app):
    from components.home.callbacks import register_home_callbacks
    from components.links.callbacks import register_links_callbacks
    from components.analytics.callbacks import register_analytics_callbacks
    from components.update.callbacks import register_update_callbacks


    register_home_callbacks(app)
    register_links_callbacks(app)
    register_analytics_callbacks(app)
    register_update_callbacks(app)
