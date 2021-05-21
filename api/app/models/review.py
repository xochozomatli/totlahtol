from flask import url_for, current_app
from datetime import datetime, timedelta
from time import time
from app import db
# from app.search import add_to_index, remove_from_index, query_index
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
import jwt
import os
import base64
import threading
from app.lesson_handler import handle_lesson
import json

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    rating = db.Column(db.Integer)

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

