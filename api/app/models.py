from flask import url_for
from datetime import datetime, timedelta
from time import time
from app import db
# from app.search import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
# import jwt
import os
import base64

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    tlahtolli = db.relationship('Tlahtolli', backref='user', lazy='dynamic')
    authored = db.relationship('Lesson', backref='author', lazy='dynamic')
    # viewed = db.relationship('Lesson', backref='author_id', lazy='dynamic')
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https:gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)#Just in case you're getting a token from a User who's not yet in the database
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            # 'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
        #     'post_count': self.posts.count(),
        #     'follower_count': self.followers.count(),
        #     'followed_count': self.followed.count(),
             '_links': {
        #        'self': url_for('api.get_user', id=self.id),
        #         'followers': url_for('api.get_followers', id=self.id),
        #         'followed': url_for('api.get_followed', id=self.id),
        #        'avatar': self.avatar(128)
             }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

class Lesson(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    content = db.Column(db.String(15000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    prev = db.Column(db.Integer)
    next = db.Column(db.Integer)

    def to_dict(self, include_content=False):
        data = {
            'id':self.id,
            'title':self.title,
            'timestamp':self.timestamp,
            '_links':{
                'self':url_for('api.get_lesson', id=self.id),
                #'prev':url_for('api.get_lesson', id=self.prev),
                #'next':url_for('api.get_lesson', id=self.next),
                'author':url_for('api.get_user', id=self.author_id)
            }
        }
        if include_content:
            data['content'] = self.content
        return data

    def from_dict(self, data):
        for field in ['title','author_id', 'content', 'prev', 'next']:
            if field in data:
                setattr(self, field, data[field])
    
    def __repr__(self):
        return '<Lesson {}>'.format(self.title)

class Tlahtolli(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(120), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    definition = db.Column(db.String(120))
    state = db.Column(db.String(10), db.CheckConstraint("state in ['known','tlahtolli','ignore']"))

    def to_dict(self):
        data = {
            'id':self.id,
            'word':self.word,
            'user_id':self.user_id,
            'definition':self.definition,
            'state':self.state
        }
        return data

    def from_dict(self, data):
        for field in ['word', 'user_id', 'definition', 'state']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<{} {}>'.format(self.word, User.query.filter_by(id=self.user_id).first().username)

