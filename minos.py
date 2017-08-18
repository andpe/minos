from flask import Flask, redirect, url_for
from modules import music

app = Flask(__name__)

app.register_blueprint(music, url_prefix='/music')

@app.route("/")
def index():
    return redirect(url_for('music.index'))


if __name__ == '__main__':
    app.run(debug=True)