""" Database-related functionality for Minos. """
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SonosConfig(db.Model):
    
    """ Database-class that contains the configuration for Sonos funcionality. """

    __tablename__ = 'sonos_config'

    key = db.Column(db.String, nullable=False, primary_key=True)
    value = db.Column(db.String)