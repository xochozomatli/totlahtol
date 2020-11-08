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
import threading
from app.lesson_handler import handle_lesson
import json

"""Defines each of the tables in the database: User, Lesson, Tlahtolli(word) as a python class using SQLAlchemy
   When you make a change to one of these classes, don't forget to run:
       flask db migrate -m "migrate message that explains what you did"
       flask db upgrade

    TODO add lesson id hash process, could be stored in its own db with the lesson id
"""

class PaginatedAPIMixin(object):
    """Ok, so this is a mixin. A mixin is basically just a class that encapsulates a certain kind of common functionality
       (in this case collecting objects to be sent to the frontend eg Lessons for the lesson feed) to be inherited by other classes,
       that's why it just defines the one method and then all the other classes subclass it.
    """
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
    #key to join all the various dbs
    id = db.Column(db.Integer, primary_key=True)
    #Basic User Info
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
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
            return json.dumps({ 'token': self.token, 'token_expiration': self.token_expiration, 'refresh_token': self.refresh_token })
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

class Lesson(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    content = db.Column(db.String(15000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    #tags = db.Column(db.LargeBinary(120), default=b'\x00'*120)
    ratings = db.relationship('Review', backref='lesson', lazy='dynamic')
    #hash_id = db.Column(db.String(120))
    prev = db.Column(db.Integer)
    next = db.Column(db.Integer)

    def set_tags(self):
        ''' This is the set_tags method. It sets tags.
            It takes in a dict or list of tuples
            or other dict-convertible iterable of tag:weight pairs
            and saves it to the Lesson's 'tags' field as a json string.
        '''
        def calculate_and_save_tags(lesson):
            lesson.tag = handle_lesson(lesson.content)
            return None
        daemon = threading.Thread(target=calculate_and_save_tags, args=(self,))
        daemon.setDaemon(True)
        daemon.start()
        return None

    def to_dict(self, include_content=False):
        data = {
            'id':self.id,
            'title':self.title,
            'timestamp':self.timestamp,
            'author': User.query.filter_by(id=self.author_id).first().username,
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

    def get_user_tlahtolli(self, user):
        word_set = set(''.join([char for char in self.content.lower() if char.isalnum() or char is ' ']).split())
        user_tlahtolli = [tlahtolli.to_dict() for tlahtolli in Tlahtolli.query.filter(Tlahtolli.user_id==user.id, Tlahtolli.word.in_(word_set)).all()]
        return user_tlahtolli
        

    
    def __repr__(self):
        return '<Lesson {}>'.format(self.title)

    @staticmethod
    def make_tag_matrix(self):
        """Looks at all tag lists and concats into a matrix
        
        outputs
        tag_matrix: numpy array, contains all the thumbsup/down behavior of users
        """
        pass

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

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    rating = db.Column(db.Integer, db.CheckConstraint("state in [1,-1]"))

    def to_dict(self):
        data = {
            'id':self.id,
            'reviewer_id':self.reviewer_id,
            'lesson_id':self.lesson_id,
            'rating':self.rating
        }

    def from_dict(self, data):
        for field in ['reviewer_id', 'lesson_id', 'rating']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        options = {1:'likes', -1:'dislikes'}
        return '<{} {} {}>'.format(
            User.query.filter_by(id=self.reviewer_id).first().username,
            options[self.rating],
            Lesson.query.filter_by(id=self.lesson_id).first().title)

