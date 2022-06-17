"""Models for adopt app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DEFAULT_IMAGE = ''


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Class for a pet"""

    __tablename__ = "pets"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    name = db.Column(
        db.String(50),
        nullable=False)
    species = db.Column(db.String(50),
                        nullable=False)
    photo_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMAGE)
    age = db.Column(db.String(10),
                    nullable=False)
    notes = db.Column(db.Text,
                      nullable=False,
                      default='')
    available = db.Column(db.String(10),
                          nullable=False,
                          default=True)
