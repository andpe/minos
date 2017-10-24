""" Database-related functionality for Minos. """
from flask_sqlalchemy import SQLAlchemy
from .app import app, cache

db = SQLAlchemy()


class SonosConfig(db.Model):
    
    """ Database-class that contains the configuration for Sonos funcionality. """

    __tablename__ = 'sonos_config'

    key = db.Column(db.String, nullable=False, primary_key=True)
    value = db.Column(db.String)
    _type = db.Column('type', db.String)


class OAuthConfig(db.Model):

    """ Configuration of OAuth providers. """

    __tablename__ = 'oauth_settings'

    id = db.Column(db.Integer, primary_key=True)
    provider_name = db.Column(db.String, nullable=False, index=True)
    key = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    __table_args__ = (db.UniqueConstraint('provider_name', 'key', name='oauth_settings_provider_key_uq'),)


# Track user roles in a table.
user_roles = db.Table(
    'user_roles',
    db.Column(
        'user_id',
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),
    db.Column(
        'role_id',
        db.Integer,
        db.ForeignKey('roles.id', ondelete='CASCADE'),
        primary_key=True
    )
)


class Role(db.Model):

    """ A role represents a type of user in the system.

    Roles do no support inheritence and are simply flat permission classes
    instead of a hierarchy.
    """

    __tablename__ = 'roles'

    # Columns.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    # Relationships and constraints.
    users = db.relationship(
        'User',
        secondary=user_roles,
        back_populates='roles'
    )


class User(db.Model):

    __tablename__ = 'users'

    # Columns.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), unique=True, nullable=False)
    provider = db.Column(db.String, nullable=False)
    provider_token = db.Column(db.String, nullable=False)
    provider_token_secret = db.Column(db.String, nullable=False)

    # Relationships and constraints.
    roles = db.relationship(
        'Role',
        secondary=user_roles,
        back_populates='users'
    )


    @app.cache.memoize(timeout=300)
    def has_role(self, role_name):
        """ Check if a user has a role. """
        try:
            from flask import session

            # If the user is not logged in, bail out right away.
            if not session.get('logged_in', False):
                return False
        except:
            pass

        # If any of the role names match ours then we have that role.
        return any(map(lambda r: r.name == role_name, self.roles))

class UserVote(db.Model):
    __tablename__ = 'votes'

    __table_args__ = (db.PrimaryKeyConstraint('uid', 'uri', name='uservotes_pk'),)

    uid = db.Column(db.ForeignKey('users.id'))
    uri = db.Column(db.String(), nullable=False, index=True)
    speaker = db.Column(db.String, nullable=False)
    direction = db.Column(db.Integer, nullable=False)

class Sessions(db.Model):

    """ Session object for Flask-Session. """

    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(256), unique=True)
    data = db.Column(db.LargeBinary)
    expiry = db.Column(db.DateTime)