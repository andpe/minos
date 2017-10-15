from flask import Blueprint, render_template, redirect, url_for, g, current_app, make_response, session
from database import db

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

@music.before_request
def redis_connect():
    import redis

    g.redis = redis.StrictRedis(host='redis')

@music.route("/index")
@music.route("/")
def index():
    import urllib.parse
    tracks = g.sonos.get_queue()
    current = g.sonos.get_current_track_info()

    index = int(current['playlist_position'])
    tracks = list(tracks)
    played = tracks[:index]
    future = tracks[index:]

    for track in tracks:
        track['uri'] = urllib.parse.unquote(track['uri'])

    user_voted = []

    if 'username' in session:
        from database import UserVote, User
        user = db.session.query(User).filter(User.name == session['username']).first()
        user_voted = db.session.query(UserVote).filter(UserVote.uid == User.id).all()
        user_voted = [urllib.parse.unquote(x.uri) for x in user_voted]

    return render_template('music/hello.html', tracks=future + played, current=current, user_voted=user_voted)

@music.route("/vote/<uri>/<direction>", methods=["POST"])
def vote(uri, direction):
    """ Handle votes up or down on tracks. """
    import requests
    import json


    if 'username' in session:
        from database import UserVote, User
        user = db.session.query(User).filter(User.name == session['username']).first()
        vote = vote_exists(user, uri)
        if not vote:
            # Log that this user has voted on this track.
            db.session.add(
                UserVote(uid=user.id, uri=uri, direction=direction)
            )
            db.session.flush()
            db.session.commit()
 
            requests.post(
                'http://nginx:81/pub/',
                data=json.dumps({
                    'track': uri,
                    'direction': direction
                })
            )
        else:
            if vote.direction == direction:
                db.session.delete(vote)
                db.session.commit()
            else:
                return make_response('ERR_ALREADY_VOTED', 200, {})

    return make_response('OK', 200, {})

# Vote helpers
def vote_exists(user, uri):
    """ Check if a vote from this user for this track already exists. """
    from database import UserVote
    vote = db.session.query(UserVote).filter(UserVote.uid == user.id, UserVote.uri == uri).first()

    return vote
