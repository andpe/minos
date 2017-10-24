from flask import Blueprint, render_template, redirect, url_for, g, current_app, make_response, session
from ..database import db

music = Blueprint('music', __name__, template_folder='templates/')

@music.before_request
def wrapper_setup():
    from ..sonos import SonosWrapper
    from ..database import SonosConfig
    import soco

    speakers = {}
    with current_app.app_context():
        speakers = db.session.query(SonosConfig).filter(
            SonosConfig.key == 'speakers'
        ).first()

        if speakers:
            from json import loads
            speakers = loads(speakers.value)
            speakers = {x: soco.SoCo(x) for x in speakers}
        else:
            speakers = {
                '10.203.70.133': soco.SoCo('10.203.70.133')
            }

    g.sonos = SonosWrapper(speakers)

    # If we're running in debug mode then just turn on
    # mocking for the speaker...
    if current_app.debug:
        g.sonos.toggle_debug()

@music.before_request
def redis_connect():
    import redis

    g.redis = redis.StrictRedis(host='redis')

@music.route("/<ip>/")
@music.route("/")
def index(ip=''):
    import urllib.parse
    import re
    from hashlib import sha256
    from ..sonos import Track
    from ..database import UserVote, User
    from sqlalchemy import func

    if len(ip) < 1:
        from ..database import SonosConfig
        from json import loads

        speakers = g.db.session.query(SonosConfig).filter(
            SonosConfig.key == 'speakers'
        ).first()

        if speakers is not None and len(speakers.value) > 0:
            speakers = loads(speakers.value)
            ip = speakers[0]

    if not re.match('^\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}$', ip):
        return make_response('Invalid queue ID', 404, {})

    sha = sha256()
    sha.update(ip.encode('utf-8'))
    ip_hash = sha.hexdigest()

    tracks = current_app.cache.get('minos_tracklist_' + ip_hash)
    current = current_app.cache.get('minos_current_song_' + ip_hash)

    if tracks:
        index = int(current.playlist_position)
        tracks = list(tracks)
        played = tracks[:index]
        future = tracks[index:]
    else:
        index = 0
        tracks = []
        played = []
        future = []

    user_voted = []

    if 'username' in session:
        user = db.session.query(User).filter(User.name == session['username']).first()
        user_voted = db.session.query(UserVote).filter(UserVote.uid == User.id).all()
        user_voted = {urllib.parse.unquote(x.uri): x.direction for x in user_voted}

    votes_total = db.session.query(
        UserVote.uri,
        UserVote.direction,
        func.count(UserVote.uri)
    ).group_by(
        UserVote.uri,
        UserVote.direction
    ).all()

    return render_template(
        'music/hello.html',
        tracks=future + played,
        current=current,
        user_voted=user_voted,
        votes_total_up={track: votes for track, direction, votes in votes_total if direction == 'up'},
        votes_total_down={track: votes for track, direction, votes in votes_total if direction == 'down'}
    )

@music.route("/vote/<uri>/<direction>", methods=["POST"])
def vote(uri, direction):
    """ Handle votes up or down on tracks. """
    import requests
    import json


    if 'username' in session:
        from ..database import UserVote, User
        user = db.session.query(User).filter(User.name == session['username']).first()
        vote = vote_exists(user, uri)
        if not vote:
            # Log that this user has voted on this track.
            db.session.add(
                UserVote(uid=user.id, uri=uri, direction=direction)
            )
            db.session.flush()
            db.session.commit()

            #if direction == 'down':
            #    tracks = current_app.cache.get('minos_tracklist')
            #    new = []
            #    print(tracks)
            #    for track in tracks:
            #        if track.uri.split('?')[0] == uri:
            #            print('Skipping!')
            #            continue
            #        new.append(track)
            #    print(new)
            #    current_app.cache.set('minos_tracklist', new)
 
            requests.post(
                'http://nginx:81/pub/',
                data=json.dumps({
                    'track': uri,
                    'direction': direction,
                    'removed': False
                })
            )
        else:
            if vote.direction == direction:
                db.session.delete(vote)
                db.session.commit()
                requests.post(
                    'http://nginx:81/pub/',
                    data=json.dumps({
                        'track': uri,
                        'direction': direction,
                        'removed': True
                    })
                )
            else:
                return make_response('ERR_ALREADY_VOTED', 200, {})

    return make_response('OK', 200, {})

# Vote helpers
def vote_exists(user, uri):
    """ Check if a vote from this user for this track already exists. """
    from ..database import UserVote
    vote = db.session.query(UserVote).filter(UserVote.uid == user.id, UserVote.uri == uri).first()

    return vote
