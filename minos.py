from flask import Flask, redirect, url_for, g
from modules import music
from database import db

app = Flask(__name__)

app.register_blueprint(music, url_prefix='/music')

@app.before_request
def connect_db():
    g.db = db

@app.route("/")
def index():
    return redirect(url_for('music.index'))


if __name__ == '__main__':
    app.run(debug=True)