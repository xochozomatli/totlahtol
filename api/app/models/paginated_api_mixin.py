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

