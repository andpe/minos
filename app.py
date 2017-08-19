from flask import Flask
from flask_caching import Cache

# We need access to these right away
app = Flask('Minos')
app.config.from_envvar('FLASK_SETTINGS')
cache = Cache()
app.cache = cache

def create_app(init=False):
    """ Create a new flask app. """
    global app, cache, oauth

    from database import db
    from flask_session import Session

    # Create flask apps and plugins
    session = Session()

    # Initialize the apps and plugins
    cache.init_app(app)
    db.init_app(app)

    app.db = db
    session.init_app(app)

    # If we're not doing init stuff then we can load blueprints.
    if not init:
        from blueprints.music import music
        # Register blueprints
        app.register_blueprint(music, url_prefix='/music')

        from blueprints.users import users
        app.register_blueprint(users, url_prefix='/users')

    return app
