from flask import url_for, current_app
from datetime import datetime, timedelta
from time import time
from app import db
from . import PaginatedAPIMixin
# from app.search import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
import os
import base64
import threading
from app.lesson_handler import handle_lesson
import json

class User(PaginatedAPIMixin, db.Model):
    #key to join all the various dbs
    id = db.Column(db.Integer, primary_key=True)
    #Basic User Info
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    verified = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    refresh_token = db.Column(db.String(32), index=True, unique=True)
    refresh_token_expiration = db.Column(db.DateTime)
    ###Add a user lesson db
    tlahtolli = db.relationship('Tlahtolli', backref='user', lazy='dynamic')
    authored = db.relationship('Lesson', backref='author', lazy='dynamic')
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    ###Add a user app interaction/activity db
    #TODO a sparsematrix of the lesson id and the thumb up or down
    #positive and negative ratings (1, 0, or -1)
    reviews = db.relationship('Review', backref='reviewer', lazy='dynamic') #add thumbs_down
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    # viewed = db.relationship('Lesson', backref='', lazy='dynamic') This may be necessary come time in the future, but not today

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https:gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def get_token(self, expires_in=3600, refresh_token_expires_in=604800):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return { 'token': self.token, 'token_expiration': self.token_expiration, 'refresh_token': self.refresh_token, 'refresh_token_expiration': self.refresh_token_expiration }
        self.token = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        self.refresh_token = base64.urlsafe_b64encode(os.urandom(24)).decode('utf-8')
        self.refresh_token_expiration = now + timedelta(seconds=refresh_token_expires_in)
        db.session.add(self)#Just in case you're getting a token from a User who's not yet in the database
        token_dict = { 'token': self.token, 'token_expiration': self.token_expiration, 'refresh_token': self.refresh_token, 'refresh_token_expiration': self.refresh_token_expiration }
        print(token_dict)
        return token_dict

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        self.refresh_token_expiration = datetime.utcnow() - timedelta(seconds=1)
        print('tokens supposedly revoked')
        print(self.refresh_token_expiration, datetime.utcnow(),sep=' vs ')

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        print(user.token_expiration, datetime.utcnow(),sep=' vs ')
        print(user)
        return user

    @staticmethod
    def refresh(refresh_token):
        user = User.query.filter_by(refresh_token=refresh_token).first()
        if user is None:
            return None
        elif user.refresh_token_expiration < datetime.utcnow():
            print("Refresh Token Expired; We're very sorry:(")
            return None
        print("Refresh Token Valid; Right this way, sir!")
        return user.get_token()

    def get_email_verification_token(self, expires_in=600):
        return jwt.encode({'verify_user_email': self.id, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
        current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_email(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['verify_user_email']
        except:
            return
        return User.query.get(id)

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'verified': str(self.verified).lower(),
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

    def from_dict(self, data):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if 'password' in data:
            self.set_password(data['password'])

    #@staticmethod
    def get_reviews(self):
        """returns an array, user by lesson_id,
           shows the rating (1, 0, or -1) of each lesson in the db

           to be implemented: each time a lesson is added, 
           this activity database needs to be updated, once or twice a day
        """
        #TODO implement:
        #convert self.reviews from sparse matrix to full matrix for all lessons to consider
        return review_matrix_format(self.reviews)
            
    def get_rec(self):
        """
        pulls together rec_like and rec_tag
        """

    #to address cold start problem: checks if user activity is above 5 or so lessons
    # if yes returns recs based on user2user_similarity
    # else returns recs based on item2item_similarity
        pass
