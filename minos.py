from flask import Flask, redirect, url_for, g
from blueprints import music
from database import db
from app import create_app, app

@app.before_request
def connect_db():
    g.db = db

@app.route("/")
def index():
    return redirect(url_for('music.index'))


app = create_app()