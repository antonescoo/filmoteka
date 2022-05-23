import re
import email_validator
from slugify import slugify

from app import db
from datetime import datetime

from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users', db.Column('user_id', db.Integer(),
                                                db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))


class Genres(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    genre_name = db.Column(db.String(255), unique=True, nullable=False)


class Posters(db.Model):
    poster_id = db.Column(db.Integer, primary_key=True)
    poster_name = db.Column(db.String(255))
    poster_url = db.Column(db.String(255))


class Films(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(140), unique=True)
    genres_genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    director = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    rating = db.Column(db.Integer)
    poster = db.Column(db.String(255), nullable=True)


    def __init__(self, *args, **kwargs):
        super(Films, self).__init__(*args, **kwargs)
        self.generate_slug()


    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)


    def __repr__(self):
        return '<Film id: {}, name: {}, director: {}, description: {}, ' \
               'slug: {}' \
               '>'.format(
            self.id,
            self.name,
            self.director,
            self.description,
            self.slug
        )
