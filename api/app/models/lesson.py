from flask import url_for, current_app
from datetime import datetime, timedelta
from time import time
from app import db
from . import PaginatedAPIMixin, User, Tlahtolli
# from app.search import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
import os
import re
import base64
import threading
from app.lesson_handler import handle_lesson
import json

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
        author=User.query.filter_by(id=self.author_id).first()
        data = {
            'id':self.id,
            'title':self.title,
            'timestamp':self.timestamp,
            'author_name': author.username,
            'author_id': author.id,
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
        word_set = set([w for w in re.split(r"[^\w'-]", self.content.lower()) if w is not ''])
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
