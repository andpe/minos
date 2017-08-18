from flask import Flask

app = None

def create_app():
    """ Create a new flask app. """
    global app

    from modules.music import music
    from database import db

    app = Flask('Minos')
    db.init_app(app)