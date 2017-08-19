from authentication import oauth
from database import db, OAuthConfig
from app import app

twitter = None

with app.app_context():
    from sqlalchemy.orm.exc import NoResultFound
    consumer_key = None
    consumer_secret = None

    try:
        consumer_key = db.session.query(OAuthConfig.value).filter(
            OAuthConfig.provider_name == 'twitter',
            OAuthConfig.key == 'consumer_key'
        ).one()
        consumer_secret = db.session.query(OAuthConfig.value).filter(
            OAuthConfig.provider_name == 'twitter',
            OAuthConfig.key == 'consumer_secret'
        ).one()
    except NoResultFound:
        raise RuntimeError("Could not find a twitter configuration")

    if consumer_key and consumer_secret:
        consumer_key = consumer_key[0]
        consumer_secret  = consumer_secret[0]

        twitter = oauth.remote_app(
            'twitter',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key=consumer_key,
            consumer_secret=consumer_secret
        )

__all__ = ['twitter']
