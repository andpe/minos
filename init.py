""" Initialization script for Minos. """

from app import create_app
from database import db

# Create the app and push the context
app = create_app(init=True)
app.app_context().push()

app.config.from_envvar('FLASK_SETTINGS')

# Create all tables and stuff.
db.create_all()
