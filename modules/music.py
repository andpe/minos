from flask import Blueprint, render_template, redirect, url_for, g, current_app

music = Blueprint('music', __name__, template_folder='templates/music/')

@music.before_request
def wrapper_setup():
    from sonos import SonosWrapper

    # Create this with an empty config for now.
    g.sonos = SonosWrapper()

    # If we're running in debug mode then just turn on
    # mocking for the speaker.
    if current_app.debug:
        g.sonos.toggle_debug()

@music.route("/index")
@music.route("/")
def index():
    tracks = g.sonos.get_queue()
    current = g.sonos.get_current_track_info()

    index = int(current['playlist_position'])
    tracks = list(tracks)
    played = tracks[:index]
    future = tracks[index:]

    return render_template('hello.html', tracks=future + played, current=current)