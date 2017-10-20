from flask_oauthlib.client import OAuth
from ..app import app

oauth = OAuth()
oauth.init_app(app)