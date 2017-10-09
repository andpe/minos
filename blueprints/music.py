from flask import Blueprint, render_template, redirect, url_for, g, current_app, make_response

music = Blueprint('music', __name__, template_folder='templates/')

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

    return render_template('music/hello.html', tracks=future + played, current=current)

@music.route("/vote/<uri>/<direction>", methods=["POST"])
def vote(uri, direction):
    """ Handle votes up or down on tracks. """
    import requests
    import json

    requests.post(
        'http://nginx:81/pub/',
        data=json.dumps({
            'track': uri,
            'direction': direction
        })
    )

    return make_response('OK', 200, {})