from ..authentication.twitter import twitter
from ..database import User
from flask import (Blueprint, current_app, flash, g, redirect, render_template,
                   request, session, url_for)

users = Blueprint('users', __name__, template_folder='templates/')

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@users.route("/login", methods=['GET', 'POST'])
def login():
    """ Redirect a user to a provider for login. """
    if request.method == 'GET':
        return render_template('users/login.html')

@users.route("/login/twitter", methods=['GET'])
def login_twitter():
    return twitter.authorize(callback=url_for('users.oauth_authorize_twitter', next='/music/'))

@users.route("/oauth_authorize_twitter", methods=['GET', 'POST'])
def oauth_authorize_twitter():
    from ..database import db

    next_url = request.args.get('next', None) or url_for('music.index')
    resp = twitter.authorized_response()

    if resp is None:
        flash('Request denied')
 
    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    session['username'] = resp['screen_name']

    user = None
    with current_app.app_context():
        user = db.session.query(User).filter(User.name == resp['screen_name']).first()

        # If there's no matching user then we create a new one using the twitter data.
        if not user:

            user = User(
                name=resp['screen_name'],
                provider='twitter',
                provider_token=resp['oauth_token'],
                provider_token_secret=resp['oauth_token_secret']
            )

            db.session.add(user)
            db.session.commit()
        else:
            user.provider_token = resp['oauth_token']
            user.provider_token_secret = resp['oauth_token_secret']
            db.session.add(user)
            db.session.commit()


        flash('You were signed in as %s' % resp['screen_name'])

    return redirect(next_url)

@users.route("/logout", methods=['POST'])
def logout():
    """ Log out the user from the system. """

    # Wipe out the entire session
    session.clear()
    return redirect(url_for('music.index'))