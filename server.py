from flask import Flask, redirect, url_for, g, render_template
from minos.blueprints import music
from minos.database import db
from minos.app import create_app, app
#from werkzeug.exceptions import HTTPException

@app.before_request
def connect_db():
    g.db = db

@app.route("/")
def index():
    return redirect(url_for('music.index'))

@app.errorhandler(404)
def notfound(e):
    return render_template('404.html')

@app.errorhandler(Exception)
def error(e: Exception):
    import traceback
    exc = traceback.format_exception(type(e), e, e.__traceback__)
    return render_template('500.html', exc=exc)

app = create_app()